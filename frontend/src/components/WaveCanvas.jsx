import React, { useEffect, useRef, useState } from 'react';
import { Play, Pause, RotateCcw, Radio, Zap } from 'lucide-react';

export default function WaveCanvas({ initialFreq = 900, initialHt = 30 }) {
  const canvasRef = useRef(null);
  const [paused, setPaused] = useState(false);
  const [freqUnit, setFreqUnit] = useState('MHz'); // 'MHz' or 'GHz'
  const [freqMhz, setFreqMhz] = useState(initialFreq);
  const [ht, setHt] = useState(initialHt);
  const [liveStats, setLiveStats] = useState({
    d: 1.0,
    fspl: 91.52,
    okumura: 97.9,
    hata: 126.4,
    umi_los: 82.2,
    umi_nlos: 88.3,
    umi_trans: 82.2,
  });

  const isMmWave = freqMhz >= 10000; // >= 10 GHz is mmWave regime

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    let animId;
    let tick = 0;
    let pulses = [];
    let progress = 0;

    const calcFSPL = (d) => 20 * Math.log10(Math.max(d, 0.01)) + 20 * Math.log10(freqMhz) + 32.44;

    const calcHata = (d) => {
      const f = Math.min(Math.max(freqMhz, 150), 3000);
      const a = (1.1 * Math.log10(f) - 0.7) * 1.5 - (1.56 * Math.log10(f) - 0.8);
      return (
        69.55 +
        26.16 * Math.log10(f) -
        13.82 * Math.log10(Math.max(ht, 1)) -
        a +
        (44.9 - 6.55 * Math.log10(Math.max(ht, 1))) * Math.log10(Math.max(d, 0.05))
      );
    };

    const calcOkumura = (d) => {
      const f = Math.min(Math.max(freqMhz, 150), 1920);
      const corr = -4.78 * Math.pow(Math.log10(f), 2) + 18.33 * Math.log10(f) - 40.94;
      return calcHata(d) + corr;
    };

    // 3GPP TR 38.901 & IEEE Access 2026 mmWave UMi Calculations
    const calcMMWave = (dKm) => {
      const dM = Math.max(dKm * 1000, 5.0);
      const fGhz = freqMhz / 1000.0;
      const d3d = Math.sqrt(dM * dM + Math.pow(Math.max(ht - 1.5, 1.0), 2));

      const plLos = 32.4 + 21.0 * Math.log10(d3d) + 20.0 * Math.log10(fGhz);
      const plNlosPrime = 22.4 + 35.3 * Math.log10(d3d) + 21.3 * Math.log10(fGhz);
      const plNlos = Math.max(plLos, plNlosPrime);

      // LoS Probability
      let pLos = 1.0;
      if (dM > 18.0) {
        pLos = (18.0 / dM) + Math.exp(-dM / 36.0) * (1.0 - (18.0 / dM));
      }
      pLos = Math.min(Math.max(pLos, 0.0), 1.0);
      const plTrans = pLos * plLos + (1.0 - pLos) * plNlos;

      return { los: plLos, nlos: plNlos, trans: plTrans };
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

      // Signal Wave Pulses (mmWave pulses are more frequent and dense)
      const pulseInterval = isMmWave ? 18 : 36;
      const pulseSpeed = isMmWave ? 2.8 : 2.4;

      if (!paused) {
        if (tick % pulseInterval === 0) pulses.push({ r: 0 });
        pulses = pulses.filter((p) => p.r < w * 1.15);
        pulses.forEach((p) => (p.r += pulseSpeed));
      }

      pulses.forEach((p) => {
        const alpha = Math.max(0, 1 - p.r / (w * 0.95));

        if (isMmWave) {
          // mmWave Wavefronts: Cyan (LoS), Lime (IEEE Access Transition), Rose (NLoS)
          // 1. Blue/Sky Arc: Free Space
          ctx.beginPath();
          ctx.arc(txX, txY, p.r, -0.42, 0.42);
          ctx.strokeStyle = `rgba(56, 189, 248, ${alpha * 0.7})`;
          ctx.lineWidth = 1.8;
          ctx.stroke();

          // 2. Cyan Arc: 3GPP UMi LoS
          ctx.beginPath();
          ctx.arc(txX, txY, p.r * 0.82, -0.42, 0.42);
          ctx.strokeStyle = `rgba(6, 182, 212, ${alpha * 0.85})`;
          ctx.lineWidth = 2.4;
          ctx.stroke();

          // 3. Lime Arc: IEEE Access Transition Model
          ctx.beginPath();
          ctx.arc(txX, txY, p.r * 0.62, -0.42, 0.42);
          ctx.strokeStyle = `rgba(132, 204, 22, ${alpha * 0.9})`;
          ctx.lineWidth = 2.8;
          ctx.stroke();

          // 4. Rose Arc: 3GPP UMi NLoS (Heavy urban building blockage)
          ctx.beginPath();
          ctx.arc(txX, txY, p.r * 0.38, -0.42, 0.42);
          ctx.strokeStyle = `rgba(225, 29, 72, ${alpha * 0.95})`;
          ctx.lineWidth = 2.2;
          ctx.stroke();
        } else {
          // Sub-6 GHz Wavefronts: Blue (Free Space), Lime (Okumura), Red (Hata)
          // 1. Blue Arc: Free Space
          ctx.beginPath();
          ctx.arc(txX, txY, p.r, -0.45, 0.45);
          ctx.strokeStyle = `rgba(56, 189, 248, ${alpha * 0.8})`;
          ctx.lineWidth = 2.5;
          ctx.stroke();

          // 2. Lime Green Arc: Okumura Open Area
          ctx.beginPath();
          ctx.arc(txX, txY, p.r * 0.72, -0.45, 0.45);
          ctx.strokeStyle = `rgba(168, 235, 18, ${alpha * 0.85})`;
          ctx.lineWidth = 2.5;
          ctx.stroke();

          // 3. Coral Red Arc: Hata Urban
          ctx.beginPath();
          ctx.arc(txX, txY, p.r * 0.46, -0.45, 0.45);
          ctx.strokeStyle = `rgba(248, 113, 113, ${alpha * 0.9})`;
          ctx.lineWidth = 2.5;
          ctx.stroke();
        }
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
      ctx.fillStyle = isMmWave ? '#06b6d4' : '#A8EB12';
      ctx.fill();

      // Moving Mobile Receiver
      if (!paused) {
        progress = (progress + 0.0022) % 1;
        tick++;
      }

      const rxX = txX + 45 + progress * (w - txX - 105);
      // For mmWave, distance scale is 50m to 1km; for sub-6 GHz it is 1km to 20km
      const curD = isMmWave
        ? Math.max(0.05, 0.05 + progress * 0.95) // 50m to 1.0 km
        : Math.max(1.0, 1.0 + progress * 19.0); // 1.0 km to 20 km

      // Mobile Icon
      ctx.fillStyle = isMmWave ? '#06b6d4' : '#A8EB12';
      ctx.fillRect(rxX - 7, groundY - 24, 14, 22);
      ctx.fillStyle = '#0b1311';
      ctx.fillRect(rxX - 5, groundY - 21, 10, 14);

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px "JetBrains Mono", monospace';
      ctx.textAlign = 'center';
      const distLabel = isMmWave && curD < 1.0
        ? `${Math.round(curD * 1000)} m`
        : `${curD.toFixed(1)} km`;
      ctx.fillText(distLabel, rxX, groundY + 18);

      if (tick % 5 === 0) {
        const mm = calcMMWave(curD);
        setLiveStats({
          d: curD,
          fspl: calcFSPL(curD),
          okumura: calcOkumura(curD),
          hata: calcHata(curD),
          umi_los: mm.los,
          umi_nlos: mm.nlos,
          umi_trans: mm.trans,
        });
      }

      ctx.restore();
      animId = requestAnimationFrame(render);
    };

    animId = requestAnimationFrame(render);
    return () => cancelAnimationFrame(animId);
  }, [paused, freqMhz, ht, isMmWave]);

  const handleFreqSlider = (val) => {
    const num = Number(val);
    if (freqUnit === 'GHz') {
      setFreqMhz(Math.round(num * 1000));
    } else {
      setFreqMhz(num);
    }
  };

  return (
    <section id="wave-animation" className="max-w-7xl mx-auto px-6 py-20">
      <div className="bg-white rounded-3xl p-6 sm:p-10 shadow-xl border border-black/5">
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#134729] text-[#A8EB12] text-xs font-bold mb-2">
              <Radio className="w-3.5 h-3.5" />
              REAL-TIME MOTION GRAPHICS (SUB-6 GHz & 5G/6G mmWave)
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#111827]">
              Live Signal Wavefront Propagation{' '}
              <span className="text-base font-medium text-[#6B7280]">
                (Visualizing Clutter & LoS-NLoS Transitions)
              </span>
            </h2>
          </div>

          {/* Animation Controls */}
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
                setFreqUnit('MHz');
                setFreqMhz(900);
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

        {/* Controls Bar with MHz/GHz Toggle & Presets */}
        <div className="bg-[#F3F4EF] p-5 rounded-2xl mb-6 space-y-4">
          <div className="grid sm:grid-cols-2 gap-6">
            {/* Frequency Slider & Unit Toggle */}
            <div>
              <div className="flex items-center justify-between text-xs font-bold text-[#111827] mb-1">
                <span>Carrier Frequency:</span>
                <div className="inline-flex rounded-lg border border-black/15 p-0.5 bg-white">
                  <button
                    type="button"
                    onClick={() => {
                      setFreqUnit('MHz');
                      if (freqMhz > 3500) setFreqMhz(900);
                    }}
                    className={`px-2 py-0.5 rounded text-[10px] font-bold transition ${
                      freqUnit === 'MHz' ? 'bg-[#134729] text-white' : 'text-[#6B7280]'
                    }`}
                  >
                    MHz
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setFreqUnit('GHz');
                      if (freqMhz < 1000) setFreqMhz(28000);
                    }}
                    className={`px-2 py-0.5 rounded text-[10px] font-bold transition ${
                      freqUnit === 'GHz' ? 'bg-[#134729] text-white' : 'text-[#6B7280]'
                    }`}
                  >
                    GHz
                  </button>
                </div>
              </div>

              <div className="flex items-baseline justify-between mb-2">
                <span className="text-[11px] text-[#6B7280]">
                  {isMmWave ? '5G/6G Millimeter-Wave Regime' : 'Sub-6 GHz Cellular Regime'}
                </span>
                <span className="font-mono font-extrabold text-sm text-[#134729]">
                  {freqUnit === 'GHz' || freqMhz >= 1000
                    ? `${(freqMhz / 1000).toFixed(2)} GHz`
                    : `${freqMhz} MHz`}
                </span>
              </div>

              {freqUnit === 'GHz' ? (
                <input
                  type="range"
                  min="0.5"
                  max="100.0"
                  step="0.5"
                  value={freqMhz / 1000}
                  onChange={(e) => handleFreqSlider(e.target.value)}
                  className="rf-slider"
                />
              ) : (
                <input
                  type="range"
                  min="150"
                  max="3500"
                  step="50"
                  value={freqMhz}
                  onChange={(e) => handleFreqSlider(e.target.value)}
                  className="rf-slider"
                />
              )}
            </div>

            {/* Tower Antenna Height */}
            <div>
              <div className="flex justify-between text-xs font-bold text-[#111827] mb-2">
                <span>Tower Antenna Height hₜ (Base Station in m):</span>
                <span className="font-mono text-[#134729]">{ht} meters</span>
              </div>
              <input
                type="range"
                min={isMmWave ? 5 : 15}
                max={isMmWave ? 30 : 200}
                step={isMmWave ? 1 : 5}
                value={ht}
                onChange={(e) => setHt(Number(e.target.value))}
                className="rf-slider"
              />
              <div className="flex justify-between text-[11px] text-[#6B7280] mt-1">
                <span>{isMmWave ? '5 m (Lamp Post)' : '15 m (Rooftop)'}</span>
                <span>{isMmWave ? '30 m (UMi Pole)' : '200 m (Macro Tower)'}</span>
              </div>
            </div>
          </div>

          {/* Quick Frequency Band Pills */}
          <div className="pt-2 border-t border-black/10 flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-bold text-[#6B7280]">Quick Bands:</span>
            {[
              { label: '900 MHz (GSM Course)', mhz: 900, unit: 'MHz', ht: 30 },
              { label: '1800 MHz (LTE)', mhz: 1800, unit: 'MHz', ht: 40 },
              { label: '3.5 GHz (5G C-Band)', mhz: 3500, unit: 'GHz', ht: 25 },
              { label: '28 GHz (5G mmWave)', mhz: 28000, unit: 'GHz', ht: 10 },
              { label: '39 GHz (5G mmWave)', mhz: 39000, unit: 'GHz', ht: 10 },
              { label: '73 GHz (6G sub-THz)', mhz: 73000, unit: 'GHz', ht: 10 },
            ].map((pill) => (
              <button
                key={pill.label}
                type="button"
                onClick={() => {
                  setFreqUnit(pill.unit);
                  setFreqMhz(pill.mhz);
                  setHt(pill.ht);
                }}
                className={`px-3 py-1 rounded-full text-xs font-bold border transition ${
                  freqMhz === pill.mhz
                    ? 'bg-[#134729] text-[#A8EB12] border-[#134729] shadow-xs'
                    : 'bg-white hover:bg-[#e4e6df] text-[#374151] border-black/10'
                }`}
              >
                {pill.label}
              </button>
            ))}
          </div>
        </div>

        {/* Canvas Viewport */}
        <canvas
          ref={canvasRef}
          className="w-full h-[310px] rounded-2xl border border-black/10 block"
        />

        {/* Live Telemetry Readout Cards */}
        {isMmWave ? (
          /* mmWave Telemetry (3GPP & IEEE Access Transitions) */
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
            <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5">
              <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                Microcell Distance
              </div>
              <div className="text-2xl font-extrabold font-mono text-[#111827] mt-1">
                {liveStats.d < 1.0 ? `${Math.round(liveStats.d * 1000)} m` : `${liveStats.d.toFixed(2)} km`}
              </div>
              <div className="text-[11px] text-[#6B7280] mt-1">Street canyon position</div>
            </div>

            <div className="p-4 rounded-2xl bg-cyan-50 border border-cyan-200">
              <div className="flex items-center gap-2 text-[11px] font-bold text-cyan-950 uppercase">
                <span className="w-2.5 h-2.5 rounded-full bg-cyan-500" />
                Cyan Arc: 3GPP LoS (dB)
              </div>
              <div className="text-2xl font-extrabold font-mono text-cyan-950 mt-1">
                {liveStats.umi_los.toFixed(2)} dB
              </div>
              <div className="text-[11px] text-cyan-800 mt-1">Clear line-of-sight reach</div>
            </div>

            <div className="p-4 rounded-2xl bg-lime-50 border border-lime-300">
              <div className="flex items-center gap-2 text-[11px] font-bold text-lime-950 uppercase">
                <span className="w-2.5 h-2.5 rounded-full bg-[#84cc16]" />
                Lime Arc: IEEE Transition (dB)
              </div>
              <div className="text-2xl font-extrabold font-mono text-lime-950 mt-1">
                {liveStats.umi_trans.toFixed(2)} dB
              </div>
              <div className="text-[11px] text-lime-900 mt-1">LoS-to-NLoS state transition</div>
            </div>

            <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200">
              <div className="flex items-center gap-2 text-[11px] font-bold text-rose-950 uppercase">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                Rose Arc: 3GPP NLoS (dB)
              </div>
              <div className="text-2xl font-extrabold font-mono text-rose-950 mt-1">
                {liveStats.umi_nlos.toFixed(2)} dB
              </div>
              <div className="text-[11px] text-rose-800 mt-1">Non-line-of-sight obstruction</div>
            </div>
          </div>
        ) : (
          /* Sub-6 GHz Telemetry (Friis, Okumura, Hata) */
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
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
              <div className="text-[11px] text-sky-800 mt-1">Theoretical lower bound</div>
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
              <div className="text-[11px] text-red-800 mt-1">Blocked by building clutter</div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
