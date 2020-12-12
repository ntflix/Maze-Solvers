# Maze

| | |
-|-
Type | `Maze class`
Inherits from | [`MazeProtocol`](MazeProtocol.md)
Delcared in | `modules/data_structures/maze/maze/maze.py`
Description | The Maze class.

---

## Variables

Name | Type | Default Value | Comment
 --- | --- | --- | ---
`__maze` | [`Graph`](../Data%20Structures/Graph.md)`[`[`MazeCell`](MazeCell.md)`]` | NA | A graph representation of a maze, made up of [`MazeCell`](MazeCell.md)s.
`__coordinates` | `Dict[`[`MazeCell`](MazeCell.md)`, Tuple[int, int]]` | NA | Dictionary of MazeCells and their XY coordinates in the maze

## Methods

Name | Return Type | Comment
 --- | --- | ---
 `__init__` | `size: Tuple[int, int]` | `None` | Initialise a maze from a given size
 `addWallBetween` | `cellA: `[`MazeCell`](MazeCell.md)`, cellB: `[`MazeCell`](MazeCell.md)`, bidirectional: bool = True` | `None` | Add a wall between two adjacent cells
 `removeWallBetween` | `cellA: `[`MazeCell`](MazeCell.md)`, cellB: `[`MazeCell`](MazeCell.md)`, bidirectional: bool = True` | `None` | Remove a wall between two adjacent cells
`getCoordinatesOf` | `mazeCell: `[`MazeCell`](MazeCell.md) | `tuple[int, int]` | Get the coordinates of a given maze cell
`getNeighboursOf` | `mazeCell: `[`MazeCell`](MazeCell.md) | `list[MazeCell]` | Get the neighbours of a given maze cell
`getCellAtCoordinates` | `coordinates: tuple[int, int]` | `Optional[`[`MazeCell`](MazeCell.md)`]` | Get the [`MazeCell`](MazeCell.md) at specified coordinates. Returns `None` if nonexistent. Raises `IndexError` if coordinates out of bounds.