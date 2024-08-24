from base import Grid, Cell, ShapeKind

def grid_to_string(grid: Grid) -> str:
    """
    Convert a Grid object to a string representation.

    Args:
        grid (Grid): The grid to convert.

    Returns:
        str: The string representation of the grid.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    result = []

    result.append('+' + '-' * (width * 2) + '+')
    for row in grid:
        row_str = '|'
        for cell in row:
            if cell is None:
                row_str += '  '
            else:
                player, shape = cell
                row_str += str(player) + ' '
        row_str += '|'
        result.append(row_str)
    result.append('+' + '-' * (width * 2) + '+')

    return '\n'.join(result)

def string_to_grid(s: str) -> Grid:
    """
    Convert a string representation of a grid back to a Grid object.

    Args:
        s (str): The string representation of the grid.

    Returns:
        Grid: The grid object.
    """
    lines = s.strip().split('\n')
    cells: Grid = []

    for line in lines[1:-1]:
        row = []
        for i in range(1, len(line) - 1, 2):
            char = line[i]
            if char == ' ':
                row.append(None)
            else:
                player = int(char)
                row.append((player, ShapeKind.One))  # Assuming ShapeKind.One for simplicity
        cells.append(row)

    return cells

def test_grid_1() -> None:
    """
    Test case for a 5x5 board with a small configuration.
    """
    cells: Grid = [
        [None, None, None, None, None],
        [None, (1, ShapeKind.ONE), (1, ShapeKind.ONE), None, None],
        [None, (1, ShapeKind.ONE), (1, ShapeKind.ONE), None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]
    grid = cells
    s = """
    +----------+
    |          |
    | 1 1      |
    | 1 1      |
    |          |
    |          |
    +----------+
    """
    assert s.strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_2() -> None:
    """
    Test case for a 6x6 board with a diagonal configuration.
    """
    cells: Grid = [
        [None, (2, ShapeKind.ONE), None, None, None, None],
        [(1, ShapeKind.ONE), None, None, None, None, None],
        [None, None, (1, ShapeKind.ONE), None, None, None],
        [None, None, None, (2, ShapeKind.ONE), None, None],
        [None, None, None, None, None, (2, ShapeKind.ONE)],
        [None, None, None, None, (1, ShapeKind.ONE), None],
    ]
    grid = cells
    s = """
    +------------+
    | 2          |
    |1           |
    |    1       |
    |      2     |
    |          2 |
    |        1   |
    +------------+
    """
    assert s.strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))

def test_grid_3() -> None:
    """
    Test case for a 4x4 board with two player pieces.
    """
    cells: Grid = [
        [None, None, None, None],
        [None, (1, ShapeKind.ONE), None, None],
        [None, None, (2, ShapeKind.ONE), None],
        [None, None, None, None],
    ]
    grid = cells
    s = """
    +--------+
    |        |
    |  1     |
    |    2   |
    |        |
    +--------+
    """
    assert s.strip() == grid_to_string(grid)
    assert grid == string_to_grid(grid_to_string(grid))
