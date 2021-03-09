from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from typing import Optional
from modules.data_structures.maze.maze_protocol import MazeProtocol
from modules.file_handling.maze.maze_file_handler import MazeFileHandler
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.main_window import MazeSolverUI
import logging


class UIStateModel:
    __ui: MazeSolverUI
    __maze: Optional[MazeProtocol]
    __agent: Optional[MazeSolver] = None
    __solverSpecification: Optional[MazeSolverSpecification]
    __agentVariablesWindowVisible: bool = False

    def __init__(self) -> None:
        self.__initUI()

    def __initUI(self) -> None:
        self.__ui = MazeSolverUI(
            agent=self.__agent,
            onLoadLastMazePressed=self.__onLoadLastMazePressed,
            onMazeFilePathChosen=self.__onMazeFilePathChosen,
            onPlayButtonPressed=self.__onPlayButtonPressed,
            onPauseButtonPressed=self.__onPauseButtonPressed,
            onStepButtonPressed=self.__onStepButtonPressed,
            onRestartButtonPressed=self.__onRestartButtonPressed,
            onSpeedControlValueChanged=self.__onSpeedControlValueChanged,
            onOpenLogButtonPressed=self.__onOpenLogButtonPressed,
            onGenerateMazeButtonPressed=self.__onGenerateMazeButtonPressed,
            onSolveButtonPressed=self.__onSolveButtonPressed,
            onAgentVariablesButtonPressed=self.__onAgentVariablesButtonPressed,
        )

    def __onMazeInstantiated(self, maze: MazeProtocol) -> None:
        logging.debug(f"Maze {maze} instantiated")
        self.__maze = maze

        self.__ui.showMazeViewWindow(self.__maze)
        self.__ui.setMazeSolverControlsEnabled.emit(False)

    def __onLoadLastMazePressed(self) -> None:
        print("__onLoadLastMazePressed")

    def __onMazeFilePathChosen(self, filePath: str) -> None:
        maze: MazeProtocol
        mazeIsValid = False

        while not mazeIsValid:
            fileHandler = MazeFileHandler(filePath)
            try:
                maze = fileHandler.load()
            except FileNotFoundError as noFileError:
                logging.error(f"Maze file does not exist: {noFileError}")
                raise FileNotFoundError()
            except RuntimeError as invalidFileError:
                logging.error(f"Invalid maze file: {invalidFileError}")
                raise FileNotFoundError()
            else:
                logging.debug(f"Maze loaded from `{filePath}` successfully.")
                self.__onMazeInstantiated(maze)
                break

    def __onPlayButtonPressed(self) -> None:
        print("__onPlayButtonPressed")

    def __onPauseButtonPressed(self) -> None:
        print("__onPauseButtonPressed")

    def __onStepButtonPressed(self) -> None:
        # Step through the maze solver by one command
        result = self.__agent.advance()  # type: ignore # maze solver agent is bound here so we can unwrap optional value
        logging.debug(result)
        # update UI
        if self.__agent is not None:
            self.__ui.onMazeSolverAgentUpdate(self.__agent)
        print("__onStepButtonPressed")

    def __onRestartButtonPressed(self) -> None:
        print("__onRestartButtonPressed")

        self.__onSolveButtonPressed(
            self.__solverSpecification,  # type: ignore
        )

    def __onSpeedControlValueChanged(self, newValue: int) -> None:
        print(f"__onSpeedControlValueChanged: {newValue}")

    def __onOpenLogButtonPressed(self) -> None:
        print("__onOpenLogButtonPressed")

    def __onGenerateMazeButtonPressed(
        self,
        mazeSpecification: MazeGenerationSpecification,
    ) -> None:
        logging.debug(
            f"Generate Maze button pressed with maze specification: {mazeSpecification}"
        )
        print("__onGenerateMazeButtonPressed", mazeSpecification)

    def __onSolveButtonPressed(
        self,
        solverSpecification: MazeSolverSpecification,
    ):
        print(f"__onSolveButtonPressed {solverSpecification}")
        self.__solverSpecification = solverSpecification
        self.__agent = self.__instantiateSolver(solverSpecification)
        self.__ui.setMazeSolverControlsEnabled.emit(True)
        # send the mazeSolverUpdate event to the UI with our new solver agent
        self.__ui.onMazeSolverAgentUpdate(self.__agent)
        # only update the agent vars window if it is already open
        if self.__agentVariablesWindowVisible:
            self.__ui.showAgentVariablesWindow()

    def __instantiateSolver(
        self, solverSpecification: MazeSolverSpecification
    ) -> MazeSolver:
        return solverSpecification.solverType(  # see how awesome protocols are? you can do stuff like this with complete safety!
            maze=self.__maze,  # type: ignore # maze is not optional here, as the solver controls view is only present when a MazeView is present
            startingPosition=solverSpecification.startPosition,
        )

    def startApplication(self) -> int:
        self.__ui.showMazeLoader()
        return self.__ui.exec()

    def __onAgentVariablesButtonPressed(self) -> None:
        if self.__agent is not None:
            self.__agentVariablesWindowVisible = True
            self.__ui.showAgentVariablesWindow()
