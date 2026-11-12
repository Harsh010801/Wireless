import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';

export default function FeaturesGrid({ onSelectModel }) {
  const cards = [
    {
      key: 'mmwave_transition',
      title: '5G / 6G mmWave LoS–NLoS Transition (IEEE Access 2026)',
      watermark: '6G',
      bg: 'bg-gradient-to-br from-[#134729] to-[#0B2E1A] text-white',
      badge: 'NEW • 2026 RESEARCH',
      desc: 'Statistical state transition model (Inam Ullah et al., IEEE Access). Evaluates 3GPP TR 38.901 LoS/NLoS probabilities across 28 GHz, 39 GHz, and 73 GHz sub-THz.',
      reading: '28 GHz (n257) • 73 GHz 6G • P_LoS(d) Decay',
    },
    {
      key: 'hata',
      title: 'Okumura-Hata Urban (Macrocell Cellular Standard)',
      watermark: 'dB',
      bg: 'bg-gradient-to-br from-[#bef264] to-[#65a30d] text-[#0B2E1A]',
      badge: 'CLASSIC MACRO',
      desc: 'Closed-form cellular planning equations modeling building clutter, rooftop diffraction, and mobile antenna height corrections across 150–1500 MHz.',
      reading: '1 km: 126.40 dB • 20 km: 172.23 dB (900 MHz)',
    },
    {
      key: 'cost231',
      title: 'COST-231 Hata (1.5–2.0 GHz Extended Standard)',
      watermark: 'PCS',
      bg: 'bg-gradient-to-br from-[#84cc16] to-[#4d7c0f] text-white',
      badge: 'EUROPEAN PCS',
      desc: 'EURO-COST extension calibrated for 1800 MHz DCS/LTE macrocells in medium and metropolitan cities with constant clutter offsets Cm.',
      reading: '1800 MHz LTE • Urban Center Clutter',
    },
    {
      key: 'fspl',
      title: 'Free Space Path Loss (Friis Theoretical Minimum)',
      watermark: 'λ',
      bg: 'bg-gradient-to-br from-[#d9f99d] to-[#bef264] text-[#0B2E1A]',
      badge: 'VACUUM BOUND',
      desc: 'Idealized line-of-sight reference. Loss rises strictly at 20 dB/decade (n = 2). Defines the physical theoretical lower bound for any antenna.',
      reading: '1 km: 91.52 dB • 20 km: 117.55 dB',
    },
    {
      key: 'shadowing',
      title: 'Log-Normal Shadowing (Stochastic Fade Margin)',
      watermark: 'σ',
      bg: 'bg-gradient-to-br from-[#d9f99d] to-[#a3e635] text-[#0B2E1A]',
      badge: 'STOCHASTIC',
      desc: 'Adds zero-mean Gaussian random variation Xσ ~ N(0, σ²) to model obstacle clutter variability, computing cell-edge outage probabilities.',
      reading: 'Configurable σ (dB) • 95% Outage Thresholds',
    },
  ];

  return (
    <section id="models-section" className="max-w-7xl mx-auto px-6 py-20">
      {/* Header Row */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <span className="inline-block px-4 py-1.5 rounded-full bg-[#134729] text-white text-xs font-bold">
          Propagation Engines (Sub-6 GHz & 5G/6G mmWave)
        </span>
        <span className="text-xs font-semibold text-[#6B7280]">
          From Legacy Cellular (900/1800 MHz) to Next-Gen Millimeter-Wave (28–100 GHz)
        </span>
      </div>

      {/* Editorial Headline */}
      <h2 className="text-3xl sm:text-4xl lg:text-[42px] font-bold text-[#111827] max-w-4xl leading-[1.18] tracking-tight mb-14">
        Achieve <span className="text-[#58b92c]">propagation clarity</span> across Sub-6 GHz and{' '}
        <span className="text-[#0e7490]">5G/6G Millimeter-Wave</span> — with verified 3GPP and IEEE Access models.
      </h2>

      {/* Feature Cards Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-5">
        {cards.map((card, i) => (
          <motion.div
            key={card.key}
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.45, delay: i * 0.08 }}
            whileHover={{ y: -6 }}
            onClick={() => onSelectModel(card.key)}
            className={`${card.bg} relative rounded-3xl p-5 h-[340px] flex flex-col justify-between overflow-hidden cursor-pointer shadow-lg border border-black/5 group`}
          >
            {/* Subtle Oversized Watermark */}
            <div className="absolute -bottom-6 -right-2 text-[120px] font-extrabold opacity-10 select-none pointer-events-none leading-none">
              {card.watermark}
            </div>

            <div className="relative z-10">
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-[10px] font-extrabold px-2 py-0.5 rounded-full bg-black/15 uppercase tracking-wide">
                  {card.badge}
                </span>
                <span className="w-7 h-7 rounded-full bg-black/10 flex items-center justify-center shrink-0 group-hover:scale-110 transition">
                  <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>
              <h3 className="text-base font-extrabold leading-snug mt-1">{card.title}</h3>
            </div>

            <div className="relative z-10 space-y-2">
              <p className="text-[11px] leading-relaxed opacity-90 font-medium">{card.desc}</p>
              <div className="pt-2 border-t border-black/10 text-[10px] font-mono font-bold opacity-85">
                {card.reading}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
