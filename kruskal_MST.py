# Dini Irdina Ahmad Ubaidah, 31279279
# Credits and acknowledgement: Tutorial videos, lecture notes, (functions for reading and writing to the file retrieved from fellow classmate)
# DFS function from Geeksforgeeks


from queue import PriorityQueue
import sys

class DisjointSet():
    def __init__(self, vertices, edge_list) -> None:

        self.parent = [-1] * (vertices+1)
        self.vertice_connections = [[] for i in range(0, vertices+1)]  # list of CHOSEN edges that correspond to a vertice
        self.sorted_edges = edge_list   # will be sorted in kruskal's function below

        self.smallest_sum = 0  
        self.second_smallest_sum = 0

        self.smallest_tree_edges = []
        self.second_tree_edges = [] # list of edges for the second smallest spanning tree

        self.leftovers = []  # list of edges that were not selected for the first minimum spanning tree
        self.smallest_difference = float('inf')

        self.track_edges = []   # list for tracking the edges that have been traveled in the DFS algo below


    def find(self,a):
        """Function retrieved from lecture slides."""
        if self.parent[a] < 0:
            return a
        else:
            self.parent[a] = self.find(self.parent[a])
            return self.parent[a]

    def union(self, a,b):
        """Function retrieved from lecture slides."""
        a_root = self.find(a)
        b_root = self.find(b)

        if a_root == b_root:
            return False
        height_a = -1*(self.parent[a_root])
        height_b = -1*(self.parent[b_root])

        if height_a > height_b:
            self.parent[b_root] = a_root
            return True
        elif height_b > height_a:
            self.parent[a_root] = b_root
            return True
        else:
            self.parent[a_root] = b_root
            self.parent[b_root] = -1 * (height_b+1)
            return True


    def DFSUtil(self, current_vertex_edge, target_vertex, visited_vertices, visited_edges, heaviest):

        """Helper function for the DFS algorithm."""
        condition = current_vertex_edge[1][0] == self.start_vertex or current_vertex_edge[1][0] == target_vertex or \
            current_vertex_edge[1][1] == self.start_vertex or current_vertex_edge[1][1] == target_vertex  # ensures that only edges that contain either u or v will be considered

        if condition and current_vertex_edge[1] not in self.track_edges:  # keep track of edges in MST that have been visited
            self.track_edges.append(current_vertex_edge[1])

        # check for the edge with the heaviest weight
        if current_vertex_edge[1][2] > heaviest[0] and current_vertex_edge[1] != self.exclude_edge and condition:
            heaviest[0] = current_vertex_edge[1][2]
            heaviest[1] = current_vertex_edge[1]

        visited_vertices.append(current_vertex_edge[0])
        visited_edges.append(current_vertex_edge[1])   

        for i in self.vertice_connections[current_vertex_edge[0]]:
            x, y = i[0], i[1]

            if x == current_vertex_edge[0]:
                next_v = y
            else:
                next_v = x

            if target_vertex in visited_vertices:
                return
            if next_v not in visited_vertices and target_vertex not in visited_vertices:
                self.DFSUtil((next_v, i),target_vertex, visited_vertices, visited_edges, heaviest)
 

    def DFS(self, u_vertex_edge, v):
        """Depth-First Search algorithm to find cycle between u, v of an edge"""
        self.start_vertex = u_vertex_edge[0]

        visited = []
        visited_edges = []
        heaviest = [0,u_vertex_edge[1]]  # the first item stores the weight and the second item is the corresponding edge
 
        self.exclude_edge = u_vertex_edge[1]
        self.DFSUtil(u_vertex_edge,v, visited, visited_edges, heaviest)
        return heaviest


    def kruskal(self): 
        """Main algorithm to create both the MST and the second MST. The first MST is created by using Kruskal's union-find 
           algorithm while the second MST has a more complex process that is detailed below.
           """
        self.sorted_edges.sort(key = lambda x: x[2]) #sort edges by weight first

        self.leftovers = self.sorted_edges.copy()  # create a copy of the list of sorted edges
        counter = 0

        while len(self.smallest_tree_edges) < len(self.parent)-2:  # loop as long as there are less than (n-1) edges in MST

            v1 = self.sorted_edges[counter][0]  
            v2 = self.sorted_edges[counter][1] 

            if self.union(v1,v2):
                self.smallest_tree_edges.append(self.sorted_edges[counter]) 
                self.second_tree_edges.append(self.sorted_edges[counter])

                self.vertice_connections[v1].append(self.sorted_edges[counter])  # record the edge added for the two corresponding vertices
                self.vertice_connections[v2].append(self.sorted_edges[counter])

                self.smallest_sum += self.sorted_edges[counter][2]  
                self.second_smallest_sum += self.sorted_edges[counter][2]

                self.leftovers.remove(self.sorted_edges[counter])  # remove selected edge from the list of "excluded" edges

            counter += 1

        optimal_edge = None
        cut_edge = None


        """Process for second MST. For every excluded edge, find the cycle between u, v of edge and mark the heaviest edge.
           Find the smallest difference in weight between the excluded edge and the heaviest edge in cycle. Loop this until
           we have traveled through every edge in the MST. Then simply process to add the new edge and remove the old
           corresponding edge from the second MST. """
        for i in range(len(self.leftovers)):

            if len(self.track_edges) > len(self.parent):  # terminate early if we have traveled through all edges in MST
                break

            edge = self.leftovers[i]
            DFS_results = self.DFS((edge[0], edge), edge[1])
            weight = DFS_results[0]
            
            if edge[2] - weight < self.smallest_difference:
                self.smallest_difference = edge[2] - weight
                optimal_edge = edge
                cut_edge = DFS_results[1]


        self.second_tree_edges.append(optimal_edge)
        self.second_tree_edges.remove(cut_edge)
        self.second_smallest_sum -= cut_edge[2]
        self.second_smallest_sum += optimal_edge[2]

        self.smallest_tree_edges.sort(key= lambda x: (x[0], x[1]))
        self.second_tree_edges.sort(key= lambda x: (x[0], x[1]))
        
        return (self.smallest_tree_edges, self.smallest_sum, self.second_tree_edges, self.second_smallest_sum)
            


