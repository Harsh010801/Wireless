"""
Generate animated GIF of path loss curves being drawn progressively.
Saves: animated_path_loss.gif
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams

rcParams['font.size'] = 12

# Parameters
f = 900        # MHz
ht = 30        # m
hr = 1.5       # m
d_range = np.linspace(1, 20, 200)

# Model calculations
def fspl(d, f):
    return 20*np.log10(d) + 20*np.log10(f) + 32.44

def hata_urban(d, f, ht, hr):
    a_hr = (1.1*np.log10(f) - 0.7)*hr - (1.56*np.log10(f) - 0.8)
    return 69.55 + 26.16*np.log10(f) - 13.82*np.log10(ht) - a_hr + (44.9 - 6.55*np.log10(ht))*np.log10(d)

def okumura_open(d, f, ht, hr):
    corr = -4.78*(np.log10(f))**2 + 18.33*np.log10(f) - 40.94
    return hata_urban(d, f, ht, hr) + corr

pl_fspl = fspl(d_range, f)
pl_oku = okumura_open(d_range, f, ht, hr)
pl_hata = hata_urban(d_range, f, ht, hr)

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#1e293b')

ax.set_xlim(0, 21)
ax.set_ylim(80, 180)
ax.set_xlabel('Distance (km)', color='#94a3b8', fontsize=13)
ax.set_ylabel('Path Loss (dB)', color='#94a3b8', fontsize=13)
ax.set_title('Path Loss vs Distance (f=900 MHz) — Animated Simulation', color='white', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, color='#334155')
ax.tick_params(colors='#94a3b8')
for spine in ax.spines.values():
    spine.set_color('#334155')

line_fspl, = ax.plot([], [], 'o-', color='#38bdf8', lw=2.5, markersize=0, label='Free Space Path Loss')
line_oku, = ax.plot([], [], 's--', color='#4ade80', lw=2.5, markersize=0, label='Okumura (Open Area)')
line_hata, = ax.plot([], [], '^-', color='#f87171', lw=2.5, markersize=0, label='Hata (Urban Model)')

dot_fspl, = ax.plot([], [], 'o', color='#38bdf8', markersize=10, zorder=5)
dot_oku, = ax.plot([], [], 's', color='#4ade80', markersize=10, zorder=5)
dot_hata, = ax.plot([], [], '^', color='#f87171', markersize=10, zorder=5)

legend = ax.legend(loc='upper left', fontsize=10, facecolor='#1e293b', edgecolor='#334155', labelcolor='#e2e8f0')

# Info text box
info_text = ax.text(14, 90, '', fontsize=10, color='#e2e8f0',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='#0f172a', edgecolor='#38bdf8', alpha=0.9),
                    verticalalignment='bottom', fontfamily='monospace')

# Team watermark
ax.text(0.98, 0.02, 'Harsh Yadav · Utkarsh Dabas · Tamanna Singh\n21CSE458T — Wireless & Mobile Communication',
        transform=ax.transAxes, fontsize=8, color='#475569', ha='right', va='bottom')

total_frames = 80

def init():
    line_fspl.set_data([], [])
    line_oku.set_data([], [])
    line_hata.set_data([], [])
    dot_fspl.set_data([], [])
    dot_oku.set_data([], [])
    dot_hata.set_data([], [])
    info_text.set_text('')
    return line_fspl, line_oku, line_hata, dot_fspl, dot_oku, dot_hata, info_text

def animate(frame):
    n = min(int((frame / total_frames) * len(d_range)), len(d_range))
    if n < 1:
        n = 1

    line_fspl.set_data(d_range[:n], pl_fspl[:n])
    line_oku.set_data(d_range[:n], pl_oku[:n])
    line_hata.set_data(d_range[:n], pl_hata[:n])

    # Moving dots at the tip
    dot_fspl.set_data([d_range[n-1]], [pl_fspl[n-1]])
    dot_oku.set_data([d_range[n-1]], [pl_oku[n-1]])
    dot_hata.set_data([d_range[n-1]], [pl_hata[n-1]])

    # Info box
    d_curr = d_range[n-1]
    info_text.set_text(
        f'd = {d_curr:.1f} km\n'
        f'FSPL:    {pl_fspl[n-1]:.1f} dB\n'
        f'Okumura: {pl_oku[n-1]:.1f} dB\n'
        f'Hata:    {pl_hata[n-1]:.1f} dB\n'
        f'Δ(Hata-FSPL): {pl_hata[n-1]-pl_fspl[n-1]:.1f} dB'
    )

    return line_fspl, line_oku, line_hata, dot_fspl, dot_oku, dot_hata, info_text

anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=total_frames + 15,  # +15 for pause at end
                                interval=80, blit=True)

output_path = 'animated_path_loss.gif'
print(f'[*] Rendering {total_frames + 15} frames to {output_path}...')
anim.save(output_path, writer='pillow', fps=12, dpi=120)
print(f'[+] Animation saved: {output_path}')
plt.close()

