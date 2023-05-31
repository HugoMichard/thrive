from typing import Dict
import csv
import time
from entities.entity import Entity
from logger import Logger
import numpy as np


class Simulator:
    def __init__(self, map_size, fps, starting_entities) -> None:
        with open("/home/hugo/Projects/thrive/frames.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['frame', 'id', 'x', 'y', 'color', 'size'])

        with open("/home/hugo/Projects/thrive/logs.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(['frame', 'log'])

        self.logger = Logger()
        self.fps = fps
        self.frame = 0
        self.map_size = map_size
        self.max_map_value = map_size - map_size // 2
        self.entities: Dict[str, Entity] = {}
        idx = 0
        for entity_cls in starting_entities:
            for _ in range(entity_cls['nb']):
                params = {'id': idx, 'x': np.random.randint(map_size - map_size // 2), 'y': np.random.randint(map_size - map_size // 2)}
                self.entities[idx] = entity_cls['cls'](self, params)
                idx += 1
        self.last_entity_id = idx

    def launch(self):
        while True:
            self.logger.reset_logs()
            print(f'Simulating frame {self.frame}')
            self.simulate()

            with open("/home/hugo/Projects/thrive/frames.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows([[self.frame, entity.id, entity.x, entity.y, entity.color, entity.size] for entity in self.entities.values()])

            with open("/home/hugo/Projects/thrive/logs.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerows(self.logger.format_rows_for_frame(self.frame))

            self.frame += 1
            time.sleep(1 / self.fps)

    def simulate(self):
        entities_alive = []
        existing_entities = list(self.entities.values())
        for entity in existing_entities:
            entity.animate()
            if entity.is_dead:
                entity.color = '000000'

    def add_entity(self, entity):
        self.last_entity_id = entity.id
        self.entities[entity.id] = entity
