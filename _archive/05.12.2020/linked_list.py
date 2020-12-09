#!python3.10

from typing import Generator, Generic, Optional, TypeVar

# Linked List Node for the list
from modules.data_structures.linked_list.linked_list_node import LinkedListNode

T = TypeVar("T")


class LinkedList(Generic[T]):
    __head: Optional[LinkedListNode[T]] = None

    def __init__(self, nodes: list[T] = []) -> None:
        """The constructor for a `LinkedList` object.

        Args:
            nodes (list[LinkedListNode[T]]): A list of data for the linked list to create itself from.

        Raises:
            ValueError: `nodes` argument not supplied.

        Instantiate and print an empty linked list
        >>> emptyLinkedList = LinkedList[int]()
        >>> str(emptyLinkedList)
        '[]'

        Instantiate and print a linked list of sample objects
        >>> mazeCellsIndices = LinkedList[int]([0, 1, 2, 3, 4, 5])
        >>> mazeCellsIndices._LinkedList__head
        0 (1 (2 (3 (4 (5 (None))))))
        """
        # set `self.__head` to `None` as no items have been added to the list yet
        self.__head = None
        # check that some items have been provided in this function's arguments
        if nodes is None:
            raise ValueError("`nodes` argument must be a list of `T`.")
        else:
            if len(nodes) == 0:
                # an empty list of nodes was given so initialize `self.__head` to `None` and return
                self.__head = None
                return  # don't execute the rest of the function

            # set `node` to the first item of the provided nodes
            node = LinkedListNode(nodes.pop(0))
            #  set `self.__head` to the above-defined variable `node`
            self.__head = node
            # loop over each of the nodes in the nodes provided in this function's arguments
            for thisNode in nodes:
                # set the current node's next node to a new `LinkedListNode` object of `thisNode`
                node.nextNode = LinkedListNode(thisNode)
                #  set the current node to the next node to move on
                node = node.nextNode

    def __str__(self) -> str:
        return str(self.toList())

    def __iter__(self) -> Generator[LinkedListNode[T], None, None]:
        """Helper method to iterate over items in the list. Yields each value (rather than return everything as a list) as to not use up potentially infinite memory.
        The `yield` statement pauses the function, saving all its states and later continues from there on successive calls.

        Yields:
            LinkedListNode: The next node in the linked list — either element 0 of the list, or the `nextNode` attribute of the previous node.

        Iterate over a linked list
        Instantiate a `LinkedList` and print it all out, testing iteration and generator
        >>> mazeCellsIndices = LinkedList[int]([9, 4, 3, 6])
        >>> [listItem.data for listItem in mazeCellsIndices]
        [9, 4, 3, 6]

        Iterate over an empty linked list
        >>> [item.data for item in LinkedList[str]()]
        []
        """
        # check that there are actually any items in the list
        if self.__head is not None:
            # set node to an optional `LinkedListNode` of type `T` so we can set it to the next node, which may or may not be optional. The optional allows us to check the next node exists and not accidentally yield a `None` value.
            node: Optional[LinkedListNode[T]] = self.__head
            # check the (next) node exists
            while node is not None:
                # yield the node, pausing the function, saving its states and allowing it to continue from here on successive calls.
                yield node
                # set node to the next node referenced by this node. This may or may not exist, hence we have to be careful and unwrap the value as we have above.
                node = node.nextNode

    def __getitem__(self, key: int) -> T:
        """Get item at specified index

        Args:
            key (int): the index of the item to get.

        Raises:
            IndexError: Index out of range.

        Returns:
            T: The data of the item at specified index.

        >>> mazeCellsIndices = LinkedList[int]([14, 11, 3, 6, 8])
        >>> mazeCellsIndices[0]
        14
        >>> mazeCellsIndices[2]
        3
        >>> mazeCellsIndices[4]
        8
        >>> mazeCellsIndices[6] # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        IndexError: LinkedList index 6 is out of range
        >>> mazeCellsIndices[-1] # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        IndexError: LinkedList index -1 is out of range
        """
        index = 0
        currentNode = self.__head

        while currentNode is not None:
            if index == key:
                return currentNode.data
            elif index > key:
                raise IndexError(
                    "LinkedList index {} is out of range".format(str(index))
                )
            else:
                # we're not there yet so increment index and set node to the nextNode
                index += 1
                currentNode = currentNode.nextNode
        # looped over everything without finding index
        raise IndexError("LinkedList index {} is out of range".format(str(index)))

    def __setitem__(self, key: int, newValue: T):
        """setitem method of LinkedList. Used to set an item specified at an index in the LinkedList.

        Args:
            key (int): The index of the LinkedList item to set.
            newValue (T): The new value of the LinkedList item.

        Raises:
            IndexError: Index of `key` out of range.

        Test setting linked list nodes via their indices
        >>> indices = LinkedList[int]([1, 2, 3, 4])
        >>> indices[0] = 5
        >>> indices[1] = 6
        >>> indices[2] = 7
        >>> indices[3] = 8
        >>> print(indices)
        [5, 6, 7, 8]

        >>> indices[4] = 9
        >>> print(indices)
        [5, 6, 7, 8, 9]

        >>> indices[6] = 11
        Traceback (most recent call last):
        ...
        IndexError: LinkedList index 6 is out of range

        >>> indices[-1] = 4
        Traceback (most recent call last):
        ...
        IndexError: LinkedList index -1 is out of range
        """
        self.setItemRecursively(key, newValue)

    def setItemRecursively(
        self,
        index: int,
        newValue: T,
        currentNode: Optional[LinkedListNode[T]] = None,
        recursiveIndex: int = 0,
    ) -> Optional[LinkedListNode[T]]:
        """Recursively set a node's data at specified index.

        Args:
            index (int): The index of the node whose data you wish to set.
            newValue (T): The new value for the node's data
            currentNode (Optional[LinkedListNode[T]], optional): Used for recursion, keeping track of nodes. Defaults to None.
            recursiveIndex (int, optional): Used for recursion, the value for the index of the recursion. Defaults to 0.

        Raises:
            IndexError: LinkedList index is out of range.

        Returns:
            Optional[LinkedListNode[T]]: Used for recursion. The updated LinkedListNode.
        """

        if (recursiveIndex == 0) and (currentNode is None):
            # if this function was called with default recursiveIndex and currentNode parameters
            currentNode = self.__head

        if currentNode is None:
            if index > recursiveIndex:
                # the index is out of range...
                raise IndexError(
                    "LinkedList index {} is out of range".format(str(index))
                )

        if recursiveIndex == index:
            # we've got to the right node index
            # check if this node is None so we can set nextNode appropriately
            if currentNode is None:
                nextNode = None
            else:
                # this node is not None so we just set nextNode to this node's nextNode
                nextNode = currentNode.nextNode
            # we've set nextNode to appropriate value here so we make a new node and return it
            newNode = LinkedListNode[T](newValue, nextNode)
            self.__head = newNode
            return newNode
        elif recursiveIndex < index:
            # we're not there yet
            if currentNode is None:
                # the index is out of range
                raise IndexError(
                    "LinkedList index {} is out of range".format(str(index))
                )
            else:
                # call recursively to get the nextNode
                nextNode = self.setItemRecursively(
                    index, newValue, currentNode.nextNode, recursiveIndex + 1
                )
                # set newNode to this node with the previously set nextNode as its nextNode
                newNode = LinkedListNode[T](currentNode.data, nextNode=nextNode)
                self.__head = newNode
                return newNode
        elif recursiveIndex > index:
            # gone over!
            raise IndexError("LinkedList index {} is out of range".format(str(index)))

    def toNode(self) -> Optional[LinkedListNode[T]]:
        return self.__head

    def clone(self) -> "LinkedList[T]":
        """Clone this class object to overcome Python's pass-by-reference argument types.

        Returns:
            LinkedList[T]: clone of the object.
        """
        linkedList = LinkedList[T]()
        if self.__head is not None:
            linkedList.extendByNode(self.__head)
        return linkedList

    def toList(self) -> list[T]:
        """Generate a list of the data of all the objects in the linked list.

        Returns:
            list[T]: The data of each of the linked list nodes.

        Create Python list from instantiated linked list
        >>> mazeCellsIndices = LinkedList[int]([11, 13, 17, 19])
        >>> mazeCellsIndices.toList()
        [11, 13, 17, 19]

        Create Python list from empty linked list
        >>> emptyList = LinkedList[str]()
        >>> emptyList.toList()
        []
        """
        return [item.data for item in self]

    def insertLinkedListAtBeginning(self, linkedList: "LinkedList[T]") -> None:
        """Insert a linked list at the start of another.

        Args:
            linkedList (LinkedList): The linked list to insert at the beginning of `self`.

        Insert linked list at beginning of another
        >>> mazeCellsIndices = LinkedList[int]([11, 13, 17, 19])
        >>> moreMazeCellsIndices = LinkedList[int]([2, 3, 5, 7])
        >>> mazeCellsIndices.insertLinkedListAtBeginning(moreMazeCellsIndices)
        >>> print(mazeCellsIndices)
        [2, 3, 5, 7, 11, 13, 17, 19]
        >>> print(moreMazeCellsIndices)
        [2, 3, 5, 7, 7]

        Insert empty list at beginning of another
        >>> moreMazeCellsIndices.insertLinkedListAtBeginning(LinkedList[int]())
        >>> print(moreMazeCellsIndices)
        [2, 3, 5, 7]

        Insert linked list at beginning of empty linked list
        >>> evenMoreMazeCellsIndices = LinkedList[int]([1, 4])
        >>> emptyLinkedList = LinkedList[int]()
        >>> emptyLinkedList.insertLinkedListAtBeginning(evenMoreMazeCellsIndices)
        >>> print(emptyLinkedList)
        [1, 4]

        Insert empty linked list at beginning of empty linked list
        >>> emptyList = LinkedList[int]()
        >>> emptyList.insertLinkedListAtBeginning(LinkedList[int]())
        >>> print(emptyList)
        []
        """

        node = linkedList.toNode()

        if node is not None:
            self.insertNodeAtBeginning(node)

    def insertNodeAtBeginning(
        self, nodeValues: LinkedListNode[T], clone: bool = True
    ) -> None:
        """Recursively inserts any number of nodes in the beginning of this LinkedList by checking if each provided node's `nextNode` attribute is set.

        Args:
            node (LinkedListNode[T]): The node to add potentially with a nextNode attribute, which may contain a node with a nextNode attribute, which may contain a node with a nextNode attribute, which may contain a node with a nextNode attribute, which...
            clone (bool): whether to clone the passed values. Only used when recursing or for special cases where you want the original list edited too.
        """

        if clone:
            # then don't modify the passed-in LinkedListNode argument
            node = nodeValues.clone()  # to pass by value, not reference
        else:
            # recursively called so we want to modify the passed-in LinkedList argument
            node = nodeValues

        # check if this node has a `nextNode`, and if so, call this same function on the `nextNode`, again and again, until there's no `nextNode`...
        if node.nextNode is None:
            # `node.nextNode` is None
            # this node's `nextNode` is None so we can set its `nextNode` to `self.__head`... -->
            node.nextNode = self.__head
        else:
            # `node.nextNode` is *not* None
            #  so we call this function recursively to traverse the chain of `LinkedListNodes` to be able to find the last node in the list and add them to our list.
            self.insertNodeAtBeginning(
                node.nextNode, clone=False
            )  # modifies the inout node parameter
            # --> ...and after we have gotten to setting the node (whose `nextNode` is `None`) to `self.__head`, we then set our `self.__head` to the node to have finished inserting the nodes.
            self.__head = node

    def extendByLinkedList(self, linkedList: "LinkedList[T]") -> None:
        """Appends the contents of a linked list to another.

        Args:
            linkedList (LinkedList[T]): The linked list to add onto `self`.

        Extend linked list by another
        >>> mazeCellsIndices = LinkedList[int]([2, 4, 12, 15])
        >>> moreMazeCellsIndices = LinkedList[int]([17, 24, 28, 31])
        >>> mazeCellsIndices.extendByLinkedList(moreMazeCellsIndices)
        >>> print(mazeCellsIndices)
        [2, 4, 12, 15, 17, 24, 28, 31]

        Extend empty linked list by a normal linked list
        >>> mazeCellsIndices = LinkedList[int]()
        >>> moreMazeCellsIndices = LinkedList[int]([1, 3, 5])
        >>> mazeCellsIndices.extendByLinkedList(moreMazeCellsIndices)
        >>> print(mazeCellsIndices)
        [1, 3, 5]

        Extend normal linked list by an empty one
        >>> mazeCellsIndices = LinkedList[int]([1, 3, 5])
        >>> moreMazeCellsIndices = LinkedList[int]()
        >>> mazeCellsIndices.extendByLinkedList(moreMazeCellsIndices)
        >>> print(mazeCellsIndices)
        [1, 3, 5]

        Extend empty linked list by an empty linked list
        >>> emptyList = LinkedList[int]()
        >>> anotherEmptyList = LinkedList[int]()
        >>> emptyList.extendByLinkedList(anotherEmptyList)
        >>> print(emptyList)
        []
        """

        node = linkedList.toNode()

        if node is not None:
            self.extendByNode(node)

    def extendByNode(
        self, node: LinkedListNode[T], insertOnto: Optional[LinkedListNode[T]] = None
    ) -> None:
        """Recursively appends nodes to the end of this LinkedList by checking each of this LinkedList's node's `nextNode` attribute is set.

        Args:
            node (LinkedListNode[T]): The node or chain of nodes you wish to append to the LinkedList.
            insertOnto (Optional[LinkedListNode[T]]): The node or chain of nodes to insert `node` onto the end of. Don't worry about this if you simply want to insert onto the end of the `LinkedList` because it traverses that automatically. Defaults to `self.__head`.
        """
        if insertOnto is None:
            # note that this function is being called without an `insertOnto` parameter, meaning we want to insert it onto the end of the `self.__head` node chain.
            if self.__head is None:
                # `self.__head` is None so we can simply set it to the given node.
                self.__head = node
            else:
                self.extendByNode(node, insertOnto=self.__head)
        # `insertOnto` is not None >
        else:
            # > meaning we have recursively called this function and intend to chain our inserts from one node to its `nextNode`.
            if insertOnto.nextNode is not None:
                # call this function (recursively) with the `nextNode` of the `insertOnto` argument of this function call.
                self.extendByNode(node, insertOnto.nextNode)
            else:
                # `insertOnto.nextNode` is None
                # We've traversed the entire chain and got to the end, where `nextNode` has no value.
                insertOnto.nextNode = node

    def removeNode(self, toRemove: T, node: Optional[LinkedListNode[T]] = None) -> None:
        """Remove a node with data `toRemove` from the list, by linking the node before it to the node after it.

        Args:
            toRemove (T): The data of the node to remove. The first node with this data will be the one removed.
            node (Optional[LinkedListNode[T]], optional): Parameter used for recursively calling this function –
            don't worry about this if you plan on starting at the start of this LinkedList. Defaults to None.

        Raises:
            Exception: List is empty, therefore the function cannot remove any value.
            Exception: The provided data was not found in any node.

        Removing a node at the start of the list
        >>> mazeCells = LinkedList[int]([2, 8, 4, 7, 16, 22, 12])
        >>> mazeCells.removeNode(2)
        >>> print(mazeCells)
        [8, 4, 7, 16, 22, 12]

        Removing a node in the middle of the list
        >>> mazeCells = LinkedList[int]([2, 8, 4, 7, 16, 22, 12])
        >>> mazeCells.removeNode(7)
        >>> print(mazeCells)
        [2, 8, 4, 16, 22, 12]

        Removing a node at the end of the list
        >>> mazeCells = LinkedList[int]([2, 8, 4, 7, 16, 22, 12])
        >>> mazeCells.removeNode(12)
        >>> print(mazeCells)
        [2, 8, 4, 7, 16, 22]

        Removing a node that does not exist
        >>> mazeCells = LinkedList[int]([2, 8, 4, 7, 16, 22, 12])
        >>> mazeCells.removeNode(5) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        Exception: Node not found with data '5'.
        >>> print(mazeCells)
        [2, 8, 4, 7, 16, 22, 12]

        """

        # check the specified node is `None` to see if we are starting at the beginning of this LinkedList or from a different node
        if node is None:
            # set `node` to `self.__head` to traverse the list from the beginning
            if self.__head is not None:
                node = self.__head
                # if the start of the list is the one we want to remove, just set `self.head` to the next one
                if node.data == toRemove:
                    self.__head = node.nextNode
                    return
            else:
                raise Exception("List is empty.")

        # node has been set to `self.__head`
        # check that this node's nextNode is the right one
        if node.nextNode is None:
            # we have traversed the entire list without finding the desired item
            raise Exception("Node not found with data '{}'.".format(toRemove))

        if node.nextNode.data == toRemove:
            # the next node is the one we must remove.
            # set this node's `nextNode` to its `nextNode`'s `nextNode`:
            node.nextNode = node.nextNode.nextNode
            # we are making the list 'skip out' the next node and instead pointing it to the one after that.
        else:
            # the next node is not the wanted one just yet, so we recursively call this same function with the `node` parameter as this node's `nextNode`.
            self.removeNode(toRemove, node.nextNode)
