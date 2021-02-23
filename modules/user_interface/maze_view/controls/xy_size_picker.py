from modules.common_structures.xy import XY
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QWidget, QSpinBox, QHBoxLayout, QLabel


class XYPicker(QWidget):
    __ySpinBox: QSpinBox
    __xSpinBox: QSpinBox

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A horizontal dual spin box widget designed for the XY size of a maze.
        """
        super(XYPicker, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        mazeSizePickerLayout = QHBoxLayout()
        mazeSizePickerLayout.setContentsMargins(0, 0, 0, 0)

        self.__xSpinBox = QSpinBox()
        self.__ySpinBox = QSpinBox()

        self.__xSpinBox.setMinimum(2)
        self.__ySpinBox.setMinimum(2)

        self.__xSpinBox.setMaximum(250)
        self.__ySpinBox.setMaximum(250)

        mazeSizePickerLayout.addWidget(self.__xSpinBox)
        mazeSizePickerLayout.addWidget(QLabel("by"))
        mazeSizePickerLayout.addWidget(self.__ySpinBox)

        self.setLayout(mazeSizePickerLayout)

    def getValues(self) -> XY:
        """Get the X and Y values of this input widget.

        Returns
        -------
        Tuple[int, int]
            The X and Y values of the number picker spin boxes.
        """
        return XY(
            self.__xSpinBox.value(),
            self.__ySpinBox.value(),
        )