import React from 'react';
import { motion } from 'framer-motion';
import { ArrowUpRight } from 'lucide-react';

export default function FeaturesGrid({ onSelectModel }) {
  const cards = [
    {
      key: 'fspl',
      title: 'Free Space Path Loss (Friis Lower Bound)',
      watermark: 'λ',
      bg: 'bg-gradient-to-br from-[#d9f99d] to-[#bef264] text-[#0B2E1A]',
      desc: 'Idealized line-of-sight vacuum baseline. Loss rises strictly at 20 dB/decade (n = 2). Serves as the theoretical minimum reference.',
      reading: '1 km: 91.52 dB  •  20 km: 117.55 dB',
    },
    {
      key: 'okumura',
      title: 'Okumura Empirical (Tokyo Field Curves)',
      watermark: 'Aμ',
      bg: 'bg-gradient-to-br from-[#84cc16] to-[#4d7c0f] text-white',
      desc: 'Calibrated directly from 1968 drive-test measurements in Tokyo. Captures terrain roughness and open-area vs urban morphology.',
      reading: '1 km: 97.90 dB  •  20 km: 143.73 dB',
    },
    {
      key: 'hata',
      title: 'Okumura-Hata Urban (Macrocell Standard)',
      watermark: 'dB',
      bg: 'bg-gradient-to-br from-[#bef264] to-[#65a30d] text-[#0B2E1A]',
      desc: 'Closed-form cellular engineering equations modeling rooftop diffraction and building clutter across 150–1500 MHz.',
      reading: '1 km: 126.40 dB  •  20 km: 172.23 dB',
    },
    {
      key: 'shadowing',
      title: 'Log-Normal Shadowing (Stochastic Outage)',
      watermark: 'σ',
      bg: 'bg-gradient-to-br from-[#d9f99d] to-[#a3e635] text-[#0B2E1A]',
      desc: 'Adds reproducible zero-mean Gaussian variation Xσ to compute link fade margins and 95% cell-edge coverage reliability.',
      reading: 'Configurable σ (dB)  •  Outage Probability (%)',
    },
  ];

  return (
    <section id="models-section" className="max-w-7xl mx-auto px-6 py-20">
      {/* Header Row */}
      <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
        <span className="inline-block px-4 py-1.5 rounded-full bg-[#134729] text-white text-xs font-bold">
          Propagation Engines (7 Models Available)
        </span>
        <span className="text-xs font-semibold text-[#6B7280]">
          Everything you need for RF planning, nothing you don&apos;t.
        </span>
      </div>

      {/* Editorial Headline */}
      <h2 className="text-3xl sm:text-4xl lg:text-[42px] font-bold text-[#111827] max-w-4xl leading-[1.18] tracking-tight mb-14">
        Achieve <span className="text-[#58b92c]">propagation clarity</span> and predict wireless
        coverage with verified <span className="text-[#0e7490]">engineering models</span> — all in
        one unified simulation platform.
      </h2>

      {/* 4 Tall Gradient Feature Cards */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {cards.map((card, i) => (
          <motion.div
            key={card.key}
            initial={{ opacity: 0, y: 24 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.45, delay: i * 0.08 }}
            whileHover={{ y: -6 }}
            onClick={() => onSelectModel(card.key)}
            className={`${card.bg} relative rounded-3xl p-6 h-80 flex flex-col justify-between overflow-hidden cursor-pointer shadow-lg border border-black/5 group`}
          >
            {/* Subtle Oversized Watermark */}
            <div className="absolute -bottom-8 -right-4 text-[150px] font-extrabold opacity-10 select-none pointer-events-none leading-none">
              {card.watermark}
            </div>

            <div className="relative z-10 flex items-start justify-between gap-2">
              <h3 className="text-lg font-extrabold leading-snug">{card.title}</h3>
              <span className="w-8 h-8 rounded-full bg-black/10 flex items-center justify-center shrink-0 group-hover:scale-110 transition">
                <ArrowUpRight className="w-4 h-4" />
              </span>
            </div>

            <div className="relative z-10 space-y-3">
              <p className="text-xs leading-relaxed opacity-90 font-medium">{card.desc}</p>
              <div className="pt-2 border-t border-black/10 text-[11px] font-mono font-bold opacity-85">
                {card.reading}
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
}
