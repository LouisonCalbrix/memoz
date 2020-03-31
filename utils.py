#! /usr/bin/env python3

# Tools to be used by the memoz game that are not directly related to the game
# logic.
# date: March 2020

class Singleton(type):
    '''
    Singleton metaclass. A Singleton class's only instance can be accessed
    by name_of_class.INSTANCE
    '''
    def __init__(self, *args, **kwargs):
        self.INSTANCE = None
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self.INSTANCE is None:
            self.INSTANCE = super().__call__(*args, **kwargs)
        return self.INSTANCE


class Window(metaclass=Singleton):
    '''
    Top level
    '''
    def __init__(self, **main_menu):
        if self.INSTANCE:
            self.INSTANCE = self
        self.queue = [Scene(**main_menu)]
        self._target = 'main menu'

    @property
    def main_menu(self):
        return self.queue[0]

    def append(self, scene):
        self.queue.append(scene)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        if value == 'quit':
            print('quitting...')
        if value not in (scene.name for scene in self.queue):
            raise KeyError('non existing scene')
        self._target = value

    @property
    def current_scene(self):
        for scene in self.queue:
            if scene.name == self.target:
                return scene

    def __str__(self):
        return 'current scene:\n{}'.format(self.current_scene)


class Scene:
    '''
    Display on the screen.
    '''
    def __init__(self, name, subtitle):
        self.name = name
        self.subtitle = subtitle
        self.nav = list()

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
        cls.WINDOW = Window.INSTANCE


#---------------------------------------------------------------------------Demo
# To test that utility follow these steps:
#    1 in a python REPL import this script "from utils import *"
#    2 to see what navigation options you currently have, type:
#      print(window)
#    3 to choose an option named nav_opt, type:
#      window.current_scene['nav_opt']()
#    4 repeat steps 2 and 3 to continue navigating through the demo

window = Window(name='main menu', subtitle='MAIN MENU')

Navigation.init()

window.main_menu.add_nav(Navigation('game'))
window.main_menu.add_nav(Navigation('high scores'))
window.main_menu.add_nav(Navigation('quit'))

game = Scene('game', 'THE GAME')
game.add_nav(Navigation('pause'))

pause = Scene('pause', 'PAUSED GAME')
pause.add_nav(Navigation('game'))
pause.add_nav(Navigation('main menu'))
pause.add_nav(Navigation('quit'))

hi_scores = Scene('high scores', 'HIGH SCORES')
hi_scores.add_nav(Navigation('main menu'))

window.append(game)
window.append(pause)
window.append(hi_scores)
