import React from 'react';
import { Radio, Play, Sliders } from 'lucide-react';

export default function Navbar({ activeView, setActiveView }) {
  const scrollTo = (id) => {
    if (activeView !== 'landing') {
      setActiveView('landing');
      setTimeout(() => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <header className="sticky top-0 z-50 backdrop-blur-md bg-[#F3F4EF]/85 border-b border-black/5">
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
        {/* Brand Logo */}
        <button
          onClick={() => setActiveView('landing')}
          className="flex items-center gap-2.5 group text-left"
        >
          <div className="w-9 h-9 rounded-xl bg-[#134729] flex items-center justify-center text-[#A8EB12] shadow-sm group-hover:scale-105 transition">
            <Radio className="w-5 h-5" />
          </div>
          <div>
            <span className="font-extrabold text-xl tracking-tight text-[#111827] block leading-none">
              WAVEPULSE<span className="text-[#58b92c]">RF</span>
            </span>
            <span className="text-[11px] font-medium text-[#6B7280] whitespace-nowrap">
              Signal Propagation Lab
            </span>
          </div>
        </button>

        {/* Centered Navigation Links */}
        <nav className="hidden lg:flex items-center gap-6 text-sm font-medium text-[#374151]">
          <button
            onClick={() => scrollTo('models-section')}
            className="hover:text-[#134729] transition whitespace-nowrap"
          >
            Models <span className="text-xs text-[#6B7280]">(Theory)</span>
          </button>
          <button
            onClick={() => scrollTo('steps-section')}
            className="hover:text-[#134729] transition whitespace-nowrap"
          >
            How It Works <span className="text-xs text-[#6B7280]">(Pipeline)</span>
          </button>
          <button
            onClick={() => scrollTo('wave-animation')}
            className="hover:text-[#134729] transition whitespace-nowrap"
          >
            Wave Motion <span className="text-xs text-[#6B7280]">(Animation)</span>
          </button>
          <button
            onClick={() => setActiveView('simulator')}
            className={`transition whitespace-nowrap ${
              activeView === 'simulator' ? 'text-[#134729] font-bold' : 'hover:text-[#134729]'
            }`}
          >
            Simulator <span className="text-xs text-[#6B7280]">(Interactive Graphs)</span>
          </button>
        </nav>

        {/* Action CTA Pills */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={() => scrollTo('wave-animation')}
            className="hidden sm:inline-flex items-center gap-1.5 px-4 py-2 rounded-full text-sm font-semibold text-[#111827] hover:bg-black/5 transition whitespace-nowrap"
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            Demo Animation
          </button>
          <button
            onClick={() => setActiveView(activeView === 'simulator' ? 'landing' : 'simulator')}
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-bold border border-[#134729]/30 bg-white hover:bg-[#A8EB12] hover:border-[#A8EB12] text-[#111827] shadow-sm transition-all duration-200 whitespace-nowrap"
          >
            <Sliders className="w-4 h-4" />
            {activeView === 'simulator' ? 'Back to Home (Landing)' : 'Open Simulator (Live Lab)'}
          </button>
        </div>
      </div>
    </header>
  );
}

