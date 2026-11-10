"""
Course: 21CSE458T — Wireless and Mobile Communication (B.Tech CSE, 7th Sem)
Project: Comparative Analysis of Wireless Signal Propagation Models (Free Space, Okumura and Hata) using MATLAB/Python

Team Members:
1. Harsh Yadav (RA2311003011546)
2. Utkarsh Dabas (RA2311003011550)
3. Tamanna Singh (RA2311003011570)
"""

import numpy as np
import matplotlib.pyplot as plt

def run_simulation():
    # Simulation Parameters
    d = np.arange(1, 21)          # Distance from 1 km to 20 km
    f = 900.0                     # Carrier frequency in MHz
    h_te = 30.0                   # Base station / tower antenna height in meters
    h_re = 1.5                    # Mobile station antenna height in meters

    # 1. Free Space Path Loss (Friis Model)
    # L = 20*log10(d) + 20*log10(f) + 32.44
    fspl = 20.0 * np.log10(d) + 20.0 * np.log10(f) + 32.44

    # 2. Hata Urban Model
    # Mobile antenna correction factor a(h_re)
    a_hre = (1.1 * np.log10(f) - 0.7) * h_re - (1.56 * np.log10(f) - 0.8)
    # Urban path loss L_hata
    hata_urban = (
        69.55
        + 26.16 * np.log10(f)
        - 13.82 * np.log10(h_te)
        - a_hre
        + (44.9 - 6.55 * np.log10(h_te)) * np.log10(d)
    )

    # 3. Okumura Model (Open Area via standard Hata correction)
    correction = -4.78 * (np.log10(f) ** 2) + 18.33 * np.log10(f) - 40.94
    okumura = hata_urban + correction

    # -------------------------------------------------------------
    # Print Results Table to Console
    # -------------------------------------------------------------
    print("=" * 65)
    print("  WIRELESS PROPAGATION MODELS: NUMERICAL SIMULATION RESULTS")
    print(f"  Frequency = {f:.0f} MHz | Tower Height = {h_te:.0f} m | Mobile Height = {h_re:.1f} m")
    print("=" * 65)
    print(f"{'Distance (km)':<15} | {'Free Space (dB)':<16} | {'Okumura (dB)':<14} | {'Hata Urban (dB)':<14}")
    print("-" * 65)
    for i in range(len(d)):
        print(f"{d[i]:<15d} | {fspl[i]:<16.2f} | {okumura[i]:<14.2f} | {hata_urban[i]:<14.2f}")
    print("=" * 65)

    # Specific readings at 1 km and 20 km for report & viva
    print("\nBenchmark Readings:")
    print(f"• At 1 km  -> Free Space: {fspl[0]:.2f} dB | Okumura: {okumura[0]:.2f} dB | Hata: {hata_urban[0]:.2f} dB")
    print(f"• At 20 km -> Free Space: {fspl[-1]:.2f} dB | Okumura: {okumura[-1]:.2f} dB | Hata: {hata_urban[-1]:.2f} dB")

    # -------------------------------------------------------------
    # Plotting: Path Loss vs Distance
    # -------------------------------------------------------------
    plt.figure(figsize=(9, 6), dpi=300)
    plt.plot(d, fspl, 'b-o', linewidth=2.0, markersize=6, label='Free Space Path Loss (FSPL)')
    plt.plot(d, okumura, 'g--s', linewidth=2.0, markersize=6, label='Okumura Model (Open Area)')
    plt.plot(d, hata_urban, 'r-.^', linewidth=2.0, markersize=6, label='Hata Model (Urban)')

    plt.title("Path Loss vs Distance (f=900 MHz)", fontsize=14, fontweight='bold', pad=12)
    plt.xlabel("Distance (km)", fontsize=12, fontweight='bold')
    plt.ylabel("Path Loss (dB)", fontsize=12, fontweight='bold')
    plt.grid(True, linestyle=":", alpha=0.7)
    plt.legend(fontsize=11, loc="lower right", frameon=True)
    plt.xticks(np.arange(1, 21, 1))
    plt.tight_layout()

    # Save Graph
    graph_filename = "path_loss_graph.png"
    plt.savefig(graph_filename, dpi=300)
    print(f"\n[+] Graph successfully saved as: {graph_filename}")
    plt.close()

    return d, fspl, okumura, hata_urban

if __name__ == "__main__":
    run_simulation()

