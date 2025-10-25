# cyclic_cosmology.py - Integração unificada
from friedmann_extended import friedmann_extended, H0_gyr  # Importa função (ajuste path se preciso)
from bounce_quantum import QuantumBounce
import numpy as np

class CyclicCosmology:
    def __init__(self):
        self.qb = QuantumBounce()
        self.hubble_param = H0_gyr
        self.scale_factor = 1.0
    
    def set_hubble_parameter(self, h):
        self.hubble_param = h
    
    def evolve_scale_factor(self, a_prev, dt=0.1):
        # Evolui simples: usa H médio + cyclic
        H = self.hubble_param * np.sqrt(1 / a_prev**3 + 0.7)  # Aprox FLRW
        cyclic_osc = 0.01 * np.sin(2 * np.pi * self.time / 13.8) if hasattr(self, 'time') else 0
        self.time += dt
        return a_prev * np.exp(H * dt + cyclic_osc)
