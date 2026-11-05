"""MkDocs hook: read progress from the week READMEs and feed it to the site.

- Counts `- [ ]` / `- [x]` tasks in every phase-*/week-*/README.md.
- Exposes `journey` (phases, weeks, totals) to templates; the home page uses it.
- Adds a progress meter under the heading of each week and phase page.
- Renders the home page with overrides/home.html and drops the README's own
  title and "Phases" list there (the template draws richer versions of both).
"""

import html
import re
from datetime import datetime
from pathlib import Path

PHASE_DIR = re.compile(r"^phase-(\d+)-")
WEEK_DIR = re.compile(r"^week-(\d+)-")
PHASE_H1 = re.compile(r"^# Phase \d+:\s*(.+?)(?:\s*\((weeks? [^)]+)\))?\s*$", re.M)
WEEK_H1 = re.compile(r"^# Week \d+:\s*(.+?)\s*$", re.M)
FIELD = r"^\*\*{}:\*\*\s*(.+?)\s*$"
DATES = re.compile(r"(\d{1,2} \w{3} \d{4})\s*[–-]\s*(\d{1,2} \w{3} \d{4})")
TASK = re.compile(r"^\s*[-*] \[([ xX])\]", re.M)
PLAN_NAME = "24-Week Plan"

_journey: dict = {}
_pages: dict = {}  # src_uri -> phase or week dict


def _inline(text: str) -> str:
    """Escape text, keep `code` spans."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))


def _iso(day: str) -> str:
    return datetime.strptime(day, "%d %b %Y").date().isoformat()


def _label(iso: str) -> str:
    if not iso:
        return ""
    d = datetime.fromisoformat(iso)
    return f"{d.day} {d:%b %Y}"


def _pct(done: int, total: int) -> int:
    return round(100 * done / total) if total else 0


def on_files(files, config):
    phases: dict[int, dict] = {}
    plan_url = None

    for f in files.documentation_pages():
        parts = f.src_uri.split("/")
        if len(parts) == 1 and PLAN_NAME in parts[0]:
            plan_url = f.url
        m = PHASE_DIR.match(parts[0])
        if not m or parts[-1] != "README.md":
            continue
        num = int(m.group(1))
        phase = phases.setdefault(num, {"num": num, "weeks": []})
        text = Path(f.abs_src_path).read_text(encoding="utf-8")

        if len(parts) == 2:
            h1 = PHASE_H1.search(text)
            goal = re.search(FIELD.format("Goal"), text, re.M)
            ships = re.search(FIELD.format("Deliverable"), text, re.M)
            phase.update(
                url=f.url,
                name=h1.group(1) if h1 else f"Phase {num}",
                span=(h1.group(2) or "") if h1 else "",
                goal=_inline(goal.group(1)) if goal else "",
                ships=_inline(ships.group(1)) if ships else "",
            )
            _pages[f.src_uri] = phase
        elif len(parts) == 3 and (w := WEEK_DIR.match(parts[1])):
            marks = TASK.findall(text)
            h1 = WEEK_H1.search(text)
            dates = DATES.search(text)
            week = {
                "num": int(w.group(1)),
                "phase": num,
                "url": f.url,
                "title": h1.group(1) if h1 else parts[1],
                "start": _iso(dates.group(1)) if dates else "",
                "end": _iso(dates.group(2)) if dates else "",
                "done": sum(1 for x in marks if x.lower() == "x"),
                "total": len(marks),
            }
            week["pct"] = _pct(week["done"], week["total"])
            phase["weeks"].append(week)
            _pages[f.src_uri] = week

    ordered = [phases[k] for k in sorted(phases)]
    weeks = []
    for phase in ordered:
        phase["weeks"].sort(key=lambda w: w["num"])
        phase["done"] = sum(w["done"] for w in phase["weeks"])
        phase["total"] = sum(w["total"] for w in phase["weeks"])
        phase["pct"] = _pct(phase["done"], phase["total"])
        weeks += phase["weeks"]

    done = sum(p["done"] for p in ordered)
    total = sum(p["total"] for p in ordered)
    _journey.clear()
    _journey.update(
        phases=ordered,
        weeks=weeks,
        done=done,
        total=total,
        pct=_pct(done, total),
        weeks_done=sum(1 for w in weeks if w["total"] and w["done"] == w["total"]),
        next_week=next((w for w in weeks if w["done"] < w["total"]), weeks[-1] if weeks else None),
        start=weeks[0]["start"] if weeks else "",
        end=weeks[-1]["end"] if weeks else "",
        start_label=_label(weeks[0]["start"]) if weeks else "",
        end_label=_label(weeks[-1]["end"]) if weeks else "",
        plan_url=plan_url or "",
    )
    return files


def on_page_markdown(markdown, page, config, files):
    if page.is_homepage:
        page.meta["template"] = "home.html"
        page.meta["hide"] = ["navigation", "toc"]
    return markdown


def _meter(item, label: str) -> str:
    phase = item.get("phase", item.get("num"))
    return (
        f'<div class="jr-page-meter" style="--phase: var(--jr-phase-{phase})">'
        f'<div class="jr-meter" role="progressbar" aria-valuemin="0" aria-valuemax="100" '
        f'aria-valuenow="{item["pct"]}" aria-label="{label}"><span style="width:{item["pct"]}%"></span></div>'
        f'<p>{label}</p></div>'
    )


def on_page_content(content, page, config, files):
    if page.is_homepage:
        content = re.sub(r"<h1\b.*?</h1>", "", content, count=1, flags=re.S)
        content = re.sub(r'<h2 id="phases".*', "", content, flags=re.S)
        return content

    item = _pages.get(page.file.src_uri)
    if not item:
        return content
    if "phase" in item:  # a week
        label = f'{item["done"]} of {item["total"]} tasks done this week'
    else:
        label = f'{item["done"]} of {item["total"]} tasks done across {len(item["weeks"])} weeks'
    return re.sub(r"(</h1>)", r"\1" + _meter(item, label).replace("\\", "\\\\"), content, count=1)


def on_page_context(context, page, config, nav):
    context["journey"] = _journey
    return context
