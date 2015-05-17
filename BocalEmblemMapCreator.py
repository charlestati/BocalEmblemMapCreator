#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import random
import sys

ENV_MIN = 0
ENV_MAX = 10
EMPTY = 0
WALL = 1
BLUE_MIN = 11
BLUE_MAX = 40
RED_MIN = 41
RED_MAX = 70


class Map:
    def __init__(self, width=5, height=4):
        self.width = width
        self.height = height
        self.cells = [[0 for tmp in range(self.width + 1)] for tmp in range(self.height + 1)]
        self.generateEmptyMap()

    def generateEmptyMap(self):
        self.cells[0] = self.cells[-1] = [1 for tmp in range(self.width + 1)]
        for i in range(1, self.height + 1):
            self.cells[i][0] = self.cells[i][-1] = 1

    def fillEnvironment(self, density, characters):
        max_env_cells = (self.width - 1) * (self.height - 1) - characters
        env_cells = int(max_env_cells * (density / 100))
        env = [i for i in range(ENV_MAX + 1)]
        env.remove(WALL)
        for i in range(env_cells):
            x, y = self.getEmptyCell()
            self.modifyCell(x, y, random.choice(env))

    def fillCharacters(self, n, min, max):
        placed = []
        for i in range(n):
            x, y = self.getEmptyCell()
            id = random.randint(min, max)
            while (id in placed):
                id = random.randint(min, max)
            self.modifyCell(x, y, id)
            placed.append(id)

    def getEmptyCell(self):
        x = random.randint(1, self.width + 1)
        y = random.randint(1, self.height + 1)
        while (not self.cellIsEmpty(x, y)):
            x = random.randint(1, self.width + 1)
            y = random.randint(1, self.height + 1)
        return (x, y)

    def cellIsEmpty(self, x, y):
        if x not in range(self.width) or y not in range(self.height + 1):
            return False
        return self.cells[y][x] == EMPTY

    def modifyCell(self, x, y, value):
        self.cells[y][x] = value

    def echo(self):
        for i in range(self.height + 1):
            for j in range(self.width + 1):
                if j > 0:
                    print(' ', end='')
                print('{}'.format(self.cells[i][j]), end='')
            print('')

    def __str__(self):
        return '\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in self.cells])


def generate_map(width, height, blue, red, density):
    map = Map(width, height)
    map.fillEnvironment(density, blue + red)
    map.fillCharacters(blue, BLUE_MIN, BLUE_MAX)
    map.fillCharacters(red, RED_MIN, RED_MAX)
    return map


def main():
    parser = argparse.ArgumentParser(description='creates a map for a BocalEmblem game')
    parser.add_argument('-W', '--width', type=int, required=True, help='width of the map')
    parser.add_argument('-H', '--height', type=int, required=True, help='height of the map')
    parser.add_argument('--blue', type=int, default=1, help='number of blue units')
    parser.add_argument('--red', type=int, default=1, help='number of red units')
    parser.add_argument('--density', type=int, default=20, help='density of environment')
    parser.add_argument('--pretty', action='store_true', help='pretty print of the map')
    args = parser.parse_args()
    width = args.width
    height = args.height
    blue = args.blue
    red = args.red
    density = args.density
    pretty = args.pretty
    try:
        if width < 0:
            raise ValueError('width must be positive')
        if height < 0:
            raise ValueError('height must be positive')
        if blue < 1:
            raise ValueError('blue must be > 0')
        if blue > (BLUE_MAX - BLUE_MIN):
            raise ValueError('blue must be <= {}'.format(BLUE_MAX - BLUE_MIN))
        if red < 1:
            raise ValueError('red must be > 0')
        if red > (RED_MAX - RED_MIN):
            raise ValueError('red must be <= {}'.format(RED_MAX - RED_MIN))
        if red + blue > (width - 1) * (height - 1):
            raise ValueError('there are too many units')
        if density < 0:
            raise ValueError('density must be positive')
        if density > 100:
            raise ValueError('density must be <= 100')
    except ValueError as e:
        print(str(e))
        raise sys.exit()
    map = generate_map(width, height, blue, red, density)
    if pretty:
        print(map)
    else:
        map.echo()


if __name__ == '__main__':
    main()
