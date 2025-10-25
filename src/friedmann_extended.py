"""
Friedmann Extension for Cyclic Cosmology Model
Implements the unifying equation with dynamic coupling (alpha), widening factor (beta),
and emergent gravity term (gamma). Solves ODEs for a(t), rho_m(t), phi(t) in FLRW metric.

Author: Marta Reinhardt
Date: October 2025
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.constants import G, c
import astropy.units as u
from astropy.cosmology import Planck18

class CyclicCosmology:
    def __init__(self, alpha=0.2, beta=0.1, gamma=0.05, Omega_m=0.3, H0=67.4):
        """
        Initialize the model parameters.
        - alpha: Dynamic coupling between DE (phi) and matter (rho_m).
        - beta: Widening factor for expansive growth.
        - gamma: Emergent gravity quantum term.
        - Omega_m: Matter density parameter.
        - H0: Hubble constant in km/s/Mpc.
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.Omega_m = Omega_m
        self.H0 = H0 * u.km / u.s / u.Mpc.to(u.s**-1)  # Convert to s^-1
        self.rho_crit = 3 * (self.H0**2) / (8 * np.pi * G)  # Critical density

    def friedmann_eq(self, t, y):
        """
        System of ODEs based on extended Friedmann equation.
        y = [a, rho_m, phi]  # Scale factor, matter density, scalar field
        Returns dy/dt.
        """
        a, rho_m, phi = y
        H = np.sqrt((8 * np.pi * G / 3) * rho_m + (self.alpha * phi * rho_m) +
                    self.beta * (np.dot(a, a) / a) + self.gamma)  # Simplified emergent gravity
        da_dt = H * a
        drho_m_dt = -3 * H * rho_m * (1 + self.alpha * phi)  # Coupled dilution
        dphi_dt = np.sqrt(2 * np.pi * G * rho_m)  # Simple scalar field evolution
        return [da_dt, drho_m_dt, dphi_dt]

    def solve(self, t_span=(0, 13.8), y0=[1e-3, self.Omega_m * self.rho_crit, 1.0], method='RK45'):
        """
        Solve the system from Big Bang (t=0) to present (13.8 Gyr).
        Returns sol object from solve_ivp.
        """
        t_eval = np.linspace(t_span[0], t_span[1], 1000) * 3.156e7 * 1e9  # Seconds
        sol = solve_ivp(self.friedmann_eq, t_span * 3.156e7 * 1e9, y0, t_eval=t_eval, method=method)
        return sol

    def hubble_param(self, z):
        """
        Compute H(z) for given redshift, comparing to Planck18.
        """
        a = 1 / (1 + z)
        # Approximate from solution or analytical
        return self.H0 * np.sqrt(self.Omega_m / a**3 + (1 - self.Omega_m) * np.exp(3 * self.alpha * z))

# Example usage
if __name__ == "__main__":
    model = CyclicCosmology(alpha=0.215)  # From JWST fit
    sol = model.solve()
    print(f"Scale factor at present: {sol.y[0][-1]:.3f}")
    print(f"H(z=7): {model.hubble_param(7):.2f} km/s/Mpc")
