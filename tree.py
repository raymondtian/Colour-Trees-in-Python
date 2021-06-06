"""
Tree
----

This file contains the tree data structure that will be used for interacting
with our coloured nodes.
The tree contains a "root" node, which is the topmost node of the tree.
It is interconnected through children and finally ends at external nodes ending
at the leaves.
"""

from node import Node
from colours import Colour

class Tree:
    """
    Tree Class
    ----------

    Contains the data structure of a tree, where each node of the tree has a
    parent and children.
    If a node has no parent, it is considered the "root" of the tree.
    If a node has zero (0) children, it is a leaf (or is "external").

    Each node in the tree has the type `Node`, which is defined in `node.py`.

    ====== Functions ======

    - __init__ : Sets up the tree with a specified root.
    - put(node, child) : Adds the `child` to the `node`.
    - swap(subtree_a, subtree_b) : Swaps the position of the subtrees.
    - is_coloured_to_depth_k(node, colour, k) : Checks that the subtree rooted
        at `node` has the same colour until `k` levels deep.

    == Things to note ==

    1. Every node given as an argument WILL be in the tree, you do not have to
        check whether it exists in the tree.
    2. Every node will be initialised with a parent (unless it is the root node
        of the tree).
    3. The ordering of the children does not matter.
    """

    def __init__(self, root: Node) -> None:
        """
        Initialises the tree with a root of type `Node` from `node.py`

        :param root: The root node of our tree.
        """

        self.root = root

    def update_node_colour(self, n: Node, new_colour: Colour) -> None:
        """
        Update the colour of a node.

        :param n: The node to change the colour of.
        :param new_colour: The new colour to change to.
        """

        if (n.parent == None):
            n.update_colour(new_colour)
            if (Colour.cmp(n.colour, n.propagated_colour) == 1):
                n.propagated_colour = n.colour
        else:
            n.update_colour(new_colour) #n.colour = new_colour
            if (Colour.cmp(n.colour, n.propagated_colour) == 1):
                n.propagated_colour = n.colour
            curr_node = n

            for child in curr_node.get_children():
                if (Colour.cmp(child.propagated_colour, curr_node.propagated_colour) == 1):
                    curr_node.propagated_colour = child.propagated_colour

            while curr_node.parent is not None:
                curr_node = curr_node.parent
                curr_node.propagated_colour = curr_node.colour
                for child in curr_node.get_children():
                    if (Colour.cmp(child.propagated_colour, curr_node.propagated_colour) == 1):
                        curr_node.propagated_colour = child.propagated_colour

    def put(self, parent: Node, child: Node) -> None:
        """
        Inserts a node into the tree.
        Adds `child` to `parent`.

        :param parent: The parent node currently in the tree.
        :param child: The child to add to the tree.
        """

        parent.add_child(child)
        child.set_parent(parent)
        curr_node = child

        while curr_node.parent is not None:
            if (Colour.cmp(curr_node.propagated_colour, curr_node.parent.propagated_colour) == 1):
                curr_node.parent.propagated_colour = curr_node.propagated_colour
            curr_node = curr_node.parent

    def rm(self, child: Node) -> None:
        """
        Removes child from parent.

        :param child: The child node to remove.
        """

        if child.parent is not None:
            curr_node = child.parent
            curr_node.remove_child(child)
            curr_node.propagated_colour = curr_node.colour
            for children in curr_node.get_children():
                if (Colour.cmp(children.propagated_colour, curr_node.propagated_colour) == 1):
                    curr_node.propagated_colour = children.propagated_colour

            while curr_node.parent is not None:
                curr_node = curr_node.parent
                curr_node.propagated_colour = curr_node.colour
                for children in curr_node.get_children():
                    if (Colour.cmp(children.propagated_colour, curr_node.propagated_colour) == 1):
                        curr_node.propagated_colour = children.propagated_colour

    def swap(self, subtree_a: Node, subtree_b: Node) -> None:
        """
        Swaps subtree A with subtree B

        :param subtree_a : Root of the subtree A.
        :param subtree_b : Root of the subtree B.

        Example:

            A
           / \
           B  C
         /   / \
        D   J   K

        SWAP(B, C)
            A
           / \
          C  B
         / |  \
        J  K   D

        SWAP(D, C)

            A
           / \
          D  B
              \
               C
              / \
             J   K
        """

        a_tmp = subtree_a.parent
        b_tmp = subtree_b.parent

        self.rm(subtree_a)
        self.rm(subtree_b)

        subtree_a.set_parent(b_tmp)
        subtree_b.set_parent(a_tmp)

        self.put(subtree_a.parent, subtree_a)
        self.put(subtree_b.parent, subtree_b)

    def recursive_colour_check(self, curr_node: Node, colour: Colour, k: int, depth: int) -> bool:
        if depth <= k:
            if Colour.cmp(curr_node.colour, colour) != 0:
                return False
            if depth == k or len(curr_node.get_children()) == 0:
                return True
            else:
                is_true = True
                for child in curr_node.get_children():
                    if not self.recursive_colour_check(child, colour, k, depth + 1):
                        is_true = False
                return is_true

    def is_coloured_to_depth_k(self, start_node: Node, colour: Colour, k: int) -> bool:
        """
        Checks whether all nodes in the subtree (up and including level `k`
            starting from the start node) have the same colour!

        (This checks node.colour)

        :param start_node : The node to start checking.
        :param colour: The colour to compare a node's colour to.
        :param k: The depth we should check until.

        === Examples ===

        (start)---> G
                   / \
                  G   G
                 /|   |
                G R   G
                  |
                  R

        is_coloured_to_depth_k(start, Colour.GREEN, 0) => True
        is_coloured_to_depth_k(start, Colour.RED, 0) => False
        is_coloured_to_depth_k(start, Colour.GREEN, 1) => True
        is_coloured_to_depth_k(start, Colour.GREEN, 2) => False
        """

        return self.recursive_colour_check(start_node, colour, k, 0)
