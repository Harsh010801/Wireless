import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Play, Wifi, Activity, Radio } from 'lucide-react';

export default function HeroSection({ onLaunchSimulator, onWatchAnimation }) {
  const tags = [
    '3GPP mmWave (28/39/73 GHz)',
    'IEEE Access (LoS-NLoS Transition)',
    'Free Space (Friis Minimum)',
    'Hata Urban (Macrocell)',
    'COST-231 (2 GHz Extended)',
    'Okumura (Tokyo Empirical)',
    'Two-Ray Ground Bounce',
    'Log-Normal Shadowing (σ Outage)',
  ];

  const miniBars = [38, 52, 46, 70, 64, 86, 78, 95, 88];

  return (
    <section className="max-w-7xl mx-auto px-6 pt-12 pb-16 lg:pt-20 lg:pb-24 overflow-hidden">
      <div className="grid lg:grid-cols-12 gap-12 items-center">
        {/* LEFT COLUMN — Headline, CTAs & Model Tags */}
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.65, ease: 'easeOut' }}
          className="lg:col-span-6 space-y-6"
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#134729]/10 text-[#134729] text-xs font-bold tracking-wide">
            <span className="w-2 h-2 rounded-full bg-[#58b92c] animate-pulse" />
            WIRELESS & MOBILE COMMUNICATION (SIMULATION STUDY)
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-[54px] font-extrabold text-[#111827] leading-[1.08] tracking-tight">
            Your Partner in <br />
            Smarter <span className="text-[#58b92c]">Signal Loss</span> <br />
            Analysis
          </h1>

          <p className="text-base sm:text-lg text-[#4B5563] max-w-xl leading-relaxed">
            Evaluate legacy sub-6 GHz models (Okumura, Hata, COST-231) and modern
            <span className="font-bold text-[#134729]"> 5G / 6G Millimeter-Wave (28–100 GHz) </span>
            propagation with 3GPP TR 38.901 & IEEE Access 2026 statistical LoS–NLoS transition modeling.
          </p>

          {/* CTA Buttons with bracket explanations */}
          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={onLaunchSimulator}
              className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full bg-[#A8EB12] hover:bg-[#9ae009] text-[#0B2E1A] font-bold text-sm shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all"
            >
              Launch Live Simulator (Interactive Graphs)
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              onClick={onWatchAnimation}
              className="inline-flex items-center gap-3 text-sm font-semibold text-[#111827] hover:text-[#134729] group transition"
            >
              <span className="w-11 h-11 rounded-full bg-[#134729] text-[#A8EB12] flex items-center justify-center shadow-md group-hover:scale-105 transition">
                <Play className="w-4 h-4 fill-current ml-0.5" />
              </span>
              Watch Wave Animation (Live Motion)
            </button>
          </div>

          {/* Model Pill Tags Row */}
          <div className="pt-6 border-t border-black/10">
            <p className="text-xs font-semibold uppercase tracking-wider text-[#6B7280] mb-3">
              Sub-6 GHz & 5G/6G mmWave Models (All Calibrated & Ready to Compare):
            </p>
            <div className="flex flex-wrap gap-2">
              {tags.map((tag) => (
                <button
                  key={tag}
                  onClick={onLaunchSimulator}
                  className="px-3.5 py-1.5 rounded-full border border-black/15 bg-white/70 hover:bg-[#A8EB12]/40 hover:border-[#134729]/40 text-xs font-semibold text-[#1F2937] transition"
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
        </motion.div>

        {/* RIGHT COLUMN — Orbital Rings + Floating 3D Signal Telemetry Cards */}
        <motion.div
          initial={{ opacity: 0, scale: 0.94 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.75, delay: 0.15 }}
          className="lg:col-span-6 relative min-h-[430px] flex items-center justify-center"
        >
          {/* Outer Orbital Radar Rings */}
          <div className="absolute w-[410px] h-[410px] rounded-full border border-[#58b92c]/25 animate-orbit pointer-events-none" />
          <div className="absolute w-[310px] h-[310px] rounded-full border border-[#134729]/15 animate-orbit-reverse pointer-events-none" />
          <div className="absolute w-[210px] h-[210px] rounded-full bg-[#A8EB12]/10 blur-2xl pointer-events-none" />

          {/* Floating Mini Statistics Card (Top Left) */}
          <motion.div
            animate={{ y: [0, -8, 0] }}
            transition={{ repeat: Infinity, duration: 4.5, ease: 'easeInOut' }}
            className="absolute top-3 left-2 sm:left-6 z-30 bg-white rounded-2xl p-4 shadow-xl border border-black/5 w-52"
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-bold text-[#111827]">Path Loss Trend</span>
              <span className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-[#A8EB12]/30 text-[#134729]">
                900 MHz
              </span>
            </div>
            <div className="flex items-end justify-between gap-3">
              <div>
                <div className="text-[11px] text-[#6B7280]">1 km → 20 km</div>
                <div className="text-sm font-extrabold text-[#111827] font-mono">+45.8 dB</div>
              </div>
              <div className="flex items-end gap-1 h-10">
                {miniBars.map((val, idx) => (
                  <div
                    key={idx}
                    style={{ height: `${val}%` }}
                    className={`w-1.5 rounded-t ${
                      idx >= 6 ? 'bg-[#58b92c]' : 'bg-[#134729]/25'
                    }`}
                  />
                ))}
              </div>
            </div>
          </motion.div>

          {/* Top Floating Vibrant Lime RF Card (Hata Urban) */}
          <motion.div
            animate={{ y: [0, -6, 0] }}
            transition={{ repeat: Infinity, duration: 5.2, ease: 'easeInOut', delay: 0.4 }}
            className="relative z-20 translate-x-6 -translate-y-10 card-lime-gradient rounded-2xl p-6 w-80 sm:w-[340px] shadow-2xl border border-white/40 text-[#0B2E1A]"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-extrabold uppercase tracking-widest opacity-80">
                HATA URBAN MODEL
              </span>
              <Wifi className="w-5 h-5 opacity-80" />
            </div>
            <div className="mt-5">
              <div className="text-[11px] font-semibold opacity-75">
                Predicted Attenuation @ 20 km (Cell Edge)
              </div>
              <div className="text-3xl font-extrabold font-mono tracking-tight mt-0.5">
                172.23 dB
              </div>
            </div>
            <div className="mt-6 flex items-center justify-between text-xs font-bold">
              <div>
                <div className="text-[10px] opacity-70 uppercase">Freq / Tower</div>
                <div>900 MHz / 30 m</div>
              </div>
              <div>
                <div className="text-[10px] opacity-70 uppercase">Decay Slope</div>
                <div>35.22 dB / dec</div>
              </div>
              <div className="px-2.5 py-1 rounded-full bg-[#0B2E1A] text-[#A8EB12] text-[10px]">
                REALISTIC
              </div>
            </div>
          </motion.div>

          {/* Bottom Floating Dark Forest Green RF Card (Free Space) */}
          <motion.div
            animate={{ y: [0, 6, 0] }}
            transition={{ repeat: Infinity, duration: 5.6, ease: 'easeInOut' }}
            className="absolute bottom-6 left-4 sm:left-10 z-10 card-forest-gradient rounded-2xl p-6 w-80 sm:w-[330px] shadow-2xl border border-white/10 text-white"
          >
            <div className="flex items-center justify-between">
              <span className="font-extrabold tracking-wider text-sm text-[#A8EB12]">
                FRIIS FREE SPACE
              </span>
              <Radio className="w-5 h-5 text-[#A8EB12]" />
            </div>
            <div className="mt-5">
              <div className="text-[11px] text-white/70">
                Theoretical Lower Bound @ 1 km (No Clutter)
              </div>
              <div className="text-3xl font-extrabold font-mono tracking-tight mt-0.5">
                91.52 dB
              </div>
            </div>
            <div className="mt-5 flex items-center justify-between text-xs text-white/80">
              <span>Exponent n = 2.0</span>
              <span className="font-mono text-[#A8EB12]">20 dB / dec</span>
            </div>
          </motion.div>

          {/* Floating Divergence Pill Badge (Bottom Right) */}
          <motion.div
            animate={{ y: [0, -5, 0] }}
            transition={{ repeat: Infinity, duration: 3.8, ease: 'easeInOut' }}
            className="absolute bottom-14 right-4 sm:right-8 z-30 bg-white rounded-full px-4 py-2 shadow-lg border border-black/5 flex items-center gap-2"
          >
            <span className="w-7 h-7 rounded-full bg-[#134729] text-[#A8EB12] flex items-center justify-center">
              <Activity className="w-3.5 h-3.5" />
            </span>
            <div className="text-left">
              <div className="text-[10px] text-[#6B7280] font-semibold leading-none">
                Reality Gap (Δ)
              </div>
              <div className="text-xs font-extrabold text-[#111827] font-mono">
                +54.68 dB @ 20km
              </div>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
}

