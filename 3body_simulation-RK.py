import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Planet:
    def __init__(self, x, y, radius, color, mass, vx=0, vy=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.vx = vx
        self.vy = vy
        self.orbit_euler = [(x, y)]  # Separate orbits for Euler and Runge-Kutta methods
        self.orbit_rk = [(x, y)]

def update_position(planet, dt):
    planet.x += planet.vx * dt
    planet.y += planet.vy * dt

def update_velocity(planet, force, dt):
    ax = force[0] / planet.mass
    ay = force[1] / planet.mass
    planet.vx += ax * dt
    planet.vy += ay * dt

def gravitational_force(planet1, planet2):
    G = 1.0
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    distance_squared = dx**2 + dy**2
    distance = math.sqrt(distance_squared)
    force_magnitude = G * planet1.mass * planet2.mass / distance_squared
    force_x = force_magnitude * dx / distance
    force_y = force_magnitude * dy / distance
    return (force_x, force_y)

def euler_step(planet, dt, planets):
    for planet in planets:
        net_force = [0, 0]
        for other_planet in planets:
            if planet != other_planet:
                force = gravitational_force(planet, other_planet)
                net_force[0] += force[0]
                net_force[1] += force[1]


        update_velocity(planet, net_force, dt)
    for planet in planets:
        update_position(planet, dt)
        planet.orbit_euler.append((planet.x, planet.y))
    

def runge_kutta_step(planet, dt, planets):
    # Backup the original velocities and positions
    vx_backup, vy_backup = planet.vx, planet.vy
    x_backup, y_backup = planet.x, planet.y

    # Calculate forces at the initial position
    initial_force = calculate_total_force(planet, planets)

    # Update velocity using Runge-Kutta method
    k1x, k1y = initial_force[0] / planet.mass, initial_force[1] / planet.mass
    planet.vx = vx_backup + k1x * dt / 2
    planet.vy = vy_backup + k1y * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2

    second = calculate_total_force(planet, planets)
    k2x, k2y = second[0] / planet.mass, second[1] / planet.mass
    planet.vx = vx_backup + k2x * dt / 2
    planet.vy = vy_backup + k2y * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2

    third = calculate_total_force(planet, planets)
    k3x, k3y = third[0] / planet.mass, third[1] / planet.mass
    planet.vx = vx_backup + k3x * dt / 2
    planet.vy = vy_backup + k3y * dt / 2
    planet.x = x_backup + planet.vx * dt / 2
    planet.y = y_backup + planet.vy * dt / 2

    last = calculate_total_force(planet, planets)
    k4x, k4y = last[0] / planet.mass, last[1] / planet.mass

    planet.vx = vx_backup + (k1x + 2 * k2x + 2 * k3x + k4x) * dt / 6
    planet.vy = vy_backup + (k1y + 2 * k2y + 2 * k3y + k4y) * dt / 6

    # Update position
    update_position(planet, dt)

    # Append the updated position to the orbit
    planet.orbit_rk.append((planet.x, planet.y))

def calculate_total_force(planet, planets):
    total_force = [0, 0]
    for other_planet in planets:
        if planet != other_planet:
            force_component = gravitational_force(planet, other_planet)
            total_force[0] += force_component[0]
            total_force[1] += force_component[1]
    return total_force


def simulate(planets, dt, method):
    if method == 'euler':
        for planet in planets:
            euler_step(planet, dt, planets)
    elif method == 'runge_kutta':
        for planet in planets:
            runge_kutta_step(planet, dt, planets)

        

def animate(frame, planets, ax, method):
    dt = 0.01
    simulate(planets, dt, method)
    ax.clear()
    
    # Add Cartesian axis lines
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    
    for planet in planets:
        orbit = planet.orbit_euler if method == 'euler' else planet.orbit_rk
        ax.scatter(planet.x, planet.y, color=planet.color, s=100, label=f'{planet.color} Planet')
        updated_points = list(zip(*orbit))
        ax.plot(updated_points[0], updated_points[1], color=planet.color, linewidth=2)

    # Set legend outside the animation function
    ax.legend()


# Create instances of Planet with initial coordinates and velocities
v = 1
L = 2
planet_A = Planet(-L/2, 0, 0.1, 'red', 2, v, 0)
planet_B = Planet(L/2, 0, 0.1, 'green', 2, -v / 2, v * math.sqrt(3) / 2)
planet_C = Planet(0, L * math.sqrt(3) / 2, 0.1, 'blue', 1, -v / 2, -v * math.sqrt(3) / 2)
planets = [planet_A, planet_B, planet_C]

# Configure the animation for Euler's method
fig, ax = plt.subplots()
ani_euler = FuncAnimation(fig, animate, frames=range(100), fargs=(planets, ax, 'euler'), interval=50)
ax.set_title("Euler's Method")

plt.show()


v = 1
L = 2
planet_A = Planet(-L/2, 0, 0.1, 'red', 2, v, 0)
planet_B = Planet(L/2, 0, 0.1, 'green', 2, -v / 2, v * math.sqrt(3) / 2)
planet_C = Planet(0, L * math.sqrt(3) / 2, 0.1, 'blue', 1, -v / 2, -v * math.sqrt(3) / 2)
planets = [planet_A, planet_B, planet_C]

# Create a list of planets


fig, ax = plt.subplots()
ani_rk = FuncAnimation(fig, animate, frames=range(100), fargs=(planets, ax, 'runge_kutta'), interval=50)
ax.set_title("Runge-Kutta Method")

plt.show()

