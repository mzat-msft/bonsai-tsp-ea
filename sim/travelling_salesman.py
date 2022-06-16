"""
Implementation of the Travelling Salesman Problem.

Cities are located on a plane.
"""
import dataclasses
import random
import string
from typing import Any, Dict, Sequence, Union

WORLD_LIM_X = 200
WORLD_LIM_Y = 200


@dataclasses.dataclass
class City:
    """Class that represent a city with name and 2D coordinates."""

    name: str
    x: float
    y: float

    def __eq__(self, other):
        return (
            self.name == self.name
            and self.x == self.x
            and self.y == self.y
        )

    def __hash__(self):
        return hash((self.x, self.y))

    def dist(self, other):
        """Get the distance between two cities on a plane."""
        if not isinstance(other, City):
            raise ValueError("Distance can only be computed between cities.")
        return ((self.x - other.x)**2 + (self.y - other.y)**2)**0.5


class World:
    """A world is a set of cities."""

    def __init__(self, cities: Sequence[City]):
        self.cities = {city.name: city for city in cities}

        if len(cities) != len(self.cities):
            raise ValueError('Some cities are missing. Check for duplicate names.')

    def __len__(self):
        return len(self.cities)

    @classmethod
    def load_from_tsp(cls, tsp_file):
        """Load a World class from a TSP file."""
        nodes = []
        with open(tsp_file, 'r') as fp:
            for line in fp:
                line_split = line.split()
                try:
                    if not line_split[0].isdigit():
                        continue
                except IndexError:
                    continue
                line_split[1] = float(line_split[1])
                line_split[2] = float(line_split[2])
                nodes.append(City(*line_split))
        return World(nodes)

    @classmethod
    def load_from_json(cls, data):
        """
        Load a World class from a dictionary object.

        The dictionary has the city name as keys and the coordinates as values.
        """
        nodes = []
        for city, coords in data.items():
            nodes.append(City(city, *coords))
        return World(nodes)


class Route:
    """
    Class that implements a solution to the problem.

    The solution can come in the form of a list of City or as a list of str.
    If a list of str is given, a World object must be provided.

    The solution requires the salesman to visit a city maximum one time.
    It also assumes that the salesman ends the route at the first city, so
    there is no need to provide that at the last step.
    """
    def __init__(self, cities: Sequence[Union[str, City]], world: World = None):
        path = []
        for city in cities:
            if isinstance(city, City):
                path.append(city)
            elif isinstance(city, str):
                if not isinstance(world, World):
                    raise ValueError(
                        'world must be provided when cities are a list of str.'
                    )
                path.append(world.cities[city])
            else:
                raise TypeError('cities must be of type City or str.')

        if not len(set(cities)) == len(path):
            raise ValueError("Invalid route: cities must be visited max one time.")

        self.path = path

    def __len__(self):
        return len(self.path)

    @property
    def length(self) -> float:
        """Return the length of the route."""
        length = 0.
        for a, b in zip(self.path, self.path[1:] + [self.path[0]]):
            length += a.dist(b)
        return length


class TSP:
    def __init__(self, config: Dict[str, Any]):
        self.world = self.generate_world(config)

    @staticmethod
    def generate_world(config) -> World:
        """
        Generate a World class from a given config.

        If config contains a ``world`` key with value of type World, that World
        is used as is.  If config contains a ``world`` key with value a string,
        that string is used to load a world configuration available in the data
        folder.  Otherwise, ``n_cities`` with an integer value must be provided
        to generate a random world.
        """
        if isinstance(config.get('world'), World):
            return config.get('world')
        elif config.get('world') == 'burma14':
            return World.load_from_tsp('data/burma14.tsp')

        n_cities = config.get('n_cities', 100)
        chars = string.ascii_uppercase + string.digits
        return World(
            [
                City(
                    ''.join(random.choice(chars) for _ in range(6)),
                    WORLD_LIM_X * random.random(),
                    WORLD_LIM_Y * random.random(),
                )
                for i in range(n_cities)
            ]
        )

    @property
    def n_cities(self):
        return len(self.world)

    def parse_route(self, route):
        """Parse ``route`` in order to get a ``Route`` object."""
        if isinstance(route, Route):
            return route
        elif isinstance(route, list):
            return Route(route, world=self.world)
        raise TypeError(f'Unrecognized type for route: {type(route)}')

    def solve(self, route):
        """Return the the length of a route going through cities in the ``World``."""
        route = self.parse_route(route)
        if len(route) != len(self.world):
            raise ValueError('route should visit all cities.')
        return route.length
