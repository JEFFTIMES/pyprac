from random import *

class KeySize:
    def __get__(self, instance, instance_type):
        return len(instance.keys)


class Node:
    # descriptor n, the number of the keys that the node holds.
    n = KeySize()

    # constructor()
    def __init__(self, t=3, is_leaf=True):
        self.keys = []  # the keys ard saved in current node
        # self.n = 0  # number of keys
        self.children = []  # saved pointers of the children
        self.t = t  # minimum degrees, the maximum n = 2t-1
        self.is_leaf = is_leaf  # is leaf flag

    def get_n(self):
        return len(self.keys)

    def traverse(self):
        # printing the keys of current node
        print(f'Keys:{self.keys}, n={self.n}, is leaf={self.is_leaf}')
        # if reaching base case, is_leaf == True
        if self.is_leaf:
            return

        # else, iterating all the children
        for node in self.children:
            node.traverse()

    # returns True and the node which has the k in its keys if the k is found
    # otherwise, returns False and the final leaf node has been visited.
    def search(self, k):
        # find the first i which let keys[i] greater than or equal to k
        for key in self.keys:
            # if k in current keys, return k and current node
            if key == k:
                return True, self
            # else, go into the keys.index(key) th child to search the k
            if key > k and self.is_leaf is False:
                return self.children[self.keys.index(key)].search(k)

        # k is not found even in a leaf node, return False and the current node
        if self.is_leaf:
            return False, self

        # if there isn't a key in the keys >= k, go to the last child to find
        return self.children[len(self.keys)].search(k)

    def insert(self, k):
        for key in self.keys:
            if key > k:
                self.keys.insert(self.keys.index(key), k)
                # self.n += 1
                return k, self
        self.keys.append(k)
        # self.n += 1
        return k, self

    def delete(self, k):
        for key in self.keys:
            if key == k:
                self.keys.remove(k)
                return k, self
        return None, self


class BTree:
    # constructor(), init the root =None and the degree t =t
    def __init__(self, t):
        self.root = None
        self.t = t

    # traverse(), if root !=None, call its traverse() method.
    def traverse(self):
        if self.root is not None:
            self.root.traverse()

    # search(k), searching the given key =k.
    def search(self, k):
        if self.root is not None:
            return self.root.search(k)
        return None

    # insert(k), inserting a Key =k to a tree.
    def insert(self, k):
        # if the first time insert a k, initialize a Node as leaf to assign to self.root
        if self.root is None:
            self.root = Node(self.t, is_leaf=True)

            # print(f'insert(): k={k}, child.keys={self.root.keys}, child.n={self.root.n}')

            self.root.insert(k)

        # otherwise, traverse the tree to find a proper node to insert
        # but check if the k exists in the tree before the traverse
        # if found is True, the k exists in the tree, return True and the node which has k
        found, node = self.root.search(k)
        if found is True:
            return True, node

        # now, start from the root node to find the proper node and its parent node,
        # get the parent node is that if the node need to be split, the lift_key should be saved to the parent

        child = parent = self.root

        while True:
            # if the chosen child is full, split it then reset the parent and child, loop again.

            if child.n == self.t * 2 - 1:
                l_node, r_node, lift_key = self.split_node(child)

                # when the chosen child is root node and is full, create a new parent and assign it to root
                if child is self.root:
                    parent = Node(t=self.t, is_leaf=False)
                    parent.keys += [lift_key]
                    parent.children += [l_node, r_node]
                    self.root = parent

                # replace this child in parent.children[] with l_node, and insert the r_node after it.
                else:
                    parent.insert(lift_key)
                    position_of_child = parent.children.index(child)
                    parent.children[position_of_child] = l_node
                    parent.children.insert(position_of_child + 1, r_node)

                # target the next child to look up
                i = 0
                while i < parent.n:
                    if parent.keys[i] > k:
                        break
                    i += 1
                child = parent.children[i]

            # otherwise, the chosen child is not full, insert the k and return when the child is a leaf node,
            # or set the parent and child down to the next level and loop again.
            else:

                # child is a leaf node, ether it is the root node and the root is the only node in the tree,
                # or it is a normal leaf node, insert the k in the node.
                if child.is_leaf is True:
                    child.insert(k)
                    # print(f'insert(): k={k}, child.keys={child.keys}, child.n={child.n}')
                    return k, child

                # child is not a leaf node, even it is not full, the k should not be inserted in it,
                # find the next qualify node to check again
                else:
                    parent = child
                    i = 0
                    while i < parent.n:
                        if parent.keys[i] > k:
                            break
                        i += 1
                    child = parent.children[i]

    # split_node(node), split a child to 2 new children and 1 key
    def split_node(self, node):
        l_node = Node(self.t)
        r_node = Node(self.t)

        def split_keys(keys):
            k = len(keys) // 2
            return keys[0:k], keys[k + 1:], keys[k]

        l_node.keys, r_node.keys, lift_key = split_keys(node.keys)

        def split_children(children):
            k = len(children) // 2
            print(f'split children: {children[0:k]}, {children[k:]}')
            return children[0:k], children[k:]

        # the node to be split has leaves, split it and set the is_leaf flag to False for both of the split nodes.
        if not node.is_leaf:
            l_node.children, r_node.children = split_children(node.children)
            l_node.is_leaf = r_node.is_leaf = False
        return l_node, r_node, lift_key

    # delete(), delete a Key =k from a tree.
    def delete(self, k):
        pass

def test():
    tree = BTree(t=3)

    for i in range(20):
        k = int(uniform(1, 1000))
        print(i, k)
        tree.insert(k)
        tree.traverse()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test()