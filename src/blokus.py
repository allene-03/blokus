from shape_definitions import ShapeKind, definitions
from piece import Point, Shape, Piece
from base import BlokusBase, Grid
from typing import Optional


class Blokus(BlokusBase):
    """
    Blokus class that pulls directly from the Blokus base
    """
    _num_players: int
    _start_positions: set[Point]
    _size: int

    _curr_player: int
    _shapes: dict[ShapeKind, Shape]
    _shapes_played: dict[int, list[ShapeKind]]
    _grid: list[list[Optional[tuple[int, ShapeKind]]]]
    _retired: set[int]

    def __init__(self, num_players: int, size: int, start_positions: set[Point]) -> None:
        """
        Constructor for the Blokus class

        Inputs:
            num_players[int]: number of players
            size [int]: size of the board
            start_positions [set[Point]]: the locations available at start

        Returns None
        """

        # Basic assertions
        if num_players < 1 or num_players > 4:
            raise ValueError('Game requires 1-4 players to start.')
        elif size < 5:
            raise ValueError('Minimum size of the board is 5 by 5.')
        elif len(start_positions) < num_players:
            raise ValueError('There must be a start position for every player.')
        
        for position in start_positions:
            x, y = position
            if not (0 <= x <= size - 1 and 0 <= y <= size - 1):
                raise ValueError('Start position must be within grid.')

        # Initialize super-classed variables afterwards
        super().__init__(num_players, size, start_positions)

        # Initialize everything else
        self._curr_player = 1
        self._shapes = {shape_kind: Shape.from_string(shape_kind, definition)
                        for shape_kind, definition in definitions.items()}
        self._shapes_played = {plr: [] for plr in range(1, num_players + 1)}
        self._grid = [[None] * size for _ in range(size)]
        self._retired = set()

    ######## PROPERTIES

    @property
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        See BlokusBase
        """
        return self._shapes
    
    @property
    def size(self) -> int:
        """
        See BlokusBase
        """
        return self._size

    @property
    def start_positions(self) -> set[Point]:
        """
        See BlokusBase
        """
        return self._start_positions

    @property
    def num_players(self) -> int:
        """
        See BlokusBase
        """
        return self._num_players

    @property
    def curr_player(self) -> int:
        """
        See BlokusBase
        """
        return self._curr_player

    @property
    def retired_players(self) -> set[int]:
        """
        See BlokusBase
        """
        return self._retired

    @property
    def grid(self) -> Grid:
        """
        See BlokusBase
        """
        return self._grid

    @property
    def game_over(self) -> bool:
        """
        See BlokusBase
        """
        current_player = self._curr_player

        for player in range(1, self._num_players + 1):
            self._curr_player = player

            if player in self.retired_players:
                continue
            elif len(self.remaining_shapes(player)) <= 0:
                continue
            else:
                self._curr_player = current_player
                return False

        return True
    
    @property
    def winners(self) -> Optional[list[int]]:
        """
        See BlokusBase
        """
        if self.game_over:
            scores = [self.get_score(player)
                      for player in range(1, self.num_players + 1)]
            return [player + 1 for player, score in enumerate(scores)
                    if score == max(scores)]
        else:
            return None

    ######## METHODS

    def progress_turn(self) -> None:
        """
        Progresses to the next player's turn given there are players that aren't
        retired with available turns and that the game is still in-progress.
        """
        self._curr_player = (self.curr_player % self.num_players) + 1

        while ((self._curr_player in self.retired_players) or 
               len(self.remaining_shapes(self._curr_player)) <= 0) and \
                not self.game_over:
            self._curr_player = (self._curr_player % self.num_players) + 1
            
    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        Returns the list of remaining shapes that a given player has
        used yet

        Inputs:
            player [int]: the player that we're evaluating
        
        Returns [list[ShapeKind]]: the list of shapes that a player 
            can still use
        """
        return [shape for shape in self.shapes.keys() \
            if shape not in self._shapes_played[player]]
        
    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        if not piece.anchor:
            raise ValueError("Piece anchor is not set.")
        elif piece.shape.kind not in self.remaining_shapes(self._curr_player):
            raise ValueError("Player does not have the specified piece.")
        
        for x, y in piece.squares():
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                return True
            
        return False

    def any_collisions(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        if not piece.anchor:
            raise ValueError("Piece anchor is not set.")
        elif piece.shape.kind not in self.remaining_shapes(self._curr_player):
            raise ValueError("Player does not have the specified piece.")
        
        if self.any_wall_collisions(piece):
            return True
        
        for x, y in piece.squares():
            if self.grid[x][y] is not None:
                return True
        
        return False

    def legal_to_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        if not piece.anchor:
            raise ValueError("Piece anchor is not set.")
        elif piece.shape.kind not in self.remaining_shapes(self._curr_player):
            raise ValueError("Player does not have the specified piece.")

        if self.any_collisions(piece):
            return False
        elif len(self._shapes_played[self._curr_player]) <= 0:
            touching_start = False
            
            for square in piece.squares():
                if square in list(self._start_positions):
                    touching_start = True
            if not touching_start:
                return False
        else:
             # Corners = intercardinal neighbors, edges = cardinal neighbors
            touching_corner = False
            edges, corners = piece.cardinal_neighbors(), \
                piece.intercardinal_neighbors()

            # Edges rule 
            for x, y in edges:
                x, y = min(self.size - 1, max(0, x)), min(self.size - 1, max(0, y))
                edge_on_grid = self._grid[x][y] 

                if edge_on_grid and edge_on_grid[0] == self._curr_player:
                    return False

            # Corners rule
            for x, y in corners:
                x, y = min(self.size - 1, max(0, x)), min(self.size - 1, max(0, y))
                corner_on_grid = self._grid[x][y] 

                if corner_on_grid and corner_on_grid[0] == self._curr_player:
                    touching_corner = True

            # Make sure that it's touching a corner
            if not touching_corner:
                return False
        
        return True

    def maybe_place(self, piece: Piece) -> bool:
        """
        See BlokusBase
        """
        current_player = self._curr_player

        if current_player not in self.retired_players:
            if not piece.anchor:
                raise ValueError("Piece anchor is not set.")
            elif piece.shape.kind not in self.remaining_shapes(current_player):
                raise ValueError("Player does not have the specified piece.")
            elif not self.legal_to_place(piece):
                return False
            
            for x, y in piece.squares():
                self._grid[x][y] = (current_player, piece.shape.kind)

            self._shapes_played[current_player].append(piece.shape.kind)

        self.progress_turn()
        return True

    def retire(self) -> None:
        """
        See BlokusBase
        """
        self._retired.add(self._curr_player)
        self.progress_turn()

    def get_score(self, player: int) -> int:
        """
        See BlokusBase
        """
        remaining_shapes = self.remaining_shapes(player)
        
        if len(remaining_shapes) > 0:
            score = 0
            for shape in remaining_shapes:
                score -= len(self.shapes[shape].squares)
            return score
        elif len(self.shapes[self._shapes_played[player][-1]].squares) == 1:
            return 20
        else:
            return 15

    def available_moves(self) -> set[Piece]:
        """
        See BlokusBase
        """
        moves_left = set()

        for shape_kind in self.remaining_shapes(self.curr_player):
            shape = self.shapes[shape_kind]
            test_piece = Piece(shape)

            for x in range(self.size):
                for y in range(self.size):
                    test_piece.set_anchor((x, y))
                    
                    if self.legal_to_place(test_piece):
                        piece = Piece(shape)
                        piece.set_anchor((x, y))
                        moves_left.add(piece)

        return moves_left
