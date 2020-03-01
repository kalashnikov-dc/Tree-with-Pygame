#!/usr/bin/python
# _*_ coding: utf-8 _*_

import pygame, sys
from pygame.color import Color
from random import choice, randint
from itertools import cycle
from msg import color_my_message


FPS = 30
TITLE = 'Tree'
BACKGROUND = 25, 25, 30
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption(TITLE)
CLOCK = pygame.time.Clock()
pygame.init()

# SET TIMES
pygame.time.set_timer(1, 50) # TEMPO DE CRESCIMENTO DA RAMIFICACAO


class Branch(): #Configuracoes do primeiro galho
    pos_inicial = [WIDTH/2, 500+17]
    x, y = WIDTH/2, 500+17
    width = 10
    direction = 'up'
    color = (200,200, 200)
    have_children = False
    score_x, score_y = 0, 0
    goal_x, goal_y = 0, 70

class Fruit():
    pos = 0, 0
    color = Color('Black')
    size = 3

class Tree():
    generation_limit = 1000
    generations = 0
    branchers = [Branch()]
    directions = cycle(['up', 'up_left', 'up_right'])
    branch_color = (200,200, 200)
    amount_of_new_branches = 2
    min_x, max_x = 10, 40
    min_y, max_y = 10, 40
    fruits = []
    fruit_colors = [(0, 0, 0)]
    fruit_size = 3
    possibility_to_bear_fruit = 1
    add_fruits_in_generation = 100
    
    def draw_tree(self):
        for branch in self.branchers:
            pygame.draw.line(SCREEN, branch.color,
                             branch.pos_inicial,
                             [branch.x, branch.y],
                             branch.width)
    
    def draw_fruits(self):
        for fruit in self.fruits:
            pygame.draw.circle(SCREEN, fruit.color,
                               fruit.pos, fruit.size)

    def events(self, event):
        if event.type == 1:
            self.check()
         
    def check(self):

        for branch in self.branchers:
            if branch.score_x == branch.goal_x \
            and branch.score_y == branch.goal_y:

                if branch.have_children == False:
                    self.change_attributes()
                    self.add_branchers(branch)
                    self.add_fruit(branch)

            else:

                if self.generations < self.generation_limit:
                    self.grow_X(branch)
                    self.grow_Y(branch)

    def grow_X(self, branch):
        if branch.goal_x != branch.score_x:
            if branch.direction == 'up_right' \
            or branch.direction == 'right':

                branch.x += 1

            elif branch.direction == 'up_left' \
            or branch.direction == 'left':

                branch.x -= 1
                    
            branch.score_x += 1


    def grow_Y(self, branch):
        if branch.goal_y != branch.score_y:
            if branch.direction == 'up_left' \
            or branch.direction == 'up_right' \
            or branch.direction == 'up':

                branch.y -= 1

            elif branch.direction == 'down_left' \
            or branch.direction == 'down_right':

                branch.y += 1

            branch.score_y += 1

    def change_attributes(self): 
        if self.generations == 0:
            self.amount_of_new_branches = 3
            self.directions = cycle(['up_left','up','up_right'])
            self.min_x, self.max_x = 40, 50
            self.min_y, self.max_y = 40, 80
            
        else:
            self.amount_of_new_branches = 2
            self.directions = cycle(['up_right', 'up_left'])
            self.min_x, self.max_x = 30, 60
            self.min_y, self.max_y = 20, 50


    def add_branchers(self, branch_father):


        for i in range(self.amount_of_new_branches):
            x, y = branch_father.x, branch_father.y
            new_branch = Branch()
            new_branch.direction = next(self.directions)
            new_branch.x, new_branch.y = x, y
            new_branch.pos_inicial = [x, y]
            new_branch.color =  self.branch_color
            new_branch.goal_x = randint(self.min_x, self.max_x)
            new_branch.goal_y = randint(self.min_y, self.max_y)

            if branch_father.width == 1:
                new_branch.width = 1
            else:
                new_branch.width = branch_father.width-1

            self.branchers.append(new_branch)
           
        branch_father.have_children = True

        self.branch_color = branch_father.color[0]-1, branch_father.color[1]-10, branch_father.color[2]-1

        self.generations += 1

    

        message = '[Branchers]: '+str(len(self.branchers))+' (Generations): '+str(self.generations)+' {Fruits}: '+str(len(self.fruits))


    def add_fruit(self, branch_father):
        value = randint(1, self.possibility_to_bear_fruit) 
        if value == 1 and self.generations > self.add_fruits_in_generation:
            new_fruit = Fruit()
            new_fruit.pos = branch_father.x, branch_father.y
            new_fruit.size = self.fruit_size

            new_fruit.color = choice(self.fruit_colors)

            self.fruits.append(new_fruit)



tree = Tree()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        tree.events(event)

    SCREEN.fill(BACKGROUND)
    tree.draw_tree()
    tree.draw_fruits()
    CLOCK.tick(FPS)
    pygame.display.update()


#if __name__ == '__main__':
#    Main()
