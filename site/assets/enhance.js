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
    ".recognition-grid > .award-item",
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

/* Chapter scrollspy — highlights the active chapter link in the header. */
(function () {
  "use strict";
  if (!("IntersectionObserver" in window)) return;
  var ids = ["profile", "ch-path", "ch-expertise", "ch-science", "ch-recognition"];

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var links = {};
    var targets = [];
    ids.forEach(function (id) {
      var a = document.querySelector('.nav-links a[href="#' + id + '"]');
      var t = document.getElementById(id);
      if (a) links[id] = a;
      if (t) targets.push(t);
    });
    if (!targets.length) return;

    var vis = {};
    function refresh() {
      var current = null;
      for (var i = 0; i < ids.length; i++) {
        if (vis[ids[i]]) { current = ids[i]; break; }
      }
      if (!current) return;
      Object.keys(links).forEach(function (id) {
        links[id].classList.toggle("active", id === current);
      });
    }

    var obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) { vis[e.target.id] = e.isIntersecting; });
        refresh();
      },
      { rootMargin: "-90px 0px -55% 0px", threshold: 0 }
    );
    targets.forEach(function (t) { obs.observe(t); });
  });
})();

/* Scroll progress hairline — fixed teal bar at the top edge. */
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var bar = document.createElement("div");
    bar.className = "scroll-progress";
    document.body.appendChild(bar);
    var ticking = false;
    function update() {
      ticking = false;
      var doc = document.documentElement;
      var max = (doc.scrollHeight - doc.clientHeight) || 1;
      var p = Math.min(1, Math.max(0, (window.scrollY || doc.scrollTop) / max));
      bar.style.transform = "scaleX(" + p + ")";
    }
    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update, { passive: true });
    update();
  });
})();

/* Magnetic navigation — header links ease toward the cursor on hover. */
(function () {
  "use strict";
  if (
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    return;
  }
  // Pointer-fine only — skip touch, where there's no hover.
  if (window.matchMedia && !window.matchMedia("(hover: hover)").matches) {
    return;
  }
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var links = document.querySelectorAll(".nav-links a");
    var PULL = 0.34; // fraction of cursor offset the link follows
    var MAX = 7; // px cap
    Array.prototype.forEach.call(links, function (a) {
      a.addEventListener("pointermove", function (e) {
        var r = a.getBoundingClientRect();
        var dx = (e.clientX - (r.left + r.width / 2)) * PULL;
        var dy = (e.clientY - (r.top + r.height / 2)) * PULL;
        dx = Math.max(-MAX, Math.min(MAX, dx));
        dy = Math.max(-MAX, Math.min(MAX, dy));
        a.style.transform = "translate(" + dx.toFixed(1) + "px," + dy.toFixed(1) + "px)";
      });
      a.addEventListener("pointerleave", function () {
        a.style.transform = "";
      });
    });
  });
})();

/* Chapter-band entrance — dedicated one-shot observer, independent of the
   reveal fail-safe so the cinematic entrance plays no matter when a chapter
   is scrolled into view. */
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var bands = Array.prototype.slice.call(
      document.querySelectorAll(".chapter-band")
    );
    if (!bands.length) return;

    function show(b) {
      b.classList.add("band-in");
    }

    if (!("IntersectionObserver" in window)) {
      bands.forEach(show);
      return;
    }

    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) {
            show(e.target);
            io.unobserve(e.target);
          }
        });
      },
      { rootMargin: "0px 0px -12% 0px", threshold: 0.15 }
    );

    var vh = window.innerHeight || document.documentElement.clientHeight;
    bands.forEach(function (b) {
      // Already comfortably in view at load → reveal on next frame so the
      // animation still runs from its start state.
      if (b.getBoundingClientRect().top < vh * 0.85) {
        requestAnimationFrame(function () { show(b); });
      } else {
        io.observe(b);
      }
    });

    // Absolute fail-safe: never leave a chapter hidden.
    setTimeout(function () { bands.forEach(show); }, 4000);
  });
})();
