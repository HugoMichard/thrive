from simulator import Simulator
from entities.plants.plant import Plant

starting_entities = [
    {'cls': Plant, 'nb': 2}
]

if __name__ == '__main__':
    s = Simulator(map_size=500, fps=5, starting_entities=starting_entities)
    s.launch()
