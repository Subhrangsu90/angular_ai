"""MkDocs hook: tidy the auto-generated sidebar.

- Section titles come from the folder's README.md heading instead of the folder name
  ("Week 1: How LLMs work" instead of "Week 01 how llms work").
- Inside a section: README first, then weeks, then labs, then projects.
- A folder holding a single page (lab-*/PLAN.md, project-*/PLAN.md) shows as that page.
"""

from pathlib import Path

from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page


def _h1(page: Page) -> str | None:
    try:
        text = Path(page.file.abs_src_path).read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _rank(item) -> int:
    if isinstance(item, Page):
        return 0 if item.is_index else 1
    title = (item.title or "").lower()
    if title.startswith("lab"):
        return 3
    if title.startswith("project"):
        return 4
    return 2


def _tidy(items, parent):
    items.sort(key=_rank)  # stable: keeps the alphabetical order within each group
    for i, item in enumerate(items):
        if not isinstance(item, Section):
            continue
        _tidy(item.children, item)
        pages = [c for c in item.children if isinstance(c, Page)]
        if len(item.children) == 1 and pages:
            pages[0].parent = parent
            items[i] = pages[0]
            continue
        index = next((p for p in pages if p.is_index), None)
        if index and (title := _h1(index)):
            item.title = title
    return items


def _flatten(items):
    for item in items:
        if isinstance(item, Page):
            yield item
        elif isinstance(item, Section):
            yield from _flatten(item.children)


def on_nav(nav, config, files):
    _tidy(nav.items, None)
    pages = list(_flatten(nav.items))
    for prev, cur in zip([None, *pages], pages):
        cur.previous_page = prev
        if prev:
            prev.next_page = cur
    if pages:
        pages[-1].next_page = None
    nav.pages = pages
    return nav
