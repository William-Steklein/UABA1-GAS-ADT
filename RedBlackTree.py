"""
ADT voor rood-zwartboom
"""

from graphviz import Graph

def createTreeItem(key,val):
    return key, val

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

    def print(self, depth=0, node=None, start=True):
        """
        Print de rood-zwartboom in de console.
        :return: None
        """
        if start:
            if self.root is None:
                print(None)
                return
            node = self.root

        # Print de huidige node
        if node.color == "black":
            print('%s' % ((depth * '\t') + "|B| " + str(node.key) + ": " + str(node.value)))
        else:
            print('%s' % ((depth * '\t') + "|R| " + str(node.key) + ": " + str(node.value)))

        # Als beide kinderen None zijn dan return
        if node.left is None and node.right is None:
            return

        # Print linkerkind
        if node.left is not None:
            self.print(depth + 1, node.left, False)
        else:
            print('%s' % (((depth + 1) * '\t') + "None"))

        # Print rechterkind
        if node.right is not None:
            self.print(depth + 1, node.right, False)
        else:
            print('%s' % (((depth + 1) * '\t') + "None"))

    def isEmpty(self):
        """
        Bepaalt of de rood-zwartboom leeg is.
        :return: boolean
        """
        if self.root is None:
            return True
        else:
            return False

    def getHeight(self, current_node=None, start=True):
        """
        Geeft de hoogte van de rood-zwartboom.
        :return: integer, boolean
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                return 0
            current_node = self.root

        # Geef 1 terug als de node geen kinderen heeft
        if current_node.left is None and current_node.right is None:
            return 1

        # Zoek de grootste hoogte bij de kinderen
        else:
            max_height = 0
            if current_node.left is not None:
                temp = self.getHeight(current_node.left, False)
                if temp > max_height:
                    max_height = temp

            if current_node.right is not None:
                temp = self.getHeight(current_node.right, False)
                if temp > max_height:
                    max_height = temp

            # Geef 1 + de hoogte van langste pad onder node
            return 1 + max_height

    def getNumberOfNodes(self):
        """
        Geeft het aantal knopen in de rood-zwartboom.
        :return: integer, boolean
        """
        return self.count

    def getRootData(self):
        """
        Geeft de waarde dat in de root van de rood-zwartboom zit.
        :return: value, boolean
        """
        return self.root.value

    def insertItem(self, t, key, value=None, current_node=None, start=True):
        """
        Voegt een nieuwe item toe aan de rood-zwartboom.
        :param key: searchkey
        :param value: waarde
        :return: boolean
        """
        # Als de boom leeg is
        if self.root is None:
            self.root = RBTNode(key, value, "black")
            return True
        else:
            pass


        # Als de root geen kinderen heeft
            # Als de root minder dan 3 elementen bevat

            # Als de root 3 elementen bevat

        # Als de root kinderen heeft
            # Vind de node en splits alle 4nodes onderweg

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
        self.root = None

    def getNode(self, key, current_node=None, start=True):
        """
        Geeft de node terug die de search key bevat.
        :param key: search key (int of string)
        :return: waarde
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                return
            current_node = self.root

        # return de node als de key van de node gelijk is aan de gegeven key
        if current_node.key == key:
            return current_node

        # Zoek bij de kinderen
        else:
            # Als de key kleiner is dan de key van de huidige node
            if key < current_node.key and current_node.left is not None:
                temp = self.getNode(key, current_node.left, False)
                if temp is not None:
                    return temp

            # Als de key groter is dan de key van de huidige node
            if key > current_node.key and current_node.right is not None:
                temp = self.getNode(key, current_node.right, False)
                if temp is not None:
                    return temp

    def searchTreeRetrieve(self, key):
        """
        Geeft een waarde terug uit de rood-zwartboom mbv de searchkey.
        :param key: search key (int of string)
        :return: waarde
        """
        node = self.getNode(key)
        if node is not None:
            return node.value, True
        else:
            return None, False

    def contains(self, data, node=None, start=True):
        """
        Bepaalt of dat de gegeven waarde in de boom zit.
        :param key: searchkey
        :return: boolean
        """
        if start:
            if self.root is None:
                return
            node = self.root

        if node.value == data:
            return True

        # Zoek bij de kinderen
        else:
            if node.left is not None:
                temp = self.contains(data, node.left, False)
                if temp is not None:
                    return temp
            if node.right is not None:
                temp = self.contains(data, node.right, False)
                if temp is not None:
                    return temp

        # Als het niet gevonden is en we zitten in de eerste stap van recursie
        if start:
            return False

    def preorderTraverse(self, current_node=None, start=True):
        """
        Doorloopt de knopen in de rood-zwartboom in preorder.
        :return: None
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                print(None)
                return
            current_node = self.root

        # Print de searchkey van de huidige node
        print(current_node.key)

        # Doorloop de linkerdeelboom van de node
        if current_node.left is not None:
            self.preorderTraverse(current_node.left, False)

        # Doorloop de rechterdeelboom van de node
        if current_node.right is not None:
            self.preorderTraverse(current_node.right, False)

    def inorderTraverse(self, current_node=None, start=True):
        """
        Doorloopt de knopen in de rood-zwartboom in inorder.
        :return: None
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                print(None)
                return
            current_node = self.root

        # Doorloop de linkerdeelboom van de node
        if current_node.left is not None:
            self.inorderTraverse(current_node.left, False)

        # Print de searchkey van de huidige node
        print(current_node.key)

        # Doorloop de rechterdeelboom van de node
        if current_node.right is not None:
            self.inorderTraverse(current_node.right, False)

    def postorderTraverse(self, current_node=None, start=True):
        """
        Doorloopt de knopen in de rood-zwartboom in postorder.
        :return: None
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                print(None)
                return
            current_node = self.root

        # Doorloop de linkerdeelboom van de node
        if current_node.left is not None:
            self.postorderTraverse(current_node.left, False)

        # Doorloop de rechterdeelboom van de node
        if current_node.right is not None:
            self.postorderTraverse(current_node.right, False)

        # Print de searchkey van de huidige node
        print(current_node.key)

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
    # boom.load(d)
    boom.insertItem(5)
    print(boom.save())
    boom.print()

    # boom.preorderTraverse()
    # print("-----------------------------------")
    # boom.inorderTraverse()
    # print("-----------------------------------")
    # boom.postorderTraverse()
    boom.toDot()
