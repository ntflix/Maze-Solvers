#!python3.10

from modules.data_structures.circular_queue.circular_queue import CircularQueue
from typing import Generic, Optional, TypeVar
from enum import Enum

T = TypeVar('T')

class Node(Generic[T]):
    # This could easily be made into a `Tuple` rather than a whole new class but for debugging purposes, I chose to make this a class.

    data: T     # this node's data
    connections: list[int]   # pointers of this node's connections

    def __init__(self, data: T, connections: list[int] = list[int]()) -> None:
        """Constructor for a binary tree node.

        Args:
            data (T): This node's data, e.g. 'Barry'.
            connections (list[int], optional): The list of pointers that are connections of this node. Defaults to an emply list[int]().
        """
        self.data = data
        self.connections = connections

class Graph(Generic[T]):
    """A binary graph of type {T}."""

    nodes: list[Node[T]]    # the list of nodes of this graph
    graph: dict[str, Node[T]]   # the actual graph

    def __init__(self):
        """Constructor for a binary tree of type {T}.

        Args:
            type (T): The value type of the values of the nodes of the tree. For example, a tree storing names would have a value type of {str}.

        Returns:
            None.
        """

        self.nodes: list[Node[T]] = []  # Initialize `self.nodes` to an empty list
    
    def setNodesFromNodesList(self, nodes: list[Node[T]]) -> None:
        self.nodes = nodes

    def setNodesFromValuesAndConnections(self, values: list[T], connectionsPointers: list[list[int]]) -> None:
        """Give a Tree object some nodes.

        Args:
            values (List[T]): the value of each node.
            connectionsPointers (List[List[int]]): the connections that each node has.
        """

        self.connections = connectionsPointers  # and set `self.connections` to provided connections

        for i in range(len(values)):
            thisNode: Node[T] = Node(data = values[i], connections = connectionsPointers[i])    # make new `Node` with this value's data and left and right pointers
            self.nodes.append(thisNode)     # append new node to `self.nodes`

    # TODO: Implement breadth first traversal.

    def _exists(self, nodePointer: int) -> bool:
        """Determine whether or not a pointer points to a valid node.

        Args:
            nodePointer (int): The index of the node the pointer points to.

        Returns:
            bool: Whether the pointer is valid.
        """

        return not nodePointer in [-1]
    
    def breadthFirstTraversal(self, node: Optional[Node[T]] = None) -> list[T]:
        raise NotImplementedError("This method hasn't been implemented yet.")

        class VisitedStatus(Enum):
            visited = 0
            medium = 1
            unvisited = 2

        A = TypeVar('A')
        class NodeWithVisitedStatus(Node[A]):
            """custom Node class with added parameter `visitedStatus`

            Args:
                Node ([type]): The type of data this node will store
            """
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