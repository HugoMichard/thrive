import math


class Circle:
    def __init__(self, x, y, r) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.area = self.compute_area()
    
    def check_if_overlaps(self, circle) -> bool:
        d = math.sqrt((self.x - circle.x)**2 + (self.y - circle.y)**2)
        return d <= self.r - circle.r or d <= circle.r - self.r or d <= self.r + circle.r

    def compute_area(self) -> float:
        return math.pi * (self.r**2)
