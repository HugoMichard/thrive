import numpy as np
from entities.entity import Entity


class Plant(Entity):
    def __init__(self, simulator, params) -> None:
        super().__init__(simulator, params)
        self.reproduce_speed = 20
        self.expansion_distance = 10
        self.drink_speed = 1.5
        self.color = "00ba32"

    def animate(self):
        super().animate()
        self.drink()
        self.eat()
        self.reproduce()
    
    def grow(self):
        super().grow()
        self.size += 1
        self.max_water_reserve += 1
        self.max_health += 1

    def drink(self):
        nb_plants_nearby = len([e for e in self.overlapping_entities if isinstance(e, Plant)])
        drink_speed = max(self.drink_speed - nb_plants_nearby, 0)
        self.water_reserve = min(self.max_water_reserve, (drink_speed * self.water_need) + self.water_reserve)
        self.simulator.logger.add_log(f"{self.id}: Water at {self.water_reserve}")

    def reproduce(self):
        if self.reproduce_timer == self.reproduce_speed:
            self.reproduce_timer = 0
            self.give_birth()
        else:
            self.reproduce_timer += 1

    def give_birth(self):
        max_expansion_distance = self.size // 2 + self.expansion_distance
        random_x = np.random.randint(max_expansion_distance) - (max_expansion_distance / 2)
        random_y = np.random.randint(max_expansion_distance) - (max_expansion_distance / 2)
        birth_x = self.x + random_x
        birth_y = self.y + random_y
        birth_x = min(max(0, birth_x), self.simulator.max_map_value)
        birth_y = min(max(0, birth_y), self.simulator.max_map_value)
        params = {
            'id': self.simulator.last_entity_id + 1,
            'x': birth_x,
            'y': birth_y
        }
        self.simulator.add_entity(Plant(self.simulator, params))
