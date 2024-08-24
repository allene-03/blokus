"""
Blokus shape definitions.

String representations for each of the 21 kinds of shapes,
each of which is identified by a single-character name
(such as "1", "C", and "Z"). See the Blokus Specification
document for a visual summary.

The squares of a shape are denoted by 'X' and 'O' characters.
The 'O', if any, denotes the origin for rotation.

The origin for "V" is denoted by '@' (rather than 'O');
there is no square at this position.

Shapes without an origin (namely, "1" and "O") cannot be
flipped or rotated: flipping or rotating these shapes would
have no visual effect anyway. The "X" shape is another
candidate for not having an origin. However, the explicit
origin provided allows for more natural flips and rotations
than the default origin (0, 0) that would otherwise be used.

Each shape's string representation begins with an empty line;
the second line corresponds to row 0 of the shape's squares.
Furthermore, subsequent lines are all indented to improve
readability; this vertical rule corresponds to column 0 of the
shape's squares. To "dedent" lines, see the textwrap.dedent()
function.

Do not modify this file.
"""

from enum import Enum


class ShapeKind(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SEVEN = "7"
    A = "A"
    C = "C"
    F = "F"
    S = "S"
    L = "L"
    N = "N"
    LETTER_O = "O"
    P = "P"
    T = "T"
    U = "U"
    V = "V"
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"


definitions: dict[ShapeKind, str] = {
    #
    # 1-square piece
    #
    ShapeKind.ONE: """
         X
         """,
    #
    # 2-square piece
    #
    ShapeKind.TWO: """
         OX
         """,
    #
    # 3-square pieces
    #
    ShapeKind.THREE: """
         XOX
         """,
    ShapeKind.C: """
         OX
         X
         """,
    #
    # 4-square pieces
    #
    ShapeKind.FOUR: """
         XOXX
         """,
    ShapeKind.SEVEN: """
         XX
          O
          X
         """,
    ShapeKind.S: """
          OX
         XX
         """,
    ShapeKind.LETTER_O: """
         XX
         XX
         """,
    ShapeKind.A: """
          X
         XOX
         """,
    #
    # 5-square pieces
    #
    ShapeKind.F: """
          XX
         XO
          X
         """,
    ShapeKind.FIVE: """
         X
         X
         O
         X
         X
         """,
    ShapeKind.L: """
         X
         X
         O
         XX
         """,
    ShapeKind.N: """
          X
         OX
         X
         X
         """,
    ShapeKind.P: """
         XX
         XO
         X
         """,
    ShapeKind.T: """
         XXX
          O
          X
         """,
    ShapeKind.U: """
         X X
         XOX
         """,
    ShapeKind.V: """
           X
          @X
         XXX
         """,
    ShapeKind.W: """
           X
          OX
         XX
         """,
    ShapeKind.X: """
          X
         XOX
          X
         """,
    ShapeKind.Y: """
          X
         XO
          X
          X
         """,
    ShapeKind.Z: """
         XX
          O
          XX
         """,
}


NUM_SHAPES = 21

assert len(ShapeKind) == NUM_SHAPES
assert len(definitions) == NUM_SHAPES