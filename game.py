# title: Hallomatch
# author: Alfonso Saavedra "Son Link"
# desc:  Hallomatch is a small Halloween-themed card matching game.
# site: https://github.com/son-link/hallomtach
# license: GNU General Public License v3.0
# version: 0.3.0

import pyxel
import random
from random import randint

# Globals

# Screen size
WITH = 320
HEIGHT = 177

# Game states
STATE_MAIN_MENU = 1
STATE_PLAYING = 2
STATE_PAUSE = 3
STATE_FINISH = 4
STATE_GAME_OVER = 5


class HallowenMatch():
    def __init__(self):
        self.game_state = STATE_MAIN_MENU  # Game state

        # Card's sprites
        self.card = {
            'back': (8, 0),
            'front': (32, 0)
        }

        # The position of yhe sprites in the image bank
        self.cards = {
            'skull': (72, 0),
            'witch': (104, 0),
            'zombie': (56, 0),
            'vampire': (88, 0),
            'wolf': (120, 0),
            'ghost': (136, 0),
            'bat': (152, 0),
            'pumpkin': (168, 0),
            'dragon': (184, 0),
            'demon': (200, 0),
            'mimic': (216, 0),
            'sphinx': (232, 0),
        }

        self.level = None  # Current level

        # The levels and his default values
        self.levels = {
            'easy': {
                'cols': 4,
                'rows': 3,
                'time': 40
            },
            'medium': {
                'cols': 6,
                'rows': 4,
                'time': 60
            },
            'hard': {
                'cols': 8,
                'rows': 4,
                'time': 60
            },
            'very_hard': {
                'cols': 8,
                'rows': 6,
                'time': 70
            },
            'hell': {
                'cols': 12,
                'rows': 6,
                'time': 90
            }
        }

        self.flip_down = False  # If true, the cards will be turned face down.
        self.font = pyxel.Font("retro-pixel-cute-mono.bdf")  # The font to use
        self.frame_count = 0  # The number of frames that have transcured
        self.matchs = None  # In this list the cards of the game will be stored.

        # The displacement on the vertical and horizontal axes from which the cards will start to be drawn.
        self.offset_x = 0
        self.offset_y = 0
        self.time = 60  # Playing time

        # We start Pyxel, load the assets, the image of the initial screen and enable the mouse.
        pyxel.init(WITH, HEIGHT, title='Hallomatch', display_scale=3,
                   capture_scale=2, capture_sec=60)
        pyxel.load('assets.pyxres')
        pyxel.mouse(True)
        pyxel.images[1].load(0, 0, 'main_screen.png')

        pyxel.run(self.update, self.draw)

    def centerText(self, text: str, y: int, color: int, font=None):
        '''This function displays a text centred on the horizontal axis'''
        pyxel.text(
            (WITH / 2) - ((len(text) * 6) / 2),
            y, text, color, font
        )

    def draw(self):
        """This function is called at each frame and is where the code
            for displaying images and text on the screen will go.
        """
        pyxel.cls(0)
        if self.game_state == STATE_MAIN_MENU:
            pyxel.blt(32, 0, 1, 0, 0, WITH, HEIGHT)
            center = pyxel.floor((WITH - 60) / 2)
            self.drawBtn('Easy', center, 86, 60, 12, 9, 15)
            self.drawBtn('Medium', center, 100, 60, 12, 9, 15)
            self.drawBtn('Hard', center, 114, 60, 12, 9, 15)
            self.drawBtn('Very Hard', center, 128, 60, 12, 9, 15)
            self.drawBtn('HELL!', center, 142, 60, 12, 9, 15)
        elif self.game_state != STATE_MAIN_MENU:
            pyxel.blt(8, 6, 0, 248, 8, 8, 8)
            pyxel.text(18, 8, f'{self.time:02}', 14)
            pyxel.blt(WITH - 16, 8, 0, 248, 0, 8, 8)

            for y in range(self.level['rows']):
                for x in range(self.level['cols']):
                    xx = (x * 24) + self.offset_x
                    yy = (y * 24) + self.offset_y

                    if self.matchs[y][x]['selected']:
                        pyxel.blt(xx, yy, 0, self.card['front'][0], self.card['front'][1], 24, 24)
                        sprite = self.matchs[y][x]['sprite']
                        pyxel.blt(xx + 4, yy + 4, 0, sprite[0], sprite[1], 16, 16, 14)
                    else:
                        pyxel.blt(xx, yy, 0, self.card['back'][0], self.card['back'][1], 24, 24)

        if self.game_state == STATE_FINISH:
            left = pyxel.floor((WITH - 196) / 2)
            pyxel.rect(left, 64, 196, 28, 9)
            self.centerText('YOU WIN!', 64, 11, self.font)
            self.centerText('Press to return to the main menu', 74, 15, self.font)

        elif self.game_state == STATE_GAME_OVER:
            left = pyxel.floor((WITH - 196) / 2)
            pyxel.rect(left, 64, 196, 28, 9)
            self.centerText('YOU LOOSE', 64, 6, self.font)
            self.centerText('Press to return to the main menu', 74, 15, self.font)
        elif self.game_state == STATE_PAUSE:
            left = pyxel.floor((WITH - 72) / 2)
            btnLeft = pyxel.floor((WITH - 52) / 2)
            pyxel.rect(left, 64, 72, 50, 0)
            self.centerText('PAUSED', 65, 15, self.font)
            self.drawBtn('Continue', btnLeft, 84, 52, 12, 11, 15)
            self.drawBtn('Exit', btnLeft, 98, 52, 12, 6, 15)

    def drawBtn(self, text: str, x: int, y: int, w: int, h: int, bg: int, color: int):
        """This function draws a button on the screen

        Args:
            text (str): The text to show in the button
            x (int): The initial position on the horizontal axis
            y (int): The initial position on the vertical axis
            w (int): Button width
            h (int): Button height
            bg (int): Button color
            color (int): Text color
        """
        pyxel.rect(x, y, w, h, bg)
        text_w = len(text) * 6
        text_x = x + pyxel.floor((w - text_w) / 2)
        text_y = y - 2
        pyxel.text(text_x, text_y, text, color, self.font)

    def initGame(self):
        """This function starts a new game, thus resetting several of the game variables.
        """
        self.matchs = []
        self.matchs = [[0 for i in range(self.level['cols'])] for j in range(self.level['rows'])]
        self.selected = []
        self.win = False

        for y in range(self.level['rows']):
            x = 0
            for x in range(0, self.level['cols'], 2):
                key, value = random.choice(list(self.cards.items()))
                self.matchs[y][x] = {
                    'card': key,
                    'sprite': value,
                    'selected': False
                }
                self.matchs[y][x + 1] = {
                    'card': key,
                    'sprite': value,
                    'selected': False
                }

        self.matchs = self.suffle(self.matchs)
        self.offset_x = ((WITH - (self.level['cols'] * 24)) / 2)
        self.offset_y = ((HEIGHT - (self.level['rows'] * 24)) / 2)

    def update(self):
        """This function is called on every frame and is where most of the game's running code is located.
        """

        if self.game_state == STATE_MAIN_MENU:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                center = pyxel.floor((WITH - 60) / 2)
                __level = None
                if pyxel.mouse_x >= center and pyxel.mouse_x <= center + 60:
                    self.time = 60
                    if pyxel.mouse_y >= 86 and pyxel.mouse_y <= 98:
                        __level = 'easy'
                    elif pyxel.mouse_y >= 100 and pyxel.mouse_y <= 112:
                        __level = 'medium'
                    elif pyxel.mouse_y >= 114 and pyxel.mouse_y <= 126:
                        __level = 'hard'
                    elif pyxel.mouse_y >= 128 and pyxel.mouse_y <= 140:
                        __level = 'very_hard'
                    elif pyxel.mouse_y >= 142 and pyxel.mouse_y <= 154:
                        __level = 'hell'

                    if __level:
                        self.level = self.levels[__level]
                        self.initGame()
                        self.game_state = STATE_PLAYING
                        self.time = self.level['time']

        elif self.game_state == STATE_PLAYING:
            self.frame_count += 1
            if self.frame_count % 60 == 0:
                self.time -= 1
                if self.time == 0:
                    self.game_state = STATE_GAME_OVER

            if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_P):
                self.game_state = STATE_PAUSE

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if (
                    pyxel.mouse_x >= WITH - 16 and pyxel.mouse_x <= WITH - 8 and
                    pyxel.mouse_y >= 8 and pyxel.mouse_y <= 16
                ):
                    self.game_state = STATE_PAUSE

                elif not self.flip_down:
                    # If you are not waiting for the cards to turn face down,
                    # we calculate the position in the array of the selected card
                    x = pyxel.floor((pyxel.mouse_x - self.offset_x) / 24)
                    y = pyxel.floor((pyxel.mouse_y - self.offset_y) / 24)

                    # If the calculated position is larger on one of the axes
                    # is larger than the size of the list, or the chart is face up,
                    # the process is stopped.
                    if (
                        (x >= 0 and x >= self.level['cols']) or
                        (y >= 0 and y >= self.level['rows']) or
                        self.matchs[y][x]['selected']
                    ):
                        return

                    # We add the selected card to the list where we store these cards.
                    self.selected.append((y, x))

                    # We mark in the list of cards that was selected
                    self.matchs[y][x]['selected'] = True

                    # If we have selected 2 cards, we get their card identifier,
                    # and if they are the same, they are marked and we add 1 second.
                    # If they are not, we indicate that they are going to be flipped and remove 1 second.
                    if len(self.selected) == 2:
                        card1 = self.matchs[self.selected[0][0]][self.selected[0][1]]
                        card2 = self.matchs[self.selected[1][0]][self.selected[1][1]]
                        if (card1['card'] == card2['card']):
                            self.selected = []
                            self.time += 1
                        else:
                            self.flip_down = self.frame_count

            # Now let's check how many cards have been revealed.
            revealed = 0
            for y in range(self.level['rows']):
                for x in range(self.level['cols']):
                    if self.matchs[y][x]['selected']:
                        revealed += 1

            # If the total number of cards revealed matches the total number of cards, you have won the game.
            if revealed == self.level['rows'] * self.level['cols']:
                self.game_state = STATE_FINISH
                self.flip_down = False

            # If it was indicated that the cards are to be flipped face down,
            # we calculate whether 1 second (60 frames) has passed since it was marked to do so.
            if self.flip_down and self.frame_count > self.flip_down and (self.frame_count - self.flip_down) % 60 == 0:
                self.matchs[self.selected[0][0]][self.selected[0][1]]['selected'] = False
                self.matchs[self.selected[1][0]][self.selected[1][1]]['selected'] = False
                self.selected = []
                self.flip_down = False

        elif (
            (self.game_state == STATE_FINISH or self.game_state == STATE_GAME_OVER) and
            pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        ):
            self.game_state = STATE_MAIN_MENU

        elif self.game_state == STATE_PAUSE:
            btnLeft = pyxel.floor((WITH - 52) / 2)
            x = pyxel.mouse_x
            y = pyxel.mouse_y
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if (
                    (x >= WITH - 16 and x <= WITH - 8 and y >= 8 and y <= 16) or
                    (x >= btnLeft and x <= btnLeft + 52 and y >= 84 and y <= 96)
                ):
                    self.game_state = STATE_PLAYING
                elif x >= btnLeft and x <= btnLeft + 52 and y >= 98 and y <= 110:
                    self.game_state = STATE_MAIN_MENU

    def suffle(self, array: list):
        """This function takes the specified list and returns it unordered.

        Args:
            array (list): This function takes the specified list and returns it unordered.

        Returns:
            list: The list unordered
        """
        for y in range(self.level['rows']):
            for x in range(self.level['cols']):
                yy = randint(0, self.level['rows'] - 1)
                xx = randint(0, self.level['cols'] - 1)
                tmp = array[y][x]
                array[y][x] = array[yy][xx]
                array[yy][xx] = tmp
        return array


HallowenMatch()
