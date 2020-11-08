"""
ADT voor rood-zwartboom
"""

from graphviz import Graph

class RBTNode:
    def __init__(self, key=None, value=None, color=None, left=None, right=None, parent=None):
        """
        Creëer een knoop voor een rood zwart boom.
        """
        self.key = key
        self.value = value
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

class RedBlackTree:
    def __init__(self):
        """
        Creëer een lege rood-zwartboom.
        """
        self.root = None
        self.count = 0

    def load(self, RBTDict, node=None, start=True):
        """
        Laadt de rood-zwartboom uit een dictionary.
        :param RBTDict: dictionary
        :return: BinarySearchTree object
        """
        if start:
            # Als de dictionary leeg is
            if RBTDict is None or RBTDict == {}:
                return None

            # Creëer een node in de root
            self.root = RBTNode()
            node = self.root

        # Assign de waarden aan de node
        if 'root' in RBTDict:
            node.key = RBTDict.get('root')
        if 'value' in RBTDict:
            node.value = RBTDict.get('value')
        if 'color' in RBTDict:
            node.color = RBTDict.get('color')

        # Voeg 1 toe aan het totaal aantal knopen in de binaire zoekboom
        self.count += 1

        # Kijk na of de node kinderen heeft
        if 'children' in RBTDict:
            if RBTDict['children'][0] is not None:
                node.left = RBTNode()
                node.left.parent = node
                self.load(RBTDict['children'][0], node.left, False)

            if RBTDict['children'][1] is not None:
                node.right = RBTNode()
                node.right.parent = node
                self.load(RBTDict['children'][1], node.right, False)

    def save(self, addvalues=False, node=None, start=True):
        """
        Slaagt de rood-zwartboom op in een dictionary.
        :return: dictionary
        """
        if start:
            # Als de binaire zoekboom leeg is
            if self.root is None:
                return {}
            node = self.root
            self.save(addvalues, node, False)

        RBTDict = {}

        # Voeg de waarden van de node toe in de dictionary
        if node.key is not None:
            RBTDict['root'] = node.key
        else:
            return
        if node.value is not None and addvalues:
            RBTDict['value'] = node.value
        if node.color is not None:
            RBTDict['color'] = node.color

        # Als de node kinderen heeft
        if not (node.left is None and node.right is None):
            RBTDict['children'] = []
            # Save the children!
            for child in [node.left, node.right]:
                if child is not None:
                    RBTDict['children'].append(self.save(addvalues, child, False))
                else:
                    RBTDict['children'].append(None)

        return RBTDict

    def toDot(self, print_value=False, current_node=None, dot=None, start=True):
        """
        Maakt een afbeelding van de rood-zwartboom
        :param print_value: True: print de waarden van de nodes False: print geen waarden
        :return: None
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                print("Dot: lege BST!")
                return
            current_node = self.root

            # Maak een dot object
            name = f"redblacktree" # f"tree{self.id}"
            print(name)
            dot = Graph(comment=name, format='png', graph_attr={"splines": "false"})

        if current_node.color == "red":
            if not print_value:
                dot.node(str(current_node.key), str(current_node.key), color="red")
            else:
                dot.node(str(current_node.key), str(current_node.key) + "\n" + str(current_node.value))
        else:
            if not print_value:
                dot.node(str(current_node.key), str(current_node.key))
            else:
                dot.node(str(current_node.key), str(current_node.key) + "\n" + str(current_node.value))

        # Doorloop de linkerdeelboom van de node
        if current_node.left is not None:
            self.toDot(print_value, current_node.left, dot, False)
            dot.edge(str(current_node.key)+":sw", str(current_node.left.key))

        # Doorloop de rechterdeelboom van de node
        if current_node.right is not None:
            self.toDot(print_value, current_node.right, dot, False)
            dot.edge(str(current_node.key)+":se", str(current_node.right.key))

        if start:
            # Geef de rood-zwartboom weer
            dot.render(f'test-output/{name}.gv', view=True)

    def print(self):
        """
        Print de rood-zwartboom op het scherm.
        :return: None
        """
        pass

    def isEmpty(self):
        """
        Bepaalt of de rood-zwartboom leeg is.
        :return: boolean
        """
        pass

    def getHeight(self):
        """
        Geeft de hoogte van de rood-zwartboom.
        :return: integer, boolean
        """
        pass

    def getNumberOfNodes(self):
        """
        Geeft het aantal knopen in de rood-zwartboom.
        :return: integer, boolean
        """
        pass

    def getRootData(self):
        """
        Geeft de waarde dat in de root van de rood-zwartboom zit.
        :return: value, boolean
        """
        pass

    def insertItem(self, key, value=None):
        """
        Voegt een nieuwe item toe aan de rood-zwartboom.
        :param key: searchkey
        :param value: waarde
        :return: boolean
        """
        pass

    def deleteItem(self, key):
        """
        Verwijdert de node dat het gegeven Entry bevat.
        :return: boolean
        """
        pass

    def clear(self):
        """
        Wist de rood-zwartboom.
        :return: boolean
        """
        pass

    def contains(self, key):
        """
        Bepaalt of dat de gegeven waarde in de boom zit.
        :param key: searchkey
        :return: boolean
        """
        pass

    def preorderTraverse(self):
        """
        Doorloopt de knopen in de rood-zwartboom in preorder.
        :return: None
        """
        pass

    def inorderTraverse(self):
        """
        Doorloopt de knopen in de rood-zwartboom in inorder.
        :return: None
        """
        pass

    def postorderTraverse(self):
        """
        Doorloopt de knopen in de rood-zwartboom in postorder.
        :return: None
        """
        pass

if __name__ == "__main__":
    d = {'root': 4, 'color': "black", 'children': [
            {'root': 2, 'color': "red", 'children': [
                {'root': 1, 'color': "black"},
                {'root': 3, 'color': "black"}
            ]},
            {'root': 6, 'color': "red", 'children': [
                {'root': 5, 'color': "black"},
                {'root': 8, 'color': "black", 'children': [
                    {'root': 7, 'color': "red"},
                    {'root': 9, 'color': "red"}
                ]}
            ]}
    ]}

    boom = RedBlackTree()
    boom.load(d)
    print(boom.save())
    boom.toDot()