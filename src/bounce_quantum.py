# bounce_quantum.py
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class QuantumBounce:
    def __init__(self, G=6.67430e-11, hbar=1.0545718e-34, rho_crit=8.62e-27):
        self.G = G
        self.hbar = hbar
        self.rho_crit = rho_crit
        self.scale_factor = 1.0
        self.hubble_param = 2.3e-18  # H0 em s^-1 approx
        
    def friedmann_equation(self, rho):
        """H² = (8πG/3) ρ"""
        return np.sqrt(8 * np.pi * self.G * rho / 3)
    
    def quantum_pressure(self, rho):
        return (self.hbar**2) / (2 * self.G * rho)  # Corrigido: / rho no denom
    
    def bounce_condition(self, rho_before, rho_after):
        return rho_before > self.rho_crit and rho_after < rho_before  # Bounce se ρ max e decresce
    
    def solve_cosmological_evolution(self, rho_init, t_span, t_eval):
        def equations(t, y):
            a, H = y
            rho = rho_init * (self.scale_factor / a)**3  # Diluição matéria
            H_calc = self.friedmann_equation(rho)
            
            # Bounce: se ρ > ρ_crit, H = -H (contração → expansão)
            if rho > self.rho_crit:
                H = -abs(H_calc)  # Simples bounce
            else:
                H = H_calc
            
            # dH/dt ≈ - (3/2) H² (1 + w) pra w=0
            dH_dt = -1.5 * H**2
            da_dt = H * a  # Mas estado é [a, H], então dadt não é derivada direta
            return [H * a, dH_dt]  # Estado [a, H]: da/dt = H a, dH/dt
        
        sol = solve_ivp(equations, t_span, [self.scale_factor, self.hubble_param], 
                        t_eval=t_eval, method='RK45')
        
        return {'t': sol.t, 'a': sol.y[0], 'H': sol.y[1]}
    
    def plot_scale_factor(self, solution):
        plt.figure(figsize=(10, 6))
        plt.plot(solution['t'], solution['a'], label='Fator de Escala')
        plt.xlabel('Tempo (s)')
        plt.ylabel('Fator de Escala (a)')
        plt.title('Evolução com Bounce Quântico')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def analyze_quantum_effects(self, rho_values):
        results = {}
        for rho in rho_values:
            pressure = self.quantum_pressure(rho)
            quantum_param = pressure / (rho * self.G) if rho > 0 else 0  # Normalizado
            regime = 'quantum' if quantum_param > 0.01 else 'classical'  # Threshold menor
            results[rho] = {'quantum_pressure': pressure, 'quantum_parameter': quantum_param, 'regime': regime}
        return results

# Exemplo
if __name__ == "__main__":
    qb = QuantumBounce()
    rho_init = 1e-26  # Perto de ρ_crit
    t_span = (0, 1e17)  # ~3 Gyr em s
    t_eval = np.linspace(0, 1e17, 1000)
    
    solution = qb.solve_cosmological_evolution(rho_init, t_span, t_eval)
    qb.plot_scale_factor(solution)
    
    rho_test = np.logspace(-28, -25, 5)
    quantum_analysis = qb.analyze_quantum_effects(rho_test)
    print("Análise Quântica:")
    for rho, data in quantum_analysis.items():
        print(f"Densidade: {rho:.2e}, Regime: {data['regime']}")
    
    rho_before = 1e-26
    rho_after = 1e-27
    bounce = qb.bounce_condition(rho_before, rho_after)
    print(f"Bounce ativado: {bounce}")
