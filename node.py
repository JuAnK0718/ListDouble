# node.py - Doubly linked list node


class Quasar:
    """
    Represents a node in a doubly linked list.
    Each Quasar holds a patient record and links to adjacent nodes.
    """

    def __init__(self, data):
        self.data = data        # Patient object stored in this node
        self.next = None        # Pointer to the next node
        self.previous = None    # Pointer to the previous node

    def __str__(self):
        return f"Quasar({self.data})"
