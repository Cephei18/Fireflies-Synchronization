import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parameters
n_fireflies = 20
phases = np.random.rand(n_fireflies) * 0.5  # start more spread out
delta = 0.01                                # slower phase increase
eps = 0.05                                  # weaker sync force


# Data for sync meter
sync_values = []

# Create figure with 2 subplots (top: bars, bottom: sync graph)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [3, 1]})

# Bar chart (firefly phases)
bars = ax1.bar(range(n_fireflies), phases, color='blue')
ax1.set_ylim(0, 1.1)
ax1.set_title("Firefly Synchronization")
ax1.set_ylabel("Phase (0 to 1)")

# Line plot (sync meter)
sync_line, = ax2.plot([], [], color='green')
ax2.set_xlim(0, 200)  # 200 frames
ax2.set_ylim(0, 0.3)  # phase std dev range
ax2.set_title("Synchronization Meter (Standard Deviation of Phases)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Std Dev")

def update(frame):
    global phases, sync_values

    new_phases = phases + delta
    flashed = new_phases >= 1.0

    for i in range(n_fireflies):
        if flashed[i]:
            new_phases[i] = 0
            for j in range(n_fireflies):
                if i != j:
                    new_phases[j] += eps * (1 - new_phases[j])

    new_phases = np.clip(new_phases, 0, 1)

    # Update bars
    for bar, h in zip(bars, new_phases):
        bar.set_height(h)
        bar.set_color('yellow' if h > 0.95 else 'blue')

    # Update sync meter
    std = np.std(new_phases)
    sync_values.append(std)
    sync_line.set_data(range(len(sync_values)), sync_values)

    # Auto-scroll x-axis
    if len(sync_values) > 200:
        ax2.set_xlim(len(sync_values)-200, len(sync_values))

    phases[:] = new_phases
    return bars, sync_line

ani = animation.FuncAnimation(fig, update, frames=400, interval=50, blit=False)
plt.tight_layout()
plt.show()
