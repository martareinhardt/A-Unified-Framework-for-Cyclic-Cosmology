import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('.')  # Pra importar local
from cyclic_cosmology import CyclicCosmology  # Agora existe!

def run_simulations():
    cosmology = CyclicCosmology()
    num_steps = 1000
    initial_scale_factor = 0.5  # Começa em contração
    hubble_parameter = 0.7
    dt = 0.014  # Passo ~0.014 Gyr

    scale_factors = np.zeros(num_steps)
    scale_factors[0] = initial_scale_factor
    cosmology.set_hubble_parameter(hubble_parameter)
    cosmology.time = 0  # Init time

    for i in range(1, num_steps):
        scale_factors[i] = cosmology.evolve_scale_factor(scale_factors[i-1], dt)

    plt.figure(figsize=(10, 6))
    plt.plot(scale_factors)
    plt.xlabel('Passo de Tempo')
    plt.ylabel('Fator de Escala')
    plt.title('Simulação de Cosmologia Cíclica Unificada')
    plt.grid(True)
    plt.show()

    print(f"Simulação completa! a(final) = {scale_factors[-1]:.3f}")

if __name__ == "__main__":
    run_simulations()
