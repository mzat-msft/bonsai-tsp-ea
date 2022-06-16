import pytest

from sim import travelling_salesman

andermatt = travelling_salesman.City('andermatt', 0., 1.)
barcelona = travelling_salesman.City('barcelona', 0., 0.)
como = travelling_salesman.City('como', 1., 0.)
dijon = travelling_salesman.City('dijon', 1., 1.)

world = travelling_salesman.World([andermatt, barcelona, como, dijon])

pairs = [
    ((andermatt, barcelona), 1.),
    ((andermatt, como), 2.**0.5),
    ((andermatt, dijon), 1.),
    ((barcelona, dijon), 2.0**0.5),
]


@pytest.mark.parametrize("pair, distance", pairs)
def test_distance(pair, distance):
    assert pair[0].dist(pair[1]) == distance


def test_distance_fail():
    with pytest.raises(ValueError):
        travelling_salesman.City('', 0., 0.).dist(10)


routes = [
    ((andermatt, barcelona, dijon), 2. + 2.0**0.5),
    ((andermatt, barcelona), 2.),
    (('andermatt', 'barcelona'), 2.),
]


@pytest.mark.parametrize("route, length", routes)
def test_length(route, length):
    try:
        assert travelling_salesman.Route(route).length == length
    except ValueError:
        assert travelling_salesman.Route(route, world).length == length


def test_route_fail():
    with pytest.raises(ValueError):
        travelling_salesman.Route((andermatt, barcelona, andermatt))


tsp_solutions = [
    (world, ['andermatt', 'barcelona', 'como', 'dijon'], 4.0),
    (world, [andermatt, barcelona, como, dijon], 4.0),
]


@pytest.mark.parametrize("world, route, length", tsp_solutions)
def test_tsp(world, route, length):
    problem = travelling_salesman.TSP({"world": world})
    assert problem.solve(route) == length


def test_tsp_fail():
    with pytest.raises(ValueError):
        travelling_salesman.TSP({"world": world}).solve([andermatt])
