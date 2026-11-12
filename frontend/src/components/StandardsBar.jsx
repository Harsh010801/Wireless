import React from 'react';

export default function StandardsBar() {
  const standards = [
    { name: '3GPP TR 38.901', sub: '5G / 6G mmWave (0.5–100 GHz)' },
    { name: 'IEEE Access (2026)', sub: 'Inam Ullah et al. LoS-NLoS' },
    { name: 'IEEE VT', sub: 'Hata (1980) Macrocell' },
    { name: 'ECL TOKYO', sub: 'Okumura (1968)' },
    { name: 'COST-231', sub: 'European 2 GHz PCS' },
    { name: 'SRM CTECH', sub: 'Wireless Research Lab' },
  ];

  return (
    <section className="max-w-6xl mx-auto px-6 py-8 border-y border-black/5">
      <p className="text-center text-xs font-semibold uppercase tracking-widest text-[#6B7280] mb-6">
        Built on International Standards (3GPP, ITU-R) & Peer-Reviewed Literature (IEEE Access 2026)
      </p>
      <div className="flex flex-wrap items-center justify-center md:justify-between gap-6 opacity-85">
        {standards.map((s) => (
          <div key={s.name} className="text-center group hover:opacity-100 transition">
            <div className="text-lg font-extrabold tracking-tight text-[#374151] group-hover:text-[#134729] transition">
              {s.name}
            </div>
            <div className="text-[11px] font-medium text-[#6B7280]">{s.sub}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
