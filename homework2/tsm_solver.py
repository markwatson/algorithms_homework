import sys
import os
import random
import math
import json
import copy

# helper functions for reading files
def read_tsp_file(fname):
    """
    Parses the file.
    """
    header = {
        'name': fname,
        'dimension': 0,
        'edgeweight': '',
        }

    in_data = False
    cities = []
    for L in open(fname, 'r'):
        data = L.strip().split(' ')
        if in_data and L != 'EOF' and len(data) == 3:
            cities.append((float(data[1]), float(data[2])))
        else:
            if data[0] == "NAME":
                header['name'] = data[2]
            elif data[0] == "DIMENSION":
                header['dimension'] = int(data[2])
            elif data[0] == "EDGE_WEIGHT_TYPE":
                header['edgeweight'] = data[2]
            elif data[0] == "NODE_COORD_SECTION":
                in_data = True

    return cities, header

def read_tour_file(fname):
    """
    Parses the tour file.
    """
    header = {
        'name': fname,
        'dimension': 0,
        }

    in_data = False
    path = []
    for L in open(fname, 'r'):
        L = L.strip()
        data = L.split(' ')
        if in_data and L != 'EOF' and len(data) == 1 and L != '-1':
            path.append(int(data[0]))
        else:
            if data[0] == "NAME":
                header['name'] = data[2]
            elif data[0] == "DIMENSION":
                header['dimension'] = int(data[2])
            elif data[0] == "TOUR_SECTION":
                in_data = True

    return path, header

def permutations(s):
    """
    Finds all permutations of a set, s. The permutations are generated
    using the johnson-trotter algorithm.
    """
    # the index
    value_ind = 0
    direction_ind = 1

    # johnson-trotter works with sorted sequences.
    s = sorted(s)
    
    # initialize the directions
    s = [[x, -1] for x in s]

    # yield the first elements
    yield [x[value_ind] for x in s]

    # main loop
    while True:
        # get mobile elements
        mobile_elements = []
        for i in xrange(len(s)):
            if (i + s[i][direction_ind] >= 0 and
                i + s[i][direction_ind] < len(s) and
                s[i + s[i][direction_ind]][value_ind] < s[i][value_ind]):
                mobile_elements.append(i)
        
        # exit case
        if not mobile_elements:
            break
        
        # largest element
        k = None
        m = None
        for i in mobile_elements:
            if m is None or s[i][value_ind] > m:
                m = s[i][value_ind]
                k = i
        
        # just in case
        if k is None:
            break

        # swap k and the element k points to
        dest_loc = k + s[k][direction_ind]
        s[dest_loc], s[k] = s[k], s[dest_loc]
            # fix the k index
        k = dest_loc

        # reverse the direction of all the elements that are larger than k
        for i in xrange(len(s)):
            if s[i][value_ind] > s[k][value_ind]:
                if s[i][direction_ind] == -1:
                    s[i][direction_ind] = 1
                else:
                    s[i][direction_ind] = -1
        
        # yield the element
        yield [x[value_ind] for x in s]

class TSM(object):
    def __init__(self):
        self._reset()

    def _reset(self):
        self.name = "N/A"
        self.cities = []
        self.city_distances = {}
        self.optimal_path = None

        self.o_file = None
        self.i_file = None

    def create_random_cities(self, n, span=100):
        """
        Generates evenly ditributed random cities over a plane.

        Arguments:
        n -- The number of cities
        span -- A tuple containing the width and height of the area
                to generate cities over.
        """
        for i in xrange(n):
            self.cities.append(
                (random.uniform(0, span), random.uniform(0, span)))

        # set name and calculate distances
        self.name = "%d randomly located towns." % len(self.cities)
        self._calculate_distances()
    
    def get_distance(self, a, b):
        """ Get the distance from city a to city b. """
        return self.city_distances[a][b]

    def _calculate_distances(self):
        """
        Calculates all the distances between the cities and stores
        them in memory.
        """
        # for each city
        for i, city in enumerate(self.cities):
            # loop through each other city
            for j, other_city in enumerate(self.cities):
                # find the length
                if city != other_city:
                    self.city_distances.setdefault(i, {})[j] = \
                        self._euclidean_distance(city, other_city)

    def _euclidean_distance(self, vect1, vect2):
        """ Takes the euclidean distance between two vectors. """
        if len(vect1) != len(vect2):
            return False
        return math.sqrt(sum(map(
                lambda x:pow(vect2[x] - vect1[x],2), xrange(len(vect1))
            )))

    def load(self):
        if self.i_file:
            f = open(self.i_file, 'r')
            data = '\n'.join(f.readlines())
            f.close()
            data = json.loads(data)
            self.name = data.get('name', "N/A")
            self.cities = data.get('cities', [])
            self.optimal_path = data.get('optimal_path', None)
            temp = data.get('distances', {})
            self.city_distances = dict([(int(x[0]),
                                         dict([(int(y[0]), y[1])
                                               for y in x[1].iteritems()]))
                                        for x in temp.iteritems()])
            if self.cities and not self.city_distances:
                self._calculate_distances()

    def save(self):
        if self.o_file:
            f = open(self.o_file, "wb")
            data = {
                "name": self.name,
                "cities": self.cities,
                "optimal_path": self.optimal_path,
                "distances": self.city_distances,
            }
            f.write(json.dumps(data, sort_keys=True, indent=4))
            f.close()

    def finish(self):
        self.save()

    def plot(self, path):
        if not self.optimal_path or not self.cities:
            raise Exception("We don't have anything to plot...")

        import matplotlib.path as mpath
        import matplotlib.patches as mpatches
        import matplotlib.pyplot as plt

        tour = [self.cities[x] for x in path]

        Path = mpath.Path
        fig = plt.figure()
        ax = fig.add_subplot(111)
        pathdata = []
        for x in tour:
            pathdata.append([Path.LINETO, (x[0], x[1])])
        pathdata[0][0] = Path.MOVETO
        pathdata.append([Path.CLOSEPOLY, (tour[0][0], tour[0][1])])

        codes, verts = zip(*pathdata)
        path = mpath.Path(verts, codes)

        x, y = zip(*path.vertices)
        line, = ax.plot(x, y, 'go-')
        ax.grid()
        #ax.set_xlim(-3,4)
        #ax.set_ylim(-3,4)
        ax.set_title(self.name)
        plt.show()

    def get_length(self, path):
        route_length = 0.0
        for i in xrange(len(path)):
            next_i = i + 1
            # if this is the last city, then wrap around to first
            if i == len(path) - 1:
                next_i = 0
            
            # get distances
            route_length += self.get_distance(path[i], path[next_i])
        return route_length

