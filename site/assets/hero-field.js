/* Neutral Shift Lab — hero "signal field" (living background).
   A dense teal signal field behind the hero: flowing field lines that part
   around a glowing focus point (follows the cursor, drifts when idle),
   bright data packets streaming along the lines, and a faint pulsing node
   lattice. Decorative only — behind hero content, pointer-events none, and
   fully disabled under prefers-reduced-motion. No dependencies. */
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
    var mobile = false;
    var traces = 9;
    var t = 0;
    var raf = null;
    var visible = true;

    var focus = { x: 0, y: 0, tx: 0, ty: 0, active: false, last: 0 };

    // Data packets streaming along the field lines.
    var packets = [];
    function seedPackets() {
      packets = [];
      var n = mobile ? Math.max(7, Math.round(w / 90)) : Math.max(14, Math.round(w / 60));
      for (var i = 0; i < n; i++) {
        packets.push({
          band: Math.floor(Math.random() * traces),
          x: Math.random() * w,
          spd: 26 + Math.random() * 46,
          size: 1.1 + Math.random() * 1.7,
          a: 0.35 + Math.random() * 0.45,
        });
      }
    }

    // Faint node lattice — a hex-ish dot grid that gently pulses.
    var nodes = [];
    function seedNodes() {
      nodes = [];
      var step = Math.max(64, w * 0.075);
      var row = 0;
      for (var y = step * 0.5; y < h; y += step * 0.86, row++) {
        var off = row % 2 ? step * 0.5 : 0;
        for (var x = off; x < w + step; x += step) {
          nodes.push({ x: x, y: y, ph: Math.random() * Math.PI * 2 });
        }
      }
    }

    function bandY(i) {
      var frac = traces > 1 ? i / (traces - 1) : 0.5;
      return h * (0.1 + 0.82 * frac);
    }

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 1.6);
      var r = hero.getBoundingClientRect();
      w = Math.max(1, r.width);
      h = Math.max(1, r.height);
      mobile = w < 640;
      traces = mobile ? 5 : 9;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.style.width = w + "px";
      canvas.style.height = h + "px";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (!focus.x) {
        focus.x = focus.tx = w * 0.42;
        focus.y = focus.ty = h * 0.5;
      }
      seedPackets();
      seedNodes();
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

    // Shared line shape so packets ride exactly on the drawn field lines.
    function lineY(i, x, sigma2) {
      var baseY = bandY(i);
      var amp = 9 + i * 4;
      var freq = 0.008 + 0.0012 * i;
      var speed = 0.5 + 0.12 * i;
      var bandFall = Math.exp(-Math.pow((baseY - focus.y) / (h * 0.5), 2));
      var dir = baseY < focus.y ? -1 : 1;
      var y = baseY + amp * Math.sin(x * freq + t * speed + i);
      var dx = x - focus.x;
      var infl = Math.exp(-(dx * dx) / sigma2);
      y += dir * infl * 52 * bandFall;
      return y;
    }

    function loop(now) {
      raf = requestAnimationFrame(loop);

      // Idle: focus drifts on a slow Lissajous around the left/centre.
      if (!focus.active || now - focus.last > 2600) {
        focus.active = false;
        var a = now * 0.00015;
        focus.tx = w * (0.42 + 0.28 * Math.cos(a));
        focus.ty = h * (0.5 + 0.3 * Math.sin(a * 1.25));
      }
      focus.x += (focus.tx - focus.x) * 0.06;
      focus.y += (focus.ty - focus.y) * 0.06;

      t += 0.016;
      ctx.clearRect(0, 0, w, h);

      var sigma = Math.max(90, w * 0.14);
      var twoSig2 = 2 * sigma * sigma;

      // --- Node lattice (subtle, drawn first, normal blend) ---
      for (var k = 0; k < nodes.length; k++) {
        var nd = nodes[k];
        var ndx = nd.x - focus.x;
        var ndy = nd.y - focus.y;
        var prox = Math.exp(-(ndx * ndx + ndy * ndy) / (sigma * sigma * 1.4));
        var pulse = 0.5 + 0.5 * Math.sin(t * 1.3 + nd.ph);
        var na = 0.05 + 0.16 * prox + 0.05 * pulse;
        var nr = 0.8 + 1.6 * prox;
        ctx.fillStyle = "rgba(94,234,212," + na.toFixed(3) + ")";
        ctx.beginPath();
        ctx.arc(nd.x, nd.y, nr, 0, Math.PI * 2);
        ctx.fill();
      }

      ctx.globalCompositeOperation = "lighter";

      // --- Field lines ---
      for (var i = 0; i < traces; i++) {
        var alpha = 0.12 + 0.045 * i;
        ctx.beginPath();
        for (var x = 0; x <= w; x += 7) {
          var y = lineY(i, x, twoSig2);
          if (x === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.strokeStyle = "rgba(94,234,212," + alpha.toFixed(3) + ")";
        ctx.lineWidth = 1.3;
        ctx.stroke();
      }

      // --- Data packets streaming along the lines ---
      for (var p = 0; p < packets.length; p++) {
        var pk = packets[p];
        pk.x += pk.spd * 0.016;
        if (pk.x > w + 20) {
          pk.x = -20;
          pk.band = Math.floor(Math.random() * traces);
        }
        var py = lineY(pk.band, pk.x, twoSig2);
        // brighten near the focus
        var pdx = pk.x - focus.x;
        var pdy = py - focus.y;
        var glow = Math.exp(-(pdx * pdx + pdy * pdy) / (sigma * sigma * 0.9));
        var pa = Math.min(1, pk.a + glow * 0.5);
        var pr = pk.size + glow * 1.6;
        // short trailing streak
        var tg = ctx.createLinearGradient(pk.x - 14, py, pk.x + pr, py);
        tg.addColorStop(0, "rgba(94,234,212,0)");
        tg.addColorStop(1, "rgba(160,255,240," + (pa * 0.5).toFixed(3) + ")");
        ctx.strokeStyle = tg;
        ctx.lineWidth = pr * 0.9;
        ctx.beginPath();
        ctx.moveTo(pk.x - 14, py);
        ctx.lineTo(pk.x, py);
        ctx.stroke();
        ctx.fillStyle = "rgba(190,255,246," + pa.toFixed(3) + ")";
        ctx.beginPath();
        ctx.arc(pk.x, py, pr, 0, Math.PI * 2);
        ctx.fill();
      }

      // --- Focus glow ---
      var g = ctx.createRadialGradient(
        focus.x, focus.y, 0,
        focus.x, focus.y, sigma * 1.2
      );
      g.addColorStop(0, "rgba(45,212,191,0.2)");
      g.addColorStop(1, "rgba(45,212,191,0)");
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(focus.x, focus.y, sigma * 1.2, 0, Math.PI * 2);
      ctx.fill();

      // Bright core dot with soft ring.
      ctx.strokeStyle = "rgba(120,255,238,0.35)";
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(focus.x, focus.y, 7 + 1.5 * Math.sin(t * 2.4), 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = "rgba(190,255,244,0.8)";
      ctx.beginPath();
      ctx.arc(focus.x, focus.y, 2.6, 0, Math.PI * 2);
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
