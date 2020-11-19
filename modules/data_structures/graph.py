#!python3.10

# from modules.data_structures.circular_queue.circular_queue import CircularQueue
from typing import Generator, Generic, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """A node of a graph. Stores data and its connections.

    Args:
        Generic ([type]): The type of data the node will store.
    """
    # This could easily be made into a Tuple rather than a whole new class but for debugging purposes, I chose to make this a class.

    data: T     # this node's data  - public because the graph may want to set its data again
    connections: list[int]  # pointers of this node's connections   – public bc it needs to be read by the graph
    visited: bool = False  # a helper variable to assist in traversals of a graph of nodes

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
        return str(self.data + " -> (" + ', '.join(map(str, self.connections)) + ")")


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
        return "[" + '], ['.join(list(map(str, self.__nodes))) + "]"

    # @staticmethod
    # def createFullyConnected(sizeX: int, sizeY: int) -> 'Graph':
    #     graph = Graph()

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

    def setNodesFromValuesAndConnections(self, values: list[T], connectionsPointers: list[list[int]]) -> None:
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
            thisNode: Node[T] = Node(
                data=values[i], connections=connectionsPointers[i])
            self.__nodes.append(thisNode)     # append new node to `self.nodes`

    def isConnectionBetween(self, nodeValueA: T, nodeValueB: T):
        # for thisNode in self:
        pass

    # def __iter__(self) -> Generator[Node[T], None, None]:
    #     """Helper method to iterate over items in the graph. Operates as a depth first traversal.
    #     Yields each value (rather than return everything as a list) as to not use up potentially infinite memory.
    #     The `yield` statement pauses the function, saving all its states and later continues from there on successive calls.

    #     Yields:
    #         _LinkedListNode: The next node in the graph — either element 0 of the list, or the `nextNode` attribute of the previous node.

    #     Instantiate a `LinkedList` and print it all out, testing iteration and generator
    #     >>> myLinkedList = LinkedList[str](['People', 'often', 'joke', 'that', 'in', 'order', 'to', 'understand', 'recursion,', 'you', 'must', 'first', 'understand', 'recursion.'])
    #     >>> sentence = ' '.join([listItem.data for listItem in myLinkedList])
    #     >>> sentence
    #     'People often joke that in order to understand recursion, you must first understand recursion.'
    #     """
    #     pass

        # if self.head is not None:
        #     # set node to an optional `_LinkedListNode` of type `T` so we can set it to the next node, which may or may not be optional. The optional allows us to check the next node exists and not accidentally yield a `None` value.
        #     node: Optional[_LinkedListNode[T]] = self.head
        #     # check the (next) node exists
        #     while node is not None:
        #         # yield the node, pausing the function, saving its states and allowing it to continue from here on successive calls.
        #         yield node
        #         # set node to the next node referenced by this node. This may or may not exist, hence we have to be careful and unwrap the value as we have above.
        #         node = node.nextNode

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

    def depthFirstTraversal(self, nodeIndex: Optional[int] = None) -> Generator[Node[T], None, None]:
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
            Generator[Node[T], None, None]: Each node's data.

        >>> socialNetwork = Graph[str]()
        >>> socialNetwork.setNodesFromNodesList([
        ...     Node("Alice",  [1, 4]),         # 0
        ...     Node("Bob",    [0, 4]),         # 1
        ...     Node("Calvin", [4, 3]),         # 2
        ...     Node("Daniel", [2, 4]),         # 3
        ...     Node("Eve",    [0, 1, 2, 3])    # 4 
        ... ])
        >>> for person in socialNetwork.depthFirstTraversal():
        ...     person

        """
        if nodeIndex is None:
            # the function has been called without a starting node so we start from the beginning!
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
        # only continue if `self.__nodes[currentNode]` is not visited
        if (self.__nodes[nodeIndex].visited == False):
            # the node is not visited
            self.__nodes[nodeIndex].visited = True
            for connectionIndex in self.__nodes[nodeIndex].connections:
                self.depthFirstTraversal(connectionIndex)

            yield self.__nodes[nodeIndex].data

    # TODO: Implement breadth first traversal.

    """
    def breadthFirstTraversal(self, node: Optional[Node[T]] = None) -> list[T]:
        raise NotImplementedError("This method hasn't been implemented yet.")

        class VisitedStatus(Enum):
            visited = 0
            medium = 1
            unvisited = 2

        A = TypeVar('A')
        class NodeWithVisitedStatus(Node[A]):
            \"""custom Node class with added parameter `visitedStatus`

            Args:
                Node ([type]): The type of data this node will store
            \"""
            visitedStatus: VisitedStatus = VisitedStatus.unvisited

        # if no node provided, start from the beginning of the graph
        if node is None:
            node = self.nodes[0]
        
        # create a queue of NodeWithVisitedStatus to keep track of which nodes we have yet to visit
        toVisit = CircularQueue[NodeWithVisitedStatus[T]](len(self.nodes))
        # enqueue the given node
        toVisit.enQueue(NodeWithVisitedStatus(node.data, node.connections))

        # create an empty list of nodes we have visited
        visitedNodes = list[NodeWithVisitedStatus[T]]()

        while toVisit.length > 0:
            # set `currentNode` to the result of popping the queue
            currentNode = toVisit.deQueue()
            currentNode.visitedStatus = VisitedStatus.visited
            visitedNodes.append(currentNode)

            for thisNeighbourIndex in currentNode.connections:
                # checking the visited status of this neighbour
                # if self.nodes[thisNeighbourIndex].visitedStatus
                pass
    """
