class MazeCell:
    index: int

    def __init__(self, index: int) -> None:
        super().__init__()
        self.index = index

    def __str__(self) -> str:
        return f"MazeCell ({self.index})"