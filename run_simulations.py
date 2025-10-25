import numpy as np
import matplotlib.pyplot as plt

class CyclicCosmology:
    def __init__(self):
        self.hubble_param = 70 / 3.08568e19 * 3.15576e16  # H0 real em 1/Gyr ~0.023 (aprox)
        self.time = 0.0
        self.bounce_happened = False  # Flag pra bounce só uma vez
        self.a_min = 0.001  # Ponto de bounce (a_min correspondente a ρ_crit)
        self.omega_m = 0.341  # Do fit JWST! (ajustado pro excesso early galaxies)
        self.omega_l = 1 - self.omega_m  # DE
    
    def set_hubble_parameter(self, h):
        self.hubble_param = h
    
    def evolve_scale_factor(self, a_prev, dt=0.1):
        # Densidade relativa: rho ~ Omega_m / a^3 + Omega_l
        rho_rel = self.omega_m / a_prev**3 + self.omega_l
        H = self.hubble_param * np.sqrt(rho_rel)
        
        cyclic_osc = 0.01 * np.sin(2 * np.pi * self.time / 13.8)  # Oscilação cíclica
        
        # Bounce: Só se NÃO aconteceu ainda E a < a_min (alta densidade)
        if not self.bounce_happened and a_prev < self.a_min:
            print(f"Bounce ativado em t={self.time:.1f} Gyr, a={a_prev:.3f}!")  # Log pra ver
            H = abs(H)  # Flip pra positivo (rebound)
            self.bounce_happened = True  # Só uma vez por ciclo
        
        self.time += dt
        new_a = a_prev * np.exp(H * dt + cyclic_osc)
        return max(new_a, 1e-10)  # Evita zero/NaN

def run_simulations():
    cosmology = CyclicCosmology()
    num_steps = 2000  # Mais passos pra ciclo completo (~28 Gyr)
    initial_scale_factor = 1.0  # Começa no "presente" e contrai primeiro (simula ciclo)
    dt = 0.014  # ~0.014 Gyr/step

    scale_factors = np.zeros(num_steps)
    scale_factors[0] = initial_scale_factor
    
    # Primeira fase: Contração (H negativo manual pra simular ciclo)
    for i in range(1, num_steps):
        # Inverte H na "fase de contração" (primeiros 700 steps, ~10 Gyr)
        if i < 700:
            H_adj = -cosmology.hubble_param * np.sqrt(cosmology.omega_m / scale_factors[i-1]**3 + cosmology.omega_l)
        else:
            H_adj = cosmology.hubble_param * np.sqrt(cosmology.omega_m / scale_factors[i-1]**3 + cosmology.omega_l)
        
        cyclic_osc = 0.01 * np.sin(2 * np.pi * cosmology.time / 13.8)
        scale_factors[i] = scale_factors[i-1] * np.exp(H_adj * dt + cyclic_osc)
        cosmology.time += dt
        scale_factors[i] = max(scale_factors[i], 1e-10)  # Anti-zero

    # Plot melhorado: Adiciona linha vertical no bounce
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(scale_factors, 'b-', linewidth=2, label='Fator de Escala a(t)')
    bounce_step = np.argmin(scale_factors)  # Ponto de min a (bounce)
    ax.axvline(x=bounce_step, color='r', linestyle='--', label='Ponto de Bounce')
    ax.set_xlabel('Passo de Tempo')
    ax.set_ylabel('Fator de Escala (a)')
    ax.set_title('Simulação de Cosmologia Cíclica Unificada (Contração → Bounce → Expansão)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.show()

    print(f"Simulação completa! a(final) = {scale_factors[-1]:.3f}")
    print(f"a(mínima no bounce) = {np.min(scale_factors):.3e}")
    print(f"Tempo total simulado: ~{num_steps * dt:.1f} Gyr")
    print(f"Passo do bounce: {bounce_step} (~{bounce_step * dt:.1f} Gyr)")

# Rode!
if __name__ == "__main__":
    run_simulations()
