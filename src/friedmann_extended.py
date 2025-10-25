import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants (em units cosmológicas, H0 em 1/Gyr pra simplicidade)
H0 = 70  # km/s/Mpc, mas convertemos pra 1/Gyr ~ 0.23 /Gyr (aprox)
H0_gyr = 0.23  # Hubble em 1/Gyr
Omega_m = 0.315
Omega_L = 0.685
Omega_k = 1 - Omega_m - Omega_L
Gyr_to_s = 3.156e16  # Mas usamos t em Gyr

# Equação de Friedmann estendida pra cosmologia cíclica
def friedmann_extended(t, y, Omega_m, Omega_L, Omega_k, H0_gyr):
    a, da_dt = y  # Estado: [a, \dot{a}]
    
    # H atual
    H = H0_gyr * np.sqrt(Omega_m / a**3 + Omega_L + Omega_k / a**2)
    
    # Derivada: \dot{a} = H a
    dadt = H * a
    
    # Aceleração: \ddot{a} = - (4πG/3) (ρ + 3p) a + cyclic_term
    # Simplificado: pra flat matter+DE, \ddot{a}/a = - (H0^2 /2) (Ω_m / a^3) + cyclic
    accel = -0.5 * H0_gyr**2 * (Omega_m / a**3) * a
    cyclic_term = 0.05 * np.sin(2 * np.pi * t / 13.8) * a  # Oscilação fraca em escala de Hubble
    da_dt_dt = accel + cyclic_term
    
    return [dadt, da_dt_dt]

# Condições iniciais (evita overflow: early universe a~0.01)
a0 = 0.01
da_dt0 = H0_gyr * a0  # Consistente com H inicial

# Tempo em Gyr
t_span = (0, 14)  # 14 Gyr
t_eval = np.linspace(0, 14, 1000)

# Resolve ODE
sol = solve_ivp(friedmann_extended, t_span, [a0, da_dt0],
                args=(Omega_m, Omega_L, Omega_k, H0_gyr),
                t_eval=t_eval, method='RK45', rtol=1e-6)

# Resultados
a = sol.y[0]
t = sol.t

# Plot Scale Factor
plt.figure(figsize=(10, 6))
plt.plot(t, a, label='Fator de Escala (a)')
plt.xlabel('Tempo (Gyr)')
plt.ylabel('Fator de Escala')
plt.title('Evolução em Cosmologia Cíclica Estendida')
plt.legend()
plt.grid(True)
plt.show()

# Hubble Parameter
H = (np.gradient(a, t) / a)  # Numérico, ou use fórmula
plt.figure(figsize=(10, 6))
plt.plot(t, H / H0_gyr, label='H/H0')
plt.xlabel('Tempo (Gyr)')
plt.ylabel('H/H0')
plt.title('Parâmetro de Hubble')
plt.legend()
plt.grid(True)
plt.show()

print(f"Sucesso! a(final) = {a[-1]:.3f}, esperado ~1.0 em t=13.8 Gyr.")
