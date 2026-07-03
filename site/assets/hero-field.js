/* Neutral Shift Lab — hero "signal field".
   Flowing teal field lines that part around a glowing focus point which
   follows the cursor (and drifts on its own when idle). No dependencies.
   Decorative only: sits behind hero content, pointer-events none, and is
   fully disabled under prefers-reduced-motion. */
(function () {
  "use strict";

  if (
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    return;
  }

  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }

  ready(function () {
    var hero = document.querySelector(".hero-home, .profile-hero");
    if (!hero) return;

    var canvas = document.createElement("canvas");
    canvas.className = "hero-field-canvas";
    canvas.setAttribute("aria-hidden", "true");
    hero.insertBefore(canvas, hero.firstChild);

    var ctx = canvas.getContext("2d");
    var w = 0;
    var h = 0;
    var dpr = 1;
    var traces = 5;
    var t = 0;
    var raf = null;
    var visible = true;

    var focus = { x: 0, y: 0, tx: 0, ty: 0, active: false, last: 0 };

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 1.6);
      var r = hero.getBoundingClientRect();
      w = Math.max(1, r.width);
      h = Math.max(1, r.height);
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!focus.x) {
        focus.x = focus.tx = w * 0.42;
        focus.y = focus.ty = h * 0.5;
      }
    }

    resize();
    window.addEventListener("resize", resize);

    hero.addEventListener("pointermove", function (e) {
      var r = hero.getBoundingClientRect();
      focus.tx = e.clientX - r.left;
      focus.ty = e.clientY - r.top;
      focus.active = true;
      focus.last = performance.now();
    });

    function loop(now) {
      raf = requestAnimationFrame(loop);

      // Idle: focus drifts on a slow Lissajous around the left/centre.
      if (!focus.active || now - focus.last > 2600) {
        focus.active = false;
        var a = now * 0.00015;
        focus.tx = w * (0.42 + 0.26 * Math.cos(a));
        focus.ty = h * (0.5 + 0.28 * Math.sin(a * 1.25));
      }
      focus.x += (focus.tx - focus.x) * 0.055;
      focus.y += (focus.ty - focus.y) * 0.055;

      t += 0.016;
      ctx.clearRect(0, 0, w, h);
      ctx.globalCompositeOperation = "lighter";

      var sigma = Math.max(80, w * 0.13);
      var twoSig2 = 2 * sigma * sigma;

      for (var i = 0; i < traces; i++) {
        var frac = traces > 1 ? i / (traces - 1) : 0.5;
        var baseY = h * (0.16 + 0.68 * frac);
        var amp = 9 + i * 4;
        var freq = 0.008 + 0.0012 * i;
        var speed = 0.5 + 0.12 * i;
        var alpha = 0.14 + 0.05 * i;
        var bandFall = Math.exp(-Math.pow((baseY - focus.y) / (h * 0.5), 2));
        var dir = baseY < focus.y ? -1 : 1;

        ctx.beginPath();
        for (var x = 0; x <= w; x += 8) {
          var y = baseY + amp * Math.sin(x * freq + t * speed + i);
          var dx = x - focus.x;
          var infl = Math.exp(-(dx * dx) / twoSig2);
          y += dir * infl * 44 * bandFall;
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "rgba(94,234,212," + alpha + ")";
        ctx.lineWidth = 1.4;
        ctx.stroke();
      }

      // Focus glow.
      var g = ctx.createRadialGradient(
        focus.x, focus.y, 0,
        focus.x, focus.y, sigma * 1.15
      );
      g.addColorStop(0, "rgba(45,212,191,0.16)");
      g.addColorStop(1, "rgba(45,212,191,0)");
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(focus.x, focus.y, sigma * 1.15, 0, Math.PI * 2);
      ctx.fill();

      // Bright core dot.
      ctx.fillStyle = "rgba(180,255,244,0.7)";
      ctx.beginPath();
      ctx.arc(focus.x, focus.y, 2.4, 0, Math.PI * 2);
      ctx.fill();

      ctx.globalCompositeOperation = "source-over";
    }

    function start() {
      if (!raf) raf = requestAnimationFrame(loop);
    }
    function stop() {
      if (raf) {
        cancelAnimationFrame(raf);
        raf = null;
      }
    }

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(
        function (es) {
          visible = es[0].isIntersecting;
          if (visible) start();
          else stop();
        },
        { threshold: 0 }
      ).observe(hero);
    }

    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop();
      else if (visible) start();
    });

    start();
  });
})();
