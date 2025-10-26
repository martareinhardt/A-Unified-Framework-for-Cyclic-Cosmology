# greek_phases.py - Simulação das fases gregas com τ anomaly
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

def friedmann_with_tau(a, t, alpha=0.215, beta=1.0, gamma=0.8, tau=0.042, phi=1.618):
    """Friedmann estendida com termo τ anômalo."""
    rho = 1 / a**3  # Densidade matéria simplificada
    H2_base = (8 * np.pi / 3) * rho + 1 / 3  # Λ fake =1
    tau_term = tau * np.exp(-tau * t / phi) * rho  # Anomalia transitória
    # Adiciona fases cumulativas (simplificado)
    H2_cum = H2_base + alpha * phi * rho + beta * (1 / a) * rho + gamma * rho**0.5 + tau_term
    return np.sqrt(H2_cum)

def simulate_cycle(tau=0.042, phi=1.618, t_max=10, n_points=100):
    """Simula ciclo completo."""
    t = np.linspace(0, t_max, n_points)
    a = np.exp(t)  # Expansão fake (widening)
    H_tau = [friedmann_with_tau(a_i, t_i, tau=tau, phi=phi) for t_i, a_i in zip(t, a)]
    H_no = [friedmann_with_tau(a_i, t_i, tau=0, phi=phi) for t_i, a_i in zip(t, a)]
    return t, {'tau': np.array(H_tau), 'no_tau': np.array(H_no)}

if __name__ == "__main__":
    t, H = simulate_cycle()
    plt.plot(t, H['tau'], label='Com τ')
    plt.plot(t, H['no_tau'], label='Sem τ')
    plt.xlabel('Tempo Cósmico')
    plt.ylabel('H(t)')
    plt.legend()
    plt.savefig('../results/h_t_simulation.png')  # Salva em /results/
    plt.show()
    print("Simulação rodou! Drop médio:", np.mean(H['tau'] - H['no_tau']))
