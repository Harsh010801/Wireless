import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  AreaChart,
  Area,
} from 'recharts';
import {
  Sliders,
  Download,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
  Info,
  TrendingUp,
  Zap,
  Table2,
  Activity,
  FileText,
  Radio,
  BookOpen,
  HelpCircle,
} from 'lucide-react';
import {
  fetchSimulation,
  fetchComparisonMatrix,
  fetchBenchmark900MHz,
  evaluateLinkBudget,
  fetchMmWaveTransition,
} from '../services/api';

const ALL_MODELS = [
  { key: 'fspl', label: 'Free Space (Friis — Theoretical Minimum)', color: '#0284c7', dash: undefined, lineDesc: 'Solid Blue' },
  { key: 'two_ray', label: 'Two-Ray (Direct + Ground Bounce)', color: '#f97316', dash: '6 4', lineDesc: 'Dashed Orange' },
  { key: 'log_distance', label: 'Log-Distance (Configurable Exponent n)', color: '#16a34a', dash: '8 4 2 4', lineDesc: 'Dash-Dot Green' },
  { key: 'okumura', label: 'Okumura (Tokyo Drive-Test Curves)', color: '#dc2626', dash: '3 3', lineDesc: 'Dotted Red' },
  { key: 'hata', label: 'Okumura-Hata (Urban Macrocell Standard)', color: '#134729', dash: undefined, lineDesc: 'Solid Forest Green' },
  { key: 'cost231', label: 'COST-231 Hata (1.5–2.0 GHz Extended)', color: '#7c3aed', dash: '6 4', lineDesc: 'Dashed Violet' },
  { key: 'shadowing', label: 'Log-Normal Shadowing (Stochastic Xσ)', color: '#db2777', dash: undefined, lineDesc: 'Solid Magenta' },
  { key: 'mmwave_umi_los', label: '3GPP UMi LoS (5G/6G mmWave)', color: '#06b6d4', dash: undefined, lineDesc: 'Solid Cyan' },
  { key: 'mmwave_umi_nlos', label: '3GPP UMi NLoS (5G/6G mmWave)', color: '#e11d48', dash: '6 4', lineDesc: 'Dashed Rose' },
  { key: 'mmwave_transition', label: 'LoS–NLoS Transition (IEEE Access 2026)', color: '#84cc16', dash: '8 4', lineDesc: 'Long Dash Lime' },
  { key: 'mmwave_ci', label: 'Close-In (CI) mmWave Model (1m Ref)', color: '#ca8a04', dash: '3 3', lineDesc: 'Dotted Amber' },
];

