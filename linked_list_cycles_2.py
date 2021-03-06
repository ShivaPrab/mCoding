from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, Iterator

T = TypeVar('T')


@dataclass
class Node(Generic[T]):
    data: T
    next: Optional['Node[T]']


class LinkedList(Generic[T]):

    def __init__(self):
        self.head: Optional[Node[T]] = None

    def push_left(self, value: T) -> None:
        node = Node(value, None)
        node.next = self.head
        self.head = node

    def __str__(self) -> str:
        return f'[{",".join(map(str, self.iter_values()))}]'

    def iter_nodes(self, limit: int = -1) -> Iterator[T]:
        node = self.head
        while node and limit:
            yield node
            node = node.next
            limit -= 1

    def iter_values(self, limit: int = -1) -> Iterator[T]:
        for node in self.iter_nodes(limit):
            yield node.data

    def get_node(self, item) -> Node[T]:
        if not (isinstance(item, int) and item >= 0):
            raise ValueError(f'Index must be non-negative int, got: {item}')
        n = 0
        for node in self.iter_nodes():
            if n == item:
                return node
            n += 1
        raise KeyError(item)

    def __getitem__(self, item) -> T:
        return self.get_node(item).data

    def find_cycle_prefer_speed_over_memory(self) -> Optional[Node[T]]:
        seen: set[int] = set()
        for node in self.iter_nodes():
            if id(node) in seen:
                return node
            seen.add(id(node))
        return None

    def find_cycle_prefer_memory_over_speed(self) -> Optional[Node[T]]:
        tort = self.tortoise_hare_meeting_point()
        if tort is None:
            return None
        node = self.head
        while tort is not node:
            tort = tort.next
            node = node.next
        return tort

    def is_cyclic(self) -> bool:
        return self.tortoise_hare_meeting_point() is not None

    def tortoise_hare_meeting_point(self) -> Optional[Node[T]]:
        tort: Node[T] = self.head
        hare: Node[T] = self.head

        while hare and hare.next:
            hare = hare.next.next
            tort = tort.next
            if tort is hare:
                return tort

        return None


def main():
    ll = LinkedList()
    for value in reversed(range(6)):
        ll.push_left(value)
    print(ll)
    print(ll.is_cyclic())

    ll.get_node(5).next = ll.get_node(3)
    print(ll.is_cyclic())

    for node in ll.iter_nodes(limit=16):
        print(node.data, end=',')

    print()
    print(ll.find_cycle_prefer_speed_over_memory().data)
    print(ll.find_cycle_prefer_memory_over_speed().data)


if __name__ == '__main__':
    main()
