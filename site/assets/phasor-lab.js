/* ==========================================================================
   phasor-lab.js — live single-phase earth-fault phasor for #research
   Balanced 3-phase star → ground point slides to the faulted phase, neutral
   displaces (3U0), healthy phases grow to √3·Uф. 3D projection tilts with the
   cursor; click discharges a burst + shock ring. Hextech / cyber styling.
   ========================================================================== */
(function () {
  "use strict";
  const canvas = document.querySelector(".phasor-canvas");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const REDUCE = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const TEAL = "#5eead4", TEALD = "#2dd4bf", GOLD = "#f5b544", SLATE = "#cbd5e1";
  let W = 0, H = 0, dpr = 1, running = false, raf = 0, t0 = 0, t = 0;
  let cx = 0, cy = 0, R = 0;
  const tilt = { x: 0.3, y: 0 };
  const mouse = { x: 0, y: 0, active: false };
  let cycT = 0;             // fault-cycle clock
  let faultPhase = 0, lastCycle = -1;
  const B = [];             // burst sparks
  let shock = null;         // {age}

  function resize() {
    const r = canvas.getBoundingClientRect();
    if (!r.width) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    cx = W / 2; cy = H * 0.47;
    R = Math.min(W * 0.30, H * 0.34);
  }

  function glow(color, blur, width) {
    ctx.strokeStyle = color; ctx.lineWidth = width;
    ctx.shadowColor = color; ctx.shadowBlur = blur;
    ctx.lineJoin = "round"; ctx.lineCap = "round";
  }
  function noShadow() { ctx.shadowBlur = 0; }
  function smooth(x) { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); }

  // fault factor over a 7s cycle
  function faultF(c) {
    c = c % 7;
    if (c < 2) return 0;
    if (c < 3) return smooth(c - 2);
    if (c < 5.5) return 1;
    if (c < 6.5) return 1 - smooth(c - 5.5);
    return 0;
  }

  // 3D-ish projection: tilt plane around X and Y (orthographic)
  function proj(px, py) {
    const ax = tilt.x, ay = tilt.y;
    const y1 = py * Math.cos(ax);
    const z1 = py * Math.sin(ax);
    const x2 = px * Math.cos(ay) + z1 * Math.sin(ay);
    return [cx + x2, cy + y1];
  }

  function ellipse(rad, style, width, blur) {
    ctx.beginPath();
    for (let i = 0; i <= 48; i++) {
      const a = (i / 48) * Math.PI * 2;
      const [X, Y] = proj(Math.cos(a) * rad, Math.sin(a) * rad);
      i ? ctx.lineTo(X, Y) : ctx.moveTo(X, Y);
    }
    glow(style, blur || 0, width); ctx.stroke(); noShadow();
  }

  function arrow(from, to, color, width, blur) {
    ctx.beginPath(); ctx.moveTo(from[0], from[1]); ctx.lineTo(to[0], to[1]);
    glow(color, blur, width); ctx.stroke();
    const ang = Math.atan2(to[1] - from[1], to[0] - from[0]);
    const s = 7;
    ctx.beginPath();
    ctx.moveTo(to[0], to[1]);
    ctx.lineTo(to[0] - s * Math.cos(ang - 0.4), to[1] - s * Math.sin(ang - 0.4));
    ctx.moveTo(to[0], to[1]);
    ctx.lineTo(to[0] - s * Math.cos(ang + 0.4), to[1] - s * Math.sin(ang + 0.4));
    ctx.stroke(); noShadow();
  }

  function label(txt, X, Y, color, size, alpha) {
    ctx.font = (size || 11) + "px 'IBM Plex Mono', monospace";
    ctx.fillStyle = color; ctx.globalAlpha = alpha == null ? 1 : alpha;
    ctx.fillText(txt, X, Y); ctx.globalAlpha = 1;
  }

  function hexAt(X, Y, r, color, blur) {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const a = Math.PI / 6 + i * Math.PI / 3;
      const x = X + r * Math.cos(a), y = Y + r * Math.sin(a);
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.closePath(); glow(color, blur || 0, 1.4); ctx.stroke(); noShadow();
  }

  function frame(now, dt) {
    ctx.clearRect(0, 0, W, H);

    // tilt easing toward cursor (or gentle idle)
    let tgx, tgy;
    if (mouse.active) {
      tgx = 0.30 + Math.max(-0.42, Math.min(0.42, (mouse.y - cy) / H)) * -0.9;
      tgy = Math.max(-0.5, Math.min(0.5, (mouse.x - cx) / W)) * 1.1;
    } else {
      tgx = 0.30 + 0.05 * Math.sin(now * 0.5);
      tgy = 0.16 * Math.sin(now * 0.32);
    }
    tilt.x += (tgx - tilt.x) * 0.06;
    tilt.y += (tgy - tilt.y) * 0.06;

    const rot = now * 0.55;
    const f = faultF(cycT);
    const cyc = Math.floor(cycT / 7);
    if (cyc !== lastCycle) { lastCycle = cyc; faultPhase = Math.floor(Math.random() * 3); }
    const fp = faultPhase;
    const angs = [rot - Math.PI / 2, rot - Math.PI / 2 + 2.094395, rot - Math.PI / 2 + 4.18879];
    const cols = [TEAL, GOLD, SLATE];
    const names = ["A", "B", "C"];
    const tips = angs.map((a) => [Math.cos(a) * R, Math.sin(a) * R]); // plane coords
    const G = [f * tips[fp][0], f * tips[fp][1]]; // ground slides to the faulted phase

    // reference ellipses + axes
    ellipse(R, "rgba(94,234,212,0.16)", 1);
    ellipse(R * 1.732, "rgba(245,181,68,0.16)", 1);
    ctx.setLineDash([2, 5]);
    let p1 = proj(-R * 1.9, 0), p2 = proj(R * 1.9, 0);
    ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]);
    glow("rgba(255,255,255,0.10)", 0, 1); ctx.stroke();
    p1 = proj(0, -R * 1.9); p2 = proj(0, R * 1.9);
    ctx.beginPath(); ctx.moveTo(p1[0], p1[1]); ctx.lineTo(p2[0], p2[1]); ctx.stroke();
    ctx.setLineDash([]); noShadow();

    const O = proj(0, 0);
    const Gp = proj(G[0], G[1]);
    const tp = tips.map((v) => proj(v[0], v[1]));

    // source EMF triangle (faint)
    ctx.beginPath();
    tp.forEach((p, i) => (i ? ctx.lineTo(p[0], p[1]) : ctx.moveTo(p[0], p[1])));
    ctx.closePath(); glow("rgba(94,234,212,0.22)", 0, 1); ctx.stroke(); noShadow();

    // EMF vectors O -> tips (thin)
    tp.forEach((p, i) => {
      ctx.beginPath(); ctx.moveTo(O[0], O[1]); ctx.lineTo(p[0], p[1]);
      glow(cols[i], 0, 1); ctx.globalAlpha = 0.5; ctx.stroke(); ctx.globalAlpha = 1;
    });
    noShadow();

    // neutral-displacement trail + U0 vector O -> G
    if (f > 0.02) {
      arrow(O, Gp, GOLD, 2.4, 12);
      const midU = proj(G[0] * 0.5, G[1] * 0.5);
      label("U₀", midU[0] + 6, midU[1] - 4, GOLD, 11, Math.min(1, f * 1.4));
      // trig projection of U0 onto Re / Im axes
      const gx = proj(G[0], 0), gy = proj(0, G[1]);
      ctx.setLineDash([3, 4]);
      glow("rgba(245,181,68,0.5)", 0, 1);
      ctx.beginPath(); ctx.moveTo(Gp[0], Gp[1]); ctx.lineTo(gx[0], gx[1]);
      ctx.moveTo(Gp[0], Gp[1]); ctx.lineTo(gy[0], gy[1]); ctx.stroke();
      ctx.setLineDash([]); noShadow();
      ctx.globalAlpha = Math.min(1, f * 1.4);
      label("Re", gx[0] - 4, gx[1] + 14, "rgba(245,181,68,0.9)", 9);
      label("Im", gy[0] + 6, gy[1], "rgba(245,181,68,0.9)", 9);
      ctx.globalAlpha = 1;
    }

    // measured phase-to-ground vectors G -> tips (hero)
    tp.forEach((p, i) => {
      const faulted = i === fp;
      const w = faulted ? 2 + (1 - f) * 1.5 : 2.6;
      const a = faulted ? (1 - f * 0.85) : 1;
      ctx.globalAlpha = a;
      arrow(Gp, p, cols[i], w, faulted ? 6 : 10);
      ctx.globalAlpha = 1;
    });

    // tips: hex nodes + labels
    tp.forEach((p, i) => {
      hexAt(p[0], p[1], 6, cols[i], 6);
      ctx.beginPath(); ctx.arc(p[0], p[1], 2.4, 0, Math.PI * 2);
      ctx.fillStyle = cols[i]; ctx.shadowColor = cols[i]; ctx.shadowBlur = 8; ctx.fill(); noShadow();
      const out = proj(tips[i][0] * 1.16, tips[i][1] * 1.16);
      label(names[i], out[0] - 3, out[1] + 4, cols[i], 12);
    });
    // faulted phase note
    if (f > 0.5) label("U" + names[fp] + " → 0", tp[fp][0] + 8, tp[fp][1] + 4, GOLD, 10, (f - 0.5) / 0.5);

    // center O node
    ctx.beginPath(); ctx.arc(O[0], O[1], 3, 0, Math.PI * 2);
    ctx.fillStyle = "#9fb2ae"; ctx.fill();

    // ground node G (earth glyph)
    hexAt(Gp[0], Gp[1], 7 + f * 2, GOLD, 10 * f + 4);
    ctx.beginPath(); ctx.arc(Gp[0], Gp[1], 3.4, 0, Math.PI * 2);
    ctx.fillStyle = "#fff"; ctx.shadowColor = GOLD; ctx.shadowBlur = 14; ctx.fill(); noShadow();
    for (let i = 0; i < 3; i++) {
      const ly = Gp[1] + 9 + i * 3, lw = 10 - i * 3;
      ctx.beginPath(); ctx.moveTo(Gp[0] - lw / 2, ly); ctx.lineTo(Gp[0] + lw / 2, ly);
      glow(GOLD, 0, 1.4); ctx.globalAlpha = 0.4 + 0.6 * f; ctx.stroke(); ctx.globalAlpha = 1;
    }
    noShadow();

    // status label
    label(f < 0.1 ? "СИММЕТРИЯ · ω" : "ОЗЗ · фаза " + names[fp], 12, 20, f < 0.1 ? TEAL : GOLD, 11);

    // shock ring (click)
    if (shock) {
      shock.age += dt;
      const a = Math.max(0, 1 - shock.age / 0.7);
      if (a <= 0) shock = null;
      else {
        ellipse(shock.age * 260, "rgba(150,245,225," + (0.6 * a) + ")", 2, 16);
      }
    }
    // burst sparks
    if (B.length) {
      ctx.globalCompositeOperation = "lighter";
      for (let i = B.length - 1; i >= 0; i--) {
        const p = B[i];
        p.life -= dt * 1.5; if (p.life <= 0) { B.splice(i, 1); continue; }
        p.vx *= 0.94; p.vy *= 0.94; p.x += p.vx * dt; p.y += p.vy * dt;
        const c = p.gold ? GOLD : TEAL;
        ctx.globalAlpha = Math.max(0, p.life);
        ctx.beginPath(); ctx.arc(p.x, p.y, 1.3 + p.life * 2, 0, Math.PI * 2);
        ctx.fillStyle = c; ctx.shadowColor = c; ctx.shadowBlur = 10 * p.life; ctx.fill();
      }
      ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over"; noShadow();
    }

    // scanline
    const sx = ((now * 0.04) % 1) * W;
    const gs = ctx.createLinearGradient(sx - 40, 0, sx + 40, 0);
    gs.addColorStop(0, "rgba(94,234,212,0)"); gs.addColorStop(0.5, "rgba(94,234,212,0.07)"); gs.addColorStop(1, "rgba(94,234,212,0)");
    ctx.fillStyle = gs; ctx.fillRect(sx - 40, 0, 80, H);
  }

  function loop(ts) {
    if (!running) return;
    if (!t0) t0 = ts;
    const now = (ts - t0) / 1000;
    const dt = Math.min(0.05, now - t); t = now;
    if (!mouse.hold) cycT += dt;
    frame(now, dt);
    raf = requestAnimationFrame(loop);
  }
  function start() { if (running) return; running = true; t0 = 0; raf = requestAnimationFrame(loop); }
  function stop() { running = false; cancelAnimationFrame(raf); }

  function onMove(e) {
    const r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; mouse.active = true;
  }
  function onLeave() { mouse.active = false; }
  function onDown() {
    cycT = 2.0; // jump to fault onset
    faultPhase = Math.floor(Math.random() * 3); lastCycle = 0;
    shock = { age: 0 };
    for (let i = 0; i < 22; i++) {
      const a = (i / 22) * Math.PI * 2 + Math.random() * 0.3, sp = 60 + Math.random() * 150;
      B.push({ x: cx, y: cy, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1, gold: Math.random() < 0.4 });
    }
  }

  function init() {
    resize();
    if (REDUCE) { cycT = 4; frame(0.6, 0); return; }
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerleave", onLeave);
    canvas.addEventListener("pointerdown", onDown);
    if ("IntersectionObserver" in window) {
      new IntersectionObserver((es) => es.forEach((e) => (e.isIntersecting ? start() : stop())), { threshold: 0.05 }).observe(canvas);
    } else { start(); }
  }

  let rz;
  window.addEventListener("resize", () => {
    clearTimeout(rz);
    rz = setTimeout(() => { resize(); if (REDUCE) frame(0.6, 0); }, 160);
  });

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
