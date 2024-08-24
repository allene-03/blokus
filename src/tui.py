import curses
from piece import Piece
from curses import wrapper
from blokus import Blokus, ShapeKind, Point, Shape
import click
from typing import Optional, Tuple, List, Dict, Set

class BlokusTUI:
    """
    TUI class for Blokus Game
    """
    def __init__(self, blokus: Blokus, screen: 'curses._CursesWindow') -> None:
        """
        TUI constructor

        Input:
            blokus[Blokus]: A blokus game
        
        Returns [None] constructs the text user interface(TUI)
        """
        self.blokus = blokus
        self.screen = screen

        # initalizes curses colors
        curses.start_color() 
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.colors = [1, 2, 3, 4, 5]
        
        self.size = self.blokus.size
        self.piece: Optional[Piece] = None
        self.placed_pieces: Dict[Tuple[int, int], Tuple[int, str]] = {}  # Dict to store placed pieces
        self.dict_shapes = self.blokus._shapes  # Loads shapes

        # Dict of keyboard actions
        self.key_actions: Dict[int, ShapeKind] = {
            ord('1'): ShapeKind.ONE, ord('2'): ShapeKind.TWO,
            ord('3'): ShapeKind.THREE, ord('c'): ShapeKind.C,
            ord('4'): ShapeKind.FOUR, ord('7'): ShapeKind.SEVEN,
            ord('s'): ShapeKind.S, ord('o'): ShapeKind.LETTER_O,
            ord('a'): ShapeKind.A, ord('f'): ShapeKind.F,
            ord('5'): ShapeKind.FIVE, ord('l'): ShapeKind.L, ord('n'): ShapeKind.N,
            ord('p'): ShapeKind.P, ord('t'): ShapeKind.T, ord('u'): ShapeKind.U,
            ord('v'): ShapeKind.V, ord('w'): ShapeKind.W, ord('x'): ShapeKind.X,
            ord('y'): ShapeKind.Y, ord('z'): ShapeKind.Z
        }

    def _print(self, string: str, color: int, row: Optional[int] = None,
                col: Optional[int] = None) -> None:
        """
        Prints a string at an optional location

        Inputs:
            string[str]: The string to print
            color[int]: Curses color pair index
            row[int]: Row on the grid to be placed
            col[int]: Column on the grid to be placed
        
        Returns [None]: prints out a given string
        """
        if row is not None and col is not None:
            self.screen.addstr(row, col, string, curses.color_pair(color))
        else:
            self.screen.addstr(string, curses.color_pair(color))

    def draw_board(self) -> None:
        """
        Draws the TUI board

        Input:
            None besides self

        Returns [None]: prints TUI
        """
        for row in range(self.size):
            for col in range(self.size):
                valid_piece = self.piece != None and (row, col) in self.piece.squares()

                # Prints the pending piece onto the board
                if valid_piece and not self.blokus.any_collisions(self.piece):
                    color = self.colors[self.blokus.curr_player - 1]
                    self._print("▣", color, row, col)

                # Prints the start positions at beggining of game
                elif (row, col) in self.blokus.start_positions and self.blokus.grid[row][col] is None:
                    self._print("S", self.colors[4], row, col)

                # Prints already placed pieces
                elif (row, col) in self.placed_pieces:
                    color, symbol = self.placed_pieces[(row, col)]
                    self._print(symbol, color, row, col)
                
                # Prints the grid using dots
                else:
                    self._print(".", 0, row, col)

            self._print("\n", 0)

        # Prints each player's remaining pieces
        self._print(f"\nCurrent Player: Player {self.blokus.curr_player}\n", 0)
        self._print("\nRemaining Pieces:\n", 2)
        for player in range(1, self.blokus.num_players + 1):
            color = self.colors[player - 1]
            remaining_pieces = ""

            # reprints remaining shapes every time a shape is used
            for shape in self.blokus.remaining_shapes(player):
                remaining_pieces += shape.value + " "
            self._print(f"Player {player}: {remaining_pieces}", color)
            if player in self.blokus.retired_players:
                self._print(" (Retired)", self.colors[3])
            self._print(f" Score: {self.blokus.get_score(player)}\n", self.colors[4])

        # Prints game over screen 
        if self.blokus.game_over:
            winners = self.blokus.winners
            if len(winners) == 1:
                self._print(f"\nGame Over! Player {winners[0]} wins!\n", self.colors[2])
            else:
                winner_str = ", ".join(map(str, winners))
                self._print(f"\nGame Over! Players {winner_str} are tied!\n", self.colors[2])

    def choose_piece(self, shape_key: Optional[ShapeKind] = None) -> None:
        """
        Chooses a piece for the current player based on the key pressed.

        Input:
            shape_key [ShapeKind]: Shapekind in remaning shapes
        
        Return [none]: updates self.piece
        """
        remaining_shapes = self.blokus.remaining_shapes(self.blokus.curr_player)
        if not remaining_shapes:
            self.piece = None
            return
        if shape_key and shape_key in remaining_shapes:
            selected_shape = shape_key
        else:
            # If the selected shape is not in the remaining shapes, do nothing
            return

        shape = self.dict_shapes[selected_shape]
        self.piece = Piece(shape)
        self.piece.set_anchor((self.size // 2, self.size // 2))
        self.draw_board()


    def handle_user_input(self) -> None:
        """
        Handles user input for moving the pending piece

        Input: 
            None besides self
        
        Returns [None] interacts with keyboard
        """
        self.draw_board()

        while True:
            key = self.screen.getch()

            if key in self.key_actions:
                self.choose_piece(self.key_actions[key])

            if self.piece:  # Only process movement if a piece is selected
                r, c = self.piece.anchor

                if key == curses.KEY_UP:
                    self.piece.set_anchor((r - 1, c))  # Move the piece up
                elif key == curses.KEY_DOWN:
                    self.piece.set_anchor((r + 1, c))  # Move the piece down
                elif key == curses.KEY_LEFT:
                    self.piece.set_anchor((r, c - 1))  # Move the piece left
                elif key == curses.KEY_RIGHT:
                    self.piece.set_anchor((r, c + 1))  # Move the piece right
                elif key == 10:  # Enter Key
                    if self.place_piece():
                        self.piece = None
                elif key == ord('r'):
                    self.piece.rotate_right()
                elif key == ord('e'):
                    self.piece.rotate_left()
                elif key == ord(' '):
                    self.piece.flip_horizontally()
                elif key == ord('q'):
                    self.blokus.retire()
                    self.piece = None

            if key == 27:  # Escape Key
                break

            self.draw_board()

    def place_piece(self) -> bool:
        """
        Places the current pending piece on the board

        Input:
            None besides self

        Returns [bool]: True if legal to place, false otherwise
        """
        color = self.colors[self.blokus.curr_player - 1]
        if self.blokus.maybe_place(self.piece):
            for square in self.piece.squares():
                self.placed_pieces[square] = (color, "▣")
            return True
        else:
            self._print('\nNot legal placement', self.colors[4])
            return False

def run_tui(game: str, num_players: int, size: int, start_positions: Optional[Set[Tuple[int, int]]], screen: 'curses._CursesWindow') -> None:
    """
    Runs the tui in the terminal

    Inputs:
        game [str]: game mode 
        num_players [int]: the number of players
        size [int]: the size of the board
        start_positions [Optional [Set[Tuple[int, int]]]]: either default start 
            positions or start positions of a specific game mode
        screen [curses._curseswindow]: display screen in terminal

    Returns [none]: runs the tui
    """
    if not start_positions:
        if game == 'mono':
            num_players = 1
            size = 11
            start_positions = set([(5, 5)])
        elif game == 'duo':
            num_players = 2
            size = 14
            start_positions = set([(4, 4), (9, 9)])
        elif game == 'classic-2':
            num_players = 2
            size = 20
            start_positions = set([(0, 0), (19, 19)])
        elif game == 'classic-3':
            num_players = 3
            size = 20
            start_positions = set([(0, 0), (19, 0), (0, 19)])
        elif game == 'classic-4':
            num_players = 4
            size = 20
            start_positions = set([(0, 0), (19, 0), (0, 19), (19, 19)])
        elif game == 'mini':
            num_players = 1 if num_players == 1 else 2
            size = 5
            start_positions = set([(0, 0), (4, 4)])

    blokus = Blokus(num_players=num_players, size=size, start_positions=start_positions)
    tui = BlokusTUI(blokus, screen)
    tui.draw_board()
    tui.handle_user_input()

@click.command()
@click.option('--game', type=click.Choice(['mini', 'mono', 'duo', 'classic-2', 'classic-3', 'classic-4']), default='duo', help='Game mode')
@click.option('--num-players', '-n', type=int, default=2, help='Number of players')
@click.option('--size', '-s', type=int, default=14, help='Board size')
@click.option('--start-position', '-p', type=(int, int), multiple=True, help='Start position')

def main(game: str, num_players: int, size: int, start_position: Tuple[int, int]) -> None:
    """
    Main game function that runs everything together to create the game

    Input:
        game [str]: game mode
        num_players [int]: the number of players
        size [int]: size of the board
        start_position [Tuple[int,int]]: start positions for the players

    Return [None]: creates the game
    """
    if start_position:
        # Validate start positions are within the grid
        for pos in start_position:
            if not (0 <= pos[0] < size and 0 <= pos[1] < size):
                raise ValueError(f'Start position {pos} must be within grid of size {size}.')

    def start_tui(screen: 'curses._CursesWindow') -> None:
        """
        Allows the tui to start using curses screen

        Inputs:
            screen [curses._curseswindow]: terminal screen

        Returns [none] allows the tui to start
        """
        run_tui(game, num_players, size, set(start_position), screen)
    
    curses.wrapper(start_tui)

if __name__ == "__main__":
    main()