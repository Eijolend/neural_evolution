import pygame as pg
from world import World
import sys

FPS = 30


pg.init()
clock = pg.time.Clock()


screen = pg.display.set_mode((900, 900))
world = World((30, 30), food_initial=(30, 20), food_growth=1 / FPS)

while True:
	for event in pg.event.get():
		if event.type == pg.QUIT: sys.exit()
	clock.tick(FPS)
	world.loop()
	world.draw(screen, pos=(0, 0), dim=(900, 900))
	pg.display.flip()
