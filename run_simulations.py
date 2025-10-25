import numpy as np
import matplotlib.pyplot as plt

# Classe CyclicCosmology (com método correto)
class CyclicCosmology:
    def __init__(self):
        self.hubble_param = 0.7
        self.scale_factor = 1.0
        self.time = 0.0
        self.rho_crit = 8.62e-27  # Densidade crítica pro bounce (de LQC)
    
    def set_hubble_parameter(self, h):  # <- Nome completo aqui!
        self.hubble_param = h
    
    def evolve_scale_factor(self, a_prev, dt=0.1):
        # Aproximação FLRW com matéria + DE
        H = self.hubble_param * np.sqrt(1 / a_prev**3 + 0.7)  # Omega_m / a^3 + Omega_L
        cyclic_osc = 0.01 * np.sin(2 * np.pi * self.time / 13.8)  # Termo cíclico fraco
        
        # Bounce quântico simples: se a < 0.1 (early universe), inverta H pra rebound
        if a_prev < 0.1:
            H = -abs(H) * 0.5  # Contração vira expansão
        
        self.time += dt
        return a_prev * np.exp(H * dt + cyclic_osc)

# Função principal de simulação
def run_simulations():
    cosmology = CyclicCosmology()
    num_steps = 1000
    initial_scale_factor = 0.01  # Começa bem pequeno (pós-bounce)
    hubble_parameter = 0.7
    dt = 0.014  # Passo ~0.014 Gyr (total ~14 Gyr)

    scale_factors = np.zeros(num_steps)
    scale_factors[0] = initial_scale_factor
    cosmology.set_hubble_parameter(hubble_parameter)  # <- Chamada corrigida!
    cosmology.time = 0.0

    for i in range(1, num_steps):
        scale_factors[i] = cosmology.evolve_scale_factor(scale_factors[i-1], dt)

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(scale_factors)
    plt.xlabel('Passo de Tempo')
    plt.ylabel('Fator de Escala (a)')
    plt.title('Simulação de Cosmologia Cíclica Unificada (com Bounce)')
    plt.grid(True)
    plt.show()

    print(f"Simulação completa! a(final) = {scale_factors[-1]:.3f}")
    print(f"Tempo total simulado: ~{num_steps * dt:.1f} Gyr")

# Rode!
run_simulations()
