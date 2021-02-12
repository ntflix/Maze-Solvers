from modules.data_structures.stack.stack import Stack
import unittest


class TestStack(unittest.TestCase):
    def testEmptyStackLength(self):
        """Initialize a Stack with 0 elements and test its length."""

        stack = Stack[int]()
        # stack should have a length of 0
        self.assertEqual(
            len(stack),
            0,
        )

    def testPushElementsToStack(self):
        """Push a few elements to the stack, testing its length each time."""

        stack = Stack[int]()
        # push a test element to the stack
        stack.push(1)

        # the stack should be of length 1
        self.assertEqual(
            len(stack),
            1,
        )

        # push another test element to the stack
        stack.push(1)

        # the stack should be of length 2
        self.assertEqual(
            len(stack),
            2,
        )

    def testPoppedValueFromStack(self):
        """Push a few items to the stack, and then pop them one-by-one,
        testing that they are correct and the length of the stack decreases."""

        stack = Stack[str]()
        stack.push("first element")
        stack.push("second element")

        # pop top element, test it is correct element, and test stack size OK
        secondElement = stack.pop()
        self.assertEqual(secondElement, "second element")
        self.assertEqual(
            len(stack),
            1,
        )

        firstElement = stack.pop()
        self.assertEqual(firstElement, "first element")
        self.assertEqual(
            len(stack),
            0,
        )

    def testErroneousPop(self):
        """Initialise an empty stack and try to pop an element."""
        stack = Stack[int]()

        # should throw error bc no elements
        with self.assertRaises(IndexError):
            # there are no elements on the stack so this should throw an error
            stack.pop()

        # length of stack should still be 0
        self.assertEqual(
            len(stack),
            0,
        )


if __name__ == "__main__":
    unittest.main()