class LinkedListNode:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

    def __repr__(self):
        return f'{self.value}'


class Linkedlist:
    def __init__(self, head=None):
        self.head = head

    def add(self, value):
        if self.head is None:
            self.head = LinkedListNode(value)
        else:
            new_node = LinkedListNode(value, self.head)
            self.head = new_node

    def get_at(self, position):
        current_node = self.head
        for i in range(position):
            current_node = current_node.next_node
        return current_node.value

    def add_first(self, value):
        node = self.head

        if self.head is None:
            self.head = LinkedListNode(value)
        else:
            while node.next_node is not None:
                node = node.next_node
            node.next_node = LinkedListNode(value, node)

    def size(self):
        s = 0
        node = self.head
        while node is not None:
            node = node.next_node
            s += 1
        return s

    def __to_array(self):
        array = []
        node = self.head
        while node is not None:
            array.append(node)
            node = node.next_node
        array.reverse()
        return array

    def __repr__(self):
        return f'{self.__to_array()}'
