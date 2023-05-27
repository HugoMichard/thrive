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
        self.overlapping_entities = []

    def animate(self):
        if self.is_dead:
            self.dead_time += 1
            if self.corpse_decomposition_speed >= self.dead_time:
                del self.simulator.entities[self.id]
            return

        self.overlapping_entities = [e for e in self.simulator.entities.values() if self.check_if_overlaps_entity(e)]
        print("I'm overlapping with : ")
        print(self.overlapping_entities)
        self.fill_needs()
        self.grow()

    def check_if_overlaps_entity(self, entity):
        is_different = entity.id != self.id
        radius = self.size // 2
        other_radius = entity.size // 2
        x_overlaps = (self.x < entity.x and self.x + radius > entity.x - other_radius) or (self.x > entity.x and self.x - radius < entity.x + other_radius)
        y_overlaps = (self.y < entity.y and self.y + radius > entity.y - other_radius) or (self.y > entity.y and self.y - radius < entity.y + other_radius)
        return is_different and x_overlaps and y_overlaps

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
