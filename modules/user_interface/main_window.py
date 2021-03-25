from modules.user_interface.agent_windows.log import AgentLogView
from modules.user_interface.agent_windows.agent_variables import AgentVariablesView
from modules.maze_solvers.solvers.maze_solver_protocol import MazeSolver
from modules.user_interface.ui_translation.maze_solver_specification import (
    MazeSolverSpecification,
)
from PyQt6.QtCore import pyqtSignal
from modules.user_interface.ui_translation.maze_generation_specification import (
    MazeGenerationSpecification,
)
from modules.user_interface.maze_loader_windows.maze_loader_view import MazeLoaderView
from modules.user_interface.maze_view.maze_view_window import MazeViewWindow
from modules.data_structures.maze.maze_protocol import MazeProtocol
from typing import Callable, List, Optional
from PyQt6.QtWidgets import QApplication


class MazeSolverUI(QApplication):
    __mazeLoaderWindow: MazeLoaderView
    __mazeViewWindow: MazeViewWindow
    __agent: Optional[MazeSolver] = None
    __agentVarsWindow: Optional[AgentVariablesView] = None
    __agentLogWindow: Optional[AgentLogView] = None

    __onLoadLastMazePressed: Callable[[], None]
    __onMazeFilePathChosen: Callable[[str], None]
    __onPlayButtonPressed: Callable[[], None]
    __onPauseButtonPressed: Callable[[], None]
    __onStepButtonPressed: Callable[[], None]
    __onRestartButtonPressed: Callable[[], None]
    __onSpeedControlValueChanged: Callable[[int], None]
    __onOpenLogButtonPressed: Callable[[], None]
    __onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None]
    __onSolveButtonPressed: Callable[[MazeSolverSpecification], None]

    setMazeSolverControlsEnabled = pyqtSignal(bool)
    setMazeGeneratorControlsEnabled = pyqtSignal(bool)

    def __init__(
        self,
        agent: Optional[MazeSolver],
        onLoadLastMazePressed: Callable[[], None],
        onMazeFilePathChosen: Callable[[str], None],
        onPlayButtonPressed: Callable[[], None],
        onPauseButtonPressed: Callable[[], None],
        onStepButtonPressed: Callable[[], None],
        onRestartButtonPressed: Callable[[], None],
        onSpeedControlValueChanged: Callable[[int], None],
        onOpenLogButtonPressed: Callable[[], None],
        onGenerateMazeButtonPressed: Callable[[MazeGenerationSpecification], None],
        onSolveButtonPressed: Callable[[MazeSolverSpecification], None],
        onAgentVariablesButtonPressed: Callable[[], None],
        argv: List[str] = [],
    ) -> None:
        """
        Overarching controller for the whole UI.
        ### Keeps track of:
            • The Maze that has (or has not yet) been generated
        """
        super(MazeSolverUI, self).__init__(argv)

        self.__agent = agent
        self.__onLoadLastMazePressed = onLoadLastMazePressed
        self.__onMazeFilePathChosen = onMazeFilePathChosen
        self.__onPlayButtonPressed = onPlayButtonPressed
        self.__onPauseButtonPressed = onPauseButtonPressed
        self.__onStepButtonPressed = onStepButtonPressed
        self.__onRestartButtonPressed = onRestartButtonPressed
        self.__onSpeedControlValueChanged = onSpeedControlValueChanged
        self.__onOpenLogButtonPressed = onOpenLogButtonPressed
        self.__onGenerateMazeButtonPressed = onGenerateMazeButtonPressed
        self.__onSolveButtonPressed = onSolveButtonPressed
        self.__onAgentVariablesButtonPressed = onAgentVariablesButtonPressed

    def showMazeLoader(self) -> None:
        # construct a maze loader view
        self.__mazeLoaderWindow = MazeLoaderView(
            onMazeLoadedFromPath=self.__onMazeFilePathChosen,
            onLoadLastMazePressed=self.__onLoadLastMazePressed,
            onMazeSpecificationChosen=self.__onGenerateMazeButtonPressed,
        )
        # connect to method to call when maze is loaded
        self.__mazeLoaderWindow.show()

    def showMazeViewWindow(self, maze: MazeProtocol) -> None:
        self.__mazeLoaderWindow.destroy(True, True)

        # try:
        self.__mazeViewWindow = MazeViewWindow(
            maze=maze,
            solver=self.__agent,
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

        # self.__mazeViewWindow.onMazeSolverAgentUpdate.connect(
        #     self.onMazeSolverAgentUpdate
        # )

        # except:
        #     raise UnboundLocalError(
        #         "Attempted to load a maze that had not yet been instantiated."
        #     )

        # connect enable/disable view signal for maze generator controls enabled
        self.setMazeSolverControlsEnabled.connect(
            self.__mazeViewWindow.setMazeSolverControlsEnabled
        )
        # connect enable/disable view signal for maze solver controls enabled
        self.setMazeGeneratorControlsEnabled.connect(
            self.__mazeViewWindow.setMazeGeneratorControlsEnabled
        )

        self.__mazeViewWindow.show()

    def onMazeSolverAgentUpdate(self, agent: MazeSolver) -> None:
        self.__agent = agent
        # connect the onMazeSolverAgentUpdate signal to the mazeView Window
        self.__mazeViewWindow.onMazeSolverAgentUpdate.emit(agent)
        # connect signal to the agent variables window
        if self.__agentVarsWindow is not None:
            self.__agentVarsWindow.onSolverVariablesChange.emit(
                self.__agent.getCurrentState().solverSpecificVariables
            )

        if self.__agentLogWindow is not None:
            commandsList = self.__agent.getCompletedCommandsList()
            self.__agentLogWindow.onLogUpdate(commandsList)

    def showAgentVariablesWindow(self) -> None:
        if self.__agent is not None:
            self.__agentVarsWindow = AgentVariablesView(
                variables=self.__agent.getCurrentState().solverSpecificVariables,
            )

            self.__agentVarsWindow.show()

    def showAgentLogWindow(self) -> None:
        if self.__agent is not None:
            self.__agentLogWindow = AgentLogView()
            self.__agentLogWindow.show()
