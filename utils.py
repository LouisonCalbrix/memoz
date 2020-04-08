#! /usr/bin/env python3

'''
Tools to be used by the memoz game that are not directly related to the game
logic.
date: March 2020
'''

import pygame
from copy import copy
from collections.abc import MutableMapping
from collections import namedtuple
from abc import ABC, abstractmethod


#class Singleton(type):
#    '''
#    Singleton metaclass. A Singleton class's only instance can be accessed
#    by name_of_class.INSTANCE
#    '''
#    def __init__(self, *args, **kwargs):
#        self.INSTANCE = None
#        super().__init__(*args, **kwargs)
#
#    def __call__(self, *args, **kwargs):
#        if self.INSTANCE is None:
#            self.INSTANCE = super().__call__(*args, **kwargs)
#        return self.INSTANCE


class Stage(MutableMapping):
    '''
    Top level object that manages Scenes and call their update method.
    '''

    def __init__(self, fps):
        '''
        A Stage needs a Scene as early as instanciation, therefore it expects
        keyword arguments to instanciate TextScene. 
        '''
        # pygame init
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))      # placeholder size
        self._clock = pygame.time.Clock()
        self._fps = fps

        # scenes initialization
        self._scenes = {}
        self._target = 'main menu'
        self._active = True
        type(self).INSTANCE = self

    def play(self):
        '''
        The real main loop of the program, its body changes as the Scene being
        played is changed.
        '''
        while self._active:
            inputs = pygame.event.get()
            scene_inputs = []
            for an_input in inputs:
                if an_input.type == pygame.QUIT:
                    self._active = False
                else:
                    scene_inputs.append(an_input)
            self.current_scene.update(scene_inputs)
            pygame.display.update()
            self._clock.tick(self._fps)
        self.quit()

    def quit(self):
        '''
        This method is called when the Stage is no longer active and the program
        is closing. Re implement this method to get custom behavior when closing
        your program like for instance saving user data.
        '''
        pygame.quit()

    def nav_link(self, target):
        '''
        Return a function that changes the target of the Stage.
        '''
        def link():
            self.target = target
        return link

    @property
    def main_menu(self):
        '''
        Return the main menu Scene which is the entry point of the program.
        '''
        return self._scenes['main menu']

    @property
    def target(self):
        '''
        Name of the Scene being played.
        '''
        return self._target

    @target.setter
    def target(self, value):
        if value == 'quit':
            print('quitting...')
            self._active = False
            return
        elif value not in self:
            raise KeyError('non existing scene')
        self._target = value

    @property
    def current_scene(self):
        '''
        Scene being played.
        '''
        return self._scenes[self.target]

    # ----Implementation of MutableMapping interface

    def __getitem__(self, key):
        return self._scenes[key]

    def __setitem__(self, key, scene):
        if not isinstance(scene, Scene):
            raise TypeError('Only instances of subclasses of Scene are accepted')
        self._scenes[key] = scene

    def __delitem__(self, key):
        del self._scenes[key]

    def __len__(self):
        return len(self._scenes)

    def __iter__(self):
        yield from self._scenes

    # ----

    def __str__(self):
        return '\n'.join((self.current_scene, *self._scenes))


class Scene(ABC):
    '''
    Interface for a logical unit to be displayed on the screen.
    A Scene -meant to be contained by an instance of a top level class Stage-
    provides, via its update method, the body of the main loop of a program.
    Any subclass of Scene needs to implement the following two methods:
        - treat_event is the method that treats every single input passed by top level Stage instance.
        - draw is the method used to display the Scene onscreen
    '''

    def __init__(self, screen):
        '''
        Meant to be called by any subclass. This assign a _screen attribute to
        the instance of the subclass.
        '''
        self._screen = screen

    def update(self, inputs):
        '''
        Method to be called repeatedly by the managing Stage instance. It will
        temporarily constitute the body of the program's main loop.
        '''
        self.handle_inputs(inputs)
        self.draw()

    @abstractmethod
    def handle_inputs(self, inputs):
        '''
        Method that needs to be implemented by subclasses to define how they handle
        user events. It is supposed to treat a list of inputs, i.e. its parameter 
        inputs is a list of all the pygame events except pygame.QUIT.
        '''
        pass

    @abstractmethod
    def draw(self):
        '''
        Method that needs to be implemented by subclasses to define how they are
        drawn onscreen.
        '''
        pass


