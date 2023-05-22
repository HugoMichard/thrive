import matplotlib.pyplot as plt
from plotter import AnimatedScatter
from entities.entity import Entity


class Simulator:
    def __init__(self, speed, fps) -> None:
        self.fps = fps
        self.speed = speed
        self.animals = Entity()

    def launch(self):
        self.animator = AnimatedScatter(self, numpoints=1, fps=self.fps)
        plt.show()

    def simulate(self):
        self.animals.move()
