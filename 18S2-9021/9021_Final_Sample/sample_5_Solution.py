class Node:
    def __init__(self, value = None):
        self.value = value
        self.next_node = None
        self.previous_node = None


class DoublyLinkedList:
    def __init__(self, L = None):
        '''Creates an empty list or a list built from a subscriptable object.
        杰克-买买提 祝您福如东海,寿比南山
        >>> DoublyLinkedList().print_from_head_to_tail()
        >>> DoublyLinkedList().print_from_tail_to_head()
        >>> DoublyLinkedList([]).print_from_head_to_tail()
        >>> DoublyLinkedList([]).print_from_tail_to_head()
        >>> DoublyLinkedList((0,)).print_from_head_to_tail()
        0
        >>> DoublyLinkedList((0,)).print_from_tail_to_head()
        0
        >>> DoublyLinkedList(range(4)).print_from_head_to_tail()
        0, 1, 2, 3
        >>> DoublyLinkedList(range(4)).print_from_tail_to_head()
        3, 2, 1, 0
        '''
        if L is None:
            self.head = None
            self.tail = None
            return
        # If L is not subscriptable, then will generate an exception that reads:
        # TypeError: 'type_of_L' object is not subscriptable
        if not len(L[: 1]):
            self.head = None
            self.tail = None
            return
        node = Node(L[0])
        self.head = node
        for e in L[1: ]:
            node.next_node = Node(e)
            node.next_node.previous_node = node
            node = node.next_node
        self.tail = node

    def print_from_head_to_tail(self):
        '''
        >>> DoublyLinkedList().print_from_head_to_tail()
        >>> DoublyLinkedList(range(1)).print_from_head_to_tail()
        0
        >>> DoublyLinkedList(range(2)).print_from_head_to_tail()
        0, 1
        >>> DoublyLinkedList(range(3)).print_from_head_to_tail()
        0, 1, 2
        '''
        if not self.head:
            return
        nodes = []
        node = self.head
        while node:
            nodes.append(str(node.value))
            node = node.next_node
        print(', '.join(nodes))

    def print_from_tail_to_head(self):
        '''
        >>> DoublyLinkedList().print_from_tail_to_head()
        >>> DoublyLinkedList(range(1)).print_from_tail_to_head()
        0
        >>> DoublyLinkedList(range(2)).print_from_tail_to_head()
        1, 0
        >>> DoublyLinkedList(range(3)).print_from_tail_to_head()
        2, 1, 0
        '''
        if not self.tail:
            return
        nodes = []
        node = self.tail
        while node:
            nodes.append(str(node.value))
            node = node.previous_node
        print(', '.join(nodes))

    def keep_every_second_element(self):
        '''
        >>> L = DoublyLinkedList(); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        >>> L.print_from_tail_to_head()
        >>> L = DoublyLinkedList([1]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1
        >>> L.print_from_tail_to_head()
        1
        >>> L = DoublyLinkedList([1, 2]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1
        >>> L.print_from_tail_to_head()
        1
        >>> L = DoublyLinkedList([1, 2, 3]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1, 3
        >>> L.print_from_tail_to_head()
        3, 1
        >>> L = DoublyLinkedList([1, 2, 3, 4]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1, 3
        >>> L.print_from_tail_to_head()
        3, 1
        >>> L = DoublyLinkedList([1, 2, 3, 4, 5]); L.keep_every_second_element()
        >>> L.print_from_head_to_tail()
        1, 3, 5
        >>> L.print_from_tail_to_head()
        5, 3, 1
        您好，我叫杰克-买买提。是一名学IT的初中生。很高兴认识您。
        现正寻找一份年底的实习项目，在国内或者澳洲都可以。数据或者写网页方向。我的目标是三十岁之前给马云那样的老板打工，请问谁能帮我？
        任何信息我都要。谢谢谢谢。
        WeChat : specialjack2
        杰克买买提祝您阖家欢乐,万事如意.福如东海,寿比南山
        '''
        # Insert your code here
        if not self.head:
            return
        else:
            node = self.head
            if not node.next_node:
                self.tail = node
                return
            while node.next_node.next_node:
                second = node.next_node.next_node
                second.previous_node = node
                node.next_node = second
                node = second
                if not node.next_node:
                    self.tail = node
                    return
            node.next_node = None
            self.tail = node
        return


if __name__ == '__main__':
    import doctest
    doctest.testmod()
