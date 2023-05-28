from circle_helper import Circle


class Entity:
    def __init__(self, simulator, params) -> None:
        self.id = params['id']
        self.x = params['x']
        self.y = params['y']
        self.detection_range = 1.
        self.visibility_range = 1.
        self.size = 1.
        self.color = 0
        self.water_need = 10
        self.food_need = 10
        self.max_food_reserve = 100
        self.max_water_reserve = 100
        self.max_health = 100
        self.simulator = simulator
        self.is_dead = False
        self.food_reserve = self.max_food_reserve
        self.water_reserve = self.max_water_reserve
        self.health = self.max_health
        self.corpse_decomposition_speed = 10
        self.dead_time = 0
        self.drink_speed = self.water_need * 10
        self.eat_speed = self.water_need * 8
        # self.drink_speed = 1
        # self.eat_speed = 1
        self.age = 0
        self.position_circle = Circle(self.x, self.y, self.size)
        self.overlapping_entities = []

    def animate(self):
        if self.is_dead:
            self.dead_time += 1
            if self.corpse_decomposition_speed >= self.dead_time:
                del self.simulator.entities[self.id]
            return

        self.update_senses()

        self.overlapping_entities = [e for e in self.simulator.entities.values() if e.id != self.id and self.position_circle.check_if_overlaps(e.position_circle)]
        self.simulator.logger.add_log(f"I'm overlapping with : {[e.id for e in self.overlapping_entities]}")
        self.fill_needs()
        self.grow()

    def update_senses(self):
        self.position_circle = Circle(self.x, self.y, self.size)

    def move(self):
        pass

    def drink(self):
        self.water_reserve = min(self.max_water_reserve, self.drink_speed + self.water_reserve)

    def eat(self):
        self.food_reserve = min(self.max_food_reserve, self.eat_speed + self.food_reserve)

    def fill_needs(self):
        self.food_reserve -= self.food_need
        self.water_reserve -= self.water_need
        if self.food_reserve < 0:
            self.health += self.food_reserve
        if self.water_reserve < 0:
            self.health += self.water_reserve

        if self.health < 0:
            self.is_dead = True

    def grow(self):
        self.age += 1