def brute_solve_tsm(tsm):
    city_indexes = [x[0] for x in enumerate(tsm.cities)]
    shortest = None
    shortest_path = None

    # loop through each possible path
    for path in permutations(city_indexes):
        # get path length
        route_length = tsm.get_length(path)
        
        # check if this route is shorter
        if shortest is None or route_length < shortest:
            shortest = route_length
            shortest_path = path

    tsm.optimal_path = shortest_path
    return shortest, shortest_path

def two_opt_solve_tsm(tsm):
    # start with a random path
    path = [key for key, val in enumerate(tsm.cities)]
    random.shuffle(path)

    # Apply 2opt to the path till we get something better
    current_length = tsm.get_length(path)
    while True:
        improvements = []

        # find all path improvements
        for i in xrange(len(path)):
            for j in xrange(len(path)):
                if i != j:
                    # make a copy of the path and swap two of the towns
                    pos_path = copy.copy(path)
                    pos_path[i], pos_path[j] = pos_path[j], pos_path[i]

                    # is this path shorter?
                    pos_path_len = tsm.get_length(pos_path)
                    if pos_path_len < current_length:
                        improvements.append((current_length - pos_path_len,
                                             pos_path_len, pos_path))

        # use the highest improvement
        max_improv = None
        for improv in improvements:
            if max_improv is None or improv[0] > max_improv[0]:
                max_improv = improv
        
        if max_improv is None:
            # no more improvements to be made
            break
        
        # set path to best improvement and continue
        current_length = max_improv[1]
        path = max_improv[2]

    # save and return path values
    tsm.two_opt_path = path
    return current_length, path

def usage():
    print "Usage: python tsm_solver.py OPTIONS"
    print "   -rN: generate a random TSM of size N"
    print "   -iIN_FILE_NAME: use IN_FILE_NAME for loading the TSM"
    print "   -oOUT_FILE_NAME: save to OUT_FILE_NAME when done"
    print "   -p: Plot the route when done"
    print "   -mMETHOD: solve the TSM using the METHOD (brute, or 2opt)"
    print "   -c: Compare the given method to the optimal solution, if possible."

    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        usage()

    tsm = TSM()
    plot = False
    solve_method = None
    compare = False
    for arg in sys.argv:
        if arg.startswith('-r'):
            # generate a random tour
            tsm.create_random_cities(int(arg[2:]))
        elif arg.startswith('-i'):
            tsm.i_file = arg[2:]
            tsm.load()
        elif arg.startswith('-o'):
            tsm.o_file = arg[2:]
        elif arg.startswith('-p'):
            plot = True
        elif arg.startswith('-m'):
            if arg[2:] == 'brute' or arg[2:] == '2opt':
                solve_method = arg[2:]
            else:
                usage()
        elif arg.startswith('-c'):
            compare = True

    # init the shorted path
    shortest_path = tsm.optimal_path

    # solve if needed
    if solve_method == 'brute':
        print "Solving the TSM problem of size %d using brute force..."\
            % len(tsm.cities)
        shortest, shortest_path = brute_solve_tsm(tsm)

        # we have a solution
        print "The length is: ", shortest
        print "The path is: ", repr(shortest_path)
        print "The cities are: "
        print tsm.cities
    elif solve_method == '2opt':
        print "Solving the TSM problem of size %d using 2opt..."\
            % len(tsm.cities)
        shortest, shortest_path = two_opt_solve_tsm(tsm)

        # we have a solution
        print "The length is: ", shortest
        print "The path is: ", repr(shortest_path)
        print "The cities are: "
        print tsm.cities

        if compare and tsm.optimal_path:
            print "The optimal path length is: %f" % \
                tsm.get_length(tsm.optimal_path)
    else:
        print "Not solving since no method was specified."

    if plot and shortest_path:
        tsm.plot(shortest_path)
    
    # we're done here
    tsm.finish()
        
if __name__ == "__main__":
    main()
