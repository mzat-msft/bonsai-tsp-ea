"""Evolutionary algorithm implementation for solving the TSP."""
import itertools
import operator
import random

from sim.travelling_salesman import TSP


def get_sample_from_cdf(u: float, cdf, scored_pop):
    if u <= cdf[0]:
        return scored_pop[0][0]
    else:
        prev_cum_score = cdf[0]
        for i, cum_score in enumerate(cdf):
            if prev_cum_score < u <= cum_score:
                return scored_pop[i][0]
            else:
                prev_cum_score = cum_score


def fitness_prop_sample(scored_pop, k: int):
    scores = [score for el, score in scored_pop]
    cdf = [cum_score / sum(scores) for cum_score in itertools.accumulate(scores)]

    samples = []
    for _ in range(k):
        u = random.random()
        samples.append(get_sample_from_cdf(u, cdf, scored_pop))
    return samples


def couple(parent1, parent2):
    a, b = (sorted(random.sample(range(len(parent2) + 1), 2)))
    children1 = (
        parent2[a:b]
        + [node for node in parent1[b:] if node not in parent2[a:b]]
        + [node for node in parent1[:b] if node not in parent2[a:b]]
    )
    children2 = (
        parent1[a:b]
        + [node for node in parent2[b:] if node not in parent1[a:b]]
        + [node for node in parent2[:b] if node not in parent1[a:b]]
    )
    return [children1, children2]


class EvolutionaryAlgo:
    def __init__(
        self,
        *,
        pop_size: int,
        generations: int,
        elite_size: int,
        mutation_rate: float,
    ):
        self.pop_size = int(pop_size)
        self.generations = int(generations)
        self.elite_size = int(elite_size)
        self.mutation_rate = mutation_rate

    def generate_init_pop(self, world):
        return [
            random.sample(world.cities.keys(), len(world))
            for _ in range(self.pop_size)
        ]

    def select_parents(self, pop, tsp):
        scored_pop = sorted(
            ((el, 1. / tsp.solve(el)) for el in pop),
            key=operator.itemgetter(1),
            reverse=True,
        )

        parents = [el for el, score in scored_pop[:self.elite_size]]
        parents.extend(fitness_prop_sample(scored_pop, self.pop_size - self.elite_size))
        return parents

    def breed(self, parents):
        children = parents[:self.elite_size]

        for parent1, parent2 in zip(parents, parents[1:]):
            children.extend(couple(parent1, parent2))
            if len(children) >= self.pop_size:
                break
        return children

    def mutate(self, pop):
        new_pop = list(pop)
        for path in new_pop[self.elite_size:]:
            n_mutations = int(len(path) * random.uniform(.5, 1.5) * self.mutation_rate)
            pairs = random.sample(
                set(itertools.permutations(range(len(path)), 2)), n_mutations
            )
            for a, b in pairs:
                path[a], path[b] = path[b], path[a]
        return new_pop

    @staticmethod
    def get_best_solution(pop, tsp: TSP):
        best_score = None
        best_path = None

        for path in pop:
            if best_score is None or tsp.solve(path) < best_score:
                best_score = tsp.solve(path)
                best_path = path
        return best_score, best_path

    def solve(self, tsp: TSP):
        pop = self.generate_init_pop(tsp.world)

        for _ in range(self.generations):
            parents = self.select_parents(pop, tsp)
            children = self.breed(parents)
            pop = self.mutate(children)
        return self.get_best_solution(pop, tsp)
