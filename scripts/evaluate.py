import datetime as dt
import json
from pathlib import Path

import requests


SOLVER_HOST = '127.0.0.1'
SOLVER_PORT = '8000'
base_url = f'http://{SOLVER_HOST}:{SOLVER_PORT}'

DATA_FOLDER = 'data'


def load_world(tsp_file):
    nodes = {}
    with open(tsp_file) as fp:
        for line in fp:
            line_split = line.split()
            try:
                if not line_split[0].isdigit():
                    continue
            except IndexError:
                continue
            line_split[1] = float(line_split[1])
            line_split[2] = float(line_split[2])
            nodes[line_split[0]] = [line_split[1], line_split[2]]
    return nodes


print('name', 'length', 'seconds')
for tsp in Path(DATA_FOLDER).glob('*.tsp'):
    nodes = load_world(tsp)
    start = dt.datetime.now()
    response = requests.post(f'{base_url}/predict', json.dumps(nodes))
    seconds = (dt.datetime.now() - start).total_seconds()
    print(tsp.stem, round(response.json()['best_score'], 2), seconds)
