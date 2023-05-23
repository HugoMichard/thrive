from simulator import Simulator
from entities.plants.plant import Plant

starting_entities = [
    {'cls': Plant, 'nb': 3}
]

if __name__ == '__main__':
    s = Simulator(map_size=2000, fps=100, starting_entities=starting_entities)
    s.launch()
