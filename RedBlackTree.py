"""
ADT voor rood-zwartboom
"""

from graphviz import Graph
from random import shuffle
import os, shutil

def createTreeItem(key,val=None):
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

    def is2node(self):
        """
        Kijkt na of dat de node een 2node is
        :return: boolean
        """
        # Een node is een 2node als beide kinderen zwart zijn
        for child in [self.left, self.right]:
            if child is None:
                return False
            if child.color == "red":
                return False
        return True

    def is3node(self):
        """
        Kijkt na of dat de node een 3node is
        :return: boolean
        """
        # Een node is een 3node als 1 kind zwart is en de andere rood
        if self.left is not None and self.right is not None:
            if self.left.color == "red":
                if self.right.color == "black":
                    return True
            else:
                if self.right.color == "red":
                    return True
        return False

    def is4node(self):
        """
        Kijkt na of dat de node een 4node is
        :return: boolean
        """
        # Een node is een 4node als beide kinderen zwart zijn
        for child in [self.left, self.right]:
            if child is None:
                return False
            if child.color == "black":
                return False
        return True

    def isLeftChild(self):
        """
        Kijkt na of dat de node een linkerkind is
        :return: boolean
        """
        return self == self.parent.left

    def isRightChild(self):
        """
        Kijkt na of dat de node een rechterkind is
        :return: boolean
        """
        return self == self.parent.right

    def switchColor(self):
        """
        Wisselt de kleur van de node
        :return: None
        """
        if self.color == "red":
            self.color = "black"
        else:
            self.color = "red"

    def colorChanges(self):
        """
        Wisselt de kleur van de node en zijn kinderen
        :return: None
        """
        self.left.switchColor()
        self.right.switchColor()
        self.switchColor()

    def leftRotate(self):
        A = self.right # A = child of self
        B = self.parent # B = parent of self
        if B is not None:
            if self.isLeftChild():
                B.left = A
            else:
                B.right = A
        A.parent = B
        self.parent = A

        temp = A.left
        A.left = self
        self.right = temp
        if temp is not None:
            self.right.parent = self.right

    def rightRotate(self):
        A = self.left # A = child of self
        B = self.parent # B = parent of self
        if B is not None:
            if self.isLeftChild():
                B.left = A
            else:
                B.right = A
        A.parent = B
        self.parent = A

        temp = A.right
        A.right = self
        self.left = temp
        if temp is not None:
            self.left.parent = self.left

    def getLeftSibling(self):
        if self.parent.color == "black":
            real_parent = self.parent
        else:
            real_parent = self.parent.parent

        if real_parent.is2node():
            return self.parent.left

        elif real_parent.is3node():
            if self.parent.color == "red" and self.isRightChild():
                return self.parent.left
            elif self.parent.color == "red" and self.isLeftChild():
                return self.parent.parent.left
            elif self.parent.color == "black":
                return self.parent.left.right

        elif real_parent.is4node():
            if self.isRightChild():
                return self.parent.left
            elif self.isLeftChild() and self.parent.isRightChild():
                return self.parent.parent.left.right

    def getRightSibling(self):
        if self.parent.color == "black":
            real_parent = self.parent
        else:
            real_parent = self.parent.parent

        if real_parent.is2node():
            return self.parent.right

        elif real_parent.is3node():
            if self.parent.color == "red" and self.isLeftChild():
                return self.parent.right
            elif self.parent.color == "red" and self.isRightChild():
                return self.parent.parent.right
            elif self.parent.color == "black":
                return self.parent.right.left

        elif real_parent.is4node():
            if self.isLeftChild():
                return self.parent.right
            elif self.isRightChild() and self.parent.isLeftChild():
                return self.parent.parent.right.left


