from abc import abstractmethod
import logging
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

    def _moveForward(self) -> MazeSolverCommandResult:
        logging.debug(
            f"Attempting to move {self.__state.facingDirection} from cell {self.__state.currentCell}."
        )

        # get the walls of the agent's current cell
        walls = self.__maze.getWallsOfCellAtCoordinate(self.__state.currentCell)

        # check we're moving in a valid direction
        if self.__state.facingDirection in walls:
            # we are trying to move into a wall!
            logging.debug(
                f"Cannot move forward, wall is in direction {self.__state.facingDirection} (walls: {walls})"
            )
            return MazeSolverCommandResult(
                False,
                f"{self.__state.facingDirection} wall exists in cell {self.__state.currentCell}",
                self.__state,
            )
        else:
            # there's no wall in that direction
            # so get the index of the current cell for use later
            cellIndex = self.__maze.getIndexFromCoordinates(
                self.__state.currentCell.x,
                self.__state.currentCell.y,
            )

            # get the connections of this cell and their directions (using the index we just got)
            connectionsAndDirections = (
                self.__maze.getConnectionsAndDirectionsOfConnectionsOfCellAtIndex(
                    cellIndex
                )
            )

            # iterate through each of the Tuple[XY, AbsoluteDirection] in
            # connectionsAndDirections to find the one we're facing
            for connection in connectionsAndDirections:
                if connection[1] == self.__state.facingDirection:
                    # this is the direction we want to go in, and there
                    # are no walls in the way! so, update our state to
                    # reflect that we're moving to this new cell.
                    self.__state.currentCell = connection[0]
                    logging.debug(f"Updated agent state currentCell to {connection[0]}")
                    return MazeSolverCommandResult(
                        True,
                        f"Moved {self.__state.facingDirection}",
                        self.__state,
                    )

            errorMessage = f"FATAL – direction {self.__state.facingDirection} not found in list Tuple[XY, AbsoluteDirection]: {connectionsAndDirections}"
            logging.error(errorMessage)
            raise Exception(errorMessage)

    def _turn(self, relativeDirection: relativeDirection) -> MazeSolverCommandResult:
        # turn with a relative direction

        logging.debug(f"Attempting to turn agent {relativeDirection}")

    def _turn(self, direction: AbsoluteDirection) -> MazeSolverCommandResult:
        if self.__state.facingDirection == direction:
            # already facing that direction, so log it because it's a bit weird

            # log as info
            logging.info(
                f"Agent attempted to turn to the direction it is already currently facing: {direction}"
            )
            # and return the same state we started with
            return MazeSolverCommandResult(
                True,
                f"Already facing direction {direction}",
                self.__state,
            )
        # not facing the same direction

        # log it on debug
        logging.debug(
            f"Agent turned from {self.__state.facingDirection} to {direction}"
        )

        # update the state with the new direction
        self.__state.facingDirection = direction

        # return updated state
        return MazeSolverCommandResult(
            True,
            f"Turned to face {direction}",
            self.__state,
        )

    def _detectForward(self) -> DetectionCommandResult:
        walls = self.__maze.getWallsOfCellAtCoordinate(self.__state.currentCell)
        obstacleInFront = self.__state.facingDirection in walls

        return DetectionCommandResult(
            True,
            obstacleInFront,
            (
                # construct our lovely human-readable command result message
                ("Obstacle" if obstacleInFront else "Nothing")
                + f" detected in direction {self.__state.facingDirection}"
            ),
            self.__state,
        )

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
