#!python3.9

# support type hinting in editor and code
from typing import Generator, Generic, Iterator, List, Optional, TypeVar

# circular queue for breadth first search
from modules.data_structures.circular_queue.circular_queue import CircularQueue

# graph node
from modules.data_structures.graph.node import Node

T = TypeVar("T")


class Graph(Generic[T]):
    """A binary graph of type {T}."""

    __nodes: List[Node[T]] = []  #  the list of nodes of this graph

    def __init__(self, nodes: Optional[list[Node[T]]] = None):
        """Constructor for a binary tree of type {T}.

        Args:
            type (T): The value type of the values of the nodes of the tree. For example, a tree storing names would have a value type of {str}.

        Returns:
            None.

        Instantiating a graph:
        >>> graph = Graph[str]()
        >>> graph
        []
        """

        # Check if any nodes were provided
        if nodes is not None:
            # And if any were, set the nodes to them
            self.setNodesFromNodesList(nodes)

    def __repr__(self) -> str:
        """Return a string representation of this object.

        Returns:
            str: The string representation of this object.
        """
        # map each of the nodes in the graph to a string and put all those into a list
        # and then return the stringified list.
        return str(list(map(str, self.__nodes)))

    def __iter__(self) -> Generator[Node[T], None, None]:
        """Make this class iterable

        Yields:
            Generator[Node[T], None, None]: The nodes of the graph, in the order that the graph was initialized with them.
        """
        for node in self.__nodes:
            yield node

    def __getitem__(self, key: int) -> Optional[T]:
        index = 0
        for node in self:
            if index == key:
                return node.data
            index += 1
        # not found
        raise IndexError(f"Value at index {key} not found.")

    def __len__(self) -> int:
        return len(self.__nodes)

    def getConnectionsOfNodeAtIndex(self, index: int) -> List[int]:
        """Get the connections of a node at specified index.

        Args:
            index (int): The index of the node.

        Returns:
            List[int]: The list indices of its connected cells.
        """
        return self.__nodes[index].connections

    def setNodeData(self, index: int, newValue: T) -> None:
        for nodeIndex in range(len(self)):
            if nodeIndex == index:
                # set the node data bc index is correct
                self.__nodes[nodeIndex].data = newValue
                # make sure to return so we don't loop over everything!
                return
        # not found
        raise IndexError(f"Value at index {index} not found.")

    @staticmethod
    def createGraph(sizeX: int, sizeY: int) -> "Graph[T]":
        """Creates a graph of the specified X and Y size.

        Args:
            sizeX (int): the desired X size of the graph.
            sizeY (int): the desired Y size of the graph.

        Returns:
            Graph[T]: The (empty) graph object (of the given size).

        >>> graph = Graph.createGraph(2, 2)
        >>> [i for i in map(str, graph)]
        ['None -> []', 'None -> []', 'None -> []', 'None -> []']
        """

        if (sizeX < 0) or (sizeY < 0):
            raise ValueError(f"Invalid size `({sizeX}, {sizeY})` given.")

        # make a list of nodes of the correct length
        everyNode = [Node[T](None) for _ in range(0, sizeX * sizeY)]
        return Graph(nodes=everyNode)

    def setNodesFromNodesList(self, nodes: list[Node[T]]) -> None:
        """Set a graph's nodes from a list of nodes.

        Args:
            nodes (list[Node[T]]): The list of nodes from which to set the graph data.

        >>> sampleMaze = Graph[None]()
        >>> sampleMaze.setNodesFromNodesList([
        ...     Node(None,  [1, 4]),         # 0
        ...     Node(None,  [0, 4]),         # 1
        ...     Node(None,  [4, 3]),         # 2
        ...     Node(None,  [2, 4]),         # 3
        ...     Node(None,  [0, 1, 2, 3])    # 4
        ... ])
        >>> sampleMaze
        ['None -> [1, 4]', 'None -> [0, 4]', 'None -> [4, 3]', 'None -> [2, 4]', 'None -> [0, 1, 2, 3]']
        """
        self.__nodes = nodes

    def setNodesFromValuesAndConnections(
        self, values: list[T], connectionsPointers: list[list[int]]
    ) -> None:
        """Give a Tree object some nodes.

        Args:
            values (List[T]): the value of each node.
            connectionsPointers (List[List[int]]): the connections that each node has.

        Setting a graph's nodes from provided data and connections:
        >>> maze = Graph[None]()
        >>> maze.setNodesFromValuesAndConnections([
        ...     None,
        ...     None,
        ...     None,
        ...     None,
        ...     None,
        ... ], [
        ...     [1, 4],
        ...     [0, 4],
        ...     [4, 3],
        ...     [2, 4],
        ...     [0, 1, 2, 3]
        ... ])
        >>> maze
        ['None -> [1, 4]', 'None -> [0, 4]', 'None -> [4, 3]', 'None -> [2, 4]', 'None -> [0, 1, 2, 3]']
        """

        for i in range(len(values)):
            # make new `Node` with this value's data and left and right pointers
            thisNode: Node[T] = Node(data=values[i], connections=connectionsPointers[i])
            self.__nodes.append(thisNode)  # append new node to `self.nodes`

    def connectionExistsFrom(self, indexA: int, indexB: int) -> bool:

        """Check whether there is a connection from provided node index A to index B.

        Args:
            indexA (int): The index of the `from` node – this is checked whether it has a connection to `indexB`.
            indexB (int): The index of the `to` node.

        Returns:
            bool: whether there is a link from node indexA to node indexB.

        Raises:
            IndexError: if the node at `indexA` is nonexistent.

        >>> Graph[str]([
        ...     Node('Entrance', [1]),
        ...     Node('1', [0, 2, 3]),
        ...     Node('2', [1, 4]),
        ...     Node('3', [1, 5]),
        ...     Node('4', [2]),
        ...     Node('5', [3, 6, 7]),
        ...     Node('6', [5, 8]),
        ...     Node('7', [5, 9, 10]),
        ...     Node('Exit', [6, 11]),
        ...     Node('9', [7]),
        ...     Node('10', [7]),
        ...     Node('11', [8])
        ... ]).connectionExistsFrom(0, 1)
        True

        >>> Graph[str]([
        ...     Node('Entrance', [1]),
        ...     Node('1', [0, 2, 3]),
        ...     Node('2', [1, 4]),
        ...     Node('3', [1, 5]),
        ...     Node('4', [2]),
        ...     Node('5', [3, 6, 7]),
        ...     Node('6', [5, 8]),
        ...     Node('7', [5, 9, 10]),
        ...     Node('Exit', [6, 11]),
        ...     Node('9', [7]),
        ...     Node('10', [7]),
        ...     Node('11', [8])
        ... ]).connectionExistsFrom(48, 4)
        Traceback (most recent call last):
        ...
        IndexError: Node at index 48 is nonexistent.
        """
        try:
            # check there's a connection between indexA and indexB
            return indexB in self.__nodes[indexA].connections
        except IndexError:
            raise IndexError("Node at index {} is nonexistent.".format(str(indexA)))

    def __setAllNotVisited(self) -> None:
        """Set all the nodes of the graph's `visited` status to `False`."""
        for node in self.__nodes:
            node.visited = False

    def _exists(self, nodePointer: int) -> bool:
        """Determine whether or not a pointer points to a node which exists.

        Args:
            nodePointer (int): The index of the node the pointer points to.

        Returns:
            bool: Whether the pointer is valid.

        >>> maze = Graph[None]()
        >>> maze.setNodesFromNodesList([
        ...     Node(None,  [1, 4]),         # 0
        ...     Node(None,  [0, 4]),         # 1
        ...     Node(None,  [4, 3]),         # 2
        ...     Node(None,  [2, 4]),         # 3
        ...     Node(None,  [0, 1, 2, 3])    # 4
        ... ])
        >>> maze._exists(4)
        True
        >>> maze._exists(5)
        False
        """

        try:
            _ = self.__nodes[nodePointer].data
        except IndexError:
            # index out of range for `self.__nodes`
            return False
        else:
            # the index is OK
            return True

    def depthFirstTraversal(self, nodeIndex: Optional[int] = None) -> Iterator[T]:
        """Recursively depth-first traverse the graph.
        Yields data — rather than returning it — because returning the values would require putting everything into a list.

        `yield` basically pauses the function after yielding, saving all of its states, and only
        when the next value is required by the caller function does the yielding function continue.

        Complexity of this implementation is `O(V * E)` where `V` is the number of vertices (nodes) and `E` is the number of edges (connections).

        Args:
            currentNode (Optional[int], optional): Specify the node index to start from. Used for recursion; don't worry about this parameter. Defaults to None.

        Raises:
            Exception: The graph is empty, and therefore we cannot traverse it.

        Yields:
            Generator[Node[T]]: The nodes' data in depth-first order.

        >>> sampleGraph = Graph[int]([
        ...     Node(2,  [1, 4]),         # 0
        ...     Node(8,  [0, 4]),         # 1
        ...     Node(42,  [4, 3]),         # 2
        ...     Node(11,  [2, 4]),         # 3
        ...     Node(91,  [0, 1, 2, 3])    # 4
        ... ])
        >>> [item for item in sampleGraph.depthFirstTraversal()]
        [11, 42, 91, 8, 2]

        >>> [item for item in Graph[int]().depthFirstTraversal()]       # test traversal of empty graph
        []
        """

        # check there's actually any nodes
        if len(self.__nodes) < 1:
            # there's no nodes.
            return

        if nodeIndex is None:
            # the function has been called without a starting node so we start from the beginning!
            # so we'll make everything not visited to be able to visit stuff.
            self.__setAllNotVisited()
            # check that there are actually any items in the graph
            if (self.__nodes is []) or (self.__nodes is None):
                # there are no nodes in the graph...
                raise Exception("Cannot traverse an empty graph")
            else:
                # there are nodes in the graph :)
                # ...so we set `nodeIndex` to the first index:
                nodeIndex = 0

        # `nodeIndex` is set and guaranteed to have a value at this point
        # start with node `self.__nodes[nodeIndex]`
        # only continue if `self.__nodes[nodeIndex]` is not visited
        if self.__nodes[nodeIndex].visited == False:
            # the node is not visited
            # so set it as visited
            self.__nodes[nodeIndex].visited = True
            # for each of this node's neighbours
            for connectionIndex in self.__nodes[nodeIndex].connections:
                # perform a depth first traversal of the neighbour
                # `yield from` (emphasis on the `from`) because it is yielding the result of a recursive yield
                # see PEP 380 Syntax for Delegating to a Subgenerator – https://www.python.org/dev/peps/pep-0380/
                yield from self.depthFirstTraversal(connectionIndex)

            data = self.__nodes[nodeIndex].data

            if data is not None:
                yield data

    def breadthFirstTraversal(self) -> Iterator[T]:
        """Iteratively breadth-first traverse the graph.
        Yields data – rather than returning it – because returning values would require more memory.
        `yield` basically pauses the function after yielding, saving all of its states, and only
        when the next value is required by the caller function does the yielding function continue.

        Yields:
            Generator[Node[T]]: The nodes' data in depth-first order.

        >>> simply_connected_maze = Graph[str]([
        ...     Node('Entrance', [1]),
        ...     Node('1', [0, 2, 3]),
        ...     Node('2', [1, 4]),
        ...     Node('3', [1, 5]),
        ...     Node('4', [2]),
        ...     Node('5', [3, 6, 7]),
        ...     Node('6', [5, 8]),
        ...     Node('7', [5, 9, 10]),
        ...     Node('Exit', [6, 11]),
        ...     Node('9', [7]),
        ...     Node('10', [7]),
        ...     Node('11', [8])
        ... ])
        >>> [maze_cell for maze_cell in simply_connected_maze.breadthFirstTraversal()]  # test traversal of a simple connected maze
        ['Entrance', '1', '2', '3', '4', '5', '6', '7', 'Exit', '9', '10', '11']

        >>> non_simple_maze = Graph[str]([
        ...     Node('Entrance', [1, 2]),
        ...     Node('1', [0, 3, 4]),
        ...     Node('2', [0, 5]),
        ...     Node('3', [1, 6]),
        ...     Node('4', [1, 7]),
        ...     Node('5', [7, 8]),
        ...     Node('6', [3, 9]),
        ...     Node('7', [4, 5, 9, 10]),
        ...     Node('8', [5]),
        ...     Node('9', [6, 7, 11]),
        ...     Node('10', [7]),
        ...     Node('Exit', [9])
        ... ])
        >>> [maze_cell for maze_cell in non_simple_maze.breadthFirstTraversal()]
        ['Entrance', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Exit']

        >>> [item for item in Graph[int]().breadthFirstTraversal()]     # test a traversal of an empty graph
        []
        """

        # check there's actually any nodes
        if len(self.__nodes) < 1:
            # there's no nodes.
            return

        # initialize a queue for the visited nodes
        visitedNodes = CircularQueue[Node[T]](len(self.__nodes))

        # set the 0th node as visited
        self.__nodes[0].visited = True
        # and enqueue it
        visitedNodes.enQueue(self.__nodes[0])

        # for each item in the queue:
        while len(visitedNodes) > 0:
            # pop a node from the queue
            currentNode = visitedNodes.deQueue()
            # and yield it
            data = currentNode.data
            if data is not None:
                yield data

            # get neighbours of the node
            for neighbour in currentNode.connections:
                # check if it's been visited
                if self.__nodes[neighbour].visited == False:
                    # set it to visited bc we're visiting it now
                    self.__nodes[neighbour].visited = True
                    # and add it to the `visitedNodes` queue
                    visitedNodes.enQueue(self.__nodes[neighbour])

    def __checkIndexIsValidWithException(self, index: int) -> bool:
        if not (len(self.__nodes) > index >= 0):
            raise IndexError("Node at index {} is out of range.".format(str(index)))
        return True

    def removeLinkBetween(
        self,
        indexFrom: int,
        indexTo: int,
        bidirectional: bool = True,
    ) -> None:
        """Removes a link between two nodes

        Args:
            indexFrom (int): The `from` node to connect to the `to`
            indexTo (int): The `to` node
            bidirectional (bool, optional): Whether or not to remove the link both ways. Defaults to True.
        """

        # make sure indices are valid
        self.__checkIndexIsValidWithException(indexFrom)
        self.__checkIndexIsValidWithException(indexTo)

        # check it's in the list of indices
        if indexTo in self.__nodes[indexFrom].connections:
            self.__nodes[indexFrom].connections.remove(indexTo)
        else:
            # it isn't
            raise ValueError(
                f"Node index {indexTo} already does not exist in node at index {indexFrom}'s connections.",
            )

        # if bidirectional, flip indexTo and indexFrom and do it again
        if bidirectional:
            self.removeLinkBetween(indexTo, indexFrom, False)

    def addLinkBetween(
        self,
        indexFrom: int,
        indexTo: int,
        bidirectional: bool = True,
    ) -> None:
        """Add a link between two nodes of given indices.

        Args:
            indexFrom (int): the 'from' node to connect to the 'to'
            indexTo (int): the 'to' node
            bidirectional (bool, optional): Whether or not to connect the link both ways (i.e., `indexFrom` to `indexTo` and vice versa.). Defaults to True.

        Raises:
            Exception: If the node index `indexFrom` already exists in `indexTo`'s connections.

        >>> simply_connected_maze = Graph[str]([
        ...     Node('Entrance', [1]),
        ...     Node('1', [0, 2, 3]),
        ...     Node('2', [1, 4]),
        ...     Node('3', [1, 5]),
        ...     Node('4', [2]),
        ...     Node('5', [3, 6, 7]),
        ...     Node('6', [5, 8]),
        ...     Node('7', [5, 9, 10]),
        ...     Node('Exit', [6, 11]),
        ...     Node('9', [7]),
        ...     Node('10', [7]),
        ...     Node('11', [8])
        ... ])

        >>> simply_connected_maze.addLinkBetween(2, 3)

        >>> simply_connected_maze.addLinkBetween(2, 4)
        Traceback (most recent call last):
        ...
        ValueError: Node index '4' already exists in node 2's connections.

        >>> simply_connected_maze.addLinkBetween(55, 3)
        Traceback (most recent call last):
        ...
        IndexError: Node at index 55 is out of range.

        >>> simply_connected_maze.addLinkBetween(2, 333)
        Traceback (most recent call last):
        ...
        IndexError: Node at index 333 is out of range.
        """

        # make sure indices are valid
        self.__checkIndexIsValidWithException(indexFrom)
        self.__checkIndexIsValidWithException(indexTo)

        # check the node isn't already connected
        if self.connectionExistsFrom(indexFrom, indexTo):
            # it is, so raise an exception with a descriptive error message
            raise ValueError(
                "Node index '{}' already exists in node {}'s connections.".format(
                    str(indexTo), str(indexFrom)
                )
            )
        else:
            # add the node index in its indexA's connections list

            # do this by using a temporary variable to avoid errors when mutating list values' values
            nodeTemp: Node[T]

            try:
                nodeTemp = self.__nodes[indexFrom].clone()
            except IndexError:
                raise IndexError(
                    "Node at index {} is nonexistent.".format(str(indexFrom))
                )

            # set our temporary vars correctly
            nodeTemp.connections.append(indexTo)
            # and then set the node we want to the correctly set temporary variable
            self.__nodes[indexFrom] = nodeTemp

        if bidirectional:
            # do it again!
            #  but make sure to not do it bidirectionally because then it'd go on forever
            self.addLinkBetween(indexTo, indexFrom, False)
