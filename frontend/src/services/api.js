const API_BASE = '/api';

export async function fetchSimulation(payload) {
  const res = await fetch(`${API_BASE}/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Simulation failed (${res.status})`);
  return res.json();
}

export async function fetchComparisonMatrix() {
  const res = await fetch(`${API_BASE}/comparison-matrix`);
  if (!res.ok) throw new Error('Failed to load comparison matrix');
  return res.json();
}

export async function fetchBenchmark900MHz() {
  const res = await fetch(`${API_BASE}/benchmark-900mhz`);
  if (!res.ok) throw new Error('Failed to load 900 MHz benchmark');
  return res.json();
}

export async function evaluateLinkBudget(payload) {
  const res = await fetch(`${API_BASE}/link-budget`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error('Failed to compute link budget');
  return res.json();
}

export async function fetchMmWaveTransition(freqGhz = 28.0) {
  const res = await fetch(`${API_BASE}/mmwave-transition-data?freq_ghz=${freqGhz}`);
  if (!res.ok) throw new Error('Failed to load mmWave transition data');
  return res.json();
}

