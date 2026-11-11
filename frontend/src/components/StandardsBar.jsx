import React from 'react';

export default function StandardsBar() {
  const standards = [
    { name: 'IEEE VT', sub: 'Hata (1980) Paper' },
    { name: 'ECL TOKYO', sub: 'Okumura (1968)' },
    { name: 'COST-231', sub: 'European 2 GHz Spec' },
    { name: 'MATLAB R2024b', sub: 'Matrix Benchmark' },
    { name: 'SRM CTECH', sub: '21CSE458T Lab' },
  ];

  return (
    <section className="max-w-6xl mx-auto px-6 py-8 border-y border-black/5">
      <p className="text-center text-xs font-semibold uppercase tracking-widest text-[#6B7280] mb-6">
        Built on Peer-Reviewed Standards & Academic Simulation Benchmarks
      </p>
      <div className="flex flex-wrap items-center justify-center md:justify-between gap-8 opacity-75">
        {standards.map((s) => (
          <div key={s.name} className="text-center group hover:opacity-100 transition">
            <div className="text-xl font-extrabold tracking-tight text-[#374151] group-hover:text-[#134729] transition">
              {s.name}
            </div>
            <div className="text-[11px] font-medium text-[#6B7280]">{s.sub}</div>
          </div>
        ))}
      </div>
    </section>
  );
}
