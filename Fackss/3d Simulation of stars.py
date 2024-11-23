import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
G = 6.67430e-11  # Gravitational constant, m^3 kg^-1 s^-2
M1 = 2.0e30      # Mass of the first body (e.g., a star), kg
M2 = 1.5e30      # Mass of the second body, kg
dt = 1e5         # Time step, seconds

# Initial positions and velocities (arbitrary)
pos1 = np.array([-1.0e11, 0.0, 0.0])   # Initial position of body 1, m
pos2 = np.array([1.0e11, 0.0, 0.0])    # Initial position of body 2, m
vel1 = np.array([0.0, 1.0e4, 0.0])     # Initial velocity of body 1, m/s
vel2 = np.array([0.0, -1.5e4, 0.0])    # Initial velocity of body 2, m/s

positions1 = [pos1]
positions2 = [pos2]

# Function to compute gravitational force
def gravitational_force(pos1, pos2, M1, M2):
    r_vec = pos2 - pos1
    r_mag = np.linalg.norm(r_vec)
    r_hat = r_vec / r_mag
    force_mag = G * M1 * M2 / r_mag**2
    force_vec = force_mag * r_hat
    return force_vec

# Simulate the motion for a set number of time steps
num_steps = 10000
for _ in range(num_steps):
    # Compute forces
    force_on_1 = gravitational_force(pos1, pos2, M1, M2)
    force_on_2 = -force_on_1  # Equal and opposite

    # Update velocities
    vel1 += (force_on_1 / M1) * dt
    vel2 += (force_on_2 / M2) * dt

    # Update positions
    pos1 += vel1 * dt
    pos2 += vel2 * dt

    # Store positions
    positions1.append(pos1.copy())
    positions2.append(pos2.copy())

# Convert positions to arrays for easy plotting
positions1 = np.array(positions1[1:])
positions2 = np.array(positions2[1:])

# Create the animation
fig, ax = plt.subplots()
ax.set_xlim(-3e11, 3e11)
ax.set_ylim(-3e11, 3e11)
ax.set_zlim(-3e11, 3e11)
body1, = ax.plot([], [], 'ro', markersize=10)  # Red dot for body 1
body2, = ax.plot([], [], 'bo', markersize=10)  # Blue dot for body 2
trail1, = ax.plot([], [], 'r-', alpha=0.5)     # Trail for body 1
trail2, = ax.plot([], [], 'b-', alpha=0.5)     # Trail for body 2

def init():
    body1.set_data([], [])
    body2.set_data([], [])
    trail1.set_data([], [])
    trail2.set_data([], [])
    return body1, body2, trail1, trail2

# Add flexibility for frame step interval
frame_step = 10  # Adjust as needed for different simulation speeds
def update(frame): 
    body1.set_data(positions1[frame, 0], positions1[frame, 1])
    body2.set_data(positions2[frame, 0], positions2[frame, 1])
    trail1.set_data(positions1[:frame, 0], positions1[:frame, 1])
    trail2.set_data(positions2[:frame, 0], positions2[:frame, 1])
    return body1, body2, trail1, trail2

ani = animation.FuncAnimation(fig, update, frames=range(0, num_steps+1, frame_step),
                              init_func=init, blit=True)

plt.title("Binary Star System Simulation", fontsize=16, fontweight='bold', color='navy')
plt.xlabel("x-position (m)", fontsize=14, color='darkgreen')
plt.ylabel("y-position (m)", fontsize=14, color='darkgreen')

plt.show()