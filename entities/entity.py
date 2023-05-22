class Entity:
    def __init__(self) -> None:
        self.x = 0.
        self.y = 0.
        self.size = 1.
        self.color = 0

    def move(self):
        self.x += 1 if self.x < 8 else -1
        self.y += 1 if self.y < 8 else -1
