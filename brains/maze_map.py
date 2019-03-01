from misc.orientation import Orientation
from misc.direction import Direction
import brains.a_star as a_star
from misc.log import log
from time import time


class MazeNode(object):
    def __init__(self, id, coordinates):
        self.id = id
        self.coordinates = coordinates

    def copy(self):
        return MazeNode(
            self.id,
            self.coordinates)


class MazeEdge(object):
    def __init__(self, node_a, node_b, distance, orientation):
        self.node_a = node_a
        self.node_b = node_b
        self.distance = distance
        self.orientation = orientation
        self.id = MazeEdge.get_id(node_a, node_b)

    @staticmethod
    def get_id(node_a, node_b):
        return '{}->{}'.format(node_a.id, node_b.id)


class MazeEdgeDict(object):
    def __init__(self):
        self.edges = dict()

    def exists(self, node_a, node_b):
        return MazeEdge.get_id(node_a, node_b) in self.edges.keys()

    def add(self, node_a, node_b, orientation, distance):
        self.edges[MazeEdge.get_id(node_a, node_b)] = MazeEdge(
            node_a,
            node_b,
            distance,
            orientation
            )

    def get(self, node_a, node_b):
        return self.edges[MazeEdge.get_id(node_a, node_b)]

    def get_neighbors(self, node_a):
        return filter(lambda x: x.node_a == node_a, self.edges.values())

    def get_edges(self):
        return self.edges


class MazePath(object):
    def __init__(self, orientation, time_error):
        self.next_node_id = 0
        self.current_node = MazeNode(self.next_node_id, [0, 0])
        self.nodes = dict()
        self.edges = MazeEdgeDict()
        self.path = [self.current_node]
        self.time_error = time_error

    def add_node(self, orientation, distance, coordinates):
        self.next_node_id += 1
        node = MazeNode(self.next_node_id, coordinates)

        # add node in nodes list
        self.nodes[self.next_node_id] = node

        # connect newly found node to current one
        if not self.edges.exists(self.current_node, node):
            self.edges.add(
                self.current_node,
                node,
                orientation,
                distance
            )

        # connect current node to newly found but change orientation
        if not self.edges.exists(node, self.current_node):
            self.edges.add(
                node,
                self.current_node,
                Orientation.flip(orientation),
                distance
            )

        # mark new node as visited and make it current
        self.visit_node(node)

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
        [x, y] = [0, 0]
        if self.get_last_visited_node() is not None:
            [x, y] = self.get_last_visited_node().coordinates

        xi, yi = self.get_xy_from_distance(orientation, distance)
        x += xi
        y += yi

        return [x, y]

    def find_node(self, pos):
        for node in self.nodes.values():
            coord = node.coordinates
            if (coord[0] - self.time_error <= pos[0] and
                    pos[0] <= coord[0] + self.time_error and
                    coord[1]-self.time_error <= pos[1] and
                    pos[1] <= coord[1]+self.time_error):
                return node

        return None

    def where_i_am(self, orientation=Orientation.NORTH, distance=0):
        return self.get_coordinates(orientation, distance)

    def if_was_here(self, orientation=Orientation.NORTH, distance=0):
        return self.find_node(
            self.get_coordinates(orientation, distance)
            ) is not None


