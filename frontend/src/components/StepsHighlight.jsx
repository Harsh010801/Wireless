import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sliders, BarChart3, CheckCircle2, Plus, Radio } from 'lucide-react';

export default function StepsHighlight({ onLaunchSimulator }) {
  const [selectedBand, setSelectedBand] = useState('900');

  const readings =
    selectedBand === '900'
      ? { label: '900 MHz GSM Macrocell', fspl: '117.55 dB', oku: '143.73 dB', hata: '172.23 dB', main: '172.23 dB' }
      : { label: '1800 MHz LTE PCS', fspl: '123.57 dB', oku: '150.11 dB', hata: '179.96 dB', main: '179.96 dB' };

  const steps = [
    {
      icon: Sliders,
      title: '1. Configure RF Link Parameters (Frequency, Heights & Terrain)',
      desc: 'Set carrier frequency (150–6000 MHz), base station height (30 m), mobile height (1.5 m), and terrain clutter preset.',
    },
    {
      icon: BarChart3,
      title: '2. Run Multi-Model Comparative Engine (7 Python & MATLAB Models)',
      desc: 'Compute vectorized path loss (dB), received power (dBm), and statistical variance simultaneously with zero manual formula errors.',
    },
    {
      icon: CheckCircle2,
      title: '3. Verify Fade Margin & Export Research Deliverables (CSV, PNG, DOCX)',
      desc: 'Inspect link reliability, visualize outage zones below sensitivity thresholds, and export publication-grade academic plots.',
    },
  ];

  return (
    <section
      id="steps-section"
      className="relative bg-[#A8EB12] py-20 px-6 overflow-hidden border-y border-black/10"
    >
      {/* Subtle Giant Background Typography Matching Reference */}
      <div className="absolute inset-x-0 -bottom-10 text-center text-[140px] sm:text-[210px] font-extrabold tracking-tighter text-[#0B2E1A]/[0.05] select-none pointer-events-none leading-none">
        WAVEPULSE
      </div>

      <div className="max-w-7xl mx-auto grid lg:grid-cols-12 gap-12 items-center relative z-10">
        {/* LEFT — Floating Dark Obsidian Interactive Widget Card */}
        <motion.div
          initial={{ opacity: 0, x: -24 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.55 }}
          className="lg:col-span-5"
        >
          <div className="bg-[#141517] text-white rounded-3xl p-7 shadow-2xl border border-white/10">
            {/* Top Bar inside Dark Widget */}
            <div className="flex items-center justify-between gap-2 mb-6">
              <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/10 text-xs font-semibold">
                <Radio className="w-3.5 h-3.5 text-[#A8EB12]" />
                <span>{readings.label}</span>
              </div>
              <button
                onClick={() => setSelectedBand(selectedBand === '900' ? '1800' : '900')}
                className="px-3 py-1 rounded-full bg-white/10 hover:bg-white/20 text-[11px] font-bold transition"
                title="Switch Carrier Frequency Band"
              >
                Switch to {selectedBand === '900' ? '1800 MHz' : '900 MHz'}
              </button>
            </div>

            {/* Big Numerical Readout */}
            <div className="mb-6">
              <div className="text-xs text-white/60 font-medium">
                Hata Urban Path Loss @ 20 km Cell Edge
              </div>
              <div className="text-4xl sm:text-5xl font-extrabold font-mono tracking-tight mt-1 text-white">
                {readings.main}
              </div>
              <div className="text-xs text-[#A8EB12] mt-2 font-mono">
                FSPL: {readings.fspl} &nbsp;|&nbsp; Okumura Open: {readings.oku}
              </div>
            </div>

            {/* Bottom Action Pills Matching Reference Card */}
            <div className="flex flex-wrap items-center gap-2.5 pt-4 border-t border-white/10">
              <button
                onClick={() => setSelectedBand('900')}
                className={`px-4 py-2 rounded-full text-xs font-bold border transition ${
                  selectedBand === '900'
                    ? 'bg-white text-[#141517] border-white'
                    : 'bg-transparent text-white border-white/20 hover:border-white/50'
                }`}
              >
                900 MHz (GSM Benchmark)
              </button>
              <button
                onClick={() => setSelectedBand('1800')}
                className={`px-4 py-2 rounded-full text-xs font-bold border transition ${
                  selectedBand === '1800'
                    ? 'bg-white text-[#141517] border-white'
                    : 'bg-transparent text-white border-white/20 hover:border-white/50'
                }`}
              >
                1800 MHz (LTE PCS)
              </button>
              <button
                onClick={onLaunchSimulator}
                className="ml-auto w-9 h-9 rounded-full bg-[#A8EB12] hover:bg-[#bef264] text-[#0B2E1A] flex items-center justify-center shadow-md transition"
                title="Open Full Simulator"
              >
                <Plus className="w-5 h-5 stroke-[2.5]" />
              </button>
            </div>
          </div>
        </motion.div>

        {/* RIGHT — Headline + 3 Structured Steps */}
        <motion.div
          initial={{ opacity: 0, x: 24 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.55 }}
          className="lg:col-span-7 text-[#0B2E1A]"
        >
          <h2 className="text-3xl sm:text-4xl font-extrabold leading-tight tracking-tight mb-8">
            Start Analyzing Signal Propagation in 3 Easy Steps
          </h2>

          <div className="space-y-6">
            {steps.map((step) => {
              const Icon = step.icon;
              return (
                <div key={step.title} className="flex items-start gap-4">
                  <div className="w-11 h-11 rounded-2xl bg-[#134729]/15 flex items-center justify-center shrink-0 text-[#0B2E1A]">
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-base sm:text-lg leading-snug">{step.title}</h3>
                    <p className="text-sm text-[#0B2E1A]/80 mt-1 leading-relaxed">{step.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
