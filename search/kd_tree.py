# code from https://en.wikipedia.org/wiki/K-d_tree

from collections import namedtuple
from operator import itemgetter
from pprint import pformat


class Node(namedtuple('Node', 'location left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))


def kdtree(points, depth=0):
    try:
        dim = len(points[0])
    except IndexError:
        return None

    axis = depth % dim

    # sort and choose median as pivot element
    points.sort(key=itemgetter(axis))
    median = len(points) // 2

    return Node(
        location=points[median],
        left_child=kdtree(points[:median], depth+1),
        right_child=kdtree(points[median+1:], depth+1)
    )


def main():
    points = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    tree = kdtree(points)
    print(tree)

if __name__ == '__main__':
    main()
