// Marks today's week on the home-page strip and says where the plan stands.
// Runs on every page load, including Material's instant navigation.
(function () {
  function day(iso, endOfDay) {
    return new Date(iso + (endOfDay ? "T23:59:59" : "T00:00:00"));
  }

  function label(iso) {
    return day(iso).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" });
  }

  function mark() {
    var now = new Date();
    var cells = document.querySelectorAll(".jr-cell[data-start]");
    cells.forEach(function (cell) {
      var on = now >= day(cell.dataset.start) && now <= day(cell.dataset.end, true);
      cell.classList.toggle("is-now", on);
      if (on) cell.setAttribute("aria-current", "date");
      else cell.removeAttribute("aria-current");
    });

    var when = document.querySelector("[data-jr-when]");
    if (!when || !when.dataset.start) return;
    var start = day(when.dataset.start);
    var end = day(when.dataset.end, true);
    if (now < start) {
      var days = Math.ceil((start - now) / 86400000);
      when.textContent = "Starts " + label(when.dataset.start) + (days > 0 ? ", in " + days + (days === 1 ? " day" : " days") : "");
    } else if (now > end) {
      when.textContent = "Plan finished " + label(when.dataset.end);
    } else {
      var week = Math.floor((now - start) / (7 * 86400000)) + 1;
      when.textContent = "This is week " + week + " of " + cells.length;
    }
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(mark);
  } else {
    document.addEventListener("DOMContentLoaded", mark);
  }
})();
