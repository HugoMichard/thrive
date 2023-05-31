import numpy as np
from entities.entity import Entity


class Plant(Entity):
    def __init__(self, simulator, params) -> None:
        super().__init__(simulator, params)
        self.reproduce_speed = 20
        self.expansion_distance = 10
        self.base_drink_speed = 12
        self.drink_speed = self.base_drink_speed
        self.color = "00ba32"

    def animate(self):
        super().animate()
        if not self.is_dead:
            self.drink()
            self.eat()
            self.reproduce()
    
    def grow(self):
        super().grow()
        self.size += 1
        self.max_water_reserve += 1
        self.max_health += 1

    def drink(self):
        total_drink_speed_of_plants_nearby = sum([e.get_alone_drink_speed() for e in self.overlapping_entities if isinstance(e, Plant)]) + self.get_alone_drink_speed()
        drinking_ratio = self.drink_speed / total_drink_speed_of_plants_nearby
        self.water_reserve = min(self.max_water_reserve, (drinking_ratio * self.get_alone_drink_speed()) + self.water_reserve)
        self.simulator.logger.add_log(f"{self.id}: Drink speed {drinking_ratio * self.get_alone_drink_speed()}")

    def get_alone_drink_speed(self):
        return self.position_circle.area * self.base_drink_speed

    def reproduce(self):
        if self.reproduce_timer == self.reproduce_speed:
            self.reproduce_timer = 0
            self.give_birth()
        else:
            self.reproduce_timer += 1

    def give_birth(self):
        max_expansion_distance = self.size + self.expansion_distance
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
