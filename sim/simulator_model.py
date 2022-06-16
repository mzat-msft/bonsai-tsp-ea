import datetime as dt

from sim.evolutionary_algo import EvolutionaryAlgo
from sim.travelling_salesman import TSP


class SimulatorModel:
    interface = {'name': 'TSP-EA-Solver', 'timeout': 120}

    def reset(self, config):
        self.tsp = TSP(config)
        return {
            'n_cities': self.tsp.n_cities,
            'score': 0.,
            'seconds_run': 0.,
        }

    def step(self, action):
        ea = EvolutionaryAlgo(**action)
        start = dt.datetime.now()
        score, _ = ea.solve(self.tsp)
        run_time = (dt.datetime.now() - start)
        return {
            'n_cities': self.tsp.n_cities,
            'score': score,
            'seconds_run': run_time.total_seconds()
        }
