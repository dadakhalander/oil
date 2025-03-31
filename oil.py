import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class SimulationParams:
    initial_investment: float = 20.0  # million dollars
    drilling_cost: float = 10.0  # million dollars per well
    expected_oil_price: float = 70.0  # dollars per barrel
    success_probability: float = 0.60  # 60% chance of success
    production_volume: float = 1.0  # million barrels per successful well
    price_fluctuation: float = 0.05  # 5% annual fluctuation

class OilExplorationSimulation:
    def __init__(self, params: SimulationParams = SimulationParams(), num_simulations: int = 10000):
        self.params = params
        self.num_simulations = num_simulations
        self.results = []

    def simulate_success(self) -> bool:
        return np.random.random() < self.params.success_probability

    def simulate_oil_price(self) -> float:
        # Simulate oil price with normal distribution around expected price
        fluctuation = self.params.expected_oil_price * self.params.price_fluctuation
        return np.random.normal(self.params.expected_oil_price, fluctuation)

    def calculate_npv(self, success: bool, oil_price: float, discount_rate: float = 0.1) -> float:
        if not success:
            return -self.params.initial_investment
        
        revenue = oil_price * self.params.production_volume
        total_cost = self.params.initial_investment + self.params.drilling_cost
        cash_flow = revenue - total_cost
        
        # Simple NPV calculation assuming single period
        npv = cash_flow / (1 + discount_rate)
        return npv

    def run_simulation(self) -> Tuple[List[float], dict]:
        npv_results = []
        
        for _ in range(self.num_simulations):
            success = self.simulate_success()
            oil_price = self.simulate_oil_price()
            npv = self.calculate_npv(success, oil_price)
            npv_results.append(npv)

        statistics = {
            'mean_npv': np.mean(npv_results),
            'std_npv': np.std(npv_results),
            'min_npv': np.min(npv_results),
            'max_npv': np.max(npv_results),
            'probability_positive_npv': np.mean([npv > 0 for npv in npv_results])
        }

        return npv_results, statistics

    def run_analysis(self) -> dict:
        npv_results, stats = self.run_simulation()
        return stats

if __name__ == '__main__':
    # Run a sample simulation
    simulation = OilExplorationSimulation()
    results = simulation.run_analysis()
    
    print("\nMonte Carlo Simulation Results:")
    print(f"Mean NPV: ${results['mean_npv']:.2f} million")
    print(f"Standard Deviation: ${results['std_npv']:.2f} million")
    print(f"Minimum NPV: ${results['min_npv']:.2f} million")
    print(f"Maximum NPV: ${results['max_npv']:.2f} million")
    print(f"Probability of Positive NPV: {results['probability_positive_npv']*100:.1f}%")
