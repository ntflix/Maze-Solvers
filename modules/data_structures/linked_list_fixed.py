#!python3.10

from typing import Generator, Generic, Optional, TypeVar

T = TypeVar('T')


class _LinkedListNode(Generic[T]):
    """A node for a linked list object

    Args:
        Generic ([type]): The type of data this node will store
    """

    data: T                             # this node's data
    # the pointer of the next node  # variable type is in quotes because we are using forward referencing here to avoid recursive typing
    nextNode: Optional['_LinkedListNode[T]']

    def __init__(self, data: T, nextNode: Optional['_LinkedListNode[T]'] = None) -> None:
        """Constructor for a `_LinkedListNode`

        Args:
            data (T): The data for this node to store
            next (int): The integer pointer of the next `_LinkedListNode`

        Instantiating a `_LinkedListNode`:
        >>> myLinkedListNode = _LinkedListNode[int](65536, nextNode = 5)     # instantiate a _LinkedListNode object
        >>> myLinkedListNode.data
        65536
        >>> myLinkedListNode.nextNode
        5

        """
        self.data = data
        self.nextNode = nextNode

    def __repr__(self) -> str:
        """Generate a string representation of this object
        For example, "'Barry' -> 4" for an object where `data` = 'Barry' and `nextPointer` = 4

        Returns:
            str: the string representation of the object

        >>> _LinkedListNode[str](data = "Gareth", nextNode = 2)
        'Gareth' (2)
        """
        return "'{}' ({})".format(str(self.data), str(self.nextNode))


