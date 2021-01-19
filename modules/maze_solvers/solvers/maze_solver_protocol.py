from abc import abstractmethod
import logging
from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.maze_solver_state import MazeSolverState
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from typing import List, Tuple


class MazeSolver:
    # List of commands issued
    __commands: List[Tuple[MazeSolverCommand, MazeSolverState]]

    # The current state of the Maze Solver
    __state: MazeSolverState

    # the history of states so the user can see the progress of the solver in more depth
    __state_history: List[MazeSolverState]

    # the actual maze
    __maze: Maze

    def __init__(
        self,
        maze: Maze,
        startingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        self.__maze = maze
        # initialize the solver's state to the default start state
        self.__state = MazeSolverState(
            currentCell=startingPosition,
            facingDirection=startingDirection,
            solverSpecificVariables=dict(),
        )
        # initialize state history to an empty list
        self.__state_history = []
        # init commands list to an empty list
        self.__commands = []

    def __moveForward(self) -> MazeSolverCommandResult:
        logging.debug(
            f"Attempting to move {self.__state.facingDirection} from cell {self.__state.currentCell}."
        )

        walls: List[AbsoluteDirection] = self.__maze.getWallsOfCellAtCoordinate(self.__state.currentCell)
        if
        raise NotImplementedError()

    def __turn(self, direction: AbsoluteDirection) -> MazeSolverCommandResult:
        raise NotImplementedError()

    def __detectForward(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.
        """
        raise NotImplementedError()

    @abstractmethod
    def getCompletedCommandsWithNewStateList(
        self,
    ) -> List[Tuple[MazeSolverCommand, MazeSolverState]]:
        # commands are separate from state and
        # the state should never be modified
        # because of the command list.
        # commands are solely for feedback to user.

        # and the history of MazeSolverStates so the user can see the progress of the solver in more depth
        raise NotImplementedError()

    @abstractmethod
    def getCurrentState(self) -> MazeSolverState:
        # the current state of the maze solver
        raise NotImplementedError()
