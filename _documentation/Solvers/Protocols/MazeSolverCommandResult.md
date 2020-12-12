# MazeSolverCommandResult

| | |
-|-
Type | `Protocol class`
Super | NA
Delcared in | `modules/maze_solvers/commands/protocols/maze_solver_command_result.py`
Description | The protocol for any maze solver command result to conform to. For example, [`.detection`](../CommandResults/DetectionCommandResult.md).

---

## Variables

Name | Type | Default Value | Comment
 --- | --- | --- | ---
`humanDescription` | `str` | NA | Human-readable description of the command

## Methods

Name | Return Type | Comment
 --- | --- | ---
 `__repr__` | `str` | Returns a human-readable description of the maze solver command result
 `__init__` | `None` | Initialiser for the `MazeSolverCommandResult`