"""
This module implements a web server for the final deployment of the solution.

This example just provides one route that takes a list of cities and provides
the shortest path connecting them as found by an evolutionary algorithm.
The hyperparameters used by the evolutionary algorithm are chosen by a Bonsai brain.

In order to work the bonsai brain must be accessible at the URL and port defined
in the BRAIN_HOST and BRAIN_PORT environment variables.
"""
import os
import random
import string

import requests
from aiohttp import web

from sim.evolutionary_algo import EvolutionaryAlgo
from sim.travelling_salesman import TSP, World

CONFIG = {
    'brain_host': os.getenv('BRAIN_HOST', '127.0.0.1'),
    'brain_port': os.getenv('BRAIN_PORT', '5000'),
}


async def predict(request):
    """
    Find the best route for given list of cities.

    The cities are posted as a json. Their number is used as a
    state for the brain. The brain provides the best hyperparameters
    for the evolutionary algorithm.
    The best route is returned by the server.
    """

    client_id = ''.join(
        random.choices(string.ascii_letters + string.digits, k=10)
    )
    cities = await request.json()
    world = World.load_from_json(cities)

    state = {"n_cities": len(world)}
    payload = {'state': state}
    base_url = f'http://{CONFIG["brain_host"]}:{CONFIG["brain_port"]}'
    response = requests.post(
        f'{base_url}/v2/clients/{client_id}/predict', json=payload
    )

    tsp = TSP({'world': world})
    hyperparams = response.json()["concepts"]["TuneHyperparams"]["action"]
    ea = EvolutionaryAlgo(**hyperparams)
    score, route = ea.solve(tsp)

    return web.json_response(
        {
            'best_route': route,
            'best_score': score,
        }
    )


def make_app():
    app = web.Application()
    app.add_routes([web.post('/predict', predict)])
    return app


def run_server():
    web.run_app(make_app())
