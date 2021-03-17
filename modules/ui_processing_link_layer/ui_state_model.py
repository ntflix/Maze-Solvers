from modules.maze_generation.recursive_backtracker import RecursiveBacktracker
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
import threading  #  so we can run the sleep ops and maze solver operations on a different thread to not freeze the UI
from time import sleep


class UIStateModel:
    __ui: MazeSolverUI
    __maze: Optional[MazeProtocol] = None
    __agent: Optional[MazeSolver] = None
    __solverSpecification: Optional[MazeSolverSpecification] = None
    __agentVariablesWindowVisible: bool = False
    __solverRate: int = 25
    __solverIsActive = False

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
        self.__solverIsActive = False
        self.__performSolver()
        print("__onPlayButtonPressed")

    def __onPauseButtonPressed(self) -> None:
        self.__solverIsActive = False
        print("__onPauseButtonPressed")

    def __onStepButtonPressed(self) -> None:
        self.__solverIsActive = False
        self.__stepSolver()
        print("__onStepButtonPressed")

    def __onRestartButtonPressed(self) -> None:
        self.__solverIsActive = False
        print("__onRestartButtonPressed")
        # simply call the '__onSolveButtonPressed' method with the _existing_ solver specification
        if self.__solverSpecification is not None:
            self.__onSolveButtonPressed(
                self.__solverSpecification,
            )

    def __onSpeedControlValueChanged(self, newValue: int) -> None:
        self.__solverRate = newValue
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

        maze: MazeProtocol

        if mazeSpecification.simplyConnected == True:
            # generate a simply connected maze
            maze = RecursiveBacktracker(mazeSpecification.size).generate()
        else:
            # generate a non-simple maze
            maze = RecursiveBacktracker(mazeSpecification.size).generate()
            raise NotImplementedError(
                "No non-simple maze generation algorithms implemented yet"
            )

        #  maze instantiated, so call appropriate method
        self.__onMazeInstantiated(maze)

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
        if self.__maze is not None:
            return solverSpecification.solverType(  # see how awesome protocols are? you can do stuff like this with complete safety!
                maze=self.__maze,
                startingPosition=solverSpecification.startPosition,
                endingPosition=solverSpecification.endPosition,
            )
        else:
            raise RuntimeError(
                "Maze unbound – `self.__maze` is `None` in UIStateModel class"
            )

    def startApplication(self) -> int:
        self.__ui.showMazeLoader()
        return self.__ui.exec()

    def __onAgentVariablesButtonPressed(self) -> None:
        if self.__agent is not None:
            self.__agentVariablesWindowVisible = True
            self.__ui.showAgentVariablesWindow()

    def __stepSolver(self) -> None:
        # Step through the maze solver by one command
        if self.__agent is not None:
            result = self.__agent.advance()
            logging.debug(result)
            # update UI
            self.__ui.onMazeSolverAgentUpdate(self.__agent)

    def __waitThenPerformSolver(self, delay: float) -> None:
        # to be called in a thread. this WILL BLOCK whatever thread it is run on, so don't run it on the main thread at least.
        sleep(delay)
        self.__stepSolver()

    def __performSolver(self) -> None:
        self.__solverIsActive = True
        delay = 1 / self.__solverRate  # e.g., 25 ops/second = 1 ÷ 25 = 0.04 Hz

        def something() -> None:
            self.__waitThenPerformSolver(delay)
            # if self.__agent is not None:
            # self.__ui.onMazeSolverAgentUpdate(self.__agent)
            if self.__solverIsActive:
                self.__performSolver()

        # run the waiting on another thread to not block the UI
        thread = threading.Thread(target=something)
        # start thread
        thread.start()
