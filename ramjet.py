import tkinter as tk
import math
from os import system
import time

from reactions import *
from substance import *

# ----------------------------------------------------
# ISM Setup
# ----------------------------------------------------

H2 = molecular_hydrogen()
H1 = proton()
He = helium()

# https://en.wikipedia.org/wiki/Interstellar_medium
# retrieved on 6.11.2021

# it seems that
# 10**6 molecules per cm^3 can be reached in cool, dense regions
# of ISM, but this number can go as low as 10**(-4) in the
# hot, diffuse regions

# molecules per cm^3 converted into molecules per m^3
medium_density = 10**5 * (0.000001)

# https://en.wikipedia.org/wiki/Interstellar_medium
# retrieved on 6.11.2021

# nearly the entirety of the rest of the matter is helium
ISM_hydrogen_ratio = 0.91

# rate of atomic hydrogen to all hydrogen
hydrogen_atomic_ratio = 0.5

density = medium_density * ISM_hydrogen_ratio * (1-hydrogen_atomic_ratio) * H2.get_molecular_mass()
density += medium_density * ISM_hydrogen_ratio * hydrogen_atomic_ratio * H1.get_molecular_mass()
density += medium_density * (1-ISM_hydrogen_ratio) * He.get_molecular_mass()

# ----------------------------------------------------
# Starship Setup
# ----------------------------------------------------

ship_mass = 100000 # kg
scoop_area = math.pi * 15000**2 # circle with 15km radius

reactor = proton_proton_chain()

# A web search says this number can go up to 100 million K, and
# fusion requires 15 million K, so I'll go with a somewhat
# conservative 30 million K
reactor_temp = 30000000 # K

# this is completely arbitrary
reactor_efficiency = 0.4
energy_conversion_efficiency = 0.02
reactor_max_power = 500000 # Watt
max_exhaust_vel = 5000000 # m/s

vel_init = 50000 # m/s

drag_coeff = 0.7

# ----------------------------------------------------
# Init Simulation
# ----------------------------------------------------

sim_time = 0 # seconds
delta_t = 1000000 # seconds
vel = vel_init
dist = 0

while True:
    sim_time += delta_t
    pp_intake_rate = (medium_density * ISM_hydrogen_ratio * (1-hydrogen_atomic_ratio) * 2
                      * scoop_area * vel) # particles/s
    pp_intake_rate += (medium_density * ISM_hydrogen_ratio * hydrogen_atomic_ratio
                      * scoop_area * vel) # particles/s

    # H2 intake rate is divided by 2 here because we need 2 hydrogen to initiate a single fusion process
    reactor_energy_output = reactor.get_energy_output(reactor_temp) * pp_intake_rate * reactor_efficiency # J/s

    # clamp energy output by max power
    reactor_energy_output = min(reactor_energy_output, reactor_max_power)
    
    reactor_material_output = reactor.get_material_output(reactor_temp)

    sum_exhaust_mass = 0
    for material in reactor_material_output[0]:
        sum_exhaust_mass += material.get_molecular_mass()
        
    avg_exhaust_mass_rate = ((sum_exhaust_mass * reactor_material_output[1]) / len(reactor_material_output[0])) * (pp_intake_rate)

    # relativity ignored
    avg_exhaust_vel = math.sqrt(2*reactor_energy_output/avg_exhaust_mass_rate) * energy_conversion_efficiency # m/s

    # clamp exhaust vel
    avg_exhaust_vel = min(avg_exhaust_vel, max_exhaust_vel)

    thrust = abs(avg_exhaust_vel * avg_exhaust_mass_rate) # Newtons (kg*m/s^-2)

    if vel > 0:
        drag = 0.5 * drag_coeff * scoop_area * density * vel**2
    else:
        drag = 0

    accel = ((thrust - drag)/ship_mass) * delta_t
    vel += accel * delta_t
    dist += vel * delta_t

    system("cls")
    print("Time: %.2f s (%.2f years)" % (sim_time, sim_time/31536000))
    print("Velocity: %.2f m/s" % vel)
    print("Dist Covered: %.2f m (%.5f ly)" % (dist, dist * 0.0000000000000001057001))
    print("Thrust: %.15f N" % thrust)
    print("Density: %.20f kg/m^3" % density)
    print("Drag: %.15f N" % drag)
    print("P-P Intake Rate: %.10f s-1" % pp_intake_rate)
    print("Reactor Energy Output: %.10f J" % reactor_energy_output)
    print("Mass Flow: %.20f kg/s" % avg_exhaust_mass_rate)
    print("Exhaust Vel: %.5f m/s" % avg_exhaust_vel)

    if thrust > drag:
        print("\nNET THRUST!")
    elif thrust == drag:
        print("\nTHRUST EQUALS DRAG!")
    else:
        print("\nCANNOT OVERCOME DRAG!")

    time.sleep(0.02)
