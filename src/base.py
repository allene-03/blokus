"""
Abstract base class for Blokus game logic.

Do not modify this file.
"""
from abc import ABC, abstractmethod
from typing import Optional

from shape_definitions import ShapeKind
from piece import Point, Shape, Piece

# Unoccupied grid cells are represented with None.
#
# Each occupied grid cell is represented as the player
# number whose piece occupies that square, plus the shape
# kind played there (ShapeKind.One, ShapeKind.W, etc).
#
# The shape kind is not needed to implement the game
# logic, but is exposed in case GUIs/TUIs would like
# to use the information in some way.
#
Cell = Optional[tuple[int, ShapeKind]]
Grid = list[list[Cell]]


class BlokusBase(ABC):
    """
    Abstract base class for Blokus game logic.
    """

    _num_players: int
    _size: int
    _start_positions: set[Point]

    def __init__(
        self,
        num_players: int,
        size: int,
        start_positions: set[Point],
    ) -> None:
        """
        Subclasses should have constructors which accept these
        same first three arguments:

            num_players: Number of players
            size: Number of squares on each side of the board
            start_positions: Positions for players' first moves

        Raises ValueError...
            if num_players is less than 1 or more than 4,
            if the size is less than 5,
            if not all start_positions are on the board, or
            if there are fewer start_positions than num_players.

        Note: This base class constructor does not raise the
        exceptions above, but subclass constructors should.
        """
        self._num_players = num_players
        self._size = size
        self._start_positions = start_positions

    #
    # PROPERTIES
    #

    @property
    @abstractmethod
    def shapes(self) -> dict[ShapeKind, Shape]:
        """
        Returns all 21 Blokus shapes, as named and defined by
        the string representations in shape_definitions.py.

        The squares and origin, if any, of each shape should
        correspond to the locations and orientations defined
        in shape_definitions. For example, the five-square
        straight piece is called ShapeKind.FIVE, defined as a
        vertical line (as opposed to horizontal), and has its
        origin at the middle (third) square.

        See shape_definitions.py for more details.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def size(self) -> int:
        """
        Returns the board size (the number of squares per side).
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def start_positions(self) -> set[Point]:
        """
        Returns the start positions.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def num_players(self) -> int:
        """
        Returns the number of players. Players are numbered
        consecutively, starting from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def curr_player(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "Whose turn is it?"). While the
        game is ongoing, this property never refers to a player
        that has played all of their pieces or that retired
        before playing all of their pieces. If the game is over,
        this property will not return a meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def retired_players(self) -> set[int]:
        """
        Returns the set of players who have retired. These
        players do not get any more turns; they are skipped
        over during subsequent gameplay.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def grid(self) -> Grid:
        """
        Returns the current state of the board (i.e. Grid).
        There are two values tracked for each square (i.e. Cell)
        in the grid: the player number (an int) who has played
        a piece that occupies this square; and the shape kind
        of that piece. If no played piece occupies this square,
        then the Cell is None.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def game_over(self) -> bool:
        """
        Returns whether or not the game is over. A game is over
        when every player is either retired or has played all
        their pieces.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def winners(self) -> Optional[list[int]]:
        """
        Returns the (one or more) players who have the highest
        score. Returns None if the game is not over.
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def remaining_shapes(self, player: int) -> list[ShapeKind]:
        """
        Returns a list of shape kinds that a particular
        player has not yet played.
        """
        raise NotImplementedError

    @abstractmethod
    def any_wall_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall. For the purposes of this
        predicate, a "wall collision" occurs when at
        least one square of the piece would be located
        beyond the bounds of the (size x size) board.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        raise NotImplementedError

    @abstractmethod
    def any_collisions(self, piece: Piece) -> bool:
        """
        Returns a boolean indicating whether or not the
        given piece (not yet played on the board) would
        collide with a wall or with any played pieces.
        A "collision" between pieces occurs when they
        overlap.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_to_place(self, piece: Piece) -> bool:
        """
        If the current player has not already played
        this shape, this method returns a boolean
        indicating whether or not the given piece is
        legal to place. This requires that:

         - if the player has not yet played any pieces,
           this piece would cover a start position;
         - the piece would not collide with a wall or any
           previously played pieces; and
         - the piece shares one or more corners but no edges
           with the player's previously played pieces.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        raise NotImplementedError

    @abstractmethod
    def maybe_place(self, piece: Piece) -> bool:
        """
        If the piece is legal to place, this method
        places the piece on the board, updates the
        current player and other relevant game state,
        and returns True.

        If not, this method leaves the board and current
        game state unmodified, and returns False.

        Note that the game does not necessarily end right
        away when a player places their last piece; players
        who have not retired and have remaining pieces
        should still get their turns.

        Raises ValueError if the player has already
        played a piece with this shape.

        Raises ValueError if the anchor of the piece
        is None.
        """
        raise NotImplementedError

    @abstractmethod
    def retire(self) -> None:
        """
        The current player, who has not played all their pieces,
        may choose to retire. This player does not get any more
        turns; they are skipped over during subsequent gameplay.
        """
        raise NotImplementedError

    @abstractmethod
    def get_score(self, player: int) -> int:
        """
        Returns the score for a given player. A player's score
        can be computed at any time during gameplay or at the
        completion of a game.
        """
        raise NotImplementedError

    @abstractmethod
    def available_moves(self) -> set[Piece]:
        """
        Returns the set of all possible moves that the current
        player may make. As with the arguments to the maybe_place
        method, a move is determined by a Piece, namely, one of
        the 21 Shapes plus a location and orientation.

        Notice there may be many different Pieces corresponding
        to a single Shape that are considered available moves
        (because they may differ in location and orientation).
        """
        raise NotImplementedError