export default function SimulatorStudio({ initialModelFocus }) {
  const [params, setParams] = useState({
    frequency_mhz: 900,
    environment: 'urban',
    min_distance_km: 1.0,
    max_distance_km: 20.0,
    num_points: 100,
    tx_power_dbm: 43.0,
    tx_gain_dbi: 15.0,
    rx_gain_dbi: 0.0,
    system_loss_db: 3.0,
    rx_sensitivity_dbm: -100.0,
    ht_m: 30.0,
    hr_m: 1.5,
    shadow_sigma_db: 6.0,
    models: [
      'fspl',
      'two_ray',
      'log_distance',
      'okumura',
      'hata',
      'cost231',
      'shadowing',
      'mmwave_umi_los',
      'mmwave_umi_nlos',
      'mmwave_transition',
    ],
  });

  const [freqUnit, setFreqUnit] = useState('MHz'); // 'MHz' or 'GHz'
  const [simData, setSimData] = useState(null);
  const [matrixData, setMatrixData] = useState(null);
  const [benchmarkData, setBenchmarkData] = useState(null);
  const [budgetTargetD, setBudgetTargetD] = useState(3.0);
  const [budgetEval, setBudgetEval] = useState(null);
  const [activeTab, setActiveTab] = useState('curves');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Dedicated mmWave Transition Explorer State
  const [mmwaveFreqGhz, setMmwaveFreqGhz] = useState(28.0);
  const [mmwaveData, setMmwaveData] = useState(null);
  const [mmwaveLoading, setMmwaveLoading] = useState(false);

  useEffect(() => {
    if (initialModelFocus) {
      if (initialModelFocus.startsWith('mmwave')) {
        setActiveTab('mmwave');
      } else if (ALL_MODELS.some((m) => m.key === initialModelFocus)) {
        setActiveTab('curves');
      }
    }
  }, [initialModelFocus]);

  useEffect(() => {
    let cancelled = false;
    const loadSim = async () => {
      setLoading(true);
      setError('');
      try {
        const res = await fetchSimulation(params);
        if (!cancelled) setSimData(res);
      } catch (err) {
        if (!cancelled) setError(err.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    const timer = setTimeout(loadSim, 180);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [params]);

  useEffect(() => {
    fetchComparisonMatrix().then(setMatrixData).catch(() => {});
    fetchBenchmark900MHz().then(setBenchmarkData).catch(() => {});
  }, []);

  useEffect(() => {
    let cancelled = false;
    setMmwaveLoading(true);
    fetchMmWaveTransition(mmwaveFreqGhz)
      .then((data) => {
        if (!cancelled) setMmwaveData(data);
      })
      .catch(() => {})
      .finally(() => {
        if (!cancelled) setMmwaveLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [mmwaveFreqGhz]);

  useEffect(() => {
    evaluateLinkBudget({
      target_distance_km: budgetTargetD,
      frequency_mhz: params.frequency_mhz,
      environment: params.environment,
      tx_power_dbm: params.tx_power_dbm,
      tx_gain_dbi: params.tx_gain_dbi,
      rx_gain_dbi: params.rx_gain_dbi,
      system_loss_db: params.system_loss_db,
      rx_sensitivity_dbm: params.rx_sensitivity_dbm,
      ht_m: params.ht_m,
      hr_m: params.hr_m,
    })
      .then(setBudgetEval)
      .catch(() => {});
  }, [budgetTargetD, params]);

  const toggleModel = (key) => {
    setParams((prev) => {
      const exists = prev.models.includes(key);
      if (exists && prev.models.length === 1) return prev;
      return {
        ...prev,
        models: exists ? prev.models.filter((m) => m !== key) : [...prev.models, key],
      };
    });
  };

  const applyPreset = (preset) => {
    if (preset === '900_course') {
      setFreqUnit('MHz');
      setParams((p) => ({
        ...p,
        frequency_mhz: 900,
        environment: 'urban',
        min_distance_km: 1.0,
        max_distance_km: 20.0,
        ht_m: 30.0,
        hr_m: 1.5,
      }));
    } else if (preset === '1800_lte') {
      setFreqUnit('MHz');
      setParams((p) => ({
        ...p,
        frequency_mhz: 1800,
        environment: 'suburban',
        min_distance_km: 0.2,
        max_distance_km: 12.0,
        ht_m: 40.0,
        hr_m: 1.5,
      }));
    } else if (preset === '28ghz_mmwave') {
      setFreqUnit('GHz');
      setMmwaveFreqGhz(28.0);
      setParams((p) => ({
        ...p,
        frequency_mhz: 28000,
        environment: 'urban',
        min_distance_km: 0.02,
        max_distance_km: 1.0,
        ht_m: 10.0,
        hr_m: 1.5,
      }));
    } else if (preset === '73ghz_6g') {
      setFreqUnit('GHz');
      setMmwaveFreqGhz(73.0);
      setParams((p) => ({
        ...p,
        frequency_mhz: 73000,
        environment: 'urban',
        min_distance_km: 0.01,
        max_distance_km: 0.5,
        ht_m: 10.0,
        hr_m: 1.5,
      }));
    }
  };

  const handleFrequencyInputChange = (val) => {
    const num = Number(val);
    if (freqUnit === 'GHz') {
      setParams({ ...params, frequency_mhz: Math.round(num * 1000) });
    } else {
      setParams({ ...params, frequency_mhz: num });
    }
  };

  const exportCsv = () => {
    if (!simData?.points?.length) return;
    const headers = Object.keys(simData.points[0]);
    const rows = simData.points.map((pt) => headers.map((h) => pt[h] ?? '').join(','));
    const csv = [headers.join(','), ...rows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `propagation_${params.frequency_mhz}MHz_${params.environment}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const activeModelsList = ALL_MODELS.filter((m) => params.models.includes(m.key));

  return (
    <div className="max-w-[1440px] mx-auto px-4 sm:px-6 py-8">
      {/* Studio Top Bar */}
      <div className="bg-white rounded-3xl p-6 shadow-sm border border-black/5 mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#A8EB12]/40 text-[#0B2E1A] text-xs font-extrabold">
            <Activity className="w-3.5 h-3.5" />
            WIRELESS PROPAGATION SIMULATION SUITE (SUB-6 GHz & 5G/6G mmWave)
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#111827] mt-2">
            Multi-Band Propagation Analyzer{' '}
            <span className="text-sm font-medium text-[#6B7280]">
              (Classical Empirical, 3GPP TR 38.901 & IEEE Access 2026 Transitions)
            </span>
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={() => applyPreset('900_course')}
            className="px-3.5 py-2 rounded-full bg-[#134729] text-[#A8EB12] text-xs font-bold hover:bg-[#0B2E1A] transition shadow-sm"
          >
            Preset: 900 MHz Urban (Course)
          </button>
          <button
            onClick={() => applyPreset('1800_lte')}
            className="px-3.5 py-2 rounded-full border border-black/15 bg-white hover:bg-[#F3F4EF] text-xs font-bold text-[#111827] transition"
          >
            Preset: 1800 MHz LTE
          </button>
          <button
            onClick={() => applyPreset('28ghz_mmwave')}
            className="px-3.5 py-2 rounded-full bg-cyan-600 hover:bg-cyan-700 text-white text-xs font-bold transition shadow-sm"
          >
            Preset: 28 GHz (5G mmWave)
          </button>
          <button
            onClick={() => applyPreset('73ghz_6g')}
            className="px-3.5 py-2 rounded-full bg-purple-700 hover:bg-purple-800 text-white text-xs font-bold transition shadow-sm"
          >
            Preset: 73 GHz (6G sub-THz)
          </button>
          <button
            onClick={exportCsv}
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-[#A8EB12] hover:bg-[#99dc0c] text-[#0B2E1A] text-xs font-bold transition shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            Export CSV
          </button>
          <a
            href="/api/download-case-study"
            download="Wireless_Propagation_Case_Study.docx"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full border border-[#134729]/30 bg-white hover:bg-[#134729] hover:text-white text-[#111827] text-xs font-bold transition shadow-sm"
          >
            <FileText className="w-3.5 h-3.5" />
            Case Study Doc
          </a>
          <a
            href="/api/download-viva-qa"
            download="Viva_Questions_and_Explanations.docx"
            className="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-full bg-[#134729] text-white hover:bg-[#0B2E1A] text-xs font-bold transition shadow-sm"
          >
            <HelpCircle className="w-3.5 h-3.5 text-[#A8EB12]" />
            Viva Q&A Doc
          </a>
        </div>
      </div>

      {/* Main Split Grid: Sidebar Parameters (Left) + Visualization Console (Right) */}
      <div className="grid lg:grid-cols-12 gap-6 items-start">
        {/* LEFT CONTROL PANEL */}
        <aside className="lg:col-span-4 xl:col-span-3 bg-white rounded-3xl p-5 shadow-sm border border-black/5 space-y-5">
          <div className="flex items-center justify-between border-b border-black/5 pb-3">
            <div className="flex items-center gap-2 font-extrabold text-sm text-[#111827]">
              <Sliders className="w-4 h-4 text-[#134729]" />
              Simulation Controls & Parameters
            </div>
            {loading && <RefreshCw className="w-4 h-4 animate-spin text-[#58b92c]" />}
          </div>

          {/* Carrier Frequency with MHz/GHz Toggle */}
          <div>
            <div className="flex items-center justify-between text-xs font-bold text-[#111827] mb-1">
              <span>Carrier Frequency:</span>
              <div className="inline-flex rounded-lg border border-black/15 p-0.5 bg-[#F3F4EF]">
                <button
                  type="button"
                  onClick={() => setFreqUnit('MHz')}
                  className={`px-2 py-0.5 rounded text-[10px] font-bold transition ${
                    freqUnit === 'MHz' ? 'bg-[#134729] text-white shadow-xs' : 'text-[#6B7280]'
                  }`}
                >
                  MHz
                </button>
                <button
                  type="button"
                  onClick={() => setFreqUnit('GHz')}
                  className={`px-2 py-0.5 rounded text-[10px] font-bold transition ${
                    freqUnit === 'GHz' ? 'bg-[#134729] text-white shadow-xs' : 'text-[#6B7280]'
                  }`}
                >
                  GHz
                </button>
              </div>
            </div>

            <div className="flex items-baseline justify-between mb-2">
              <span className="text-[11px] text-[#6B7280]">
                {freqUnit === 'GHz' ? '(Millimeter-Wave & Sub-THz)' : '(Sub-6 GHz Cellular)'}
              </span>
              <span className="font-mono font-extrabold text-sm text-[#134729]">
                {freqUnit === 'GHz'
                  ? `${(params.frequency_mhz / 1000).toFixed(2)} GHz`
                  : `${params.frequency_mhz} MHz`}
              </span>
            </div>

            {/* Slider depends on MHz vs GHz */}
            {freqUnit === 'GHz' ? (
              <input
                type="range"
                min="0.5"
                max="100.0"
                step="0.5"
                value={params.frequency_mhz / 1000}
                onChange={(e) => handleFrequencyInputChange(e.target.value)}
                className="rf-slider"
              />
            ) : (
              <input
                type="range"
                min="150"
                max="3500"
                step="50"
                value={params.frequency_mhz}
                onChange={(e) => handleFrequencyInputChange(e.target.value)}
                className="rf-slider"
              />
            )}

            {/* Quick Frequency Jump Pills */}
            <div className="flex flex-wrap gap-1.5 mt-2.5">
              {[
                { label: '900 MHz', mhz: 900, unit: 'MHz' },
                { label: '1.8 GHz', mhz: 1800, unit: 'GHz' },
                { label: '3.5 GHz (5G)', mhz: 3500, unit: 'GHz' },
                { label: '28 GHz (mmW)', mhz: 28000, unit: 'GHz' },
                { label: '39 GHz (mmW)', mhz: 39000, unit: 'GHz' },
                { label: '73 GHz (6G)', mhz: 73000, unit: 'GHz' },
              ].map((pill) => (
                <button
                  key={pill.label}
                  type="button"
                  onClick={() => {
                    setFreqUnit(pill.unit);
                    setParams({ ...params, frequency_mhz: pill.mhz });
                  }}
                  className={`px-2 py-1 rounded-md text-[10px] font-bold border transition ${
                    params.frequency_mhz === pill.mhz
                      ? 'bg-[#134729] text-[#A8EB12] border-[#134729]'
                      : 'bg-[#F3F4EF] hover:bg-[#e4e6df] text-[#374151] border-black/10'
                  }`}
                >
                  {pill.label}
                </button>
              ))}
            </div>
          </div>

          {/* Environment Preset Dropdown */}
          <div>
            <label className="block text-xs font-bold text-[#111827] mb-1">
              Environment Clutter Preset
            </label>
            <p className="text-[11px] text-[#6B7280] mb-1.5">
              (Building density & terrain morphology factor)
            </p>
            <select
              value={params.environment}
              onChange={(e) => setParams({ ...params, environment: e.target.value })}
              className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-2 text-xs font-semibold text-[#111827] focus:outline-none focus:ring-2 focus:ring-[#A8EB12]"
            >
              <option value="urban">Urban (Dense street canyon, high shadowing)</option>
              <option value="suburban">Suburban (Residential & trees, moderate loss)</option>
              <option value="rural">Rural / Open Area (Minimal clutter, lowest loss)</option>
              <option value="indoor_obstructed">Indoor Obstructed (Partitions & walls)</option>
            </select>
          </div>

          {/* Distance Range */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Min Dist (km — Near)
              </label>
              <input
                type="number"
                min="0.005"
                max="5"
                step="0.01"
                value={params.min_distance_km}
                onChange={(e) => setParams({ ...params, min_distance_km: Number(e.target.value) || 0.01 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Max Dist (km — Edge)
              </label>
              <input
                type="number"
                min="0.1"
                max="100"
                step="0.5"
                value={params.max_distance_km}
                onChange={(e) => setParams({ ...params, max_distance_km: Number(e.target.value) || 1 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
          </div>

          {/* Antenna Heights */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Tower Height hₜ (m)
              </label>
              <input
                type="number"
                min="4"
                max="300"
                step="1"
                value={params.ht_m}
                onChange={(e) => setParams({ ...params, ht_m: Number(e.target.value) || 10 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Mobile Height hᵣ (m)
              </label>
              <input
                type="number"
                min="0.5"
                max="15"
                step="0.5"
                value={params.hr_m}
                onChange={(e) => setParams({ ...params, hr_m: Number(e.target.value) || 1.5 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
          </div>

          {/* RF Power & Receiver Sensitivity */}
          <div className="space-y-3 pt-2 border-t border-black/5">
            <div className="text-xs font-extrabold text-[#134729]">
              RF Power & Link Thresholds (dBm / dBi)
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  Tx Power Pₜ (dBm)
                </label>
                <input
                  type="number"
                  value={params.tx_power_dbm}
                  onChange={(e) => setParams({ ...params, tx_power_dbm: Number(e.target.value) })}
                  className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
                />
              </div>
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  Tx Gain Gₜ (dBi)
                </label>
                <input
                  type="number"
                  value={params.tx_gain_dbi}
                  onChange={(e) => setParams({ ...params, tx_gain_dbi: Number(e.target.value) })}
                  className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
                />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  Rx Gain Gᵣ (dBi)
                </label>
                <input
                  type="number"
                  value={params.rx_gain_dbi}
                  onChange={(e) => setParams({ ...params, rx_gain_dbi: Number(e.target.value) })}
                  className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
                />
              </div>
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  Rx Sensitivity (dBm)
                </label>
                <input
                  type="number"
                  value={params.rx_sensitivity_dbm}
                  onChange={(e) => setParams({ ...params, rx_sensitivity_dbm: Number(e.target.value) })}
                  className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
                />
              </div>
            </div>
          </div>

          {/* Model Toggle Buttons */}
          <div className="pt-2 border-t border-black/5">
            <div className="text-xs font-extrabold text-[#134729] mb-2 flex items-center justify-between">
              <span>Toggle Curves (Compare Models)</span>
              <span className="text-[10px] text-[#6B7280]">({params.models.length} active)</span>
            </div>
            <div className="space-y-1.5 max-h-72 overflow-y-auto pr-1">
              {ALL_MODELS.map((m) => {
                const active = params.models.includes(m.key);
                return (
                  <button
                    key={m.key}
                    type="button"
                    onClick={() => toggleModel(m.key)}
                    className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-xl text-left text-xs font-semibold border transition ${
                      active
                        ? 'bg-[#134729]/10 border-[#134729]/30 text-[#111827]'
                        : 'bg-[#F3F4EF]/60 border-transparent text-[#6B7280]'
                    }`}
                  >
                    <span className="flex items-center gap-2 truncate">
                      <span
                        className="w-2.5 h-2.5 rounded-full shrink-0"
                        style={{ backgroundColor: active ? m.color : '#cbd5e1' }}
                      />
                      <span className="truncate text-[11px]">{m.label}</span>
                    </span>
                    <span className="text-[9px] font-bold uppercase shrink-0 ml-1">
                      {active ? 'ON' : 'OFF'}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>
        </aside>

        {/* RIGHT CONSOLE AREA */}
        <div className="lg:col-span-8 xl:col-span-9 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-800 rounded-2xl p-4 text-sm font-semibold">
              Backend connection error: {error}. Ensure FastAPI server is running on port 8000.
            </div>
          )}

          {/* Live KPI Strip */}
          {simData && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm">
                <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                  Radiated Power (EIRP)
                </div>
                <div className="text-2xl font-extrabold font-mono text-[#134729] mt-1">
                  {simData.eirp_dbm} dBm
                </div>
                <div className="text-[11px] text-[#6B7280] mt-1">
                  Pt {params.tx_power_dbm} + Gt {params.tx_gain_dbi} dBi
                </div>
              </div>

              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm">
                <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                  Carrier Frequency
                </div>
                <div className="text-2xl font-extrabold font-mono text-[#0284c7] mt-1">
                  {params.frequency_mhz >= 1000
                    ? `${(params.frequency_mhz / 1000).toFixed(2)} GHz`
                    : `${params.frequency_mhz} MHz`}
                </div>
                <div className="text-[11px] text-[#6B7280] mt-1">
                  λ = {((3e8 / (params.frequency_mhz * 1e6)) * 100).toFixed(2)} cm
                </div>
              </div>

              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm">
                <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                  Midpoint Loss @ {simData.mid_distance_km} km
                </div>
                <div className="text-2xl font-extrabold font-mono text-purple-700 mt-1">
                  {simData.fspl_mid_db ? `${simData.fspl_mid_db} dB` : '—'}
                </div>
                <div className="text-[11px] text-[#6B7280] mt-1">
                  Free space vacuum lower bound
                </div>
              </div>

              <div className="bg-[#141517] text-white rounded-2xl p-4 shadow-sm">
                <div className="text-[11px] font-bold text-white/60 uppercase">
                  Band Regime
                </div>
                <div className="text-xl font-extrabold font-mono text-[#A8EB12] mt-1">
                  {params.frequency_mhz >= 24000
                    ? '5G/6G mmWave'
                    : params.frequency_mhz >= 1000
                    ? 'Sub-6 GHz Mid-Band'
                    : 'Sub-1 GHz Cellular'}
                </div>
                <div className="text-[11px] text-white/60 mt-1">
                  {params.frequency_mhz >= 24000 ? 'Dense Urban Micro (UMi)' : 'Macrocell Standard'}
                </div>
              </div>
            </div>
          )}

          {/* Navigation Tabs */}
          <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-black/5 shadow-sm">
            {[
              { id: 'curves', label: '📈 Signal Curves (Path Loss & Power)' },
              { id: 'mmwave', label: '📡 5G / 6G mmWave & LoS–NLoS Transitions (IEEE Access 2026)' },
              { id: 'outage', label: '🎲 Shadowing & Outage (Reliability %)' },
              { id: 'budget', label: '⚡ Link Budget Chain (Fade Margin)' },
              { id: 'benchmark', label: '🎓 900 MHz Course Benchmark (1–20 km)' },
              { id: 'matrix', label: '📋 Model Matrix (All Formulas)' },
            ].map((t) => (
              <button
                key={t.id}
                type="button"
                onClick={() => setActiveTab(t.id)}
                className={`px-4 py-2.5 rounded-xl text-xs font-bold transition ${
                  activeTab === t.id
                    ? 'bg-[#134729] text-[#A8EB12] shadow-sm'
                    : 'text-[#4B5563] hover:bg-[#F3F4EF]'
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* TAB 1: PATH LOSS & RECEIVED POWER */}
          {activeTab === 'curves' && simData && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
              <div className="grid xl:grid-cols-2 gap-6">
                {/* Path Loss Chart */}
                <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                  <div className="mb-3">
                    <h3 className="font-extrabold text-base text-[#111827]">
                      Path Loss vs Distance{' '}
                      <span className="text-xs font-medium text-[#6B7280]">
                        (Higher Curve = Greater Signal Loss in dB)
                      </span>
                    </h3>
                    <p className="text-xs text-[#6B7280] mt-1">
                      Distance (km) vs Path Loss (dB) across selected propagation models.
                    </p>
                  </div>
                  <div className="h-80 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={simData.points} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis
                          dataKey="distance_km"
                          tick={{ fontSize: 11, fill: '#4b5563' }}
                          label={{ value: 'Distance d (km)', position: 'insideBottom', offset: -4, fontSize: 11 }}
                        />
                        <YAxis
                          tick={{ fontSize: 11, fill: '#4b5563' }}
                          label={{ value: 'Path Loss (dB)', angle: -90, position: 'insideLeft', fontSize: 11 }}
                        />
                        <Tooltip
                          contentStyle={{ borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                          formatter={(value, name) => [`${value} dB`, name]}
                          labelFormatter={(label) => `Distance: ${label} km`}
                        />
                        {activeModelsList.map((m) => (
                          <Line
                            key={m.key}
                            type="monotone"
                            dataKey={`pl_${m.key}`}
                            name={m.label}
                            stroke={m.color}
                            strokeWidth={2.4}
                            strokeDasharray={m.dash}
                            dot={false}
                            activeDot={{ r: 5 }}
                          />
                        ))}
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Received Power Chart */}
                <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                  <div className="mb-3">
                    <h3 className="font-extrabold text-base text-[#111827]">
                      Received Power vs Distance{' '}
                      <span className="text-xs font-medium text-[#6B7280]">
                        (Lower Curve = Weaker Signal in dBm)
                      </span>
                    </h3>
                    <p className="text-xs text-[#6B7280] mt-1">
                      Distance (km) vs Pr (dBm) — Values dropping below red threshold indicate call drops.
                    </p>
                  </div>
                  <div className="h-80 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={simData.points} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                        <XAxis
                          dataKey="distance_km"
                          tick={{ fontSize: 11, fill: '#4b5563' }}
                          label={{ value: 'Distance d (km)', position: 'insideBottom', offset: -4, fontSize: 11 }}
                        />
                        <YAxis
                          tick={{ fontSize: 11, fill: '#4b5563' }}
                          label={{ value: 'Received Power (dBm)', angle: -90, position: 'insideLeft', fontSize: 11 }}
                        />
                        <Tooltip
                          contentStyle={{ borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                          formatter={(value, name) => [`${value} dBm`, name]}
                          labelFormatter={(label) => `Distance: ${label} km`}
                        />
                        <ReferenceLine
                          y={params.rx_sensitivity_dbm}
                          stroke="#ef4444"
                          strokeDasharray="5 5"
                          strokeWidth={2}
                          label={{
                            value: `Threshold (${params.rx_sensitivity_dbm} dBm)`,
                            fill: '#ef4444',
                            fontSize: 11,
                            position: 'insideTopRight',
                          }}
                        />
                        {activeModelsList.map((m) => (
                          <Line
                            key={m.key}
                            type="monotone"
                            dataKey={`pr_${m.key}`}
                            name={m.label}
                            stroke={m.color}
                            strokeWidth={2.4}
                            strokeDasharray={m.dash}
                            dot={false}
                            activeDot={{ r: 5 }}
                          />
                        ))}
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </div>
              </div>

              {/* Legend & Line Explanation Card */}
              <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                <div className="flex items-center gap-2 font-extrabold text-sm text-[#111827] mb-4">
                  <Info className="w-4 h-4 text-[#134729]" />
                  Active Model Legend & Mathematical Formulation
                </div>
                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {activeModelsList.map((m) => {
                    const meta = simData.model_metadata?.[m.key];
                    return (
                      <div key={m.key} className="p-3.5 rounded-2xl bg-[#F3F4EF] border border-black/5">
                        <div className="flex items-center gap-2 font-bold text-xs text-[#111827]">
                          <span className="w-5 h-1 rounded-full shrink-0" style={{ backgroundColor: m.color }} />
                          <span>{m.label}</span>
                        </div>
                        <div className="text-[11px] font-mono text-[#134729] font-bold mt-1">
                          {meta?.formula || m.lineDesc}
                        </div>
                        <p className="text-[11px] text-[#4B5563] mt-1 leading-relaxed">
                          {meta?.shortDesc}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>
            </motion.div>
          )}

          {/* TAB 2: DEDICATED 5G / 6G mmWave & LoS-NLoS Transitions (IEEE Access 2026) */}
          {activeTab === 'mmwave' && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
              {/* Paper Citation Header Card */}
              <div className="bg-gradient-to-br from-[#134729] to-[#0B2E1A] text-white rounded-3xl p-6 shadow-md border border-black/10">
                <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
                  <span className="px-3 py-1 rounded-full bg-[#A8EB12] text-[#0B2E1A] text-xs font-extrabold uppercase tracking-wider">
                    IEEE Access 2026 Research Article Reference
                  </span>
                  <span className="text-xs text-white/75 font-mono">
                    DOI: 10.1109/ACCESS.2026.3741615
                  </span>
                </div>
                <h2 className="text-xl sm:text-2xl font-extrabold text-white leading-snug">
                  Statistical Path Loss Modeling of LoS–NLoS Transitions for mmWave Communications in Urban Environments
                </h2>
                <p className="text-xs text-white/80 mt-2 font-medium">
                  Authors: Inam Ullah, Hesham El-Sayed, Alexis A. Dowhuszko, and Jyri Hämäläinen (IEEE Access, Oct 2026)
                </p>
                <div className="mt-4 pt-4 border-t border-white/15 grid md:grid-cols-3 gap-4 text-xs">
                  <div>
                    <span className="text-white/60 block font-bold uppercase text-[10px]">Frequency Scope</span>
                    <span className="font-semibold text-[#A8EB12]">28 GHz, 39 GHz, 60 GHz & 73 GHz (6G sub-THz)</span>
                  </div>
                  <div>
                    <span className="text-white/60 block font-bold uppercase text-[10px]">Environment</span>
                    <span className="font-semibold text-white">Urban Micro (UMi) Street Canyons (High-Rise)</span>
                  </div>
                  <div>
                    <span className="text-white/60 block font-bold uppercase text-[10px]">Core Finding</span>
                    <span className="font-semibold text-white">LoS-to-NLoS transition causes sharp 20–35 dB drop in link budget</span>
                  </div>
                </div>
              </div>

              {/* mmWave Frequency Switcher */}
              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm flex flex-wrap items-center justify-between gap-4">
                <div className="flex items-center gap-2">
                  <Radio className="w-5 h-5 text-[#134729]" />
                  <span className="text-xs font-bold text-[#111827]">
                    Select mmWave / 6G Frequency Band to Simulate:
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {[
                    { freq: 28.0, label: '28 GHz (5G Band n257/n261)' },
                    { freq: 39.0, label: '39 GHz (5G Band n260)' },
                    { freq: 60.0, label: '60 GHz (V-Band Unlicensed)' },
                    { freq: 73.0, label: '73 GHz (6G sub-THz Band)' },
                  ].map((b) => (
                    <button
                      key={b.freq}
                      type="button"
                      onClick={() => setMmwaveFreqGhz(b.freq)}
                      className={`px-3.5 py-1.5 rounded-full text-xs font-bold transition ${
                        mmwaveFreqGhz === b.freq
                          ? 'bg-[#134729] text-[#A8EB12] shadow-sm'
                          : 'bg-[#F3F4EF] hover:bg-[#e4e6df] text-[#374151]'
                      }`}
                    >
                      {b.label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Dual Charts: Path Loss Curves + LoS Probability */}
              {mmwaveData && (
                <div className="grid xl:grid-cols-2 gap-6">
                  {/* mmWave Path Loss Comparison */}
                  <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                    <div className="mb-3">
                      <div className="flex items-center justify-between">
                        <h3 className="font-extrabold text-base text-[#111827]">
                          mmWave Path Loss at {mmwaveFreqGhz} GHz
                        </h3>
                        {mmwaveLoading && <RefreshCw className="w-4 h-4 animate-spin text-[#134729]" />}
                      </div>
                      <p className="text-xs text-[#6B7280] mt-1">
                        Comparing 3GPP UMi LoS, NLoS, Close-In (CI), and the IEEE Access LoS–NLoS Transition.
                      </p>
                    </div>
                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={mmwaveData.rows} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                          <XAxis
                            dataKey="distance_m"
                            tick={{ fontSize: 11, fill: '#4b5563' }}
                            label={{ value: 'Distance d (meters)', position: 'insideBottom', offset: -4, fontSize: 11 }}
                          />
                          <YAxis
                            tick={{ fontSize: 11, fill: '#4b5563' }}
                            label={{ value: 'Path Loss (dB)', angle: -90, position: 'insideLeft', fontSize: 11 }}
                          />
                          <Tooltip
                            contentStyle={{ borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                            formatter={(value, name) => [`${value} dB`, name]}
                            labelFormatter={(label) => `Distance: ${label} m`}
                          />
                          <Line
                            type="monotone"
                            dataKey="pl_los_db"
                            name="3GPP UMi LoS"
                            stroke="#06b6d4"
                            strokeWidth={2.4}
                            dot={false}
                          />
                          <Line
                            type="monotone"
                            dataKey="pl_nlos_db"
                            name="3GPP UMi NLoS"
                            stroke="#e11d48"
                            strokeWidth={2.4}
                            strokeDasharray="6 4"
                            dot={false}
                          />
                          <Line
                            type="monotone"
                            dataKey="pl_transition_db"
                            name="IEEE Access Transition (LoS→NLoS)"
                            stroke="#84cc16"
                            strokeWidth={3}
                            dot={false}
                          />
                          <Line
                            type="monotone"
                            dataKey="pl_ci_db"
                            name="Close-In (CI) Model (n=2.1)"
                            stroke="#ca8a04"
                            strokeWidth={2}
                            strokeDasharray="3 3"
                            dot={false}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* LoS Probability Decay Curve */}
                  <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                    <div className="mb-3">
                      <h3 className="font-extrabold text-base text-[#111827]">
                        Line-of-Sight Probability P_LoS(d) Decay
                      </h3>
                      <p className="text-xs text-[#6B7280] mt-1">
                        P_LoS = 1.0 for d ≤ 18m. As distance increases, urban obstructions cause P_LoS → 0.
                      </p>
                    </div>
                    <div className="h-80 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={mmwaveData.rows} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
                          <defs>
                            <linearGradient id="losProbGrad" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="#134729" stopOpacity={0.6} />
                              <stop offset="95%" stopColor="#A8EB12" stopOpacity={0.05} />
                            </linearGradient>
                          </defs>
                          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                          <XAxis
                            dataKey="distance_m"
                            tick={{ fontSize: 11, fill: '#4b5563' }}
                            label={{ value: 'Distance d (meters)', position: 'insideBottom', offset: -4, fontSize: 11 }}
                          />
                          <YAxis
                            tick={{ fontSize: 11, fill: '#4b5563' }}
                            domain={[0, 1]}
                            tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                            label={{ value: 'P_LoS Probability', angle: -90, position: 'insideLeft', fontSize: 11 }}
                          />
                          <Tooltip
                            contentStyle={{ borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                            formatter={(value) => [`${(Number(value) * 100).toFixed(1)}%`, 'LoS Probability']}
                            labelFormatter={(label) => `Distance: ${label} m`}
                          />
                          <Area
                            type="monotone"
                            dataKey="p_los"
                            stroke="#134729"
                            strokeWidth={2.5}
                            fillOpacity={1}
                            fill="url(#losProbGrad)"
                          />
                        </AreaChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </div>
              )}

              {/* Technical Math Derivation & Explanations */}
              <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm space-y-4">
                <h3 className="font-extrabold text-base text-[#111827] flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-[#134729]" />
                  Mathematical Formulations: 3GPP TR 38.901 & IEEE Access 2026 Model
                </h3>

                <div className="grid md:grid-cols-3 gap-4 text-xs">
                  <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5 space-y-2">
                    <span className="font-extrabold text-[#06b6d4] block uppercase">1. 3GPP UMi Line-of-Sight (LoS)</span>
                    <p className="font-mono text-[#111827] font-bold">
                      PL_LoS = 32.4 + 21.0·log₁₀(d₃_D) + 20·log₁₀(fc)
                    </p>
                    <p className="text-[#4B5563] leading-relaxed">
                      Valid for 10m ≤ d ≤ 5000m, 0.5 ≤ fc ≤ 100 GHz. Shadow fading standard deviation σ_SF = 4.0 dB.
                    </p>
                  </div>

                  <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5 space-y-2">
                    <span className="font-extrabold text-[#e11d48] block uppercase">2. 3GPP UMi Non-Line-of-Sight (NLoS)</span>
                    <p className="font-mono text-[#111827] font-bold">
                      PL_NLoS = 22.4 + 35.3·log₁₀(d₃_D) + 21.3·log₁₀(fc)
                    </p>
                    <p className="text-[#4B5563] leading-relaxed">
                      Bounded by PL_NLoS = max(PL_LoS, PL_NLoS'). Higher path loss exponent reflects rooftop/corner diffraction. σ_SF = 7.82 dB.
                    </p>
                  </div>

                  <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5 space-y-2">
                    <span className="font-extrabold text-[#84cc16] block uppercase">3. Statistical Transition (IEEE Access)</span>
                    <p className="font-mono text-[#111827] font-bold">
                      PL_trans = P_LoS(d)·PL_LoS + (1 − P_LoS(d))·PL_NLoS
                    </p>
                    <p className="text-[#4B5563] leading-relaxed">
                      Smoothly bridges the state gap in high-rise street canyons, preventing unrealistic step-discontinuities in 5G beam management.
                    </p>
                  </div>
                </div>
              </div>

              {/* Sampled mmWave Transition Data Table */}
              {mmwaveData && (
                <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                  <h3 className="font-extrabold text-base text-[#111827] mb-3">
                    Sampled mmWave Transition Telemetry ({mmwaveFreqGhz} GHz Carrier)
                  </h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs text-left">
                      <thead className="bg-[#134729] text-white">
                        <tr>
                          <th className="p-2.5 rounded-tl-xl">Distance (m)</th>
                          <th className="p-2.5">P_LoS (%)</th>
                          <th className="p-2.5">P_NLoS (%)</th>
                          <th className="p-2.5">3GPP LoS (dB)</th>
                          <th className="p-2.5">3GPP NLoS (dB)</th>
                          <th className="p-2.5 font-bold">Transition PL (dB)</th>
                          <th className="p-2.5 rounded-tr-xl">Close-In CI (dB)</th>
                        </tr>
                      </thead>
                      <tbody>
                        {mmwaveData.rows
                          .filter((_, idx) => idx % 6 === 0)
                          .map((r, i) => (
                            <tr key={r.distance_m} className={i % 2 === 0 ? 'bg-[#F3F4EF]/70' : 'bg-white'}>
                              <td className="p-2.5 font-mono font-bold">{r.distance_m} m</td>
                              <td className="p-2.5 font-mono text-emerald-700 font-bold">
                                {(r.p_los * 100).toFixed(1)}%
                              </td>
                              <td className="p-2.5 font-mono text-rose-700 font-semibold">
                                {(r.p_nlos * 100).toFixed(1)}%
                              </td>
                              <td className="p-2.5 font-mono text-cyan-700">{r.pl_los_db} dB</td>
                              <td className="p-2.5 font-mono text-rose-700">{r.pl_nlos_db} dB</td>
                              <td className="p-2.5 font-mono text-[#134729] font-extrabold bg-[#A8EB12]/20">
                                {r.pl_transition_db} dB
                              </td>
                              <td className="p-2.5 font-mono text-amber-700">{r.pl_ci_db} dB</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {/* TAB 3: SHADOWING & OUTAGE */}
          {activeTab === 'outage' && simData && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h3 className="font-extrabold text-lg text-[#111827]">
                    Log-Normal Shadowing Outage Probability{' '}
                    <span className="text-xs font-medium text-[#6B7280]">
                      (Chance of Signal Dropping Below Cutoff in %)
                    </span>
                  </h3>
                  <p className="text-xs text-[#6B7280] mt-1">
                    Adjust σ (standard deviation in dB) to see how obstacle randomness shrinks reliable cell radius.
                  </p>
                </div>
                <div className="w-72">
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span>Shadow Std Dev σ (dB):</span>
                    <span className="font-mono text-[#134729]">{params.shadow_sigma_db} dB</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="14"
                    step="0.5"
                    value={params.shadow_sigma_db}
                    onChange={(e) => setParams({ ...params, shadow_sigma_db: Number(e.target.value) })}
                    className="rf-slider"
                  />
                </div>
              </div>

              <div className="h-80 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={simData.points} margin={{ top: 10, right: 20, left: 0, bottom: 10 }}>
                    <defs>
                      <linearGradient id="outageGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#db2777" stopOpacity={0.5} />
                        <stop offset="95%" stopColor="#db2777" stopOpacity={0.05} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis
                      dataKey="distance_km"
                      tick={{ fontSize: 11, fill: '#4b5563' }}
                      label={{ value: 'Distance d (km)', position: 'insideBottom', offset: -4, fontSize: 11 }}
                    />
                    <YAxis
                      domain={[0, 100]}
                      tick={{ fontSize: 11, fill: '#4b5563' }}
                      label={{ value: 'Outage Probability (%)', angle: -90, position: 'insideLeft', fontSize: 11 }}
                    />
                    <Tooltip
                      contentStyle={{ borderRadius: '12px', border: '1px solid #e5e7eb', fontSize: '12px' }}
                      formatter={(v) => [`${v}%`, 'Outage Probability']}
                      labelFormatter={(l) => `Distance: ${l} km`}
                    />
                    <ReferenceLine
                      y={10}
                      stroke="#16a34a"
                      strokeDasharray="4 4"
                      label={{ value: '90% Cell Reliability (10% Outage)', fill: '#16a34a', fontSize: 11 }}
                    />
                    <Area
                      type="monotone"
                      dataKey="outage_pct"
                      name="Outage Probability (%)"
                      stroke="#db2777"
                      strokeWidth={2.5}
                      fillOpacity={1}
                      fill="url(#outageGrad)"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>

              <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5 text-xs text-[#4B5563] space-y-1">
                <div className="font-extrabold text-[#111827]">
                  Outage Formula: P_out(d) = Q( (Pr_median(d) − P_threshold) / σ )
                </div>
                <div>
                  Calculated based on standard Normal complementary cumulative distribution function Q(z).
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: RF LINK BUDGET */}
          {activeTab === 'budget' && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h3 className="font-extrabold text-lg text-[#111827]">
                    End-to-End RF Link Budget Chain{' '}
                    <span className="text-xs font-medium text-[#6B7280]">
                      (Fade Margin & Service Availability Verification)
                    </span>
                  </h3>
                  <p className="text-xs text-[#6B7280] mt-1">
                    Pr (dBm) = Pt + Gt + Gr − Losses − PathLoss(d). Target distance evaluation.
                  </p>
                </div>
                <div className="w-64">
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span>Target Distance (km):</span>
                    <span className="font-mono text-[#134729]">{budgetTargetD.toFixed(1)} km</span>
                  </div>
                  <input
                    type="range"
                    min="0.5"
                    max="20"
                    step="0.5"
                    value={budgetTargetD}
                    onChange={(e) => setBudgetTargetD(Number(e.target.value))}
                    className="rf-slider"
                  />
                </div>
              </div>

              {budgetEval && (
                <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5">
                    <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                      Effective Radiated Power
                    </div>
                    <div className="text-2xl font-extrabold font-mono text-[#134729] mt-1">
                      {budgetEval.eirp_dbm} dBm
                    </div>
                    <div className="text-[11px] text-[#6B7280] mt-1">Pt + Gt</div>
                  </div>

                  <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5">
                    <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                      Cellular Path Loss ({budgetEval.cellular_model_used})
                    </div>
                    <div className="text-2xl font-extrabold font-mono text-purple-700 mt-1">
                      {budgetEval.cellular_loss_db} dB
                    </div>
                    <div className="text-[11px] text-[#6B7280] mt-1">
                      Free Space: {budgetEval.fspl_loss_db} dB
                    </div>
                  </div>

                  <div className="p-4 rounded-2xl bg-[#F3F4EF] border border-black/5">
                    <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                      Received Power (Pr)
                    </div>
                    <div className="text-2xl font-extrabold font-mono text-[#0284c7] mt-1">
                      {budgetEval.rx_power_dbm} dBm
                    </div>
                    <div className="text-[11px] text-[#6B7280] mt-1">
                      Cutoff: {params.rx_sensitivity_dbm} dBm
                    </div>
                  </div>

                  <div
                    className={`p-4 rounded-2xl border ${
                      budgetEval.fade_margin_db >= 0
                        ? 'bg-emerald-50 border-emerald-200 text-emerald-900'
                        : 'bg-rose-50 border-rose-200 text-rose-900'
                    }`}
                  >
                    <div className="text-[11px] font-bold uppercase tracking-wider">
                      Fade Margin (dB) & Status
                    </div>
                    <div className="text-2xl font-extrabold font-mono mt-1">
                      {budgetEval.fade_margin_db > 0 ? `+${budgetEval.fade_margin_db}` : budgetEval.fade_margin_db}{' '}
                      dB
                    </div>
                    <div className="text-[11px] font-bold mt-1">
                      {budgetEval.link_status === 'SERVICE OK' ? '✓ Link Has Headroom' : '⚠ Link In Outage'}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 5: 900 MHz BENCHMARK TABLE */}
          {activeTab === 'benchmark' && benchmarkData && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <h3 className="font-extrabold text-lg text-[#111827]">
                    900 MHz Urban Macrocell Course Benchmark Table (1–20 km)
                  </h3>
                  <p className="text-xs text-[#6B7280] mt-1">
                    Standard lab simulation parameters: f = 900 MHz, Tower hₜ = 30 m, Mobile hᵣ = 1.5 m.
                  </p>
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-[#134729] text-white">
                    <tr>
                      <th className="p-3 rounded-tl-xl">Distance (km)</th>
                      <th className="p-3">Free Space FSPL (dB)</th>
                      <th className="p-3">Okumura Open (dB)</th>
                      <th className="p-3">Hata Urban (dB)</th>
                      <th className="p-3 rounded-tr-xl">Δ Gap (Hata − FSPL)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {benchmarkData.rows.map((r, i) => (
                      <tr key={r.distance_km} className={i % 2 === 0 ? 'bg-[#F3F4EF]/70' : 'bg-white'}>
                        <td className="p-2.5 font-bold font-mono">{r.distance_km} km</td>
                        <td className="p-2.5 font-mono text-sky-700 font-semibold">{r.fspl_db} dB</td>
                        <td className="p-2.5 font-mono text-green-700 font-semibold">{r.okumura_db} dB</td>
                        <td className="p-2.5 font-mono text-[#134729] font-bold">{r.hata_urban_db} dB</td>
                        <td className="p-2.5 font-mono text-red-600 font-bold">+{r.delta_hata_fspl_db} dB</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* TAB 6: FORMAL MODEL MATRIX */}
          {activeTab === 'matrix' && matrixData && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
              <h3 className="font-extrabold text-lg text-[#111827] mb-4">
                Comprehensive Mathematical Comparison Matrix{' '}
                <span className="text-xs font-medium text-[#6B7280]">
                  (Valid Ranges, Antenna Bounds & Deployment Applications)
                </span>
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left">
                  <thead className="bg-[#141517] text-white">
                    <tr>
                      {matrixData.columns.map((c) => (
                        <th key={c} className="p-3 font-bold">
                          {c}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {matrixData.rows.map((row, idx) => (
                      <tr key={idx} className={idx % 2 === 0 ? 'bg-[#F3F4EF]/60' : 'bg-white'}>
                        {matrixData.columns.map((c) => (
                          <td key={c} className="p-3 border-b border-black/5 align-top">
                            {String(row[c] ?? '')}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