class Button:
    '''
    Graphic element that triggers an action when it's clicked.
    '''
    def __init__(self, img, area, action):
        '''
        Parameters expected:  
            img: a pygame Surface that will be displayed onscreen to represent the
                 button
            pos: the coordinates (x, y) where the top-left corner of the button 
                 will be set onscreen
            area: the area where a click will trigger the button's action
            action: the piece of code to execute when the button is clicked
        '''
        self._img = copy(img)
        self._area = area
        self._action = action

    def click(self):
        '''
        Method to be called when the Button is clicked.
        '''
        self._action()

    @property
    def area(self):
        return self._area

    @property
    def img(self):
        return self._img

    @classmethod
    def fromstring(cls, button_string, action, fontfile=None, size_px=16,
                   bg_color=(0, 0, 0), size=None):
        '''
        Create a Button from a string. This Button will just be the piece of text
        button_string, written using font set to size_px.
        '''
        typeface = pygame.font.Font(fontfile, size_px)
        font_surface = typeface.render(button_string, True, (255, 255, 255))
        offset = (0, 0)
        if size is None:
            img = pygame.Surface(font_surface.get_size())
        else:
            img = pygame.Surface(size)
            offset = tuple((img_dim-ft_dim)//2 for ft_dim, img_dim in zip(font_surface.get_size(), size))
        img.fill(bg_color)
        img.blit(font_surface, offset)
        area = img.get_size()
        return cls(img, area, action)


# DEMOS

def button_demo():
    '''
    Meant to test the Button class. To run this demo do the following:
        1 import this script in your python shell:
          from utils import *
        2 call this function:
          button_demo()
    '''
    def zizou():
        print('oooh zizou')
    button = Button.fromstring('C L I C K', action=zizou, size=(100, 15), bg_color=(40, 200, 40)) 
    zone = pygame.Rect((100, 300), button.area)

    screen = pygame.display.set_mode((700, 700))
    screen.fill((0, 0, 255))
    screen.blit(button.img, zone)
    pygame.display.flip()

    going = True
    while going:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if zone.collidepoint(*pos):
                    button.click()
    pygame.quit()

def stage_demo():
    '''
    Meant to test the Stage and TestMenu classes. To run this demo, 
    do the following:
        1 import this script in your python shell:
          from utils import *
        2 call this function:
          stage_demo()
        3 click on the buttons to go from one scene to another
    '''


    class TestMenu(Scene):
        '''
        Example of how to subclass Scene.
        '''
        FixedButton = namedtuple('FixedButton', 'zone button')

        def __init__(self, screen, img=None):
            # call to __init__ method from superclass Scene
            super().__init__(screen)

            # custom things done by this particular class
            # graphics
            if img == None:
                self._img = pygame.Surface((700, 700))
                self._img.fill((0, 255, 80))
            else:
                self._img = copy(img)
            self._widgets_img = pygame.Surface((700, 700))
            self._widgets_img.set_colorkey((0, 255, 0))
            self._widgets_img.fill((0, 255, 0))
            self._buttons = list()

        # Implementation of mandatory Scene methods

        def handle_inputs(self, inputs):
            for an_input in inputs:
                if an_input.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for zone, button in self._buttons:
                        if zone.collidepoint(*pos):
                            button.click()

        def draw(self):
            '''
            Draw the Scene onscreen
            '''
            self._screen.blit(self._img, (0, 0))
            self._screen.blit(self._widgets_img, (0, 0))

        # Added functionnality

        def add_button_at(self, button, pos):
            '''
            Add a Button to the Scene.
            '''
            if not isinstance(button, Button):
                raise TypeError('Button instance expected')
            zone = pygame.Rect(pos, button.area)
            self._buttons.append(self.FixedButton(zone, button))
            self._widgets_img.blit(button.img, pos)


    stage = Stage(20)
    screen = stage.screen

    main_img = pygame.Surface((700, 700))
    main_img.fill((125, 125, 125))
    main_img.blit(pygame.font.Font(None, 55).render('SCREEN 1', False, (0, 0, 0)),
                  (50, 50))
    main_menu = TestMenu(screen, img=main_img)
    button1 = Button.fromstring('goto 2', action=stage.nav_link('screen2'), 
                                size=(100, 30))
    main_menu.add_button_at(button1, (15, 600))
    stage['main menu'] = main_menu

    main_img.fill((240, 140, 0))
    main_img.blit(pygame.font.Font(None, 55).render('SCREEN 2', False, (0, 0, 0)),
                  (50, 50))
    scene2 = TestMenu(screen, img=main_img)
    button2 = Button.fromstring('backto 1', action=stage.nav_link('main menu'),
                                size=(100, 30))
    scene2.add_button_at(button2, (15, 600))
    stage['screen2'] = scene2

    stage.play()

if __name__ == '__main__':
    stage_demo()
    pass
