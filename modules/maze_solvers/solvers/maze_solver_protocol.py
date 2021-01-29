from abc import abstractmethod
import copy
import logging
from modules.maze_solvers.relative_direction import RelativeDirection
from modules.maze_solvers.commands.results.detection_command_result import (
    DetectionCommandResult,
)
from modules.common_structures.xy import XY
from modules.maze_solvers.absolute_direction import AbsoluteDirection
from modules.data_structures.maze.maze import Maze
from modules.maze_solvers.maze_solver_state import MazeSolverState
from modules.maze_solvers.commands.commands.maze_solver_command import MazeSolverCommand
from modules.maze_solvers.commands.results.maze_solver_command_result import (
    MazeSolverCommandResult,
)
from typing import List


class MazeSolver:
    # List of commands issued
    _commands: List[MazeSolverCommand]

    # The current state of the Maze Solver
    _state: MazeSolverState

    # the actual maze
    __maze: Maze

    # stage of algorithm
    __step = 0

    def __init__(
        self,
        maze: Maze,
        startingPosition: XY,
        startingDirection: AbsoluteDirection = AbsoluteDirection.north,
    ) -> None:
        self.__maze = maze
        # initialize the solver's state to the default start state
        self._state = MazeSolverState(
            currentCell=startingPosition,
            facingDirection=startingDirection,
            solverSpecificVariables=dict(),
        )
        # init commands list to an empty list
        self._commands = []

        # init step to 0 by default
        self._setAlgorithmStep(0)

    def _moveForward(self) -> MazeSolverCommandResult:
        logging.info(
            f"Attempting to move {self._state.facingDirection} from cell {self._state.currentCell}."
        )

        # get the walls of the agent's current cell
        walls = self.__maze.getWallsOfCellAtCoordinate(self._state.currentCell)

        # check we're moving in a valid direction
        if self._state.facingDirection in walls:
            # we are trying to move into a wall!
            logging.info(
                f"Cannot move forward, wall is in direction {self._state.facingDirection} (walls: {walls})"
            )
            return MazeSolverCommandResult(
                False,
                f"{self._state.facingDirection} wall exists in cell {self._state.currentCell}",
                self._state,
            )
        else:
            # there's no wall in that direction
            # so get the index of the current cell for use later
            cellIndex = self.__maze.getIndexFromCoordinates(self._state.currentCell)

            # get the connections of this cell and their directions (using the index we just got)
            connectionsAndDirections = (
                self.__maze.getConnectionsAndDirectionsOfConnectionsOfCellAtIndex(
                    cellIndex
                )
            )

            # iterate through each of the Tuple[XY, AbsoluteDirection] in
            # connectionsAndDirections to find the one we're facing
            for connection in connectionsAndDirections:
                if connection[1] == self._state.facingDirection:
                    # this is the direction we want to go in, and there
                    # are no walls in the way! so, update our state to
                    # reflect that we're moving to this new cell.
                    self._state.currentCell = connection[0]
                    logging.info(f"Updated agent's currentCell to {connection[0]}")
                    return MazeSolverCommandResult(
                        True,
                        f"Moved {self._state.facingDirection}",
                        self._state,
                    )

            errorMessage = f"FATAL – direction {self._state.facingDirection} not found in list Tuple[XY, AbsoluteDirection]: {connectionsAndDirections}"
            logging.error(errorMessage)
            raise Exception(errorMessage)

    def _turn(self, relativeDirection: RelativeDirection) -> MazeSolverCommandResult:
        # turn with a relative direction
        newDirection = AbsoluteDirection.fromRelativeDirection(
            relativeDirection, self._state.facingDirection
        )
        self._state.facingDirection = newDirection
        logging.info(f"Agent turned {relativeDirection} to face {newDirection}.")

        return MazeSolverCommandResult(
            True,
            f"Turned to face {newDirection}",
            self._state,
        )

    def _turnAbsolute(self, direction: AbsoluteDirection) -> MazeSolverCommandResult:
        if self._state.facingDirection == direction:
            # already facing that direction, so log it because it's a bit weird

            # log as info
            logging.info(
                f"Agent attempted to turn to the direction it is already currently facing: {direction}"
            )
            # and return the same state we started with
            return MazeSolverCommandResult(
                True,
                f"Already facing direction {direction}",
                self._state,
            )

        # log the turn on debug
        logging.info(f"Agent turned from {self._state.facingDirection} to {direction}")

        # update the state with the new direction
        self._state.facingDirection = direction

        # return updated state
        return MazeSolverCommandResult(
            True,
            f"Turned to face {direction}",
            self._state,
        )

    def _detectForward(self) -> DetectionCommandResult:
        walls = self.__maze.getWallsOfCellAtCoordinate(self._state.currentCell)
        obstacleInFront = self._state.facingDirection in walls

        return DetectionCommandResult(
            True,
            obstacleInFront,
            (
                # construct our lovely human-readable command result message
                ("Obstacle" if obstacleInFront else "Nothing")
                + f" detected in direction {self._state.facingDirection}"
            ),
            self._state,
        )

    def _saveCommandToHistory(self, command: MazeSolverCommand) -> None:
        # save a deep copy of the command because we don't want to copy by reference,
        # we want to copy by value. this means that when the variable inevitably mutates
        # in the future, it will not impact the previously saved states.
        self._commands.append(copy.deepcopy(command))

    def getCompletedCommandsList(self) -> List[MazeSolverCommand]:
        """Returns a list of the commands performed by the solver, with their command results and new solver states.
        This method is used to get a list of:
        ```
            1. MazeSolverCommands
                1.1. MazeSolverCommandType
                1.2. Human-readable description
                1.3. MazeSolverCommandResult (optional)
                    1.3.1. success (bool)
                    1.3.2. Human readable description
                    1.3.3. MazeSolverState
        ```

        Returns:
            List[MazeSolverCommand]: List of commands that have been performed by the solver.
        """
        # commands are separate from state and
        # the state should never be modified
        # because of the command list.
        # commands are solely for feedback to user.

        # (and the history of MazeSolverStates so the user can see the progress of the solver in more depth)
        return self._commands

    def _setAlgorithmStep(self, stage: int) -> None:
        self.__step = stage

    def _getAlgorithmStep(self) -> int:
        return self.__step

    @abstractmethod
    def advance(self) -> MazeSolverCommandResult:
        """Used to `advance` the solver by one solver instruction.

        Returns:
            MazeSolverCommandResult: The result of the next instruction.
        """
        raise NotImplementedError()

    def getCurrentState(self) -> MazeSolverState:
        # the current state of the maze solver
        return self._state
