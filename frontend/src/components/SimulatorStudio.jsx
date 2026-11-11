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
} from 'lucide-react';
import {
  fetchSimulation,
  fetchComparisonMatrix,
  fetchBenchmark900MHz,
  evaluateLinkBudget,
} from '../services/api';

const ALL_MODELS = [
  { key: 'fspl', label: 'Free Space (Friis — Theoretical Minimum)', color: '#0284c7', dash: undefined, lineDesc: 'Solid Blue' },
  { key: 'two_ray', label: 'Two-Ray (Direct + Ground Bounce)', color: '#f97316', dash: '6 4', lineDesc: 'Dashed Orange' },
  { key: 'log_distance', label: 'Log-Distance (Configurable Exponent n)', color: '#16a34a', dash: '8 4 2 4', lineDesc: 'Dash-Dot Green' },
  { key: 'okumura', label: 'Okumura (Tokyo Drive-Test Curves)', color: '#dc2626', dash: '3 3', lineDesc: 'Dotted Red' },
  { key: 'hata', label: 'Okumura-Hata (Urban Macrocell Standard)', color: '#134729', dash: undefined, lineDesc: 'Solid Forest Green' },
  { key: 'cost231', label: 'COST-231 Hata (1.5–2.0 GHz Extended)', color: '#7c3aed', dash: '6 4', lineDesc: 'Dashed Violet' },
  { key: 'shadowing', label: 'Log-Normal Shadowing (Stochastic Xσ)', color: '#db2777', dash: undefined, lineDesc: 'Solid Magenta' },
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
    models: ALL_MODELS.map((m) => m.key),
  });

  const [simData, setSimData] = useState(null);
  const [matrixData, setMatrixData] = useState(null);
  const [benchmarkData, setBenchmarkData] = useState(null);
  const [budgetTargetD, setBudgetTargetD] = useState(3.0);
  const [budgetEval, setBudgetEval] = useState(null);
  const [activeTab, setActiveTab] = useState('curves');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (initialModelFocus && ALL_MODELS.some((m) => m.key === initialModelFocus)) {
      setActiveTab('curves');
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
      setParams((p) => ({
        ...p,
        frequency_mhz: 1800,
        environment: 'suburban',
        min_distance_km: 0.2,
        max_distance_km: 12.0,
        ht_m: 40.0,
        hr_m: 1.5,
      }));
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
            INTERACTIVE SIMULATION STUDIO (PYTHON FASTAPI ENGINE)
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-[#111827] mt-2">
            Multi-Model Propagation Analyzer{' '}
            <span className="text-sm font-medium text-[#6B7280]">
              (Real-Time Calculation of Path Loss, Received Power & Reliability)
            </span>
          </h1>
        </div>

        <div className="flex flex-wrap items-center gap-2.5">
          <button
            onClick={() => applyPreset('900_course')}
            className="px-4 py-2 rounded-full bg-[#134729] text-[#A8EB12] text-xs font-bold hover:bg-[#0B2E1A] transition"
          >
            Preset: 900 MHz Course Study (1–20 km Urban)
          </button>
          <button
            onClick={() => applyPreset('1800_lte')}
            className="px-4 py-2 rounded-full border border-black/15 bg-white hover:bg-[#F3F4EF] text-xs font-bold text-[#111827] transition"
          >
            Preset: 1800 MHz LTE (Suburban PCS)
          </button>
          <button
            onClick={exportCsv}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-full bg-[#A8EB12] hover:bg-[#99dc0c] text-[#0B2E1A] text-xs font-bold transition shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            Export CSV (Spreadsheet Data)
          </button>
        </div>
      </div>

      {/* Main Split Grid: Sidebar Parameters (Left) + Visualization Console (Right) */}
      <div className="grid lg:grid-cols-12 gap-6 items-start">
        {/* LEFT CONTROL PANEL */}
        <aside className="lg:col-span-4 xl:col-span-3 bg-white rounded-3xl p-5 shadow-sm border border-black/5 space-y-5">
          <div className="flex items-center justify-between border-b border-black/5 pb-3">
            <div className="flex items-center gap-2 font-extrabold text-sm text-[#111827]">
              <Sliders className="w-4 h-4 text-[#134729]" />
              Input Parameters (Controls)
            </div>
            {loading && <RefreshCw className="w-4 h-4 animate-spin text-[#58b92c]" />}
          </div>

          {/* Carrier Frequency */}
          <div>
            <div className="flex justify-between text-xs font-bold text-[#111827] mb-1">
              <span>Carrier Frequency (MHz)</span>
              <span className="font-mono text-[#134729]">{params.frequency_mhz} MHz</span>
            </div>
            <p className="text-[11px] text-[#6B7280] mb-2">
              (Radio wave frequency — higher frequency increases path loss)
            </p>
            <input
              type="range"
              min="150"
              max="3500"
              step="50"
              value={params.frequency_mhz}
              onChange={(e) => setParams({ ...params, frequency_mhz: Number(e.target.value) })}
              className="rf-slider"
            />
          </div>

          {/* Environment Dropdown */}
          <div>
            <label className="block text-xs font-bold text-[#111827] mb-1">
              Environment Clutter Preset (Terrain Type)
            </label>
            <p className="text-[11px] text-[#6B7280] mb-1.5">
              (Selects obstacle density & clutter attenuation factor)
            </p>
            <select
              value={params.environment}
              onChange={(e) => setParams({ ...params, environment: e.target.value })}
              className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-2 text-xs font-semibold text-[#111827] focus:outline-none focus:ring-2 focus:ring-[#A8EB12]"
            >
              <option value="urban">Urban (Dense buildings, high attenuation)</option>
              <option value="suburban">Suburban (Houses & trees, moderate loss)</option>
              <option value="rural">Rural / Open Area (Minimal clutter, lowest terrestrial loss)</option>
              <option value="indoor_obstructed">Indoor Obstructed (Walls & partitions)</option>
            </select>
          </div>

          {/* Distance Range */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Min Distance (km — Start)
              </label>
              <input
                type="number"
                min="0.05"
                max="10"
                step="0.1"
                value={params.min_distance_km}
                onChange={(e) => setParams({ ...params, min_distance_km: Number(e.target.value) || 0.1 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Max Distance (km — Cell Edge)
              </label>
              <input
                type="number"
                min="1"
                max="100"
                step="1"
                value={params.max_distance_km}
                onChange={(e) => setParams({ ...params, max_distance_km: Number(e.target.value) || 10 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
          </div>

          {/* Antenna Heights */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Tower Height hₜ (m — Base)
              </label>
              <input
                type="number"
                min="5"
                max="300"
                step="5"
                value={params.ht_m}
                onChange={(e) => setParams({ ...params, ht_m: Number(e.target.value) || 30 })}
                className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold text-[#111827] mb-1">
                Mobile Height hᵣ (m — User)
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

          {/* RF Link Parameters */}
          <div className="space-y-3 pt-2 border-t border-black/5">
            <div className="text-xs font-extrabold text-[#134729]">
              RF Power & Link Thresholds (dBm / dBi)
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  Tx Power Pₜ (dBm — Output)
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
                  Tx Gain Gₜ (dBi — Sector)
                </label>
                <input
                  type="number"
                  value={params.tx_gain_dbi}
                  onChange={(e) => setParams({ ...params, tx_gain_dbi: Number(e.target.value) })}
                  className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
                />
              </div>
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  System Loss Lₛ (dB — Cable)
                </label>
                <input
                  type="number"
                  value={params.system_loss_db}
                  onChange={(e) => setParams({ ...params, system_loss_db: Number(e.target.value) })}
                  className="w-full rounded-xl border border-black/15 bg-[#F3F4EF] px-3 py-1.5 text-xs font-mono font-bold"
                />
              </div>
              <div>
                <label className="block text-[11px] font-bold text-[#111827] mb-1">
                  Rx Sensitivity (dBm — Cutoff)
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

          {/* Model Checkboxes */}
          <div className="pt-2 border-t border-black/5">
            <div className="text-xs font-extrabold text-[#134729] mb-2">
              Toggle Active Curves (Compare Models)
            </div>
            <div className="space-y-1.5">
              {ALL_MODELS.map((m) => {
                const active = params.models.includes(m.key);
                return (
                  <button
                    key={m.key}
                    onClick={() => toggleModel(m.key)}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-xl text-left text-xs font-semibold border transition ${
                      active
                        ? 'bg-[#134729]/10 border-[#134729]/30 text-[#111827]'
                        : 'bg-[#F3F4EF]/60 border-transparent text-[#6B7280]'
                    }`}
                  >
                    <span className="flex items-center gap-2">
                      <span
                        className="w-3 h-3 rounded-full shrink-0"
                        style={{ backgroundColor: active ? m.color : '#cbd5e1' }}
                      />
                      <span className="truncate">{m.label}</span>
                    </span>
                    <span className="text-[10px] font-bold uppercase">
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

          {/* Top Live KPI Strip */}
          {simData && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm">
                <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                  Effective Radiated Power (EIRP)
                </div>
                <div className="text-2xl font-extrabold font-mono text-[#134729] mt-1">
                  {simData.eirp_dbm} dBm
                </div>
                <div className="text-[11px] text-[#6B7280] mt-1">
                  (Pt {params.tx_power_dbm} + Gt {params.tx_gain_dbi} dBi)
                </div>
              </div>

              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm">
                <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                  Free Space @ {simData.mid_distance_km} km
                </div>
                <div className="text-2xl font-extrabold font-mono text-sky-700 mt-1">
                  {simData.fspl_mid_db ?? '—'} dB
                </div>
                <div className="text-[11px] text-[#6B7280] mt-1">
                  (Theoretical minimum attenuation)
                </div>
              </div>

              <div className="bg-white rounded-2xl p-4 border border-black/5 shadow-sm">
                <div className="text-[11px] font-bold text-[#6B7280] uppercase">
                  Hata Urban @ {simData.mid_distance_km} km
                </div>
                <div className="text-2xl font-extrabold font-mono text-[#0B2E1A] mt-1">
                  {simData.hata_mid_db ?? '—'} dB
                </div>
                <div className="text-[11px] text-[#6B7280] mt-1">
                  (Realistic macrocell urban loss)
                </div>
              </div>

              <div className="bg-[#141517] text-white rounded-2xl p-4 shadow-sm">
                <div className="text-[11px] font-bold text-white/60 uppercase">
                  Urban Clutter Penalty (Δ Loss)
                </div>
                <div className="text-2xl font-extrabold font-mono text-[#A8EB12] mt-1">
                  +
                  {simData.hata_mid_db && simData.fspl_mid_db
                    ? (simData.hata_mid_db - simData.fspl_mid_db).toFixed(2)
                    : '—'}{' '}
                  dB
                </div>
                <div className="text-[11px] text-white/60 mt-1">
                  (Excess loss beyond free space)
                </div>
              </div>
            </div>
          )}

          {/* Studio Navigation Tabs (With Explanations in Brackets) */}
          <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-black/5 shadow-sm">
            {[
              { id: 'curves', label: '📈 Signal Curves (Path Loss & Power)' },
              { id: 'outage', label: '🎲 Shadowing & Outage (Reliability %)' },
              { id: 'budget', label: '⚡ Link Budget Chain (Fade Margin)' },
              { id: 'benchmark', label: '🎓 900 MHz Course Benchmark (1–20 km)' },
              { id: 'matrix', label: '📋 Model Matrix (All 7 Formulas)' },
            ].map((t) => (
              <button
                key={t.id}
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
                      X-Axis: Distance (km) | Y-Axis: Path Loss (dB, logarithmic attenuation)
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
                        (Lower Curve = Weaker Phone Reception in dBm)
                      </span>
                    </h3>
                    <p className="text-xs text-[#6B7280] mt-1">
                      X-Axis: Distance (km) | Y-Axis: Received Power Pr (dBm) — Drops below red cutoff = Call Drop
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
                            value: `Cutoff (${params.rx_sensitivity_dbm} dBm)`,
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

              {/* Detailed Color, Unit & Line Explanation Card */}
              <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
                <div className="flex items-center gap-2 font-extrabold text-sm text-[#111827] mb-4">
                  <Info className="w-4 h-4 text-[#134729]" />
                  Graph Legend & Engineering Explanation (Colors, Line Styles, Units & Why Curves Differ)
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
                        <div className="text-[11px] font-semibold text-[#134729] mt-1">
                          Style: {m.lineDesc}
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

          {/* TAB 2: SHADOWING & OUTAGE */}
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
                  <AreaChart data={simData.points}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                    <XAxis dataKey="distance_km" tick={{ fontSize: 11 }} />
                    <YAxis domain={[0, 100]} tick={{ fontSize: 11 }} />
                    <Tooltip formatter={(v) => [`${v}% Outage Probability`, 'Link Failure Risk']} />
                    <ReferenceLine
                      y={5}
                      stroke="#16a34a"
                      strokeDasharray="4 4"
                      strokeWidth={2}
                      label={{ value: '5% Outage Target (95% Reliability)', fill: '#16a34a', fontSize: 11 }}
                    />
                    <Area
                      type="monotone"
                      dataKey="outage_pct"
                      stroke="#dc2626"
                      fill="#fca5a5"
                      fillOpacity={0.35}
                      strokeWidth={2.5}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* TAB 3: LINK BUDGET CALCULATOR */}
          {activeTab === 'budget' && budgetEval && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm space-y-6">
              <div>
                <h3 className="font-extrabold text-lg text-[#111827]">
                  Interactive RF Link Budget Chain{' '}
                  <span className="text-xs font-medium text-[#6B7280]">
                    (Step-by-Step Power Accounting at Target Distance)
                  </span>
                </h3>
                <div className="mt-4 max-w-md">
                  <div className="flex justify-between text-xs font-bold mb-1">
                    <span>Target Evaluation Distance (km):</span>
                    <span className="font-mono text-[#134729]">{budgetTargetD.toFixed(1)} km</span>
                  </div>
                  <input
                    type="range"
                    min={params.min_distance_km}
                    max={params.max_distance_km}
                    step="0.2"
                    value={budgetTargetD}
                    onChange={(e) => setBudgetTargetD(Number(e.target.value))}
                    className="rf-slider"
                  />
                </div>
              </div>

              <div className="grid sm:grid-cols-4 gap-4">
                <div className="p-4 rounded-2xl bg-[#F3F4EF]">
                  <div className="text-xs font-bold text-[#6B7280]">EIRP (Radiated Power)</div>
                  <div className="text-2xl font-extrabold font-mono mt-1">{budgetEval.eirp_dbm} dBm</div>
                </div>
                <div className="p-4 rounded-2xl bg-[#F3F4EF]">
                  <div className="text-xs font-bold text-[#6B7280]">Cellular Loss ({budgetEval.cellular_model_used})</div>
                  <div className="text-2xl font-extrabold font-mono mt-1">−{budgetEval.cellular_loss_db} dB</div>
                </div>
                <div className="p-4 rounded-2xl bg-[#F3F4EF]">
                  <div className="text-xs font-bold text-[#6B7280]">Received Power Pᵣ</div>
                  <div className="text-2xl font-extrabold font-mono mt-1">{budgetEval.rx_power_dbm} dBm</div>
                </div>
                <div
                  className={`p-4 rounded-2xl border ${
                    budgetEval.fade_margin_db > 0
                      ? 'bg-lime-50 border-lime-300 text-[#0B2E1A]'
                      : 'bg-red-50 border-red-300 text-red-900'
                  }`}
                >
                  <div className="text-xs font-bold uppercase flex items-center gap-1.5">
                    {budgetEval.fade_margin_db > 0 ? (
                      <CheckCircle2 className="w-4 h-4 text-green-600" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-red-600" />
                    )}
                    Fade Margin ({budgetEval.link_status})
                  </div>
                  <div className="text-2xl font-extrabold font-mono mt-1">
                    {budgetEval.fade_margin_db > 0 ? '+' : ''}
                    {budgetEval.fade_margin_db} dB
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 4: 900 MHZ COURSE BENCHMARK */}
          {activeTab === 'benchmark' && benchmarkData && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
              <h3 className="font-extrabold text-lg text-[#111827] mb-1">
                21CSE458T Course Benchmark Table{' '}
                <span className="text-xs font-medium text-[#6B7280]">
                  (Exact 900 MHz, hₜ = 30 m, hᵣ = 1.5 m Values Matching MATLAB & Word Report)
                </span>
              </h3>
              <div className="overflow-x-auto mt-4">
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

          {/* TAB 5: MODEL COMPARISON MATRIX */}
          {activeTab === 'matrix' && matrixData && (
            <div className="bg-white rounded-3xl p-6 border border-black/5 shadow-sm">
              <h3 className="font-extrabold text-lg text-[#111827] mb-4">
                Formal Academic Comparison Matrix{' '}
                <span className="text-xs font-medium text-[#6B7280]">
                  (Valid Ranges, Assumptions & Practical Applications of All 7 Models)
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
