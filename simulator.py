import matplotlib.pyplot as plt
from plotter import AnimatedScatter
from entities.entity import Entity
from entities.plants.plant import Plant
import numpy as np


class Simulator:
    def __init__(self, map_size, fps, starting_entities) -> None:
        self.fps = fps
        self.map_size = map_size
        self.max_map_value = map_size - map_size // 2
        self.entities = {}
        idx = 0
        for entity_cls in starting_entities:
            for _ in range(entity_cls['nb']):
                params = {'id': idx, 'x': np.random.randint(map_size - map_size // 2), 'y': np.random.randint(map_size - map_size // 2)}
                self.entities[idx] = entity_cls['cls'](self, params)
                idx += 1
        self.last_entity_id = idx

    def launch(self):
        self.animator = AnimatedScatter(self)
        plt.show()

    def simulate(self):
        entities_alive = []
        existing_entities = list(self.entities.values())
        for entity in existing_entities:
            entity.animate()
            if entity.is_dead:
                entity.color = 255.

    def get_entities_display(self):
        x = []
        y = []
        colors = []
        sizes = []
        detections = []
        visibilities = []
        for entity in self.entities.values():
            x.append(entity.x)
            y.append(entity.y)
            colors.append(entity.color)
            sizes.append(entity.size)
            detections.append(entity.detection_range)
            visibilities.append(entity.visibility_range)

        return x, y, colors, sizes, detections, visibilities

    def add_entity(self, entity):
        self.last_entity_id = entity.id
        self.entities[entity.id] = entity
