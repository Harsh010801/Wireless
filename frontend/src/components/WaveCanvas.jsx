import React, { useEffect, useRef, useState } from 'react';
import { Play, Pause, RotateCcw, Radio } from 'lucide-react';

export default function WaveCanvas({ initialFreq = 900, initialHt = 30 }) {
  const canvasRef = useRef(null);
  const [paused, setPaused] = useState(false);
  const [freq, setFreq] = useState(initialFreq);
  const [ht, setHt] = useState(initialHt);
  const [liveStats, setLiveStats] = useState({ d: 1.0, fspl: 91.52, okumura: 97.9, hata: 126.4 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animId;
    let tick = 0;
    let pulses = [];
    let progress = 0;

    const calcFSPL = (d) => 20 * Math.log10(Math.max(d, 0.1)) + 20 * Math.log10(freq) + 32.44;
    const calcHata = (d) => {
      const a = (1.1 * Math.log10(freq) - 0.7) * 1.5 - (1.56 * Math.log10(freq) - 0.8);
      return (
        69.55 +
        26.16 * Math.log10(freq) -
        13.82 * Math.log10(Math.max(ht, 1)) -
        a +
        (44.9 - 6.55 * Math.log10(Math.max(ht, 1))) * Math.log10(Math.max(d, 0.1))
      );
    };
    const calcOkumura = (d) => {
      const corr = -4.78 * Math.pow(Math.log10(freq), 2) + 18.33 * Math.log10(freq) - 40.94;
      return calcHata(d) + corr;
    };

    const render = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      if (canvas.width !== Math.floor(rect.width * dpr)) {
        canvas.width = Math.floor(rect.width * dpr);
        canvas.height = Math.floor(rect.height * dpr);
      }
      ctx.save();
      ctx.scale(dpr, dpr);

      const w = rect.width;
      const h = rect.height;
      const groundY = h * 0.78;
      const txX = 72;
      const towerHeightPx = Math.min(ht * 0.75 + 45, h * 0.62);
      const txY = groundY - towerHeightPx;

      // Sky gradient (Deep Obsidian Night theme inside simulator viewport)
      const grad = ctx.createLinearGradient(0, 0, 0, groundY);
      grad.addColorStop(0, '#0b1311');
      grad.addColorStop(1, '#13271e');
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, groundY);

      // Ground
      ctx.fillStyle = '#0a0f0d';
      ctx.fillRect(0, groundY, w, h - groundY);

      // Urban Buildings Clutter
      const blds = [0.22, 0.3, 0.39, 0.48, 0.58, 0.67, 0.77, 0.87];
      blds.forEach((bx, idx) => {
        const x = w * bx;
        const bh = 38 + ((idx * 29) % 52);
        ctx.fillStyle = '#1b2b24';
        ctx.strokeStyle = '#2d473b';
        ctx.lineWidth = 1;
        ctx.fillRect(x, groundY - bh, 34, bh);
        ctx.strokeRect(x, groundY - bh, 34, bh);
      });

      // Signal Wave Pulses
      if (!paused) {
        if (tick % 38 === 0) pulses.push({ r: 0 });
        pulses = pulses.filter((p) => p.r < w * 1.1);
        pulses.forEach((p) => (p.r += 2.4));
      }

      pulses.forEach((p) => {
        const alpha = Math.max(0, 1 - p.r / (w * 0.95));
        // Blue Arc: Free Space
        ctx.beginPath();
        ctx.arc(txX, txY, p.r, -0.45, 0.45);
        ctx.strokeStyle = `rgba(56, 189, 248, ${alpha * 0.8})`;
        ctx.lineWidth = 2.5;
        ctx.stroke();

        // Lime Green Arc: Okumura Open Area
        ctx.beginPath();
        ctx.arc(txX, txY, p.r * 0.72, -0.45, 0.45);
        ctx.strokeStyle = `rgba(168, 235, 18, ${alpha * 0.85})`;
        ctx.lineWidth = 2.5;
        ctx.stroke();

        // Coral Red Arc: Hata Urban
        ctx.beginPath();
        ctx.arc(txX, txY, p.r * 0.46, -0.45, 0.45);
        ctx.strokeStyle = `rgba(248, 113, 113, ${alpha * 0.9})`;
        ctx.lineWidth = 2.5;
        ctx.stroke();
      });

      // Cell Tower Lattice
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(txX - 11, groundY);
      ctx.lineTo(txX, txY);
      ctx.lineTo(txX + 11, groundY);
      ctx.stroke();

      ctx.beginPath();
      ctx.arc(txX, txY, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#A8EB12';
      ctx.fill();

      // Moving Mobile Receiver
      if (!paused) {
        progress = (progress + 0.0022) % 1;
        tick++;
      }

      const rxX = txX + 45 + progress * (w - txX - 105);
      const curD = Math.max(1.0, 1.0 + progress * 19.0);

      // Mobile Icon
      ctx.fillStyle = '#A8EB12';
      ctx.fillRect(rxX - 7, groundY - 24, 14, 22);
      ctx.fillStyle = '#0b1311';
      ctx.fillRect(rxX - 5, groundY - 21, 10, 14);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`${curD.toFixed(1)} km`, rxX, groundY + 18);

      if (tick % 5 === 0) {
        setLiveStats({
          d: curD,
          fspl: calcFSPL(curD),
          okumura: calcOkumura(curD),
          hata: calcHata(curD),
        });
      }

      ctx.restore();
      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animId);
  }, [paused, freq, ht]);

  return (
    <section id="wave-animation" className="max-w-7xl mx-auto px-6 py-20">
      <div className="bg-white rounded-3xl p-6 sm:p-10 shadow-xl border border-black/5">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#134729] text-[#A8EB12] text-xs font-bold mb-2">
              <Radio className="w-3.5 h-3.5" />
              REAL-TIME MOTION GRAPHICS (WAVE PROPAGATION)
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#111827]">
              Live Signal Wavefront Propagation{' '}
              <span className="text-base font-medium text-[#6B7280]">
                (Visualizing Clutter Attenuation vs Distance)
              </span>
            </h2>
          </div>

          {/* Animation Controls with bracket labels */}
          <div className="flex items-center gap-2.5">
            <button
              onClick={() => setPaused(!paused)}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-[#134729] text-white text-xs font-bold hover:bg-[#0B2E1A] transition"
            >
              {paused ? <Play className="w-3.5 h-3.5" /> : <Pause className="w-3.5 h-3.5" />}
              {paused ? 'Resume (Play Animation)' : 'Pause (Freeze Frame)'}
            </button>
            <button
              onClick={() => {
                setFreq(900);
                setHt(30);
                setPaused(false);
              }}
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full border border-black/15 text-xs font-bold text-[#111827] hover:bg-black/5 transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Reset (900 MHz Default)
            </button>
          </div>
        </div>

        {/* Sliders Bar with bracket explanations */}
        <div className="grid sm:grid-cols-2 gap-6 bg-[#F3F4EF] p-5 rounded-2xl mb-6">
          <div>
            <div className="flex justify-between text-xs font-bold text-[#111827] mb-2">
              <span>Carrier Frequency (Wave Frequency in MHz):</span>
              <span className="font-mono text-[#134729]">{freq} MHz</span>
            </div>
            <input
              type="range"
              min="150"
              max="2000"
              step="50"
              value={freq}
              onChange={(e) => setFreq(Number(e.target.value))}
              className="rf-slider"
            />
          </div>
          <div>
            <div className="flex justify-between text-xs font-bold text-[#111827] mb-2">
              <span>Tower Antenna Height hₜ (Base Station Height in m):</span>
              <span className="font-mono text-[#134729]">{ht} meters</span>
            </div>
            <input
              type="range"
              min="30"
              max="200"
              step="5"
              value={ht}
              onChange={(e) => setHt(Number(e.target.value))}
              className="rf-slider"
            />
          </div>
        </div>

        {/* Canvas Viewport */}
        <canvas
          ref={canvasRef}
          className="w-full h-[310px] rounded-2xl border border-black/10 block"
        />

        {/* Live Telemetry Readout Row + Color Legend Explanation */}
        <div className="grid md:grid-cols-4 gap-4 mt-6">
          <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5">
            <div className="text-[11px] font-bold text-[#6B7280] uppercase">
              Mobile Distance (d in km)
            </div>
            <div className="text-2xl font-extrabold font-mono text-[#111827] mt-1">
              {liveStats.d.toFixed(1)} km
            </div>
            <div className="text-[11px] text-[#6B7280] mt-1">Moving receiver position</div>
          </div>

          <div className="p-4 rounded-2xl bg-sky-50 border border-sky-200">
            <div className="flex items-center gap-2 text-[11px] font-bold text-sky-900 uppercase">
              <span className="w-2.5 h-2.5 rounded-full bg-sky-500" />
              Blue Arc: Free Space (dB)
            </div>
            <div className="text-2xl font-extrabold font-mono text-sky-900 mt-1">
              {liveStats.fspl.toFixed(2)} dB
            </div>
            <div className="text-[11px] text-sky-800 mt-1">Longest reach, no obstacles</div>
          </div>

          <div className="p-4 rounded-2xl bg-lime-50 border border-lime-300">
            <div className="flex items-center gap-2 text-[11px] font-bold text-lime-950 uppercase">
              <span className="w-2.5 h-2.5 rounded-full bg-[#A8EB12] border border-black/20" />
              Lime Arc: Okumura Open (dB)
            </div>
            <div className="text-2xl font-extrabold font-mono text-lime-950 mt-1">
              {liveStats.okumura.toFixed(2)} dB
            </div>
            <div className="text-[11px] text-lime-900 mt-1">Moderate open-area attenuation</div>
          </div>

          <div className="p-4 rounded-2xl bg-red-50 border border-red-200">
            <div className="flex items-center gap-2 text-[11px] font-bold text-red-900 uppercase">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500" />
              Red Arc: Hata Urban (dB)
            </div>
            <div className="text-2xl font-extrabold font-mono text-red-900 mt-1">
              {liveStats.hata.toFixed(2)} dB
            </div>
            <div className="text-[11px] text-red-800 mt-1">Shortest reach (blocked by buildings)</div>
          </div>
        </div>
      </div>
    </section>
  );
}

