from modules.data_structures.maze.maze.maze import Maze
import unittest


class TestMazeMethods(unittest.TestCase):

    ###
    ### Test initialisation of mazes
    ###

    def testInit(self):
        maze = Maze(20, 20)
        self.assertIsInstance(maze, Maze)

    def testFullyConnectedInit(self):
        maze = Maze(4, 4, False)
        self.assertIsInstance(maze, Maze)
        self.assertCountEqual(maze.getConnectionsOfCellAtIndex(0), [1, 4])
        self.assertCountEqual(maze.getConnectionsOfCellAtIndex(5), [1, 4, 6, 9])

    def testInitWithZeroSize(self):
        maze = Maze(0, 0)
        self.assertIsInstance(maze, Maze)

    def testInitWithInvalidSize(self):
        with self.assertRaises(
            ValueError,
            msg="Invalid size `(-5, -7)` given.",
        ):
            _ = Maze(-5, -7)

    def testInitWithInvalidXSize(self):
        with self.assertRaises(
            ValueError,
            msg="Invalid size `(-21, 7)` given.",
        ):
            _ = Maze(-21, 7)

    def testInitWithInvalidYSize(self):
        with self.assertRaises(
            ValueError,
            msg="Invalid size `(4, -66)` given.",
        ):
            _ = Maze(4, -66)

    ###
    ### Test `getNeighboursOfCell` method
    ###

    def testGetNeighbourOfCornerCell(self):
        neighbours = Maze(20, 20).getNeighboursOfCell(0)
        actualNeighbours = [1, 20]

        self.assertCountEqual(neighbours, actualNeighbours)

    def testGetNeighbourOfWallCell(self):
        neighbours = Maze(20, 20).getNeighboursOfCell(1)
        actualNeighbours = [0, 2, 21]

        self.assertCountEqual(neighbours, actualNeighbours)

    def testGetNeighbourOfSurroundedCell(self):
        neighbours = Maze(20, 20).getNeighboursOfCell(189)
        actualNeighbours = [169, 209, 188, 190]

        self.assertCountEqual(neighbours, actualNeighbours)

    def testGetNeighbourOfOutOfRangeTooHighCell(self):
        maze = Maze(4, 4)

        with self.assertRaises(
            expected_exception=IndexError,
            msg="`cellIndex` out of range (500 not between 0 and 15).",
        ):
            _ = maze.getNeighboursOfCell(500)

    def testGetNeighbourOfOutOfRangeTooLowCell(self):
        maze = Maze(4, 4)
        with self.assertRaises(
            expected_exception=IndexError,
            msg="`cellIndex` out of range (-5 not between 0 and 15).",
        ):
            _ = maze.getNeighboursOfCell(-5)

    ###
    ### Test `getCoordinatesOf` method
    ###

    def testGetCoordinateOfFirstCell(self):
        coordinate = Maze(5, 5).getCoordinatesFromIndex(0)
        self.assertEqual(coordinate, (0, 0))

    def testGetCoordinateOfSomeCell(self):
        coordinate = Maze(5, 5).getCoordinatesFromIndex(12)
        self.assertEqual(coordinate, (2, 2))

    def testGetCoordinateOfLastCell(self):
        coordinate = Maze(5, 5).getCoordinatesFromIndex(24)
        self.assertEqual(coordinate, (4, 4))

    def testGetCoordinateOfOutOfRangeTooHighCell(self):
        with self.assertRaises(
            expected_exception=IndexError,
            msg="`cellIndex` out of range (500 not between 0 and 15),",
        ):
            _ = Maze(4, 4).getCoordinatesFromIndex(500)

    def testGetCoordinateOfOutOfRangeTooLowCell(self):
        with self.assertRaises(
            expected_exception=IndexError,
            msg="`cellIndex` out of range (-5 not between 0 and 15),",
        ):
            _ = Maze(4, 4).getCoordinatesFromIndex(-5)

    ###
    ### Test adding walls between cells and getting connections
    ###

    def testAddWall(self):
        maze = Maze(4, 4, False)
        # add a wall from first cell
        maze.addWallBetween(0, 1)
        self.assertCountEqual(maze.getConnectionsOfCellAtIndex(0), [4])
        # add another wall from first cell
        maze.addWallBetween(0, 4)
        self.assertCountEqual(maze.getConnectionsOfCellAtIndex(0), [])

    def testAddExistentWall(self):
        maze = Maze(3, 3, True)
        # add a wall that already exists
        with self.assertRaises(
            Exception,
            msg="Node index 1 already does not exist in node at index 0's connections.",
        ):
            maze.addWallBetween(0, 1)

    def testAddWallBetweenSelf(self):
        maze = Maze(2, 2)
        # add a wall between `x` and `x`, i.e., to itself
        with self.assertRaises(
            Exception,
            msg="Node index 0 already does not exist in node at index 0's connections.",
        ):
            maze.addWallBetween(0, 0)

    def testAddWallBetweenNonAdjacentCells(self):
        maze = Maze(3, 3)
        # add invalid wall between top left and bottom right cells
        with self.assertRaises(
            ValueError,
            msg="Cell at index 0 is not adjacent to cell at 8.",
        ):
            maze.addWallBetween(0, 8)

    def testAddWallFromNonExistentCell(self):
        maze = Maze(2, 2)
        with self.assertRaises(
            IndexError,
            msg="`cellIndex` out of range (55 not between 0 and 3).",
        ):
            maze.addWallBetween(55, 2)

    def testAddWallToNonExistentCell(self):
        maze = Maze(2, 2)
        with self.assertRaises(
            IndexError,
            msg="`cellIndex` out of range (55 not between 0 and 3).",
        ):
            maze.addWallBetween(2, 55)

    ###
    ### Test removing walls between cells and getting connections
    ###

    def testRemoveWall(self):
        maze = Maze(4, 4, True)
        # remove a wall from first cell
        maze.removeWallBetween(0, 1)
        self.assertCountEqual(maze.getConnectionsOfCellAtIndex(0), [1])
        # remove another wall from first cell
        maze.removeWallBetween(0, 4)
        self.assertCountEqual(maze.getConnectionsOfCellAtIndex(0), [1, 4])

    def testRemoveExistentWall(self):
        maze = Maze(3, 3, False)
        # remove a wall that doesn't exist
        with self.assertRaises(
            Exception,
            msg="Node index '1' already exists in node 0's connections.",
        ):
            maze.removeWallBetween(0, 1)

    def testRemoveWallBetweenSelf(self):
        maze = Maze(2, 2)
        # remove a wall between `x` and `x`, i.e., to itself
        with self.assertRaises(
            ValueError,
            msg="Cell at index 0 is not adjacent to cell at 8.",
        ):
            maze.removeWallBetween(0, 0)

    def testRemoveWallBetweenNonAdjacentCells(self):
        maze = Maze(3, 3)
        # remove invalid wall between top left and bottom right cells
        with self.assertRaises(
            ValueError,
            msg="Cell at index 0 is not adjacent to cell at 0.",
        ):
            maze.removeWallBetween(0, 8)

    def testRemoveWallFromNonExistentCell(self):
        maze = Maze(2, 2)
        with self.assertRaises(
            IndexError,
            msg="`cellIndex` out of range (55 not between 0 and 3).",
        ):
            maze.removeWallBetween(55, 2)

    def testRemoveWallToNonExistentCell(self):
        maze = Maze(2, 2)
        with self.assertRaises(
            IndexError,
            msg="`cellIndex` out of range (55 not between 0 and 3).",
        ):
            maze.removeWallBetween(2, 55)

    ###
    ### Test getting cells' coordinates from indices
    ###

    def testGetFirstCellCoordinatesFromIndex(self):
        maze = Maze(2, 2)
        # first cell in maze should be (0, 0)
        c = maze.getCoordinatesFromIndex(0)
        self.assertEqual(c, (0, 0))

    def testGetCentreCellCoordinatesFromIndex(self):
        maze = Maze(3, 3)
        # getting centre cell, should be (1, 1)
        c = maze.getCoordinatesFromIndex(4)
        self.assertEqual(c, (1, 1))

    def testGetLastCellCoordinatesFromIndex(self):
        maze = Maze(3, 3)
        # getting last cell in maze, should be (2, 2)
        c = maze.getCoordinatesFromIndex(8)
        self.assertEqual(c, (2, 2))

    def testGetOutOfRangeTooLowCellCoordinatesFromIndex(self):
        maze = Maze(1, 1)
        # get too low cell index coordinates
        with self.assertRaises(
            IndexError,
            msg="`cellIndex` out of range (-4 not between 0 and 0).",
        ):
            _ = maze.getCoordinatesFromIndex(-4)

    def testGetOutOfRangeTooHighCellCoordinatesFromIndex(self):
        maze = Maze(1, 1)
        # get too high cell index coordinates
        with self.assertRaises(
            IndexError,
            msg="`cellIndex` out of range (55 not between 0 and 0).",
        ):
            _ = maze.getCoordinatesFromIndex(55)

    ###
    ### Test getting cells' indices from coordinates
    ###

    def testGetFirstCellIndexFromCoordinates(self):
        maze = Maze(2, 2)
        index = maze.getIndexFromCoordinates(0, 0)
        self.assertEqual(index, 0)

    def testGetCentreCellIndexFromCoordinates(self):
        maze = Maze(3, 3)
        index = maze.getIndexFromCoordinates(1, 1)
        self.assertEqual(index, 4)

    def testGetLastCellIndexFromCoordinates(self):
        maze = Maze(3, 3)
        index = maze.getIndexFromCoordinates(2, 2)
        self.assertEqual(index, 8)

    def testGetOutOfRangeCellTooLowIndexFromCoordinate(self):
        maze = Maze(1, 1)
        with self.assertRaises(
            ValueError,
            msg="Coordinate (-44, 0) is not valid.",
        ):
            _ = maze.getIndexFromCoordinates(-44, 0)

    def testGetOutOfRangeCellTooHighIndexFromCoordinate(self):
        maze = Maze(1, 1)
        with self.assertRaises(
            ValueError,
            msg="Coordinate (72, 0) is not valid.",
        ):
            _ = maze.getIndexFromCoordinates(72, 0)


if __name__ == "__main__":
    unittest.main()