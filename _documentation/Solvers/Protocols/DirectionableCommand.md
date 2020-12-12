# DirectionableCommand

| | |
-|-
Type | `Protocol class`
Super | NA
Delcared in | `modules/maze_solvers/commands/protocols/directionable_command.py`
Description | A protocol to which a command with a direction will conform.

---

## Variables

Name | Type | Default Value | Comment
 --- | --- | --- | ---
`relativeDirection` | [`RelativeDirection`](../Common/RelativeDirection.md) | NA | The relative direction of movement for the command
`absoluteDirection` | [`AbsoluteDirection`](../Common/AbsoluteDirection.md) | NA | The absolute direction of movement for the command
`cell` | [`MazeCell`](../../Maze/MazeCell.md) | NA | The cell the command was initiated in

## Methods

Name | Return Type | Comment
 --- | --- | ---
