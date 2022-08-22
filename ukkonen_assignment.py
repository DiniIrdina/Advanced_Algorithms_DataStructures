# Dini Irdina Ahmad Ubaidah, 31279279
# Acknowledgement and Credits: Tutorial videos, lecture notes, Github(https://github.com/wein98/Advanced-Algorithm-Data-Structure/blob/master/Ukkonen.py)
# Warning: Question is not complete, only ukkonen's suffix tree building has been implemented. No substring search has been implemented.

class Node():
    """ Incoming edge info is stored in the node, hence there is no Edge class."""

    def __init__(self, start, end, j, textfile_id, leaf=True):
        self.links = None
        self.suffix_link = None
        self.isLeaf = leaf
        self.start = start
        self.end = end
        self.textfile_suffix_ids = [(textfile_id, j)]
        self.edge_length = 0

        if not leaf:
            self.change_leaf()

    # "Return children node in position i"
    # def getChildren(self, i):
    #     return self.children[i]

    def add_link(self, i, child):
        if self.isLeaf:
            self.change_leaf()
        self.links[i] = child

    def change_leaf(self):
        self.leaf = False
        self.j = None
        self.links = [None]*128

    def get_length(self):
        self.edge_length = self.get_end() - self.start + 1 
        return self.edge_length

    def get_end(self):
        if isinstance(self.end, int):
            return self.end
        else:
            return self.end.get_end()

    def add_suffix_id(self,txtfile_id, val):
        self.textfile_suffix_ids.append((txtfile_id,val))

    def get_link(self, i):
        if self.links is None:
            return None
        return self.links[i]


class End:
    def __init__(self):
        self.value = None

    def update_end(self, num):
        self.value = num

    def get_end(self):
        return self.value


class SuffixTree():
    def __init__(self, string, txtfile_id):
        self.string_length = len(string)
        self.end = End()
        self.i = 0
        self.textfile_id = txtfile_id
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0
        self.previous_node = None

        # Create a root node with start and end as -1
        self.root = None
        self.root = self.create_node(-1, -1, None, 1, False)
        self.root.suffix_link = self.root
        self.active_node = self.root # first activeNode is root

        self.insert(string, self.textfile_id)


    def create_node(self, start, end, suffix_id, txtfile, leaf=True):
        """Function used to create a new Node object and assigns suffix link back to the root."""
        new_node = Node(start, end, suffix_id, txtfile, leaf)
        new_node.suffix_link = self.root
        return new_node


    def extend_tree(self, j,my_string):
        """Main suffix tree building algorithm with the 3 rules implemented"""
        self.previous_node = None

        self.end.update_end(j)  # Extension Rule 1 - Update all leaves (Rapid Leaf Extension)


        while(self.i <= j):
            if self.active_length == 0:
                self.active_edge = j
            
            # Extention Rule 2 - Path doesn't exist, so create a branch from active node
            
            current_val = my_string[self.active_edge]
            current_val = ord(current_val)
            if self.active_node.get_link(current_val) is None:
                new_node = self.create_node(j, self.end, self.i, self.textfile_id)
                self.active_node.add_link(current_val, new_node)

                if self.previous_node is not None:
                    self.previous_node.suffix_link = self.active_node
                    self.previous_node = None
            
            else: # If the active_node has an outgoing active_edge
                next_node = self.active_node.links[current_val]
                length = next_node.get_length()

                # if there is an internal node, this becomes the active_node and move to next iteration
                if self.active_length >= length: 
                    self.active_length -= length
                    self.active_node = next_node
                    self.active_edge += length
                    continue

                # Extension Rule 3 - Path already exists
                if next_node.start < len(my_string) and my_string[j] == my_string[next_node.start + self.active_length]:
                    if self.previous_node is not None and self.active_node is not self.root:
                        self.active_node.add_suffix_id((self.textfile_id,j))   # Add new (textfile_id, suffix_id) to the node
                        self.previous_node.suffix_link = self.active_node
                        self.previous_node = None
                    
                    self.active_length += 1
                    break   # Showstopper Trick


                # Extension Rule 2 - create new internal node
                branch_start = next_node.start
                next_node.start += self.active_length
                next_position = next_node.start
                if next_node.start >= len(my_string):
                    next_position = j 

                branch_node = self.create_node(branch_start, branch_start+self.active_length-1, None, self.textfile_id, False)
                branch_node.add_link(ord(my_string[next_position]), next_node)

                new_leaf = self.create_node(j, self.end, self.i,self.textfile_id)
                branch_node.add_link(ord(my_string[j]), new_leaf)

                # this new internal node will become a child of the active node
                if branch_start >= len(my_string):
                    branch_start = j
                self.active_node.links[ord(my_string[branch_start])] = branch_node

                # If any internal nodes were formed in previous extensions of the same phase, add a suffixLink to this new internal node. 
                if self.previous_node:   
                    self.previous_node.suffix_link = branch_node
                self.previous_node = branch_node

            self.i += 1

            # change active_length and active_edge to go to root before next extension starts
            if self.active_node is self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = self.i
            else:
                self.active_node = self.active_node.suffix_link


    def insert(self, string, txtfile):
        string = string + "$"
        self.string_length = len(string)
        self.end = End()
        self.i = 0
        self.textfile_id = txtfile
        self.active_node = self.root
        self.active_edge = -1
        self.previous_node = None
        self.active_length = 0

        for j in range(self.string_length):
            self.extend_tree(j,string)


if __name__ == "__main__":      # acquired from fellow classamte
    pass
