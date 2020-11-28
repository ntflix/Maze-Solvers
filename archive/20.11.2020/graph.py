#!python3.10

# support type hinting in my editor and code
from typing import Generator, Generic, Optional, TypeVar

# queue for breadth first search
from temporary_modules import queue

T = TypeVar("T")


class Node(Generic[T]):
    """A node of a graph. Stores data and its connections.

    Args:
        Generic ([type]): The type of data the node will store.
    """

    # This could easily be made into a Tuple rather than a whole new class but for debugging purposes, I chose to make this a class.

    data: T  # this node's data  - public because the graph may want to set its data again
    connections: list[
        int
    ]  # pointers of this node's connections   – public bc it needs to be read by the graph
    visited: bool = (
        False  # a helper variable to assist in traversals of a graph of nodes
    )

    def __init__(self, data: T, connections: list[int] = list[int]()) -> None:
        """Constructor for a binary tree node.

        Args:
            data (T): This node's data, e.g. 'Barry'.
            connections (list[int], optional): The list of pointers that are connections of this node. Defaults to an emply list[int]().
        """
        self.data = data
        self.connections = connections

    def __repr__(self) -> str:
        """Return a string representation of this object

        Returns:
            str: The string representation of the object, for example:
        ```
        "Alice -> (1, 4)"
        ```
        """
        # For example, "Bob -> (0, 4)"
        return str(self.data + " -> (" + ", ".join(map(str, self.connections)) + ")")


class Graph(Generic[T]):
    """A binary graph of type {T}."""

    __nodes: list[Node[T]]  #  the list of nodes of this graph

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
        >>> graphWithPeopleInIt = Graph[str](nodes = [
        ...     Node("Alice",  [1, 4]),         # 0
        ...     Node("Bob",    [0, 4]),         # 1
        ...     Node("Calvin", [4, 3]),         # 2
        ...     Node("Daniel", [2, 4]),         # 3
        ...     Node("Eve",    [0, 1, 2, 3])    # 4
        ... ])
        >>> graphWithPeopleInIt
        [Alice -> (1, 4)], [Bob -> (0, 4)], [Calvin -> (4, 3)], [Daniel -> (2, 4)], [Eve -> (0, 1, 2, 3)]
        """

        # Initialize `self.nodes` to an empty list
        self.__nodes: list[Node[T]] = []
        # Then check if any nodes were provided
        if nodes is not None:
            # And if any were, set the nodes to them
            self.setNodesFromNodesList(nodes)

    def __repr__(self) -> str:
        return "[" + "], [".join(list(map(str, self.__nodes))) + "]"

    @staticmethod
    def createFullyConnectedSquareGraph(sizeX: int, sizeY: int) -> 'Graph':
        raise NotImplementedError()
        connections: list[list[int]]
        # generate the list of lists of length `sizeY`
        graph = Graph()

    def setNodesFromNodesList(self, nodes: list[Node[T]]) -> None:
        """Set a graph's nodes from a list of nodes.

        Args:
            nodes (list[Node[T]]): The list of nodes from which to set the graph data.

        >>> socialNetwork = Graph[str]()
        >>> socialNetwork.setNodesFromNodesList([
        ...     Node("Alice",  [1, 4]),         # 0
        ...     Node("Bob",    [0, 4]),         # 1
        ...     Node("Calvin", [4, 3]),         # 2
        ...     Node("Daniel", [2, 4]),         # 3
        ...     Node("Eve",    [0, 1, 2, 3])    # 4
        ... ])
        >>> socialNetwork
        [Alice -> (1, 4)], [Bob -> (0, 4)], [Calvin -> (4, 3)], [Daniel -> (2, 4)], [Eve -> (0, 1, 2, 3)]
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
        >>> socialNetwork = Graph[str]()
        >>> socialNetwork.setNodesFromValuesAndConnections([
        ...     "Alice",
        ...     "Bob",
        ...     "Calvin",
        ...     "Daniel",
        ...     "Eve"
        ... ], [
        ...     [1, 4],
        ...     [0, 4],
        ...     [4, 3],
        ...     [2, 4],
        ...     [0, 1, 2, 3]
        ... ])
        >>> socialNetwork
        [Alice -> (1, 4)], [Bob -> (0, 4)], [Calvin -> (4, 3)], [Daniel -> (2, 4)], [Eve -> (0, 1, 2, 3)]
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
        """
        return indexB in self.__nodes[indexA].connections

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

        >>> socialNetwork = Graph[str]()
        >>> socialNetwork.setNodesFromNodesList([
        ...     Node("Alice",  [1, 4]),         # 0
        ...     Node("Bob",    [0, 4]),         # 1
        ...     Node("Calvin", [4, 3]),         # 2
        ...     Node("Daniel", [2, 4]),         # 3
        ...     Node("Eve",    [0, 1, 2, 3])    # 4
        ... ])
        >>> socialNetwork._exists(4)
        True
        >>> socialNetwork._exists(5)
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

    def depthFirstTraversal(
        self, nodeIndex: Optional[int] = None
    ) -> Generator[Node[T], None, None]:
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

        >>> socialNetwork = Graph[str]()
        >>> socialNetwork.setNodesFromNodesList([
        ...     Node("Alice",  [1, 4]),         # 0
        ...     Node("Bob",    [0, 4]),         # 1
        ...     Node("Calvin", [4, 3]),         # 2
        ...     Node("Daniel", [2, 4]),         # 3
        ...     Node("Eve",    [0, 1, 2, 3])    # 4
        ... ])
        >>> [person for person in socialNetwork.depthFirstTraversal()]
        ['Daniel', 'Calvin', 'Eve', 'Bob', 'Alice']

        >>> [item for item in Graph[int]().depthFirstTraversal()]
        []
        """
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

            yield self.__nodes[nodeIndex].data

    def breadthFirstTraversal(self) -> Generator[Node[T], None, None]:    
        """Iteratively breadth-first traverse the graph.
        Yields data – rather than returning it – because returning values would require more memory.

        Yields:
            Generator[Node[T]]: The nodes' data in depth-first order.
        
        >>> socialNetwork = Graph[str]()
        >>> socialNetwork.setNodesFromNodesList([
        ...     Node("Alice",  [1, 4]),         # 0
        ...     Node("Bob",    [0, 4]),         # 1
        ...     Node("Calvin", [4, 3]),         # 2
        ...     Node("Daniel", [2, 4]),         # 3
        ...     Node("Eve",    [0, 1, 2, 3])    # 4
        ... ])
        >>> [person for person in socialNetwork.breadthFirstTraversal()]
        ['Alice', 'Bob', 'Eve', 'Calvin', 'Daniel']

        >>> [item for item in Graph[int]().breadthFirstTraversal()]
        []
        """
        # initialize a queue for the visited nodes
        visitedNodes = CircularQueue[Node[T]](len(self.__nodes))

        # set the 0th node as visited
        self.__nodes[0].visited = True
        # and enqueue it
        visitedNodes.enQueue(self.__nodes[0])

        # for each item in the queue:
        while visitedNodes.length > 0:
            # pop a node from the queue
            currentNode = visitedNodes.deQueue()
            # and yeild it
            yield currentNode.data

            # get neighbours of the node
            for neighbour in currentNode.connections:
                # check if it's been visited
                if self.__nodes[neighbour].visited == False:
                    # set it to visited bc we're visiting it now
                    self.__nodes[neighbour].visited = True
                    # and add it to the `visitedNodes` queue
                    visitedNodes.enQueue(self.__nodes[neighbour])