class MazeMap(object):
    def __init__(self, car, time_error=0, time_to_turn=0):
        self.time_error = time_error
        self.time_to_turn = time_to_turn
        self.path = MazePath(car.orientation, time_error)
        self.reset_distance()

        car.chassis.add_on_move_callback(self.on_move)
        car.chassis.add_on_rotate_callback(self.on_rotate)

        self.add_node(car.orientation, [0, 0])

    def add_node(self, orientation, coordinates):
        distance = self.get_distance()

        if distance > self.time_error:
            self.path.add_node(orientation, distance, coordinates)
            self.reset_distance()

    def increment_distance(self):
        pass

    def reset_distance(self, time_bias=0):
        self.distance = time()

    def get_distance(self):
        return time() - self.distance

    def on_move(self, car):
        self.increment_distance()

    def on_rotate(self, car):
        self.reset_distance(self.time_to_turn)

    def on_crossing(self, car):
        """When car faces new crossing - add a node to a map

        Arguments:
            car {Car} -- Well, a Car instance
        """

        # how long did we pass since last turn/crossing
        distance = self.get_distance()

        # what is our current absolute position
        pos = self.path.where_i_am(car.orientation, distance)

        # did we visit this place before?
        node = self.path.find_node(pos)

        # no we did not - add this node to nodes list
        if node is None:
            self.add_node(car.orientation, pos)
        else:
            # make sure this is not the same node
            # (we do another turn by mistake)
            if node.id != self.path.current_node.id:
                self.path.visit_node(node)
                self.reset_distance()

    def get_shortest_path(self, reverse=False):
        """Convert map to edges and use graph algorythms to find shortest path

        Keyword Arguments:
            reverse {bool} -- If we need to find way from end to beginning
            (default: {False})

        Returns:
            [list] -- List of node IDs to follow on shortest path
        """

        edges = dict()
        for node in self.path.nodes.values():
            current = dict()
            edges[node.id] = current
            for neighbor in self.path.edges.get_neighbors(node):
                current[neighbor.node_b.id] = neighbor.distance

        return a_star.get_shortest_path(
            edges,
            self.path.get_last_visited_node().id if reverse else 0,
            0 if reverse else self.path.get_last_visited_node().id
            )

    def navigate(self, path, current_node_id, orientation):
        """Each call to this function takes next point on
        the route and returns direction where to go to reach it

        Arguments:
            path {list} -- list of node IDs to follow - a path basically
            current_node_id {int} -- ID of node where car stands now
            orientation {Orientation} -- where car currently "looks",
            e.g. where it is oriented

        Returns:
            [Direction] -- direction car has to go to reach next node in path
        """

        ind = path.index(current_node_id)

        if ind + 1 == len(path):
            # this means we reached the end of route
            return None

        # get actual current node object by node ID
        current_node = None
        for node in self.path.path:
            if node.id == current_node_id:
                current_node = node
                break

        # fetch next node id from path
        next_node_id = path[ind + 1]
        next_node = None

        # get node by node ID
        for node in self.path.nodes[current_node_id]:
            if node.id == next_node_id:
                next_node = node
                break

        # find difference of nodes coordinates
        x = next_node.coordinates[0] - current_node.coordinates[0]
        y = next_node.coordinates[1] - current_node.coordinates[1]

        # detect which direction to go basing on coordinates diff
        node_orientation = None
        if abs(y) > abs(x):
            # south or north?
            if y < 0:
                node_orientation = Orientation.NORTH
            else:
                node_orientation = Orientation.SOUTH
        else:
            # west or east?
            if x < 0:
                node_orientation = Orientation.WEST
            else:
                node_orientation = Orientation.EAST

        if Orientation.rotate_cw(orientation) == node_orientation:
            return Direction.RIGHT

        if Orientation.rotate_ccw(orientation) == node_orientation:
            return Direction.LEFT

        if Orientation.flip(orientation) == node_orientation:
            return Direction.BACK

        return Direction.FORWARD

    def save_full_path(self, output):
        """
        Saves full path travelled in a stream as text
        :param output: output stream
        """
        x_range = [0, 0]
        y_range = [0, 0]

        time_inc = self.time_error  # * 2

        # first we find lefr-and-right-most as well as
        # top-and-bottom-most values of coordinates
        for node in self.path.path:
            coord = node.coordinates

            if coord[0] < y_range[0]:
                y_range[0] = coord[0]
            if coord[0] > y_range[1]:
                y_range[1] = coord[0]

            if coord[1] < x_range[0]:
                x_range[0] = coord[1]
            if coord[1] > x_range[1]:
                x_range[1] = coord[1]

        # fill text map with -- first
        coord_map = [['--' for i in range(
            round(y_range[1] / time_inc) -
            round(y_range[0] / time_inc) + 1)] for j in range(
                round(x_range[1] / time_inc) -
                round(x_range[0] / time_inc) + 1
                )]

        path = self.path.path

        # transform time/distance between nodes into list indexes
        y_base, x_base = abs(
            round(x_range[0] / time_inc)
            ), abs(
                round(y_range[0] / time_inc)
                )

        x, y = 0, 0
        prev_node = None
        for i in range(len(path)):
            node = path[i]

            if prev_node is None:
                prev_node = node
                continue

            # find edge leading from prev node to current one
            edge = self.path.edges.get(prev_node, node)
            prev_node = node

            xi, yi = self.path.get_xy_from_distance(
                edge.orientation,
                edge.distance)

            xr, yr = round(
                x / time_inc
                ) + x_base, round(
                    y / time_inc
                    ) + y_base

            xir, yir = round(xi / time_inc), round(yi / time_inc)

            # calculate list indexes where XX have to be put
            # to show path from prev node to current node
            x_range = [min(xr, xr + xir), max(xr, xr + xir)]
            y_range = [min(yr, yr + yir), max(yr, yr + yir)]

            # put XX where the path goes and node IDs at crossings
            for j in range(x_range[0], x_range[1] + 1):
                for jj in range(y_range[0], y_range[1] + 1):
                    try:
                        if (
                            coord_map[jj][j] == '--' or
                            coord_map[jj][j] == 'XX'
                        ):
                            coord_map[jj][j] = 'XX'
                    except:
                        pass

            # add node (crossing) id on the map
            coord_map[yr + yir][xr + xir] = (
                        '0'+str(node.id)
                        ) if node.id < 10 else str(node.id)
            x += xi
            y += yi

        for line in coord_map:
            for char in line:
                output.write(char)
            output.write('\n')
