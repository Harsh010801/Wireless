import React from 'react';
import { Radio, ArrowRight } from 'lucide-react';

export default function Footer({ onLaunchSimulator }) {
  return (
    <footer id="team-footer" className="bg-[#141517] text-white py-16 px-6 mt-12">
      <div className="max-w-7xl mx-auto">
        <div className="grid md:grid-cols-12 gap-10 pb-12 border-b border-white/10">
          <div className="md:col-span-5 space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-[#A8EB12] text-[#0B2E1A] flex items-center justify-center">
                <Radio className="w-5 h-5" />
              </div>
              <span className="font-extrabold text-xl tracking-tight">
                WAVEPULSE<span className="text-[#A8EB12]">RF</span>
              </span>
            </div>
            <p className="text-sm text-white/70 max-w-md leading-relaxed">
              Academic simulation platform for{' '}
              <strong className="text-white">Wireless and Mobile Communication</strong>{' '}
              (B.Tech CSE, 7th Semester), Department of Computing Technologies, SRM Institute of
              Science &amp; Technology.
            </p>
            <button
              onClick={onLaunchSimulator}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-[#A8EB12] text-[#0B2E1A] text-xs font-extrabold hover:bg-[#bef264] transition"
            >
              Launch Live Simulator (Interactive Lab)
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="md:col-span-4 space-y-3">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-[#A8EB12]">
              Project Team Members
            </h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between border-b border-white/5 pb-1.5">
                <span className="font-semibold">Harsh Yadav</span>
                <span className="font-mono text-white/60 text-xs">RA2311003011546</span>
              </div>
              <div className="flex justify-between border-b border-white/5 pb-1.5">
                <span className="font-semibold">Utkarsh Dabas</span>
                <span className="font-mono text-white/60 text-xs">RA2311003011550</span>
              </div>
              <div className="flex justify-between">
                <span className="font-semibold">Tamanna Singh</span>
                <span className="font-mono text-white/60 text-xs">RA2311003011570</span>
              </div>
            </div>
          </div>

          <div className="md:col-span-3 space-y-3">
            <h4 className="text-xs font-extrabold uppercase tracking-wider text-[#A8EB12]">
              Project Architecture
            </h4>
            <ul className="space-y-1.5 text-xs text-white/70 font-mono">
              <li>frontend/  (React + Tailwind UI)</li>
              <li>backend/   (FastAPI REST API)</li>
              <li>src/       (7 Python RF Models)</li>
              <li>tests/     (32 Pytest Assertions)</li>
            </ul>
          </div>
        </div>

        <div className="pt-6 flex flex-wrap items-center justify-between gap-4 text-xs text-white/50">
          <span>
            Comparative Analysis of Wireless Signal Propagation Models — Academic Year 2025–2026
          </span>
          <span>All scientific simulation data preserved identically in src/propagation/</span>
        </div>
      </div>
    </footer>
  );
}

