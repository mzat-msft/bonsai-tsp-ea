import pytest

import sim.evolutionary_algo as ea

pop_cdf_res = [
    ([('A', 0.2), ('B', 0.1)], [0.2/0.3, 1.], .8, 'B'),
    ([('A', 0.2), ('B', 0.1)], [0.2/0.3, 1.], 1., 'B'),
    ([('A', 0.2), ('B', 0.1)], [0.2/0.3, 1.], .2/.3, 'A'),
    ([('A', 0.2), ('B', 0.1)], [0.2/0.3, 1.], .2, 'A'),
    ([('A', 0.2), ('B', 0.1)], [0.2/0.3, 1.], 0., 'A'),
]


@pytest.mark.parametrize("scored_pop, cdf, u, result", pop_cdf_res)
def test_get_sample_from_cdf(scored_pop, cdf, u, result):
    assert ea.get_sample_from_cdf(u, cdf, scored_pop) == result


parents_children = [
    (
        (['A', 'B', 'C', 'D'], ['C', 'B', 'A', 'D']),
        [['B', 'A', 'D', 'C'], ['B', 'C', 'D', 'A']],
        [1, 3],
    ),
    (
        (['A', 'B', 'C', 'D'], ['C', 'B', 'A', 'D']),
        [['C', 'B', 'A', 'D'], ['A', 'B', 'C', 'D']],
        [0, 3],
    ),
    (
        (['A', 'B', 'C', 'D'], ['C', 'B', 'A', 'D']),
        [['C', 'B', 'D', 'A'], ['A', 'B', 'D', 'C']],
        [0, 2],
    ),
    (
        (['A', 'B', 'C', 'D'], ['C', 'B', 'A', 'D']),
        [['A', 'D', 'B', 'C'], ['C', 'D', 'B', 'A']],
        [2, 4],
    ),
    (
        (['A', 'B', 'C', 'D'], ['C', 'B', 'A', 'D']),
        [['C', 'B', 'A', 'D'], ['A', 'B', 'C', 'D']],
        [0, 4],
    ),
]


@pytest.mark.parametrize("parents, children, indices", parents_children)
def test_couple(parents, children, indices, mocker):
    mocker.patch('random.sample', return_value=indices)
    assert ea.couple(*parents) == children


mutants = [
    ([[0, 1, 2, 3]], 1, [(1, 3)], [[0, 3, 2, 1]]),
]


@pytest.mark.parametrize("pop, n_mut, pairs, res", mutants)
def test_mutate(pop, n_mut, pairs, res, mocker):
    mocker.patch('random.sample', return_value=pairs)
    mocker.patch('random.uniform', return_value=n_mut)
    evo = ea.EvolutionaryAlgo(
        pop_size=1,
        generations=1,
        elite_size=0,
        mutation_rate=0.25
    )
    assert evo.mutate(pop) == res
