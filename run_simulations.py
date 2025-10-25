#!/usr/bin/env python3
"""
Run Simulations for Cyclic Cosmology
CLI tool to simulate and plot the model with given parameters.

Usage: python run_simulations.py --alpha 0.2 --z_max 10 --output results/
"""

import argparse
import sys
from src.friedmann_extended import CyclicCosmology
from src.bounce_quantum import QuantumBounce
import matplotlib.pyplot as plt

def main(alpha, z_max, output_dir):
    # Cosmological simulation
    model = CyclicCosmology(alpha=alpha)
    sol = model.solve(t_span=(0, z_max / model.H0.value))  # Approximate t from z
    t = sol.t / (3.156e7 * 1e9)  # Gyr
    a = sol.y[0]
    
    # Plot H(z) approximation
    z = 1 / a - 1
    H_z = model.hubble_param(z)
    plt.figure(figsize=(10, 6))
    plt.plot(z, H_z.value, label=f'α={alpha}')
    plt.xlabel('Redshift z')
    plt.ylabel('H(z) [km/s/Mpc]')
    plt.title('Hubble Parameter in Cyclic Model')
    plt.legend()
    plt.savefig(f'{output_dir}/hubble_simulation.png')
    plt.close()
    
    # Quantum bounce
    qb = QuantumBounce(coupling=alpha)
    times, fluct = qb.simulate_bounce()
    qb.plot_bounce(times, fluct)
    
    print(f"Simulation complete. Alpha optimized: {alpha}. Check {output_dir}/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Cyclic Cosmology Simulations')
    parser.add_argument('--alpha', type=float, default=0.2, help='Dynamic coupling alpha')
    parser.add_argument('--z_max', type=float, default=10, help='Max redshift for sim')
    parser.add_argument('--output', type=str, default='results/', help='Output directory')
    args = parser.parse_args()
    main(args.alpha, args.z_max, args.output)
