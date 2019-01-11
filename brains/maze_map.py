from misc.orientation import Orientation
import brains.a_star as a_star
from time import time


class MazeNode(object):
    def __init__(self, id, distance, orientation):
        self.id = id
        self.distance = distance
        self.orientation = orientation

    def copy(self):
        return MazeNode(self.id, self.distance, self.orientation)


class MazePath(object):
    def __init__(self, orientation, time_error):
        self.next_node_id = 0
        self.current_node = MazeNode(self.next_node_id, 0, orientation)
        self.nodes = dict()
        self.coordinates = []
        self.path = [self.current_node]
        self.time_error = time_error

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
        reverse_orientation_node.orientation = Orientation.flip(
            reverse_orientation_node.orientation
            )
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

    def add_coordinates(self, orientation=Orientation.NORTH, distance=0):
        coord = self.get_coordinates(orientation, distance)

        self.coordinates.append(
            [coord[0], coord[1], self.current_node]
                )
        # print(
        #    'add_coordinates: {}',
        #    str(self.get_coordinates(orientation, distance))
        #    )

    def find_coordinates(self, pos):
        for coord in self.coordinates:
            if (coord[0] - self.time_error <= pos[0] and
                    pos[0] <= coord[0] + self.time_error and
                    coord[1]-self.time_error <= pos[1] and
                    pos[1] <= coord[1]+self.time_error):
                return coord[2]

        return None

    def where_i_am(self, orientation=Orientation.NORTH, distance=0):
        pos = self.get_coordinates(orientation, distance)

        ret = self.find_coordinates(pos)
        if ret is not None:
            return ret

        return None

    def if_was_here(self, orientation=Orientation.NORTH, distance=0):
        return self.where_i_am(orientation, distance) is not None


class MazeMap(object):
    def __init__(self, car, time_error=0, time_to_turn=0):
        self.time_error = time_error
        self.time_to_turn = time_to_turn
        self.path = MazePath(car.orientation, time_error)
        self.reset_distance()

        car.chassis.add_on_move_callback(self.on_move)
        car.chassis.add_on_rotate_callback(self.on_rotate)
        self.__make_node(car.orientation)

    def __make_node(self, orientation):
        distance = self.get_distance()
        if distance > self.time_error:
            self.path.add_node(orientation, distance)
            self.reset_distance()

    def increment_distance(self):
        pass
        # self.distance += 1

    def reset_distance(self, time_bias=0):
        # self.distance = 0
        self.distance = time()

    def get_distance(self):
        # return self.distance
        return time() - self.distance

    def on_move(self, car):
        self.increment_distance()

    def on_rotate(self, car):
        self.reset_distance(self.time_to_turn)

    def on_crossing(self, car):
        distance = self.get_distance()

        node = self.path.where_i_am(car.orientation, distance)
        if node is None:
            self.__make_node(car.orientation)
        else:
            new_node = node.copy()
            new_node.orientation = car.orientation
            new_node.distance = distance if distance >= self.time_error else 0
            self.path.visit_node(new_node)
            self.reset_distance()

    def get_shortest_path(self):
        edges = dict()
        for node in self.path.nodes:
            edges[node] = dict()
            current = edges[node]
            for neighbor in self.path.nodes[node]:
                current[neighbor.id] = neighbor.distance

        return a_star.get_shortest_path(
            edges,
            0,
            self.path.get_last_visited_node().id
            )

    def save_full_path(self, output):
        """
        Saves full path travelled in a stream as text
        :param output: output stream
        """
        self.__save(output)

    def __save(self, output):
        '''Internal method to save specific nodes sequence into a file as text

        Arguments:
            node_ids {list of int} -- Node IDs which have to be saved
        '''
        x_range = [0, 0]
        y_range = [0, 0]

        for coord in self.path.coordinates:
            if coord[0] < y_range[0]:
                y_range[0] = coord[0]
            if coord[0] > y_range[1]:
                y_range[1] = coord[0]

            if coord[1] < x_range[0]:
                x_range[0] = coord[1]
            if coord[1] > x_range[1]:
                x_range[1] = coord[1]

        coord_map = [['--' for i in range(
            round(y_range[1] / self.time_error) -
            round(y_range[0] / self.time_error) + 1)] for j in range(
                round(x_range[1] / self.time_error) -
                round(x_range[0] / self.time_error) + 1
                )]

        path = self.path.path

        y_base, x_base = abs(
            round(x_range[0] / self.time_error)
            ), abs(
                round(y_range[0] / self.time_error)
                )

        x, y = 0, 0
        for i in range(len(path)):
            node = path[i]

            xi, yi = self.path.get_xy_from_distance(
                node.orientation,
                node.distance)

            xr, yr = round(
                x / self.time_error
                ) + x_base, round(
                    y / self.time_error
                    ) + y_base

            xir, yir = round(xi / self.time_error), round(yi / self.time_error)

            x_range = [min(xr, xr + xir), max(xr, xr + xir)]
            y_range = [min(yr, yr + yir), max(yr, yr + yir)]

            for j in range(x_range[0], x_range[1] + 1):
                for jj in range(y_range[0], y_range[1] + 1):
                    try:
                        if coord_map[jj][j] == '--' or coord_map[jj][j] == 'XX':
                            if jj == y_range[1] and j == x_range[1]:
                                coord_map[jj][j] = ('0'+str(node.id)) if node.id < 10 else str(node.id)
                            else:
                                coord_map[jj][j] = 'XX'
                    except:
                        pass

            x += xi
            y += yi

        for line in coord_map:
            for char in line:
                output.write(char)
            output.write('\n')
