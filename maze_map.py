from orientation import Orientation

class MazeNode(object):
    def __init__(self, id):
        self.id = id
        self.connections = dict()


class MazeConnection(object):
    def __init__(self, node1, node2, distance, orientation):
        self.node1 = node1
        self.node2 = node2
        self.distance = distance
        self.orientation = orientation

    @staticmethod
    def make(node1, node2, distance, orientation):
        node1.connections[node2.id] = MazeConnection(node1, node2, distance, orientation)
        node2.connections[node1.id] = MazeConnection(node1, node2, distance, Orientation.flip(orientation))


class MazePath(object):
    def __init__(self):
        self.next_node_id = 0
        self.current_node = None
        self.nodes = dict()

    def add_node(self, orientation, distance):
        self.next_node_id += 1
        node = MazeNode(self.next_node_id)
        self.nodes[self.next_node_id] = node

        if self.current_node is not None:
            MazeConnection.make(self.current_node, node, distance, orientation)

        self.current_node = node


class MazeMap(object):
    def __init__(self, car = None):
        self.path = MazePath()
        self.distance = 0

        if car is not None:
            car.on_move.append(self.on_move)
            car.on_rotate.append(self.on_rotate)
            car.on_crossing.append(self.on_crossing)
            self.make_node(car.orientation)

    def make_node(self, orientation):
        if self.distance > 0:
            self.path.add_node(orientation, self.distance)
            self.reset_distance()

    def increment_distance(self):
        self.distance += 1

    def reset_distance(self):
        self.distance = 0

    def on_move(self, car, orientation):
        self.increment_distance()

    def on_rotate(self, car, orientation):
        pass

    def on_crossing(self, car, orientation):
        self.make_node(orientation)
