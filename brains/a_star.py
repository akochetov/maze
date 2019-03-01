"""Functions to perform graph shortest path search with A Star algorythm
"""


class Queue(object):
    """Simple objects queue

    Arguments:
        object {any} -- Object to put in queue
    """

    def __init__(self):
        self.queue = []

    def put(self, element):
        self.queue.append(element)

    def get(self):
        return self.queue.pop(0)

    def empty(self):
        return len(self.queue) == 0


def get_path(came_from, a, b):
    path = [a]
    next = b
    while next != a:
        path.insert(1, next)
        if next not in came_from:
            path = []
            break
        next = came_from[next]

    return path


def get_shortest_path(edges, a, b):
    frontier = Queue()
    frontier.put(a)
    came_from = {}
    cost_so_far = {}
    came_from[a] = None
    cost_so_far[a] = 0

    while not frontier.empty():
        current = frontier.get()

        if current == b:
            break

        for next in edges[current].keys():
            new_cost = cost_so_far[current] + edges[current][next]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                frontier.put(next)
                came_from[next] = current

    return get_path(came_from, a, b)
