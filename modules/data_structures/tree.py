#!python3.10

from typing import Any, Generic, TypeVar

T = TypeVar('T')

class Node(Generic[T]):
    # This could easily be made into a `Tuple` rather than a whole new class but for debugging purposes, I chose to make this a class.

    data: T     # this node's data
    left: int   # pointer for this node's left node
    right: int  # pointer for this node's right node

    def __init__(self, data: T, left: int = -1, right: int = -1) -> None:
        """Constructor for a binary tree node.

        Args:
            data (T): This node's data, e.g. 'Barry'.
            left (int, optional): The index of this node's left child, if it exists. Defaults to -1.
            right (int, optional): The index of this node's right child, if it exists. Defaults to -1.

        Returns:
            None.
        """
        self.data = data
        self.left = left
        self.right = right

class Tree(Generic[T]):
    """A binary graph of type {T}."""

    values: list[T]
    leftPointers: list[int] = []
    rightPointers: list[int] = []

    nodes: list[Node[T]]    # a helper variable, temporarily used 

    def __init__(self):
        """Constructor for a binary tree of type {T}.

        Args:
            type (T): The value type of the values of the nodes of the tree. For example, a tree storing names would have a value type of {str}.

        Returns:
            None.
        """
        self.values: list[T] = []       # Initialize self.values to an empty list to remove old values
        self.nodes: list[Node[T]] = []  # Initialize self.nodes to an empty list

        for value in self.values:
            if self.values.count(value) > 1:
                # There are duplicate values in the tree
                print("Invalid tree. Duplicate values must not exist. Value: " + str(value))
                exit(1)
    
    def setNodes(self, values: list[T], leftPointers: list[int], rightPointers: list[int]) -> None:
        """Give a Tree object some nodes.

        Args:
            values (List[T]): the value of each node
            leftPointers (List[int]): the left pointer of each node, where index is the node number
            rightPointers (List[int]): the right pointer of each node, where index is the node number
        """

        self.values = values    # set self.values to the provided values
        self.leftPointers = leftPointers    # etc
        self.rightPointers = rightPointers  # etc

        for i in range(len(values)):
            thisNode: Node[T] = Node(data = values[i], left = leftPointers[i], right = rightPointers[i])    # make new Node with this value's data and left and right pointers
            self.nodes.append(thisNode)     # append new node to self.nodes

    def pre_traversal(self, position: int) -> list[T]:
        """Perform a pre-order traversal of the tree.

        Steps:
            • Output the root
            • Perform a pre-order traversal of the left node
            • Perform a pre-order traversal of the right node

        Args:
            position (int): The 1-indexed value of the position of the starting node.

        Returns:
            List[T]: A list, in order of traversal, of the nodes visited during the traversal.
        """
        
        # position -= 1   # convert to 0-indexed by removing 1
        
        output: list[T] = []    # initialize a list of data for output

        # Step 1: Output the root
        output.append(self.nodes[position].data)    # add this node's data to output

        # Step 2: Perform a pre-order traversal of the left node
        if self._exists(self.nodes[position].left):
            # if this node's left child exists
            output.extend(self.pre_traversal(self.nodes[position].left))
            # then perform a pre-order traversal of this node's left child and add it to output

        # Step 3: Perform a pre-order traversal of the right node
        if self._exists(self.nodes[position].right):
            # if this node's right child exists
            output.extend(self.pre_traversal(self.nodes[position].right))
            # then perform a pre-order traversal of this node's left child and add it to output

        return output

    def in_order_traversal(self, position: int) -> list[T]:
        """Perform an in-order traversal of the tree.
        
        Steps:
            • Perform an in-order traversal of the left node
            • Output the root
            • Perform an in-order traversal of the right node

        Args:
            position (int): The 1-indexed value of the position of the starting node.

        Returns:
            List[T]: A list, in order of traversal, of the nodes visited during the traversal.
        """

        # position -= 1   # convert to 0-indexed by removing 1

        output: list[T] = []    # initialize a list of data for output

        # Step 1: Perform an in-order traversal of the left node
        if self._exists(self.nodes[position].left):
            # if this node's left child exists
            output.extend(self.in_order_traversal(self.nodes[position].left))
            # then perform an in-order traversal of this node's left child and add it to output
        
        # Step 2: Output the root
        output.append(self.nodes[position].data)    # add this node's data to output

        # Step 3: Perform an in-order traversal of the right node
        if self._exists(self.nodes[position].right):
            # if this node's right child exists
            output.extend(self.in_order_traversal(self.nodes[position].right))
            # then perform an in-order traversal of this node's left child and add it to output

        return output

    def post_traversal(self, position: int) -> list[T]:
        """Perform a post-order traversal of the tree.

        Steps:
            • Perform a post-order traversal of the left node
            • Perform a post-order traversal of the right node
            • Output the root

        Args:
            position (int): The 1-indexed value of the position of the starting node.

        Returns:
            List[T]: A list, in order of traversal, of the nodes visited during the traversal.
        """

        # position -= 1   # convert to 0-indexed by removing 1

        output: list[T] = []    # initialize a list of data for output
        
        # Step 1: Perform a post-order traversal of the left node
        if self._exists(self.nodes[position].left):
            # if this node's left child exists
            output.extend(self.post_traversal(self.nodes[position].left))
            # then perform a post-order traversal of this node's left child and add it to output

        # Step 2: Perform a post-order traversal of the right node
        if self._exists(self.nodes[position].right):
            # if this node's right child exists
            output.extend(self.post_traversal(self.nodes[position].right))
            # then perform a post-order traversal of this node's right child and add it to output

        # Step 3: Output the root
        output.append(self.nodes[position].data)    # add this node's data to output

        return output

    def _exists(self, nodePointer: int) -> bool:
        """Determine whether or not a pointer points to a valid node.

        Args:
            nodePointer (int): The index of the node the pointer points to.

        Returns:
            bool: Whether the pointer is valid.
        """

        return not nodePointer in [-1]

if __name__ == '__main__':
    def print_values(values: list[Any]) -> None:
        print('\'' + '\', \''.join(values) + '\'')

    values: list[str] = ['+','4','*','9','6']           # removed first empty value
    leftPointers: list[int] = [1,-1,3,-1,-1]            # converted to 0-indexed list and removed first empty value
    rightPointers: list[int] = [2,-1,4,-1,-1]           # converted to 0-indexed list and removed first empty value
    tree = Graph[str]()                                   # initialize tree of type String
    tree.setNodes(values, leftPointers, rightPointers)  # set nodes of the tree to provided ones

    print('Pre-order traversal \t', end="")
    print_values(tree.pre_traversal(0))
    print('In-order traversal  \t', end="")
    print_values(tree.in_order_traversal(0))
    print('Post-order traversal\t', end="")
    print_values(tree.post_traversal(0))
