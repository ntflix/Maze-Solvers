# MazeSolverCommand

| | |
-|-
Type | `Protocol class`
Super | NA
Delcared in | `modules/maze_solvers/commands/protocols/command_protocol.py`
Description | The protocol for any maze solver command to conform to.

---

## Variables

Name | Type | Default Value | Comment
 --- | --- | --- | ---
`humanDescription` | `str` | NA | Human-readable description of the command
`commandType` | [`MazeSolverCommandType`](MazeSolverCommandType) | NA | Type of the command (e.g., `.movement`)
`commandResult` | `Optional[`[`MazeSolverCommandResult`](MazeSolverCommandResult)`]` | `None` | Result of command – `None` if command not completed.

## Methods

Name | Return Type | Comment
 --- | --- | ---
 `__repr__` | `str` | Returns a human-readable description of the maze solver command
 `__init__` | `None` | Initializes a MazeSolverCommand class