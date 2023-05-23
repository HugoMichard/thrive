import numpy as np
from entities.entity import Entity


class Plant(Entity):
    def __init__(self, simulator, params) -> None:
        super().__init__(simulator, params)
        self.drink_speed = 1
        self.eat_speed = 1
        self.reproduce_speed = 5
        self.reproduce_timer = 0
        self.max_expansion_distance = 10

    def animate(self):
        super().animate()
        self.drink()
        self.eat()
        self.reproduce()
    
    def grow(self):
        super().grow()
        self.size += 1
        self.max_food_reserve += 1
        self.max_water_reserve += 1
        self.max_health += 1
    
    def reproduce(self):
        if self.reproduce_timer == self.reproduce_speed:
            self.reproduce_timer = 0
            self.give_birth()
        else:
            self.reproduce_timer += 1

    def give_birth(self):
        params = {
            'id': self.simulator.last_entity_id + 1,
            'x': self.x + np.random.randint(self.max_expansion_distance),
            'y': self.y + np.random.randint(self.max_expansion_distance)
        }
        self.simulator.add_entity(Plant(self.simulator, params))
