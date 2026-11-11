import React, { useState } from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import StandardsBar from './components/StandardsBar';
import FeaturesGrid from './components/FeaturesGrid';
import StepsHighlight from './components/StepsHighlight';
import WaveCanvas from './components/WaveCanvas';
import SimulatorStudio from './components/SimulatorStudio';
import Footer from './components/Footer';

export default function App() {
  const [activeView, setActiveView] = useState('landing');
  const [focusModel, setFocusModel] = useState(null);

  const openSimulator = (modelKey = null) => {
    setFocusModel(modelKey);
    setActiveView('simulator');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const scrollToWave = () => {
    if (activeView !== 'landing') {
      setActiveView('landing');
      setTimeout(() => {
        document.getElementById('wave-animation')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } else {
      document.getElementById('wave-animation')?.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-[#F3F4EF] flex flex-col">
      <Navbar activeView={activeView} setActiveView={setActiveView} />

      <main className="flex-1">
        {activeView === 'landing' ? (
          <>
            <HeroSection
              onLaunchSimulator={() => openSimulator()}
              onWatchAnimation={scrollToWave}
            />
            <StandardsBar />
            <FeaturesGrid onSelectModel={(key) => openSimulator(key)} />
            <StepsHighlight onLaunchSimulator={() => openSimulator()} />
            <WaveCanvas />
          </>
        ) : (
          <SimulatorStudio initialModelFocus={focusModel} />
        )}
      </main>

      <Footer onLaunchSimulator={() => openSimulator()} />
    </div>
  );
}
