#! /usr/bin/env python3

'''
Tools to be used by the memoz game that are not directly related to the game
logic.
date: March 2020
'''

import pygame
from copy import copy
from collections.abc import MutableSequence
from abc import ABC, abstractmethod

pygame.init()

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


class Stage(MutableSequence):
    '''
    Top level object that manages Scenes and call their update method.
    '''

    def __init__(self, **main_menu):
        '''
        A Stage needs a Scene as early as instanciation, therefore it expects
        keyword arguments to instanciate TextScene. 
        '''
        self._scenes = [TextScene(**main_menu)]
        self._target = 'main menu'
        self._active = True
        type(self).INSTANCE = self

    def play(self):
        '''
        The real main loop of the program, it's body changes as the Scene being
        played is changed.
        '''
        while self._active:
            self.current_scene.update()

    @property
    def main_menu(self):
        '''
        Return the first Scene which is the entry point of the interactive program.
        '''
        return self._scenes[0]

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
        elif value not in (scene.name for scene in self._scenes):
            raise KeyError('non existing scene')
        self._target = value

    @property
    def current_scene(self):
        '''
        Scene being played.
        '''
        for scene in self._scenes:
            if scene.name == self.target:
                return scene

    # ----Implementation of MutableSequence interface

    def __delitem__(self, index):
        del self._scenes[index]

    def __getitem__(self, index):
        return self._scenes[index]

    def __setitem__(self, index, scene):
        if not isinstance(scene, Scene):
            raise TypeError('Only instances of subclasses of Scene are accepted')
        self._scenes[index] = value

    def __len__(self):
        return len(self._scenes)

    def insert(self, index, scene):
        if not isinstance(scene, Scene):
            raise TypeError('Only instances of subclasses of Scene are accepted')
        self._scenes.insert(index, scene)
    # ----

    def __str__(self):
        return 'current scene:\n{}'.format(self.current_scene)


class Scene(ABC):
    '''
    Interface for a logical unit to be displayed on the screen.
    A Scene -meant to be contained by an instance of a top level class Stage-
    provides, via its update method, the main loop of a program. Any subclass of
    Scene needs to implement update in a way that allow the user to interact with
    the program
    '''
    @abstractmethod
    def update(self):
        '''
        Method to be called repeatedly by the managing Stage instance. It will
        temporarily constitue the main loop of the program.
        '''
        pass

# Text based example of Scene subclass
class TextScene(Scene):
    '''
    Text based Scene. It gets printed on the screen once it gets the focus.
    '''

    def __init__(self, name, subtitle):
        '''
        Expect name to be a string internally identifying the Scene,
        and subtitle to be another string to display onscreen to the user.
        '''
        self.name = name
        self.subtitle = subtitle
        self.nav = list()
        self.printed = False

    def update(self):
        if not self.printed:
            print(self)
            self.printed = True
        user_input = input('choose an option\n')
        try:
            self[user_input]()
            self.printed = False
        except LookupError as e:
            print(e)

    def add_nav(self, a_nav):
        '''
        Add a Navigation option to the Scene.
        '''
        if not isinstance(a_nav, Navigation):
            raise TypeError('Navigation instance expected')
        self.nav.append(a_nav)

    def __str__(self):
        '''
        Return a string representing both the Scene and its navigation options.
        '''
        nav_display = ('---'+str(navigation) for navigation in self.nav)
        return '\n'.join((self.subtitle, *nav_display))

    def __getitem__(self, subscript):
        '''
        Get an item whose attribute target_name is equal to subscript. This is how
        to retrieve Navigation instances contained in the nav attribute. 
        '''
        for a_nav in self.nav:
            if a_nav.target_name == subscript:
                return a_nav
        raise KeyError('no such Navigation option')


class Navigation:
    '''
    Callable object allowing a change of Scene when it's called.
    '''
    def __init__(self, target_name):
        '''
        Expect a string representing the name of an existing (or soon to be
        instanciated) Scene.
        '''
        self.target_name = target_name

    def __call__(self):
        '''
        Change the Scene being played by the Stage instance.
        '''
        self.STAGE.target = self.target_name

    def __str__(self):
        return self.target_name

    @classmethod
    def init(cls):
        '''
        Initialize class shared data.
        '''
        cls.STAGE = Stage.INSTANCE


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
#        self._pos = copy(pos)
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
    def image(self):
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
    Mean to test the Button class. To run demo do the following:
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
    screen.blit(button.image, zone)
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

def textscene_demo():
    '''
    Meant to test the Stage and TextScene classes. To run demo do the following:
        1 import this script in your python shell:
          from utils import *
        2 call this function:
          textscene_demo()
        3 a few navigation options are printed on the screen, choose one by
          typing its name.
        4 repeat steps 2 and 3 to continue navigating the demo
    '''
    stage = Stage(name='main menu', subtitle='MAIN MENU')

    Navigation.init()

    stage.main_menu.add_nav(Navigation('game'))
    stage.main_menu.add_nav(Navigation('high scores'))
    stage.main_menu.add_nav(Navigation('quit'))

    game = TextScene('game', 'THE GAME')
    game.add_nav(Navigation('pause'))

    pause = TextScene('pause', 'PAUSED GAME')
    pause.add_nav(Navigation('game'))
    pause.add_nav(Navigation('main menu'))
    pause.add_nav(Navigation('quit'))

    hi_scores = TextScene('high scores', 'HIGH SCORES')
    hi_scores.add_nav(Navigation('main menu'))

    stage.append(game)
    stage.append(pause)
    stage.append(hi_scores)

    stage.play()

if __name__ == '__main__':
    pass
