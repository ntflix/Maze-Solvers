from modules.common_structures.xy import XY
from typing import Any, Optional, Tuple
from PyQt6.QtWidgets import QWidget, QSpinBox, QHBoxLayout, QLabel


class XYPicker(QWidget):
    __ySpinBox: QSpinBox
    __xSpinBox: QSpinBox

    def __init__(
        self,
        minimum: XY,
        maximum: XY,
        initialValue: XY,
        parent: Optional[QWidget] = None,
        label: str = "by",
        *args: Tuple[Any, Any],
        **kwargs: Tuple[Any, Any],
    ) -> None:
        """
        A horizontal dual spin box widget designed for the XY size of a maze.
        """
        valid = True
        if (initialValue.x < minimum.x) or (initialValue.y > maximum.y):
            valid = False
        elif (initialValue.x < minimum.x) or (initialValue.y > maximum.y):
            valid = False

        if not valid:
            raise ValueError(
                f"Initial value for XYPicker must be between {minimum} and {maximum}."
            )

        super(XYPicker, self).__init__(parent=parent, *args, **kwargs)
        self.setContentsMargins(0, 0, 0, 0)

        mazeSizePickerLayout = QHBoxLayout()
        mazeSizePickerLayout.setContentsMargins(0, 0, 0, 0)

        self.__xSpinBox = QSpinBox()
        self.__ySpinBox = QSpinBox()

        self.__xSpinBox.setMinimum(minimum.x)
        self.__ySpinBox.setMinimum(minimum.y)

        self.__xSpinBox.setMaximum(maximum.x)
        self.__ySpinBox.setMaximum(maximum.y)

        self.__xSpinBox.setValue(initialValue.x)
        self.__ySpinBox.setValue(initialValue.y)

        mazeSizePickerLayout.addWidget(self.__xSpinBox)
        mazeSizePickerLayout.addWidget(QLabel(label))
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