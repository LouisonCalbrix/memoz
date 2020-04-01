#! /usr/bin/env python3

# Tools to be used by the memoz game that are not directly related to the game
# logic.
# date: March 2020

from collections.abc import MutableSequence
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


class Stage(MutableSequence):
    '''
    Top level object that manages Scenes and call their update method.
    '''

    def __init__(self, **main_menu):
        self._scenes = [TextScene(**main_menu)]
        self._target = 'main menu'
        self._active = True
        type(self).INSTANCE = self

    def play(self):
        while self._active:
            self.current_scene.update()

    @property
    def main_menu(self):
        return self._scenes[0]

    @property
    def target(self):
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
        for scene in self._scenes:
            if scene.name == self.target:
                return scene

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

    def __str__(self):
        return 'current scene:\n{}'.format(self.current_scene)


class Scene(ABC):
    '''
    Interface for a logical unit to be displayed on the screen.
    '''
    @abstractmethod
    def update(self):
        '''
        Method to be called every unit of time during the time the Scene has the
        focus (e.g. when it's displayed onscreen)
        '''
        pass

class TextScene(Scene):
    '''
    Text based Scene. It gets printed on the screen once it gets the focus.
    '''

    def __init__(self, name, subtitle):
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
        if not isinstance(a_nav, Navigation):
            raise TypeError('Navigation instance expected')
        self.nav.append(a_nav)

    def __str__(self):
        nav_display = ('---'+str(navigation) for navigation in self.nav)
        return '\n'.join((self.subtitle, *nav_display))

    def __getitem__(self, subscript):
        for a_nav in self.nav:
            if a_nav.target_name == subscript:
                return a_nav
        raise KeyError('no such Navigation option')


class Navigation:
    '''
    Allow a change of Scene.
    '''
    def __init__(self, target_name):
        self.target_name = target_name

    def __call__(self):
        self.WINDOW.target = self.target_name

    def __str__(self):
        return self.target_name

    @classmethod
    def init(cls):
        cls.WINDOW = Stage.INSTANCE


#---------------------------------------------------------------------------Demo
# To test that utility follow these steps:
#    1 in a python REPL import this script:
#      from utils import *
#    2 a few navigation options are printed on the screen
#    3 to choose an option type its name
#    4 repeat steps 2 and 3 to continue navigating through the demo

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
