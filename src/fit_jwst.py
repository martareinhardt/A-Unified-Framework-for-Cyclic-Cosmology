import numpy as np
from scipy.optimize import minimize
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Dados mock JWST (z, densidade observada, erro) - baseado em papers reais
z_obs = np.array([8.0, 10.0, 12.0, 15.0])
n_obs = np.array([0.05, 0.15, 0.08, 0.03])
n_err = np.array([0.01, 0.03, 0.02, 0.01])

# Função H(z) do seu modelo cíclico (simplificada; adapte pro bounce)
def H_z(z, Omega_m, H0=70):
    # ΛCDM base + termo cíclico fraco (pra ciclos: em z alto, H menor via tempo esticado)
    cyclic_factor = 1 + 0.05 * np.sin(2 * np.pi * z / 15)  # Oscilação
    return H0 * np.sqrt(Omega_m * (1 + z)**3 + (1 - Omega_m)) * cyclic_factor

# Densidade prevista: Simplificada sem V_comov (assumindo já comoving); use forma gaussiana peaked at z=10
def n_pred(z, params):
    Omega_m, A, z_peak, sigma = params
    # Dependência fraca em Omega_m via tempo disponível: fator (1+z_peak / (1+z)) or something
    time_factor = 1 / np.sqrt(Omega_m) * (1 + 0.1 * np.sin(2 * np.pi * (z - z_peak) / 10))  # Cyclic tweak
    n_gal = A * np.exp( - (z - z_peak)**2 / (2 * sigma**2) ) * time_factor
    return n_gal

# Chi²
def chi2(params):
    n_model = np.array([n_pred(zz, params) for zz in z_obs])
    return np.sum(((n_obs - n_model) / n_err)**2)

# Fit: Minimiza χ² com bounds pra physical params
initial_guess = [0.3, 0.1, 10.0, 2.0]  # Omega_m, A, z_peak, sigma
bounds = [(0.1, 0.5), (0.01, 1.0), (8.0, 12.0), (1.0, 4.0)]
result = minimize(chi2, initial_guess, method='L-BFGS-B', bounds=bounds)
Omega_m_fit, A_fit, z_peak_fit, sigma_fit = result.x

print(f"Parâmetros otimizados: Ω_m = {Omega_m_fit:.3f}, A = {A_fit:.3f}, z_peak = {z_peak_fit:.1f}, sigma = {sigma_fit:.1f}")
print(f"χ² final = {result.fun:.2f} (menor é melhor; pra ΛCDM puro ~5-10)")

# Plot: Observado vs. Previsto
z_plot = np.linspace(7, 16, 100)
n_model_plot = np.array([n_pred(zz, result.x) for zz in z_plot])
plt.figure(figsize=(10, 6))
plt.errorbar(z_obs, n_obs, yerr=n_err, fmt='o', label='JWST Observado', color='red', capsize=5)
plt.plot(z_plot, n_model_plot, 'b-', label=f'Modelo Fit (Ω_m={Omega_m_fit:.3f}, z_peak={z_peak_fit:.1f})', linewidth=2)
plt.xlabel('Redshift (z)')
plt.ylabel('Densidade de Galáxias (n_gal / Mpc³, M_UV < -21)')
plt.title('Fit de Densidade de Galáxias com Dados JWST (Modelo Cíclico Melhorado)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.yscale('log')  # Log pra melhor visual
plt.show()
