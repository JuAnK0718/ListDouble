# nebula_list.py - Doubly linked list implementation


from node import Quasar


class NebulaList:
    """
    Custom doubly linked list that manages patient records.
    Each element is a Quasar node connected bidirectionally.
    Supports insertion, deletion, search, and traversal.
    """

    def __init__(self):
        self.head = None    # First node in the list
        self.tail = None    # Last node in the list
        self.size = 0       # Total number of nodes

    # ── Insertion ──────────────────────────────────────────────

    def insert_at_end(self, data):
        """Add a new Quasar node at the end of the list."""
        new_node = Quasar(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def insert_at_beginning(self, data):
        """Add a new Quasar node at the beginning of the list."""
        new_node = Quasar(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        self.size += 1

    def insert_at_position(self, data, position):
        """Insert a node at a specific index (0-based)."""
        if position <= 0:
            self.insert_at_beginning(data)
            return
        if position >= self.size:
            self.insert_at_end(data)
            return

        new_node = Quasar(data)
        current = self.head
        for _ in range(position - 1):
            current = current.next

        new_node.next = current.next
        new_node.previous = current
        if current.next:
            current.next.previous = new_node
        current.next = new_node
        self.size += 1

    # ── Deletion ───────────────────────────────────────────────

    def delete_by_id(self, patient_id):
        """Remove the node whose patient has the given ID."""
        current = self.head
        while current:
            if current.data.patient_id == patient_id:
                if current.previous:
                    current.previous.next = current.next
                else:
                    self.head = current.next

                if current.next:
                    current.next.previous = current.previous
                else:
                    self.tail = current.previous

                self.size -= 1
                return True
            current = current.next
        return False

    # ── Search ─────────────────────────────────────────────────

    def search_by_id(self, patient_id):
        """Return the patient object matching the given ID, or None."""
        current = self.head
        while current:
            if current.data.patient_id == patient_id:
                return current.data
            current = current.next
        return None

    def search_by_name(self, name):
        """Return a list of patients whose name contains the search string."""
        results = []
        current = self.head
        while current:
            if name.lower() in current.data.name.lower():
                results.append(current.data)
            current = current.next
        return results

    # ── Traversal ──────────────────────────────────────────────

    def traverse_forward(self):
        """Return all patient records from head to tail."""
        records = []
        current = self.head
        while current:
            records.append(current.data)
            current = current.next
        return records

    def traverse_backward(self):
        """Return all patient records from tail to head."""
        records = []
        current = self.tail
        while current:
            records.append(current.data)
            current = current.previous
        return records

    # ── Utilities ──────────────────────────────────────────────

    def is_empty(self):
        return self.size == 0

    def get_size(self):
        return self.size

    def __str__(self):
        items = [str(node.data) for node in self._iter_nodes()]
        return " <-> ".join(items) if items else "Lista vacía"

    def _iter_nodes(self):
        current = self.head
        while current:
            yield current
            current = current.next
