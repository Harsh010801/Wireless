"""
Command-Line Interface for Wireless Signal Propagation Simulations.

Usage:
    python scripts/run_simulation.py --scenario urban
    python scripts/run_simulation.py --scenario rural
    python scripts/run_simulation.py --scenario indoor
    python scripts/run_simulation.py --scenario suburban
    python scripts/run_simulation.py --scenario 5g_midband
    python scripts/run_simulation.py --all
"""

import argparse
import sys
from pathlib import Path

# Add src to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from propagation.analysis.comparator import ModelComparator
from propagation.simulation.engine import SimulationEngine
from propagation.simulation.scenario import ScenarioConfig


def run_scenario(scenario_path: Path, output_dir: Path):
    print("=" * 75)
    print(f"  RUNNING SIMULATION: {scenario_path.stem.upper()}")
    print("=" * 75)

    config = ScenarioConfig.from_yaml(scenario_path)
    engine = SimulationEngine()

    print(f"Scenario Name    : {config.name}")
    print(f"Carrier Frequency: {config.frequency} {config.frequency_unit}")
    print(f"Distance Range   : {config.min_distance} to {config.max_distance} {config.distance_unit}")
    print(f"Tx Power / Gain  : {config.tx_power_dbm} dBm / {config.tx_gain_dbi} dBi")
    print(f"Antenna Heights  : ht = {config.ht} m, hr = {config.hr} m")
    print(f"Active Models    : {', '.join(config.models)}")
    print("-" * 75)

    result = engine.run_distance_sweep(config)

    # Save CSV
    output_dir.mkdir(parents=True, exist_ok=True)
    csv_path = output_dir / f"sim_results_{scenario_path.stem}.csv"
    wide_df = result.to_wide_dataframe()
    wide_df.to_csv(csv_path, index=False)
    print(f"[+] Simulation raw data saved to: {csv_path}")

    # Summary Statistics
    stats_df = ModelComparator.calculate_summary_statistics(result)
    print("\nDescriptive Summary Statistics Across Models:")
    print(stats_df.to_string(index=False))
    print("-" * 75)


def main():
    parser = argparse.ArgumentParser(
        description="Run comparative wireless signal propagation simulations."
    )
    parser.add_argument(
        "--scenario",
        type=str,
        default="urban",
        help="Scenario name ('urban', 'rural', 'suburban', 'indoor', '5g_midband', or 'all')",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/reports",
        help="Directory to save raw CSV simulation outputs",
    )

    args = parser.parse_args()
    scenarios_dir = ROOT_DIR / "experiments" / "scenarios"
    out_dir = ROOT_DIR / args.output_dir

    if args.scenario.lower() == "all":
        yaml_files = sorted(scenarios_dir.glob("*.yaml"))
        for yf in yaml_files:
            run_scenario(yf, out_dir)
    else:
        target_yaml = scenarios_dir / f"{args.scenario.lower()}.yaml"
        if not target_yaml.exists():
            print(f"Error: Scenario '{args.scenario}' not found at {target_yaml}")
            print(f"Available scenarios: {[f.stem for f in scenarios_dir.glob('*.yaml')]}")
            sys.exit(1)
        run_scenario(target_yaml, out_dir)


if __name__ == "__main__":
    main()