class RedBlackTree:
    counter = 0

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

    def toDot(self, v=False, print_value=False, current_node=None, dot=None, start=True):
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
            name = f"redblacktree{RedBlackTree.counter}" # f"tree{self.id}"
            RedBlackTree.counter += 1
            dot = Graph(comment=name, format='png', graph_attr={"splines": "false"})

        # Maak een node met de kleur van de node
        if current_node.color == "red":
            if not print_value:
                dot.node(str(current_node.key), str(current_node.key), color="red")
            else:
                dot.node(str(current_node.key), str(current_node.key) + "\n" + str(current_node.value), color="red")
        else:
            if not print_value:
                dot.node(str(current_node.key), str(current_node.key))
            else:
                dot.node(str(current_node.key), str(current_node.key) + "\n" + str(current_node.value))

        # Doorloop de linkerdeelboom van de node
        if current_node.left is not None:
            self.toDot(v, print_value, current_node.left, dot, False)
            dot.edge(str(current_node.key)+":sw", str(current_node.left.key))

        # Doorloop de rechterdeelboom van de node
        if current_node.right is not None:
            self.toDot(v, print_value, current_node.right, dot, False)
            dot.edge(str(current_node.key)+":se", str(current_node.right.key))

        if start:
            # Slaag de rood-zwartboom op en geef die weer als gevraagt is
            dot.render(f'test-output/{name}.gv', view=v)

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

    def case1(self, current_node):
        temp = current_node.parent.parent
        temp.left = current_node.parent.right
        temp.left.parent = temp
        greatgreatparent = current_node.parent.parent.parent
        greatparent = current_node.parent.parent
        if greatgreatparent is None:
            current_node.parent.parent = None
            self.root = current_node.parent
        elif greatparent.isLeftChild():
            greatgreatparent.left = current_node.parent
            current_node.parent.parent = greatgreatparent
        else:
            greatgreatparent.right = current_node.parent
            current_node.parent.parent = greatgreatparent
        temp.parent = current_node.parent
        current_node.parent.right = temp

        current_node.parent.switchColor()
        current_node.parent.right.switchColor()
        current_node.colorChanges()

    def case2(self, current_node):
        temp = current_node.parent.parent
        temp.right = current_node.parent.left
        temp.right.parent = temp
        greatgreatparent = current_node.parent.parent.parent
        greatparent = current_node.parent.parent
        if greatgreatparent is None:
            current_node.parent.parent = None
            self.root = current_node.parent
        elif greatparent.isLeftChild():
            greatgreatparent.left = current_node.parent
            current_node.parent.parent = greatgreatparent
        else:
            greatgreatparent.right = current_node.parent
            current_node.parent.parent = greatgreatparent
        temp.parent = current_node.parent
        current_node.parent.left = temp

        current_node.parent.switchColor()
        current_node.parent.left.switchColor()
        current_node.colorChanges()

    def case3(self, current_node):
        tempchild1 = current_node.left
        tempchild2 = current_node.right

        greatgreatparent = current_node.parent.parent.parent
        greatparent = current_node.parent.parent
        parent = current_node.parent

        if greatgreatparent is None:
            current_node.parent = None
            self.root = current_node
        elif greatparent.isLeftChild():
            greatgreatparent.left = current_node
            current_node.parent = greatgreatparent
        elif greatparent.isRightChild():
            greatgreatparent.right = current_node
            current_node.parent = greatgreatparent

        current_node.left = greatparent
        current_node.left.parent = current_node
        current_node.left.right = tempchild1
        current_node.left.right.parent = current_node.left

        current_node.right = parent
        current_node.right.parent = current_node
        current_node.right.left = tempchild2
        current_node.right.left.parent = current_node.right

        tempchild1.switchColor()
        tempchild2.switchColor()
        current_node.left.switchColor()

    def case4(self, current_node):
        tempchild1 = current_node.left
        tempchild2 = current_node.right

        greatgreatparent = current_node.parent.parent.parent
        greatparent = current_node.parent.parent
        parent = current_node.parent

        if greatgreatparent is None:
            current_node.parent = None
            self.root = current_node
        elif greatparent.isLeftChild():
            greatgreatparent.left = current_node
            current_node.parent = greatgreatparent
        elif greatparent.isRightChild():
            greatgreatparent.right = current_node
            current_node.parent = greatgreatparent

        current_node.right = greatparent
        current_node.right.parent = current_node
        current_node.right.left = tempchild2
        current_node.right.left.parent = current_node.right

        current_node.left = parent
        current_node.left.parent = current_node
        current_node.left.right = tempchild1
        current_node.left.right.parent = current_node.left

        tempchild1.switchColor()
        tempchild2.switchColor()
        current_node.right.switchColor()

    def split4node(self, current_node):
        if current_node.parent is not None:
            # Kijk naar de echte ouder
            if current_node.parent.color == "black":
                real_parent = current_node.parent
            else:
                real_parent = current_node.parent.parent

        # Als de node de root is
        if current_node == self.root:
            current_node.left.switchColor()
            current_node.right.switchColor()

        # Als node zijn echte ouder een 2node is
        elif real_parent.is2node():
            current_node.colorChanges()

        # Als node zijn echte ouder een 3node is
        elif real_parent.is3node() and current_node.parent.color == "red":
            # Als de ouder rood is moet die een rotatie doen

            # Als current_node en ouder linkerkinderen zijn
            if current_node.isLeftChild() and current_node.parent.isLeftChild():
                self.case1(current_node)

            # Als current_node en ouder rechterkinderen zijn
            elif current_node.isRightChild() and current_node.parent.isRightChild():
                self.case2(current_node)

            # Als current_node linkerkind is en ouder rechterkind
            elif current_node.isLeftChild() and current_node.parent.isRightChild():
                self.case3(current_node)

            # Als current_node rechterkind is en ouder linkerkind
            elif current_node.isRightChild() and current_node.parent.isLeftChild():
                self.case4(current_node)

        elif real_parent.is3node() and current_node.parent.color == "black":
            # Als de ouder niet rood is moed die color changes doen
            current_node.colorChanges()

    def insertItem(self, t, key=None, value=None, current_node=None, start=True):
        """
        Voegt een nieuwe item toe aan de rood-zwartboom.
        :param key: searchkey
        :param value: waarde
        :return: boolean
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            key, value = t[0], t[1]
            # Als de boom leeg is
            if self.root is None:
                self.root = RBTNode(key, value, "black")
                self.count += 1
                return True
            self.insertItem(None, key, value, self.root, False)
            return True

        # Als de huidige node een 4node is, splits die dan
        if current_node.is4node():
            # Verschillende situaties
            self.split4node(current_node)

        if key < current_node.key and current_node.left is None:
            current_node.left = RBTNode(key, value, "red", parent=current_node)
            new_node = current_node.left
            self.count += 1

            if current_node.color == "red" and new_node.color == "red":
                if current_node.isLeftChild():
                    current_node.parent.rightRotate()

                    current_node.switchColor()
                    current_node.right.switchColor()

                else:
                    current_node.rightRotate()
                    current_node = current_node.parent
                    current_node.parent.leftRotate()

                    current_node.switchColor()
                    current_node.left.switchColor()

                if current_node.parent is None:
                    self.root = current_node

            return True

        elif key < current_node.key and current_node.left is not None:
            self.insertItem(None, key, value, current_node.left, False)

        elif key > current_node.key and current_node.right is None:
            current_node.right = RBTNode(key, value, "red", parent=current_node)
            new_node = current_node.right
            self.count += 1

            if current_node.color == "red" and new_node.color == "red":
                if current_node.isRightChild():
                    current_node.parent.leftRotate()

                    current_node.switchColor()
                    current_node.left.switchColor()
                else:
                    current_node.leftRotate()
                    current_node = current_node.parent
                    current_node.parent.rightRotate()

                    current_node.switchColor()
                    current_node.right.switchColor()

                if current_node.parent is None:
                    self.root = current_node

            return True

        elif key > current_node.key and current_node.right is not None:
            self.insertItem(None, key, value, current_node.right, False)

    def redistribute(self):
        pass

    def merge2node(self, current_node):
        if current_node.parent is not None:
            # Kijk naar de echte ouder
            if current_node.parent.color == "black":
                real_parent = current_node.parent
            else:
                real_parent = current_node.parent.parent

        # Als de ouder 2node is
        if real_parent.is2node():
            pass

        # Als de ouder 3node is
        if real_parent.is3node():
            pass

        # Als de ouder 4node is
        if real_parent.is4node():
            pass


    def deleteSearch(self, key, current_node=None, start=True):
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            # Als de boom leeg is
            if self.root is None:
                return True
            self.deleteSearch(key, self.root, False)
            return True

        # Als de node een 2node is en die is geen root
        if current_node.color == "black" and current_node.is2node() and current_node != self.root:
            # Kijk of dat de linkersibling iets kan uitlenen
            # en dan redistribute
            left_sibling = current_node.getLeftSibling()
            if left_sibling.is3node() or left_sibling.is4node():
                pass

            # Kijk of dat de rechtersibling iets kan uitlenen
            # en dan redistribute
            right_sibling = current_node.getRightSibling()
            if right_sibling.is3node() or left_sibling.is4node():
                pass

            # Anders merge met linkersibling (of rechtersibling als waarde meest rechtse is)
            self.merge2node(current_node)


        if key == current_node.key:
            return current_node
        elif key < current_node.key and current_node.left is not None:
            self.deleteSearch(key, current_node, False)
        elif key > current_node.key and current_node.right is not None:
            self.deleteSearch(key, current_node, False)
        else:
            return None


    def deleteSearchInorderSuccessor(self, current_node):
        pass

    def deleteItem(self, key):
        """
        Verwijdert de node dat het gegeven Entry bevat.
        :return: boolean
        """
        # Zoek de node die het te verwijderen item bevat en
        # vorm elke 2-knoop (behalve de wortel) op dit pad om tot 3-knoop of een 4-knoop
        delete_node = self.deleteSearch(key)
        if delete_node is None:
            return False


        # Zoek de inorder successor van de node
        inosuc = self.deleteSearchInorderSuccessor(delete_node)

        # Swap de nodes


        # Delete het blad en corrigeer

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
        :param data: waarde
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

    def check(self, current_node=None, start=True):
        """
        Kijkt na of dat de rood-zwartboom correct is
        :return: Aantal zwarte knopen op 1 pad
        """
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            if self.root is None:
                print("---De boom is leeg---")
                return
            current_node = self.root
            # Check of dat de kleur van de root zwart is
            if current_node.color != "black":
                print("---Root is rood!---")

            # Check of dat de root geen ouder heeft
            if current_node.parent is not None:
                print("---Root heeft een ouder!---")

        else:
            # Kijk na of dat de node een ouder heeft
            if current_node.parent is None:
                print(f"---{current_node.key} heeft geen ouder!---")
            else:
                if current_node.isLeftChild():
                    if current_node.parent.left != current_node:
                        print(f"---Ouder van {current_node.key} is niet juist of ouder zijn kind is niet juist!---")
                else:
                    if current_node.parent.right != current_node:
                        print(f"---Ouder van {current_node.key} is niet juist of ouder zijn kind is niet juist!---")

        blackcountl = 0
        blackcountr = 0

        # Doorloop de linkerdeelboom van de node
        if current_node.left is not None:
            blackcountl = self.check(current_node.left, False)

        # Doorloop de rechterdeelboom van de node
        if current_node.right is not None:
            blackcountr = self.check(current_node.right, False)

        if blackcountl != blackcountr:
            print(f"---Aantal zwarte nodes kloppen niet bij {current_node.key}---")

        if not start:
            if current_node.color == "black":
                return 1 + blackcountl
            else:
                return blackcountl


if __name__ == "__main__":
    folder = './test-output'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Demo 1

    d = {'root': "dummy", 'color': "black", 'children': [
        {'root': "P", 'color': "black", 'children': [
            {'root': "T", 'color': "black", 'children': [
                {'root': "a", 'color': "black"},
                {'root': "S", 'color': "red", 'children': [
                    {'root': "b", 'color': "black"},
                    {'root': "c", 'color': "black"}
                ]}
            ]},
            {'root': "X", 'color': "black", 'children': [
                {'root': "d", 'color': "black"},
                {'root': "e", 'color': "black"}
            ]}
        ]},
        None
    ]}

    boom = RedBlackTree()
    boom.load(d)

    boom.toDot()

    boom.root.left.left.leftRotate()
    print(boom.root.left.left.key)
    boom.toDot()
    boom.root.left.rightRotate()

    boom.toDot(True)

    # l = list(range(0, 50))
    # shuffle(l)
    # print(l)
    # l = [28, 45, 6, 4, 5, 16, 44, 18, 47, 46, 11, 3, 9, 23, 32, 35, 13, 43, 25, 37, 30, 17, 42, 22, 24, 19, 14, 34, 29, 41, 20, 49, 12, 40, 7, 15, 39, 1, 38, 27, 10, 2, 21, 8, 0, 48, 31, 26, 33, 36]

    # for i in l:
    #     item = createTreeItem(i)
    #     boom.insertItem(item)
    #     # boom.toDot()
    #     # print(f"{i} has been inserted")
    #     boom.check()

    boom.toDot(True)


    # Demo 1
    #
    # d = {'root': "dummy", 'color': "black", 'children': [
    #     {'root': "P", 'color': "black", 'children': [
    #         {'root': "S", 'color': "black", 'children': [
    #             {'root': "T", 'color': "red", 'children': [
    #                 {'root': "a", 'color': "black"},
    #                 {'root': "b", 'color': "black"}
    #             ]},
    #             {'root': "c", 'color': "black"}
    #         ]},
    #         {'root': "X", 'color': "black", 'children': [
    #             {'root': "d", 'color': "black"},
    #             {'root': "e", 'color': "black"}
    #         ]}
    #     ]},
    #     None
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d)
    #
    # boom.toDot()
    #
    # boom.root.left.rightRotate()
    #
    # boom.toDot(True)