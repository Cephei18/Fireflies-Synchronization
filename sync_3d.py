from vpython import sphere, color, rate, vector
import numpy as np
import random

# Number of fireflies
n = 20

# 3D space range
space_range = 10

# Create fireflies as glowing spheres
fireflies = []
phases = np.random.rand(n)  # phase: 0 to 1
delta = 0.01                # rate of phase increase
eps = 0.05                  # sync strength

for _ in range(n):
    pos = vector(random.uniform(-space_range, space_range),
                 random.uniform(-space_range, space_range),
                 random.uniform(-space_range, space_range))
    firefly = sphere(pos=pos, radius=0.5, color=color.yellow, emissive=True)
    fireflies.append(firefly)

# Main animation loop
while True:
    rate(60)  # ~60 FPS

    new_phases = phases + delta
    flashed = new_phases >= 1.0

    for i in range(n):
        if flashed[i]:
            new_phases[i] = 0
            for j in range(n):
                if i != j:
                    new_phases[j] += eps * (1 - new_phases[j])

    new_phases = np.clip(new_phases, 0, 1)

    # Update firefly glow (brightness linked to phase)
    for i in range(n):
        intensity = 1.5 * new_phases[i]
        fireflies[i].color = vector(intensity, intensity, 0.1)  # yellowish glow

    phases = new_phases
