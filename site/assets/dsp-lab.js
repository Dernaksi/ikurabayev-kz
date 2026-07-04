/* ==========================================================================
   dsp-lab.js — live cyber/hextech DSP pipeline for #method-stack
   Canvas renders 6 animated zones: 3-phase signal → ADC → filters → FFT →
   SVD/matrix → digital twin, with energy particles flowing across the chain.
   Transparent canvas (panel supplies the grid bg). Pauses when offscreen.
   ========================================================================== */
(function () {
  "use strict";
  const canvas = document.querySelector(".dsp-canvas");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const REDUCE = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const TEAL = "#5eead4", TEALD = "#2dd4bf", GOLD = "#f5b544", SLATE = "#cbd5e1";
  let W = 0, H = 0, dpr = 1, running = false, raf = 0, t0 = 0, t = 0;
  const mouse = { x: -1, y: -1, active: false };
  let hoverZone = -1;
  const glitch = [0, 0, 0, 0, 0, 0];
  const hov = [0, 0, 0, 0, 0, 0];   // per-zone hover intensity (eased)
  const B = [];        // click-burst sparks
  let shock = null;    // {x, age} shockwave

  function resize() {
    const r = canvas.getBoundingClientRect();
    if (!r.width) return;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  // ---- geometry helpers ----
  function zone(i) {
    const zw = W / 6, x0 = i * zw;
    const pad = Math.max(10, zw * 0.1);
    return { x0, zw, px0: x0 + pad, px1: x0 + zw - pad, pw: zw - 2 * pad };
  }
  function vizBounds() {
    const top = 10, bot = H * 0.70;
    return { top, bot, mid: (top + bot) / 2, amp: (bot - top) / 2 - 3 };
  }

  function glowStroke(color, blur, width) {
    ctx.strokeStyle = color;
    ctx.lineWidth = width;
    ctx.shadowColor = color;
    ctx.shadowBlur = blur;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
  }
  function noShadow() { ctx.shadowBlur = 0; }

  // ---- energy particles along the chain ----
  const P = [];
  function seedParticles() {
    P.length = 0;
    const n = W < 560 ? 8 : 16;
    for (let i = 0; i < n; i++) {
      P.push({
        x: Math.random() * W,
        v: 42 + Math.random() * 46,
        wob: Math.random() * Math.PI * 2,
        gold: Math.random() < 0.32,
        len: 14 + Math.random() * 26
      });
    }
  }

  // ---- zone 1: three-phase + harmonics (hover: harmonics bloom) ----
  function drawSignal(z, vb, time, h) {
    h = h || 0;
    const cycles = 2.2, steps = Math.max(40, z.pw / 3);
    const cols = [SLATE, GOLD, TEAL], op = [0.7, 0.9, 1];
    const amp = vb.amp * (1 + 0.34 * h), norm = 1.18 + h * 0.26;
    for (let p = 2; p >= 0; p--) {
      ctx.beginPath();
      for (let i = 0; i <= steps; i++) {
        const tt = i / steps, x = z.px0 + z.pw * tt;
        const a = tt * cycles * Math.PI * 2 - p * (2 * Math.PI / 3) + time * (1.9 + h * 1.2);
        let y = Math.sin(a) + 0.18 * Math.sin(3 * a + 0.4)
          + h * (0.16 * Math.sin(5 * a) + 0.1 * Math.sin(7 * a + 1));
        y = y / norm;
        const yy = vb.mid - amp * y;
        i ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy);
      }
      ctx.globalAlpha = op[p];
      glowStroke(cols[p], (p === 2 ? 10 : 5) + h * 10, 2 + h * 0.6);
      ctx.stroke();
    }
    ctx.globalAlpha = 1; noShadow();
  }

  // ---- zone 2: ADC sample & hold (hover: quantization staircase) ----
  function drawADC(z, vb, time, h) {
    h = h || 0;
    const cycles = 2.2, steps = Math.max(40, z.pw / 3);
    if (h > 0.01) {
      glowStroke("rgba(94,234,212," + (0.14 * h) + ")", 0, 1);
      for (let L = -4; L <= 4; L++) {
        const yy = vb.mid - vb.amp * (L / 4);
        ctx.beginPath(); ctx.moveTo(z.px0, yy); ctx.lineTo(z.px1, yy); ctx.stroke();
      }
    }
    // faint continuous wave
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {
      const tt = i / steps, x = z.px0 + z.pw * tt;
      const a = tt * cycles * Math.PI * 2 + time * 1.9;
      const yy = vb.mid - vb.amp * Math.sin(a);
      i ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy);
    }
    ctx.globalAlpha = 0.28; glowStroke(TEAL, 0, 1.4); ctx.stroke(); ctx.globalAlpha = 1;
    const N = 14, head = (time * 0.9) % 1;
    // sample & hold staircase (quantized) on hover
    if (h > 0.01) {
      ctx.beginPath();
      for (let k = 0; k < N; k++) {
        const tt = (k + 0.5) / N, x0 = z.px0 + z.pw * (k / N), x1 = z.px0 + z.pw * ((k + 1) / N);
        const a = tt * cycles * Math.PI * 2 + time * 1.9;
        const qy = vb.mid - vb.amp * (Math.round(Math.sin(a) * 4) / 4);
        if (k === 0) ctx.moveTo(x0, qy); else ctx.lineTo(x0, qy);
        ctx.lineTo(x1, qy);
      }
      glowStroke(GOLD, 8 * h, 1.8); ctx.globalAlpha = h; ctx.stroke(); ctx.globalAlpha = 1; noShadow();
    }
    // stems + dots, with a travelling highlight
    for (let k = 0; k < N; k++) {
      const tt = (k + 0.5) / N, x = z.px0 + z.pw * tt;
      const a = tt * cycles * Math.PI * 2 + time * 1.9;
      const yy = vb.mid - vb.amp * Math.sin(a);
      const near = 1 - Math.min(1, Math.abs(tt - head) * 6);
      ctx.beginPath(); ctx.moveTo(x, vb.mid); ctx.lineTo(x, yy);
      glowStroke(TEALD, near * 8, 1.3);
      ctx.globalAlpha = 0.5 + near * 0.5; ctx.stroke(); ctx.globalAlpha = 1;
      ctx.beginPath(); ctx.arc(x, yy, 2 + near * 1.8, 0, Math.PI * 2);
      ctx.fillStyle = near > 0.5 ? GOLD : TEAL;
      ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = 6 + near * 8; ctx.fill();
    }
    noShadow();
  }

  // ---- zone 3: analog + digital filters (hover: cutoff sweep) ----
  function drawFilter(z, vb, time, h) {
    h = h || 0;
    const steps = Math.max(40, z.pw / 3), top = vb.top + 4, bot = vb.bot - 2;
    const knee = 0.34 + h * 0.26 * Math.sin(time * 1.7);
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {
      const tt = i / steps, x = z.px0 + z.pw * tt;
      const mag = 1 / Math.sqrt(1 + Math.pow(tt / Math.max(0.08, knee), 6));
      const yy = bot - (bot - top) * mag;
      i ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy);
    }
    glowStroke(TEAL, 10 + h * 8, 2.2); ctx.stroke(); noShadow();
    // cutoff scan (follows knee on hover)
    const cx = z.px0 + z.pw * (h > 0.01 ? Math.max(0.08, knee) : 0.30 + 0.05 * Math.sin(time * 1.3));
    ctx.beginPath(); ctx.moveTo(cx, top - 2); ctx.lineTo(cx, bot + 2);
    ctx.setLineDash([3, 4]); glowStroke(GOLD, 8, 1.4);
    ctx.globalAlpha = 0.9; ctx.stroke(); ctx.globalAlpha = 1; ctx.setLineDash([]); noShadow();
    // digital taps blinking (faster on hover)
    for (let k = 0; k < 5; k++) {
      const x = z.px0 + z.pw * (0.42 + k * 0.13);
      const b = 0.4 + 0.6 * Math.abs(Math.sin(time * (3 + h * 4) + k));
      ctx.beginPath(); ctx.moveTo(x, top); ctx.lineTo(x, top + 12);
      glowStroke(TEALD, 6 * b, 1.6); ctx.globalAlpha = b; ctx.stroke();
    }
    ctx.globalAlpha = 1; noShadow();
  }

  // ---- zone 4: FFT spectrum (hover: full analyzer + peak-hold) ----
  function drawFFT(z, vb, time, h) {
    h = h || 0;
    const base = [1, 0.42, 0.26, 0.16, 0.1], n = base.length;
    const bw = Math.min(14, z.pw / (n * 1.9)), gap = (z.pw - bw * n) / (n - 1);
    const bot = vb.bot, maxh = vb.bot - vb.top - 4;
    ctx.beginPath(); ctx.moveTo(z.px0, bot); ctx.lineTo(z.px1, bot);
    ctx.strokeStyle = "rgba(255,255,255,0.09)"; ctx.lineWidth = 1; ctx.stroke();
    // dense analyzer bins fade in on hover
    if (h > 0.01) {
      const M = 22;
      for (let k = 0; k < M; k++) {
        const x = z.px0 + (k + 0.2) * (z.pw / M), env = Math.exp(-k / 7);
        const hh = maxh * env * (0.3 + 0.7 * Math.abs(Math.sin(time * 5 + k * 0.9) * Math.cos(time * 2 + k))) * h;
        ctx.fillStyle = "rgba(45,212,191," + (0.5 * h) + ")";
        ctx.fillRect(x, bot - hh, z.pw / M * 0.6, hh);
      }
    }
    for (let k = 0; k < n; k++) {
      const x = z.px0 + k * (bw + gap);
      const osc = 0.82 + (0.18 + h * 0.5) * Math.sin(time * (4 + h * 3) + k * 1.3);
      const hgt = maxh * base[k] * osc;
      const gold = k === 0;
      ctx.fillStyle = gold ? GOLD : TEALD;
      ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = (gold ? 14 : 7) + h * 8;
      roundRect(x, bot - hgt, bw, hgt, 1.5); ctx.fill();
      if (h > 0.01) {
        const cap = bot - hgt - 4 - 3 * (0.5 + 0.5 * Math.sin(time * 1.5 + k));
        ctx.fillStyle = "rgba(255,255,255," + (0.7 * h) + ")";
        ctx.fillRect(x, cap, bw, 1.5);
      }
    }
    noShadow();
  }

  // ---- zone 5: SVD / matrix (hover: compute wavefront) ----
  function drawMatrix(z, vb, time, h) {
    h = h || 0;
    const cols = 4, rows = 4;
    const gx = 5, gy = 4;
    const cw = (z.pw - 10 - gx * (cols - 1)) / cols;
    const areaTop = vb.top + 6, areaBot = vb.bot - 2;
    const ch = (areaBot - areaTop - gy * (rows - 1)) / rows;
    const bx = z.px0 + 5;
    // brackets
    glowStroke(TEAL, 6, 1.6);
    ctx.beginPath();
    ctx.moveTo(bx - 3, areaTop - 3); ctx.lineTo(bx - 6, areaTop - 3);
    ctx.lineTo(bx - 6, areaBot + 3); ctx.lineTo(bx - 3, areaBot + 3);
    ctx.moveTo(z.px1 + 3, areaTop - 3); ctx.lineTo(z.px1 + 6, areaTop - 3);
    ctx.lineTo(z.px1 + 6, areaBot + 3); ctx.lineTo(z.px1 + 3, areaBot + 3);
    ctx.stroke(); noShadow();
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const x = bx + c * (cw + gx), y = areaTop + r * (ch + gy);
        const diag = r === c;
        const pulse = diag ? 0.5 + 0.5 * Math.sin(time * 3 - r * 0.9) : 0;
        const wf = h * Math.max(0, Math.sin(time * 4 - (r + c) * 0.8)); // hover wavefront
        if (diag) {
          ctx.fillStyle = "rgba(45,212,191," + (0.28 + pulse * 0.5 + wf * 0.4) + ")";
          ctx.strokeStyle = TEAL; ctx.shadowColor = TEAL; ctx.shadowBlur = 4 + pulse * 10 + wf * 10;
        } else {
          ctx.fillStyle = "rgba(45,212,191," + (0.06 + wf * 0.5) + ")";
          ctx.strokeStyle = wf > 0.1 ? TEALD : "rgba(46,67,64,0.9)";
          ctx.shadowColor = TEAL; ctx.shadowBlur = wf * 8;
        }
        ctx.lineWidth = 1;
        roundRect(x, y, cw, ch, 2); ctx.fill(); ctx.stroke();
      }
    }
    noShadow();
  }

  // ---- zone 6: digital twin (hover: model locks / syncs) ----
  function drawTwin(z, vb, time, h) {
    h = h || 0;
    const cycles = 2.2, steps = Math.max(40, z.pw / 3);
    const head = h > 0.01 ? 1.15 : (time * 0.5) % 1.15; // lock -> full trace on hover
    const off = 0.15 * (1 - h);                          // phase offset -> 0 (sync)
    // measured (solid teal, full)
    ctx.beginPath();
    for (let i = 0; i <= steps; i++) {
      const tt = i / steps, x = z.px0 + z.pw * tt;
      const yy = vb.mid - vb.amp * Math.sin(tt * cycles * Math.PI * 2);
      i ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy);
    }
    ctx.globalAlpha = 0.55 + h * 0.3; glowStroke(TEAL, 5 + h * 6, 1.6); ctx.stroke(); ctx.globalAlpha = 1;
    // model (gold), drawn up to head; dashes tighten to solid on lock
    ctx.beginPath();
    let hx = z.px0, hy = vb.mid;
    for (let i = 0; i <= steps; i++) {
      const tt = i / steps; if (tt > head) break;
      const x = z.px0 + z.pw * tt;
      const yy = vb.mid - vb.amp * Math.sin(tt * cycles * Math.PI * 2 + off);
      i ? ctx.lineTo(x, yy) : ctx.moveTo(x, yy);
      hx = x; hy = yy;
    }
    ctx.setLineDash(h > 0.85 ? [] : [4, 4]); glowStroke(GOLD, 8 + h * 6, 2); ctx.stroke(); ctx.setLineDash([]);
    if (head <= 1) {
      ctx.beginPath(); ctx.arc(hx, hy, 3.2, 0, Math.PI * 2);
      ctx.fillStyle = "#fff"; ctx.shadowColor = GOLD; ctx.shadowBlur = 14; ctx.fill();
    }
    // sync-lock ring at the end node on hover
    if (h > 0.01) {
      const ly = vb.mid - vb.amp * Math.sin(cycles * Math.PI * 2);
      const rr = 6 + 3 * Math.sin(time * 5);
      ctx.beginPath(); ctx.arc(z.px1, ly, rr, 0, Math.PI * 2);
      glowStroke(TEAL, 12 * h, 1.6); ctx.globalAlpha = h; ctx.stroke(); ctx.globalAlpha = 1;
    }
    noShadow();
  }

  // ---- connectors: hex nodes + flowing particles ----
  function drawFlow(vb, dt, time) {
    const y = vb.mid;
    // beam
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y);
    ctx.strokeStyle = "rgba(94,234,212,0.06)"; ctx.lineWidth = 1; ctx.stroke();
    // hex nodes between zones
    for (let i = 1; i < 6; i++) {
      const x = i * (W / 6);
      const pulse = 0.4 + 0.6 * Math.abs(Math.sin(time * 2 + i));
      hex(x, y, 5 + pulse * 1.5);
      ctx.strokeStyle = TEALD; ctx.lineWidth = 1.4;
      ctx.shadowColor = TEAL; ctx.shadowBlur = 6 * pulse; ctx.stroke();
    }
    noShadow();
    // particles
    ctx.globalCompositeOperation = "lighter";
    for (const p of P) {
      p.x += p.v * dt; p.wob += dt * 3;
      if (p.x > W + p.len) { p.x = -p.len; p.y = null; }
      const baseY = y + Math.sin(p.wob) * 4;
      if (p.y == null) p.y = baseY;
      let boost = 0;
      if (mouse.active) {
        const d = Math.hypot(mouse.x - p.x, mouse.y - p.y);
        const pull = Math.max(0, 1 - d / 210);
        boost = pull;
        p.y += (mouse.y - p.y) * pull * 0.22 + (baseY - p.y) * 0.05;
        p.x += (mouse.x - p.x) * pull * 0.05;
      } else {
        p.y += (baseY - p.y) * 0.12;
      }
      const py = p.y;
      const col = p.gold ? GOLD : TEAL;
      const grad = ctx.createLinearGradient(p.x - p.len, py, p.x, py);
      grad.addColorStop(0, "rgba(0,0,0,0)");
      grad.addColorStop(1, col);
      ctx.beginPath(); ctx.moveTo(p.x - p.len, py); ctx.lineTo(p.x, py);
      ctx.strokeStyle = grad; ctx.lineWidth = 1.6 + boost * 1.4; ctx.stroke();
      ctx.beginPath(); ctx.arc(p.x, py, 1.8 + boost * 2.4, 0, Math.PI * 2);
      ctx.fillStyle = col; ctx.shadowColor = col; ctx.shadowBlur = 8 + boost * 16; ctx.fill();
    }
    // cursor energy well
    if (mouse.active && mouse.y >= 0) {
      const rr = 15 + 4 * Math.sin(time * 6);
      ctx.beginPath(); ctx.arc(mouse.x, mouse.y, rr, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(94,234,212,0.7)"; ctx.lineWidth = 1.4;
      ctx.shadowColor = TEAL; ctx.shadowBlur = 16; ctx.stroke();
      for (let i = 0; i < 3; i++) {
        const a = time * 3 + i * (Math.PI * 2 / 3);
        const ox = mouse.x + Math.cos(a) * rr, oy = mouse.y + Math.sin(a) * rr;
        ctx.beginPath(); ctx.arc(ox, oy, 2, 0, Math.PI * 2);
        ctx.fillStyle = i === 1 ? GOLD : TEAL; ctx.shadowBlur = 10; ctx.fill();
      }
    }
    ctx.globalCompositeOperation = "source-over"; noShadow();
  }

  // ---- glitch flash on hovered zone ----
  function drawGlitches(time, dt) {
    for (let z = 0; z < 6; z++) {
      if (glitch[z] <= 0.001) continue;
      const g = glitch[z], Z = zone(z);
      ctx.save();
      ctx.beginPath(); ctx.rect(Z.x0, 0, Z.zw, H); ctx.clip();
      ctx.fillStyle = "rgba(94,234,212," + (0.08 * g) + ")";
      ctx.fillRect(Z.x0, 0, Z.zw, H);
      ctx.globalCompositeOperation = "lighter";
      for (let i = 0; i < 5; i++) {
        const sy = (((i * 61 + Math.floor(time * 34)) % 100) / 100) * H;
        const sh = 2 + ((i * 7) % 8);
        const dx = Math.sin(time * 45 + i * 2) * 9 * g;
        ctx.fillStyle = i % 2
          ? "rgba(245,181,68," + (0.5 * g) + ")"
          : "rgba(94,234,212," + (0.5 * g) + ")";
        ctx.fillRect(Z.x0 + dx, sy, Z.zw, sh * g + 0.5);
      }
      ctx.globalCompositeOperation = "source-over";
      ctx.strokeStyle = "rgba(94,234,212," + (0.6 * g) + ")";
      ctx.lineWidth = 1.5; ctx.shadowColor = TEAL; ctx.shadowBlur = 12 * g;
      ctx.strokeRect(Z.x0 + 1, 3, Z.zw - 2, H - 6);
      ctx.restore(); noShadow();
      glitch[z] = Math.max(0, glitch[z] - dt * 2.4);
    }
  }

  // ---- pointer interaction ----
  function onMove(e) {
    const r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; mouse.active = true;
    hoverZone = Math.floor(mouse.x / (W / 6));
  }
  function onLeave() { mouse.active = false; hoverZone = -1; }
  function onDown(e) {
    const r = canvas.getBoundingClientRect();
    const mx = e.clientX - r.left, my = e.clientY - r.top;
    const n = 24;
    for (let i = 0; i < n; i++) {
      const a = (i / n) * Math.PI * 2 + Math.random() * 0.4;
      const sp = 70 + Math.random() * 180;
      B.push({ x: mx, y: my, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: 1, gold: Math.random() < 0.35 });
    }
    shock = { x: mx, age: 0 };
    const z = Math.floor(mx / (W / 6)); if (z >= 0 && z < 6) glitch[z] = 1.25;
  }

  // ---- click burst sparks ----
  function drawBursts(dt) {
    if (!B.length) return;
    ctx.globalCompositeOperation = "lighter";
    for (let i = B.length - 1; i >= 0; i--) {
      const p = B[i];
      p.life -= dt * 1.5;
      if (p.life <= 0) { B.splice(i, 1); continue; }
      p.vx *= 0.94; p.vy *= 0.94; p.vy += 42 * dt;
      p.x += p.vx * dt; p.y += p.vy * dt;
      const col = p.gold ? GOLD : TEAL;
      ctx.globalAlpha = Math.max(0, p.life);
      ctx.beginPath(); ctx.arc(p.x, p.y, 1.3 + p.life * 2.2, 0, Math.PI * 2);
      ctx.fillStyle = col; ctx.shadowColor = col; ctx.shadowBlur = 10 * p.life; ctx.fill();
    }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = "source-over"; noShadow();
  }

  // ---- shockwave sweeping the chain ----
  function drawShock(dt) {
    if (!shock) return;
    shock.age += dt;
    const off = shock.age * 920;
    const alpha = Math.max(0, 1 - shock.age / 0.72);
    if (alpha <= 0) { shock = null; return; }
    ctx.globalCompositeOperation = "lighter";
    [shock.x - off, shock.x + off].forEach((px) => {
      if (px < -20 || px > W + 20) return;
      const g = ctx.createLinearGradient(px - 15, 0, px + 15, 0);
      g.addColorStop(0, "rgba(94,234,212,0)");
      g.addColorStop(0.5, "rgba(150,245,225," + (0.55 * alpha) + ")");
      g.addColorStop(1, "rgba(94,234,212,0)");
      ctx.fillStyle = g; ctx.fillRect(px - 15, 0, 30, H);
      const z = Math.floor(px / (W / 6)); if (z >= 0 && z < 6) glitch[z] = Math.max(glitch[z], alpha * 0.9);
    });
    ctx.globalCompositeOperation = "source-over";
  }

  // ---- primitives ----
  function roundRect(x, y, w, h, r) {
    r = Math.min(r, w / 2, h / 2);
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }
  function hex(cx, cy, r) {
    ctx.beginPath();
    for (let i = 0; i < 6; i++) {
      const a = Math.PI / 6 + i * Math.PI / 3;
      const x = cx + r * Math.cos(a), y = cy + r * Math.sin(a);
      i ? ctx.lineTo(x, y) : ctx.moveTo(x, y);
    }
    ctx.closePath();
  }

  // ---- scanline sweep ----
  function scan(time) {
    const x = ((time * 0.05) % 1) * W;
    const g = ctx.createLinearGradient(x - 40, 0, x + 40, 0);
    g.addColorStop(0, "rgba(94,234,212,0)");
    g.addColorStop(0.5, "rgba(94,234,212,0.10)");
    g.addColorStop(1, "rgba(94,234,212,0)");
    ctx.fillStyle = g; ctx.fillRect(x - 40, 0, 80, H);
  }

  function drawHoverBorders() {
    for (let i = 0; i < 6; i++) {
      if (hov[i] < 0.02) continue;
      const Z = zone(i), a = hov[i];
      ctx.strokeStyle = "rgba(94,234,212," + (0.42 * a) + ")";
      ctx.lineWidth = 1.4; ctx.shadowColor = TEAL; ctx.shadowBlur = 12 * a;
      ctx.strokeRect(Z.x0 + 1.5, 4, Z.zw - 3, H - 8);
      noShadow();
    }
  }

  function frame(now, dt) {
    ctx.clearRect(0, 0, W, H);
    const vb = vizBounds();
    for (let i = 0; i < 6; i++) {
      const tg = (mouse.active && hoverZone === i) ? 1 : 0;
      hov[i] += (tg - hov[i]) * 0.14;
    }
    scan(now);
    drawSignal(zone(0), vb, now, hov[0]);
    drawADC(zone(1), vb, now, hov[1]);
    drawFilter(zone(2), vb, now, hov[2]);
    drawFFT(zone(3), vb, now, hov[3]);
    drawMatrix(zone(4), vb, now, hov[4]);
    drawTwin(zone(5), vb, now, hov[5]);
    drawHoverBorders();
    drawFlow(vb, dt, now);
    drawShock(dt);
    drawGlitches(now, dt);
    drawBursts(dt);
  }

  function loop(ts) {
    if (!running) return;
    if (!t0) t0 = ts;
    const now = (ts - t0) / 1000;
    const dt = Math.min(0.05, now - t);
    t = now;
    frame(now, dt);
    raf = requestAnimationFrame(loop);
  }

  function start() { if (running) return; running = true; t0 = 0; raf = requestAnimationFrame(loop); }
  function stop() { running = false; cancelAnimationFrame(raf); }

  function init() {
    resize(); seedParticles();
    if (REDUCE) { frame(0.6, 0); return; }
    canvas.addEventListener("pointermove", onMove);
    canvas.addEventListener("pointerleave", onLeave);
    canvas.addEventListener("pointerdown", onDown);
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((es) => {
        es.forEach((e) => (e.isIntersecting ? start() : stop()));
      }, { threshold: 0.05 });
      io.observe(canvas);
    } else { start(); }
  }

  let rz;
  window.addEventListener("resize", () => {
    clearTimeout(rz);
    rz = setTimeout(() => { resize(); seedParticles(); if (REDUCE) frame(0.6, 0); }, 160);
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
