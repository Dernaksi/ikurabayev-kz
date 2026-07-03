/* Neutral Shift Lab — light scroll-reveal. No dependencies, fail-safe.
   Content is never left hidden: each reveal drops the hiding gate shortly
   after (via setTimeout, which fires even when the animation clock is
   throttled), so a frozen/background compositor cannot strand content. */
(function () {
  "use strict";

  var reduce =
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (reduce || !("IntersectionObserver" in window)) return;

  var selector = [
    ".hero-content",
    ".portrait-panel",
    ".section-heading",
    ".profile-layout > .card",
    ".grid > .card",
    ".method-notes > article",
    ".publication-card",
    ".recognition-grid > span",
    ".asset-figure",
    ".bridge-flow > span"
  ].join(",");

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var els = Array.prototype.slice.call(document.querySelectorAll(selector));
    if (!els.length) return;

    document.documentElement.classList.add("js-reveal");

    els.forEach(function (el) {
      el.setAttribute("data-animate", "");
      var parent = el.parentNode;
      var idx = 0;
      if (parent) {
        var sibs = Array.prototype.filter.call(parent.children, function (c) {
          return c.matches && c.matches(selector);
        });
        idx = sibs.indexOf(el);
        if (idx < 0) idx = 0;
      }
      el.style.animationDelay = Math.min(idx, 3) * 60 + "ms";
    });

    function reveal(el) {
      if (el.classList.contains("in-view")) return;
      el.classList.add("in-view");
      // Once the fade has had time to run, remove the gate entirely so the
      // element rests at its static, always-visible default state.
      setTimeout(function () {
        el.removeAttribute("data-animate");
        el.style.animationDelay = "";
      }, 820);
    }

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            reveal(e.target);
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.05 }
    );

    var vh = window.innerHeight || document.documentElement.clientHeight;

    els.forEach(function (el) {
      if (el.getBoundingClientRect().top < vh * 0.92) reveal(el);
      else io.observe(el);
    });

    // Absolute fail-safe: nothing stays hidden past this point.
    setTimeout(function () {
      els.forEach(function (el) {
        el.removeAttribute("data-animate");
      });
    }, 2000);
  });
})();

/* Cursor spotlight on cards — feeds --mx/--my to the CSS glow overlay. */
(function () {
  "use strict";
  if (!window.matchMedia || window.matchMedia("(pointer: coarse)").matches) {
    return; // skip on touch devices
  }
  var sel = ".card, .ai-mod, .profile-link";
  document.addEventListener(
    "pointermove",
    function (e) {
      var el = e.target.closest && e.target.closest(sel);
      if (!el) return;
      var r = el.getBoundingClientRect();
      el.style.setProperty("--mx", (e.clientX - r.left) + "px");
      el.style.setProperty("--my", (e.clientY - r.top) + "px");
    },
    { passive: true }
  );
})();