class LinkedList(Generic[T]):
    head: Optional[_LinkedListNode[T]] = None

    def __init__(self, nodes: list[T]) -> None:
        """The constructor for a `LinkedList` object.

        Args:
            nodes (list[_LinkedListNode[T]]): A list of data for the linked list to create itself from.

        Instantiate a `LinkedList` and print it all out
        >>> myLinkedList = LinkedList[str](['Regexophobia', 'is', 'the', 'fear', 'of', 'brackets.'])
        >>> myLinkedList.head
        'Regexophobia' ('is' ('the' ('fear' ('of' ('brackets.' (None))))))
        """
        # set `self.head` to `None` as no items have been added to the list yet
        self.head = None
        # check that some items have been provided in this function's arguments
        if nodes is not None:
            # set `node` to the first item of the provided nodes
            node = _LinkedListNode(nodes.pop(0))
            # set `self.head` to the above-defined variable `node`
            self.head = node
            # loop over each of the nodes in the nodes provided in this function's arguments
            for thisNode in nodes:
                # set the current node's next node to a new `_LinkedListNode` object of `thisNode`
                node.nextNode = _LinkedListNode(thisNode)
                # set the current node to the next node to move on
                node = node.nextNode

    def __iter__(self) -> Generator[_LinkedListNode[T], None, None]:
        """Helper method to iterate over items in the list. Yields each value (rather than return everything as a list) as to not use up potentially infinite memory.
        The `yield` statement pauses the function, saving all its states and later continues from there on successive calls.

        Yields:
            _LinkedListNode: The next node in the linked list — either element 0 of the list, or the `nextNode` attribute of the previous node.

        Instantiate a `LinkedList` and print it all out, testing iteration and generator
        >>> myLinkedList = LinkedList[str](['People', 'often', 'joke', 'that', 'in', 'order', 'to', 'understand', 'recursion,', 'you', 'must', 'first', 'understand', 'recursion.'])
        >>> sentence = ' '.join([listItem.data for listItem in myLinkedList])
        >>> sentence
        'People often joke that in order to understand recursion, you must first understand recursion.'
        """
        # check that there are actually any items in the list
        if self.head is not None:
            # set node to an optional `_LinkedListNode` of type `T` so we can set it to the next node, which may or may not be optional. The optional allows us to check the next node exists and not accidentally yield a `None` value.
            node: Optional[_LinkedListNode[T]] = self.head
            # check the (next) node exists
            while node is not None:
                # yield the node, pausing the function, saving its states and allowing it to continue from here on successive calls.
                yield node
                # set node to the next node referenced by this node. This may or may not exist, hence we have to be careful and unwrap the value as we have above.
                node = node.nextNode

    def insertAtBeginning(self, node: _LinkedListNode[T]) -> None:
        """Recursively inserts any number of nodes in the beginning of this LinkedList by checking if each provided node's `nextNode` attribute is set.

        Args:
            node (_LinkedListNode[T]): The node to add potentially with a nextNode attribute, which may contain a node with a nextNode attribute, which may contain a node with a nextNode attribute, which may contain a node with a nextNode attribute, which...

        >>> somePrimeNumbers = LinkedList[int]([11, 13, 17, 19])
        >>> someSmallerPrimeNumbers = LinkedList[int]([2, 3, 5, 7])
        >>> somePrimeNumbers.insertAtBeginning(someSmallerPrimeNumbers.head)
        >>> ' '.join([str(listItem.data) for listItem in somePrimeNumbers])
        '2 3 5 7 11 13 17 19'
        """
        # check if this node has a `nextNode`, and if so, call this same function on the `nextNode`, again and again, until there's no `nextNode`...
        if node.nextNode is None:
            # `node.nextNode` is None
            # this node's `nextNode` is None so we can set its `nextNode` to `self.head`... -->
            node.nextNode = self.head
        else:
            # `node.nextNode` is *not* None
            # so we call this function recursively to traverse the chain of `_LinkedListNodes` to be able to find the last node in the list and add them to our list.
            self.insertAtBeginning(node.nextNode)
            # --> ...and after we have gotten to setting the node (whose `nextNode` is none) to `self.head`, we then set our `self.head` to the node to have finished inserting the nodes.
            self.head = node

    def extend(self, node: _LinkedListNode[T], insertOnto: Optional[_LinkedListNode[T]] = None) -> None:
        """Recursively appends nodes to the end of this LinkedList by checking each of this LinkedList's node's `nextNode` attribute is set.

        Args:
            node (_LinkedListNode[T]): The node or chain of nodes you wish to append to the LinkedList.
            insertOnto (Optional[_LinkedListNode[T]]): The node or chain of nodes to insert `node` onto the end of. Don't worry about this if you simply want to insert onto the end of the `LinkedList` because it traverses that automatically. Defaults to `self.head`.

        >>> shoppingList = LinkedList[str](['breadboard', '7-segment display', 'LEDs'])
        >>> moreStuffForTheShoppingList = LinkedList[str](['AND gate ICs', 'NOT gate ICs', 'OR gate ICs', 'lots of connection wires'])
        >>> shoppingList.extend(moreStuffForTheShoppingList.head)
        >>> ', '.join([str(listItem.data) for listItem in shoppingList])
        'breadboard, 7-segment display, LEDs, AND gate ICs, NOT gate ICs, OR gate ICs, lots of connection wires'
        """
        if insertOnto is None:
            # note that this function is being called without an `insertOnto` parameter, meaning we want to insert it onto the end of the `self.head` node chain.
            if self.head is None:
                # `self.head` is None so we can simply set it to the given node.
                self.head = node
            else:
                self.extend(node, insertOnto=self.head)
        # `insertOnto` is not None >
        else:
            # > meaning we have recursively called this function and intend to chain our inserts from one node to its `nextNode`.
            if insertOnto.nextNode is not None:
                # call this function (recursively) with the `nextNode` of the `insertOnto` argument of this function call.
                self.extend(node, insertOnto.nextNode)
            else:
                # `insertOnto.nextNode` is None
                # We've traversed the entire chain and got to the end, where `nextNode` has no value.
                insertOnto.nextNode = node

    def removeNode(self, toRemove: T, node: Optional[_LinkedListNode[T]] = None) -> None:
        """Remove a node with data `toRemove` from the list.

        Args:
            toRemove (T): The data of the node to remove. The first node with this data will be the one removed.
            node (Optional[_LinkedListNode[T]], optional): Parameter used for recursively calling this function –
            don't worry about this if you plan on starting at the start of this LinkedList. Defaults to None.

        Raises:
            Exception: List is empty, therefore the function cannot remove any value.
            Exception: The provided data was not found in any node.
        
        >>> animalsThatFly = LinkedList[str](['crocodile', 'duck', 'pigeon', 'cow', 'goose', 'swan', 'pig'])

        Test removing a node at the start of the list
        >>> animalsThatFly.removeNode('crocodile')
        >>> ', '.join([str(animal.data) for animal in animalsThatFly])  # remove node at start
        'duck, pigeon, cow, goose, swan, pig'

        Test removing a node in the middle of the list
        >>> animalsThatFly.removeNode('cow')
        >>> ', '.join([str(animal.data) for animal in animalsThatFly])  # remove node in middle
        'duck, pigeon, goose, swan, pig'

        Test removing a node at the end of the list
        >>> animalsThatFly.removeNode('pig')
        >>> ', '.join([str(animal.data) for animal in animalsThatFly])  # remove node at end
        'duck, pigeon, goose, swan'
        """

        # remove node at the specified index by linking the node before it to the node after it

        # check the specified node is `None` to see if we are starting at the beginning of this LinkedList or from a different node
        if node is None:
            # set `node` to `self.head` to traverse the list from the beginning
            if self.head is not None:
                node = self.head
                # if the start of the list is the one we want to remove, just set `self.head` to the next one
                if node.data == toRemove:
                    self.head = node.nextNode
                    return
            else:
                raise Exception("List is empty.")
        
        # node has been set to `self.head`
        # check that this node's nextNode is the right one
        if node.nextNode is None:
            # we have traversed the entire list without finding the desired item
            raise Exception("Node not found with data \'{}\'.".format(toRemove))

        if node.nextNode.data == toRemove:
            # the next node is the one we must remove.
            # set this node's `nextNode` to its `nextNode`'s `nextNode`:
            node.nextNode = node.nextNode.nextNode
            # we are making the list 'skip out' the next node and instead pointing it to the one after that.
        else:
            # the next node is not the wanted one just yet, so we recursively call this same function with the `node` parameter as this node's `nextNode`.
            self.removeNode(toRemove, node.nextNode)