def read_input(filename):    # function for reading file input, acquired from fellow classmate
    edges = []
    with open(filename) as file:
        lines = [line.split() for line in file] 

    for i in range(1, len(lines)):
        u, v, w = lines[i][0], lines[i][1], lines[i][2]
        u, v, w= u.rstrip('), ('), v.rstrip('), ('), w.rstrip('), (')
        u, v, w = int(u), int(v), int(w)
        t = (u,v,w)
        edges.append(t)

    verts, edge = int(lines[0][0]), int(lines[0][1])
    ve = (verts, edge)

    return (edges, ve)

def write_result(result):   # function for writing the result, acquired from fellow classmate
    output_file = open("output_spanning.txt", "w")
    output_file.write("Smallest Spanning Tree Weight = " + str(result[1]) + "\n"
                        + "#List of edges in the smallest spanning tree:" + "\n")
    for i in range(len(result[0])):
        output_file.write(str(result[0][i][0]) + " " + str(result[0][i][1]) + " " + str(result[0][i][2]))
        if i != len(result[0])-1:
            output_file.write("\n")

    output_file.write( "\n" +"Second-smallest Spanning Tree Weight = " + str(result[3]) + "\n"
                        + "#List of edges in the smallest spanning tree:" + "\n")
    for i in range(len(result[2])):
        output_file.write(str(result[2][i][0]) + " " + str(result[2][i][1]) + " " + str(result[2][i][2]))
        if i != len(result[2])-1:
            output_file.write("\n")
    output_file.close()


if __name__ == "__main__":

    OUTPUT_PATH = 'output_spanning.txt'

    _, string_file= sys.argv[0], sys.argv[1]

    converted = read_input(string_file)
    data = DisjointSet(converted[1][0], converted[0])
    results = data.kruskal()

    write_result(results)