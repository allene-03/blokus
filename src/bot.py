"""
Blokus Bot Testing
Usage: $ python3 src/bot.py NUM_GAMES
"""

### MODULES
from abc import ABC, abstractmethod

# Block the annoying pygame message
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import click
import random
import pygame
from blokus import Blokus
from piece import Point, Piece
from typing import Optional

### CONSTANTS (SETTINGS)

CLOCK: pygame.time.Clock = pygame.time.Clock()
BOARD_SIZE: int = 11

DEFAULT_NUM_GAMES: int = 20
DEFAULT_BOT_ONE: str = 'N'
DEFAULT_BOT_TWO: str = 'N'

### CLASSES

class BotBase(ABC):
    '''
    Abstract base class for Bot classes.
    '''
    _game_object: Blokus

    def __init__(self, game_object: Blokus) -> None:
        '''
        Subclasses should have constructors which accept this argument:
            game_object: the game object that is going to be referenced
        '''
        self._game_object = game_object

    @property
    def game(self) -> Blokus:
        'Returns the referencing Blokus game object'
        return self._game_object
    
    @abstractmethod
    def place_piece(self) -> None:
        '''
        Handles the selection logic for the a given bot class, essentially
        making random decisions
        
        Returns None.
        '''
        assert False, "Implement place_piece for the given bot."

class U_Bot(BotBase):
    '''
    Class for the unsatisfactory bot, pulls from BotBase
    '''
    _game_object: Blokus

    def __init__(self, game_object: Blokus) -> None:
        '''
        Initialization of the unsatisfactory bot
        '''
        super().__init__(game_object)

    def place_piece(self) -> None:
        '''
        Handles the selection logic for the unsatisfactory bot
        
        Returns None.
        '''
        available_moves = self._game_object.available_moves()

        # Retires if there are no available moves left
        if len(available_moves) == 0:
            self.game.retire()
            return
        
        # Rank the smallest pieces available to place
        smallest_piece = min([len(piece.shape.squares) for piece in available_moves])

        for piece in available_moves:
            if len(piece.squares()) == smallest_piece:
                self.game.maybe_place(piece)
                return
        
class N_Bot(BotBase):
    '''
    Class for the needs improvement bot, pulls from BotBase
    '''
    _game_object: Blokus

    def __init__(self, game_object: Blokus) -> None:
        '''
        Initialization of the needs improvement bot
        '''
        super().__init__(game_object)

    def place_piece(self) -> None:
        '''
        Handles the selection logic for the needs improvement bot
        
        Returns None.
        '''
        available_moves = self.game.available_moves()

        if len(available_moves) == 0:
            self.game.retire()
        else:
            self.game.maybe_place(random.choice(list(available_moves)))

class S_Bot(BotBase):
    '''
    Class for the satisfactory bot, pulls from BotBase
    '''
    _game_object: Blokus

    def __init__(self, game_object: Blokus) -> None:
        '''
        Initialization of the satisfactory bot
        '''
        super().__init__(game_object)

    def place_piece(self) -> None:
        '''
        Handles the selection logic for the satisfactory bot
        
        Returns None.
        '''
        available_moves = self._game_object.available_moves()

        # Retires if there are no available moves left
        if len(available_moves) == 0:
            self.game.retire()
            return
        
        # Rank the largest pieces available to place
        largest_piece = max([len(piece.shape.squares) for piece in available_moves])

        for piece in available_moves:
            if len(piece.squares()) == largest_piece:
                self.game.maybe_place(piece)
                return

# MAIN SEQUENCE

@click.command()
@click.option("--num_games", "-n", type = int, default = DEFAULT_NUM_GAMES, \
    help = "Number of simulations to run")
@click.option("--strategy_1", "-1", type = str, default = DEFAULT_BOT_ONE, \
    help = "Strategy for Bot #1")
@click.option("--strategy_2", "-2", type = str, default = DEFAULT_BOT_TWO, \
    help = "Strategy for Bot #2")

def run_bot_simulation(num_games: int, strategy_1: str, strategy_2: str) -> None:
    '''
    Handles the main bot simulation logic, taking two strategies and playing them
        against each other

    Paramaters:
        num_games [int]: the number of games we're running
        strategy_1 [str]: the string representation of first bot strategy
        strategy_2 [str]: the string representation of second bot strategy

    Returns None.
    '''
    bots = {1: strategy_1, 2: strategy_2}
    wins_count, ties_count = {key: 0 for key in bots.keys()}, 0

    # Run the loop for the amount of games we assign
    for game in range(num_games):
        start_positions = {(0, 0), (BOARD_SIZE - 1, BOARD_SIZE - 1)}
        bot_blokus = Blokus(len(bots.keys()), BOARD_SIZE, start_positions)

        bot_objects = {key: (
            S_Bot(bot_blokus) if value == 'S' else
            N_Bot(bot_blokus) if value == 'N' else
            U_Bot(bot_blokus) if value == 'U' else
            None) for key, value in bots.items()}
        
        while not bot_blokus.game_over:
            bot_object = bot_objects.get(bot_blokus.curr_player)

            # Can change to errors later if desired
            assert bot_object and bot_object is not None, \
                "Bot should be defined as U, N, or S-type before running tests."
            
            # Runs the place piece function for the bot
            bot_object.place_piece()

        # Similar to wait(1/value); can alter to simulate faster; we want it to wait
        # two more seconds regardless of test volume optimally. Additionally, this 
        # slows the entire environment, not just the script, so entire terminal
        # yields including Ctrl+C to stop

        # Equals wait(1/(2 * NUM_GAMES)) or 2 seconds dispersed between all the
        # test cases; 2 seconds on top of however long it takes to run to space it
        CLOCK.tick(num_games / 2)

        # Now track the winner of this given round to be reported later
        winners = bot_blokus.winners

        if len(winners) >= len(bots.keys()):
            ties_count += 1
        else:
            wins_count[winners[0]] += 1

    # After we finish the assigned number of games, deduce our breakdown
    total_score, notification = sum(wins_count.values()) + ties_count, ''

    for bot, score in wins_count.items():
        bot_percentage = (score / total_score) * 100
        notification += f'Bot {bot} Wins |  {bot_percentage: .2f} %\n'

    ties_percentage = (ties_count / total_score) * 100
    notification += f'Ties       | {ties_percentage: .2f} %\n'

    # Finally output our results to the terminal
    print(notification)

### EXECUTE MAIN SEQUENCE

if __name__ == '__main__':
    run_bot_simulation()
