from brains.orientation import Orientation
from brains.a_star import get_shortest_path

class MazeNode(object):
    def __init__(self, id, distance, orientation):
        self.id = id
        self.distance = distance
        self.orientation = orientation

    def copy(self):
        return MazeNode(self.id, self.distance, self.orientation)


class MazePath(object):
    def __init__(self, orientation):
        self.next_node_id = 0
        self.current_node = MazeNode(self.next_node_id, 0, orientation)
        self.nodes = dict()
        self.coordinates = dict()
        self.path = [self.current_node]

    def add_node(self, orientation, distance):
        self.next_node_id += 1
        node = MazeNode(self.next_node_id, distance, orientation)

        # connect newly found node to current one
        if self.current_node.id not in self.nodes:
            self.nodes[self.current_node.id] = []
        self.nodes[self.current_node.id].append(node)

        # connect current node to newly found but change orientation
        if node.id not in self.nodes:
            self.nodes[node.id] = []
        reverse_orientation_node = self.current_node.copy()
        reverse_orientation_node.orientation = Orientation.flip(reverse_orientation_node.orientation)
        reverse_orientation_node.distance = distance
        self.nodes[node.id].append(reverse_orientation_node)

        self.visit_node(node)

        # remember coordinates of this noe
        self.add_coordinates()

    def visit_node(self, node):
        self.path.append(node)
        self.current_node = node


    def get_last_visited_node(self):
        return self.path[len(self.path)-1]

    def get_xy_from_distance(self, orientation, distance):
        x = y = 0

        if orientation == Orientation.EAST:
            x += distance
        if orientation == Orientation.WEST:
            x -= distance
        if orientation == Orientation.SOUTH:
            y += distance
        if orientation == Orientation.NORTH:
            y -= distance

        return x, y

    def get_coordinates(self, orientation, distance):
        x = y = 0
        for i in range(len(self.path)):
            node = self.path[i]
            xi, yi = self.get_xy_from_distance(node.orientation, node.distance)
            x += xi
            y += yi

        xi, yi = self.get_xy_from_distance(orientation, distance)
        x += xi
        y += yi

        return [x, y]

    def add_coordinates(self, orientation = Orientation.NORTH, distance = 0):
        self.coordinates[str(self.get_coordinates(orientation, distance))] = self.current_node

    def where_i_am(self, orientation = Orientation.NORTH, distance = 0):
        pos = str(self.get_coordinates(orientation, distance))

        if pos in self.coordinates:
            return self.coordinates[pos]

        return None

    def if_was_here(self, orientation = Orientation.NORTH, distance = 0):
        return self.where_i_am(orientation, distance) is not None

class MazeMap(object):
    def __init__(self, car):
        self.path = MazePath(car.orientation)
        self.distance = 0

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
        self.reset_distance()

    def on_crossing(self, car, orientation):
        node = self.path.where_i_am(orientation,self.distance)
        if node is None:
            self.make_node(orientation)
        else:
            new_node = node.copy()
            new_node.orientation = orientation
            new_node.distance = self.distance
            self.path.visit_node(new_node)
            self.reset_distance()

    def get_shortest_path(self):
        edges = dict()
        for node in self.path.nodes:
            edges[node] = dict()
            current = edges[node]
            for neighbor in self.path.nodes[node]:
                current[neighbor.id] = neighbor.distance

        return get_shortest_path(edges, 0, self.path.get_last_visited_node().id)