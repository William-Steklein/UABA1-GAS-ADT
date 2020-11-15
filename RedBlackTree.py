"""
ADT contract voor rood-zwartboom
"""

from graphviz import Graph
import random
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

    def getLeftSibling(self):
        if self.parent.color == "black":
            real_parent = self.parent
        else:
            real_parent = self.parent.parent

        if real_parent.is2node() and self.isRightChild():
            return self.parent.left

        elif real_parent.is3node():
            if self.parent.color == "red" and self.isRightChild():
                return self.parent.left
            elif self.parent.color == "red" and self.isLeftChild() and self.parent.isRightChild():
                return self.parent.parent.left
            elif self.parent.color == "black" and self.isRightChild():
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

        if real_parent.is2node() and self.isLeftChild():
            return self.parent.right

        elif real_parent.is3node():
            if self.parent.color == "red" and self.isLeftChild():
                return self.parent.right
            elif self.parent.color == "red" and self.isRightChild() and self.parent.isLeftChild():
                return self.parent.parent.right
            elif self.parent.color == "black" and self.isLeftChild():
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
        self.NULLNode = RBTNode()

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
            else:
                node.left = self.NULLNode

            if RBTDict['children'][1] is not None:
                node.right = RBTNode()
                node.right.parent = node
                self.load(RBTDict['children'][1], node.right, False)
            else:
                node.right = self.NULLNode
        else:
            node.left = self.NULLNode
            node.right = self.NULLNode

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
        if not (node.left == self.NULLNode and node.right == self.NULLNode):
            RBTDict['children'] = []
            # Save the children!
            for child in [node.left, node.right]:
                if child != self.NULLNode:
                    RBTDict['children'].append(self.save(addvalues, child, False))
                else:
                    RBTDict['children'].append(None)

        return RBTDict

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
        if node.left == self.NULLNode and node.right == self.NULLNode:
            return

        # Print linkerkind
        if node.left != self.NULLNode:
            self.print(depth + 1, node.left, False)
        else:
            print('%s' % (((depth + 1) * '\t') + "None"))

        # Print rechterkind
        if node.right != self.NULLNode:
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
        if current_node.left == self.NULLNode and current_node.right == self.NULLNode:
            return 1

        # Zoek de grootste hoogte bij de kinderen
        else:
            max_height = 0
            if current_node.left != self.NULLNode:
                temp = self.getHeight(current_node.left, False)
                if temp > max_height:
                    max_height = temp

            if current_node.right != self.NULLNode:
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

    def leftRotate(self, current_node):
        A = current_node.right # A = child of self
        B = current_node.parent # B = parent of self

        if current_node.parent is None:
            self.root = A

        if B is not None:
            if current_node.isLeftChild():
                B.left = A
            else:
                B.right = A
        A.parent = B

        current_node.parent = A

        temp = A.left
        A.left = current_node
        current_node.right = temp
        if temp is not None:
            current_node.right.parent = current_node

    def rightRotate(self, current_node):
        A = current_node.left # A = child of self
        B = current_node.parent # B = parent of self

        if current_node.parent is None:
            self.root = A

        if B is not None:
            if current_node.isLeftChild():
                B.left = A
            else:
                B.right = A
        A.parent = B
        current_node.parent = A

        temp = A.right
        A.right = current_node
        current_node.left = temp
        if temp is not None:
            current_node.left.parent = current_node

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
                self.root.left = self.NULLNode
                self.root.right = self.NULLNode

                self.count += 1
                return True
            self.insertItem(None, key, value, self.root, False)
            return True

        # Als de huidige node een 4node is, splits die dan
        if current_node.is4node():
            # Verschillende situaties
            self.split4node(current_node)

        if key < current_node.key and current_node.left == self.NULLNode:
            current_node.left = RBTNode(key, value, "red", parent=current_node)
            current_node.left.left = self.NULLNode
            current_node.left.right = self.NULLNode
            new_node = current_node.left
            self.count += 1

            if current_node.color == "red" and new_node.color == "red":
                if current_node.isLeftChild():
                    self.rightRotate(current_node.parent)

                    current_node.switchColor()
                    current_node.right.switchColor()

                else:
                    self.rightRotate(current_node)
                    current_node = current_node.parent
                    self.leftRotate(current_node.parent)

                    current_node.switchColor()
                    current_node.left.switchColor()

                if current_node.parent is None:
                    self.root = current_node

            return True

        elif key < current_node.key and current_node.left != self.NULLNode:
            self.insertItem(None, key, value, current_node.left, False)

        elif key > current_node.key and current_node.right == self.NULLNode:
            current_node.right = RBTNode(key, value, "red", parent=current_node)
            current_node.right.left = self.NULLNode
            current_node.right.right = self.NULLNode
            new_node = current_node.right
            self.count += 1

            if current_node.color == "red" and new_node.color == "red":
                if current_node.isRightChild():
                    self.leftRotate(current_node.parent)

                    current_node.switchColor()
                    current_node.left.switchColor()
                else:
                    self.leftRotate(current_node)
                    current_node = current_node.parent
                    self.rightRotate(current_node.parent)

                    current_node.switchColor()
                    current_node.right.switchColor()

            return True

        elif key > current_node.key and current_node.right != self.NULLNode:
            self.insertItem(None, key, value, current_node.right, False)

    def leftredistribute(self, current_node):
        if current_node.parent is not None:
            # Kijk naar de echte ouder
            if current_node.parent.color == "black":
                real_parent = current_node.parent
            else:
                real_parent = current_node.parent.parent

        left_sibling = current_node.getLeftSibling()

        if left_sibling.is3node():
            if left_sibling.right is not None and left_sibling.right.color == "red":
                self.leftRotate(left_sibling)
                left_sibling.switchColor()
                left_sibling.parent.switchColor()
                left_sibling = left_sibling.parent
                # nu moet S left sibling zijn
        else:
            self.leftRotate(left_sibling)
            left_sibling.switchColor()
            left_sibling.parent.switchColor()
            left_sibling = left_sibling.parent

        # Als echte ouder 2node is
        if real_parent.is2node():
            self.rightRotate(current_node.parent)
            current_node.switchColor()
            current_node.parent.parent.left.switchColor()

        # Als echte ouder 3node is
        elif real_parent.is3node():
            if current_node == real_parent.right.right:
                self.rightRotate(current_node.parent)
                current_node.parent.parent.colorChanges()
                current_node.switchColor()

            elif current_node == real_parent.right:
                self.leftRotate(current_node.parent.left)
                self.rightRotate(current_node.parent)
                current_node.switchColor()
                current_node.parent.parent.left.right.switchColor()

            elif current_node == real_parent.right.left:
                current_node.parent.switchColor()
                self.leftRotate(current_node.parent.parent)
                current_node.parent.left.switchColor()
                current_node.parent.left.left.switchColor()
                self.rightRotate(current_node.parent)
                current_node.switchColor()

            elif current_node == real_parent.left.right:
                current_node.parent.switchColor()
                current_node.parent.left.switchColor()
                current_node.parent.left.left.switchColor()
                self.rightRotate(current_node.parent)
                current_node.switchColor()

        # Als echte ouder 4node is
        elif real_parent.is4node():
            if current_node.isRightChild():
                self.rightRotate(current_node.parent)
                current_node.switchColor()
                current_node.parent.switchColor()
                current_node.parent.parent.switchColor()
                current_node.parent.parent.left.switchColor()
            else:
                self.leftRotate(left_sibling.parent)
                self.rightRotate(current_node.parent.parent)
                self.leftRotate(current_node.parent.parent)
                current_node.switchColor()
                current_node.parent.parent.parent.left.right.switchColor()

    def rightredistribute(self, current_node):
        if current_node.parent is not None:
            # Kijk naar de echte ouder
            if current_node.parent.color == "black":
                real_parent = current_node.parent
            else:
                real_parent = current_node.parent.parent

        right_sibling = current_node.getRightSibling()

        if right_sibling.is3node():
            if right_sibling.left is not None and right_sibling.left.color == "red":
                self.rightRotate(right_sibling)
                right_sibling.switchColor()
                right_sibling.parent.switchColor()
                right_sibling = right_sibling.parent
                # Nu moet S left sibling zijn
        else:
            self.rightRotate(right_sibling)
            right_sibling.switchColor()
            right_sibling.parent.switchColor()
            right_sibling = right_sibling.parent

        # Als echte ouder 2node is
        if real_parent.is2node():
            self.leftRotate(current_node.parent)
            current_node.switchColor()
            current_node.parent.parent.right.switchColor()

        # Als echte ouder 3node is
        elif real_parent.is3node():
            if current_node == real_parent.left.left:
                self.leftRotate(current_node.parent)
                current_node.parent.parent.colorChanges()
                current_node.switchColor()

            elif current_node == real_parent.left:
                self.rightRotate(current_node.parent.right)
                self.leftRotate(current_node.parent)
                current_node.switchColor()
                current_node.parent.parent.right.left.switchColor()

            elif current_node == real_parent.left.right:
                current_node.parent.switchColor()
                self.rightRotate(current_node.parent.parent)
                current_node.parent.right.switchColor()
                current_node.parent.right.right.switchColor()
                self.leftRotate(current_node.parent)
                current_node.switchColor()

            elif current_node == real_parent.right.left:
                current_node.parent.switchColor()
                current_node.parent.right.switchColor()
                current_node.parent.right.right.switchColor()
                self.leftRotate(current_node.parent)
                current_node.switchColor()

        # Als echte ouder 4node is
        elif real_parent.is4node():
            if current_node.isLeftChild():
                self.leftRotate(current_node.parent)
                current_node.switchColor()
                current_node.parent.switchColor()
                current_node.parent.parent.switchColor()
                current_node.parent.parent.right.switchColor()
            else:
                self.rightRotate(right_sibling.parent)
                self.leftRotate(current_node.parent.parent)
                self.rightRotate(current_node.parent.parent)
                current_node.switchColor()
                current_node.parent.parent.parent.right.left.switchColor()

    def merge2node(self, current_node):
        if current_node.parent is not None:
            # Kijk naar de echte ouder
            if current_node.parent.color == "black":
                real_parent = current_node.parent
            else:
                real_parent = current_node.parent.parent

        # Als de ouder 2node is
        if real_parent.is2node():
            # Doe een colorswitch
            current_node.switchColor()
            if current_node.isLeftChild():
                current_node.parent.right.switchColor()
            else:
                current_node.parent.left.switchColor()

        # Als de ouder 3node is
        elif real_parent.is3node():
            left_sibling = current_node.getLeftSibling()
            if left_sibling is not None:
                if current_node.isRightChild() and left_sibling.isLeftChild():
                    current_node.parent.colorChanges()
                elif current_node.isLeftChild() and left_sibling.isLeftChild():
                    self.leftRotate(current_node.parent.parent)

                    current_node.switchColor()
                    current_node.parent.left.switchColor()
                    current_node.parent.parent.switchColor()
                elif current_node.isRightChild() and left_sibling.isRightChild():
                    self.rightRotate(current_node.parent)

                    current_node.switchColor()
                    current_node.parent.left.switchColor()
                    current_node.parent.parent.switchColor()
            else:
                right_sibling = current_node.getRightSibling()
                if right_sibling.isRightChild():
                    current_node.parent.colorChanges()
                else:
                    self.leftRotate(current_node.parent)

                    current_node.switchColor()
                    current_node.parent.right.switchColor()
                    current_node.parent.parent.switchColor()

        # Als de ouder 4node is
        elif real_parent.is4node():
            left_sibling = current_node.getLeftSibling()
            if left_sibling is not None:
                if current_node.isRightChild():
                    current_node.parent.colorChanges()
                else:
                    self.rightRotate(current_node.parent.parent)
                    self.leftRotate(current_node.parent.parent)

                    current_node.switchColor()
                    current_node.parent.left.switchColor()
                    current_node.parent.parent.parent.switchColor()
            else:
                # Merge met de right sibling
                current_node.parent.colorChanges()

    def mergeOrRedistribute(self, current_node):
        # Als de node een 2node is en die is geen root
        if current_node != self.root and current_node.color == "black" and current_node.is2node():
            # Kijk of dat de linkersibling iets kan uitlenen
            # en dan redistribute
            left_sibling = current_node.getLeftSibling()
            right_sibling = current_node.getRightSibling()
            if left_sibling is not None and (left_sibling.is3node() or left_sibling.is4node()):
                self.leftredistribute(current_node)

            # Kijk of dat de rechtersibling iets kan uitlenen
            # en dan redistribute
            elif right_sibling is not None and (right_sibling.is3node() or right_sibling.is4node()):
                self.rightredistribute(current_node)

            # Anders merge met linkersibling (of rechtersibling als waarde meest rechtse is)
            else:
                self.merge2node(current_node)

    def deleteSearchNode(self, key, current_node=None, start=True):
        # Zet in het begin de current_node gelijk aan die van de root
        if start:
            # Als de boom leeg is
            if self.root is None:
                return None
            return self.deleteSearchNode(key, self.root, False)

        self.mergeOrRedistribute(current_node)

        if key == current_node.key:
            return current_node
        elif key < current_node.key and current_node.left is not None:
            if current_node.left == self.NULLNode:
                return None
            return self.deleteSearchNode(key, current_node.left, False)
        elif key > current_node.key and current_node.right is not None:
            if current_node.right == self.NULLNode:
                return None
            return self.deleteSearchNode(key, current_node.right, False)
        else:
            return None

    def deleteSearchInorderSuccessor(self, current_node, left=False):
        # Herverdeel of merge als het een 2node is
        self.mergeOrRedistribute(current_node)

        # Ga eerst 1 keer naar rechts
        if not left:
            if current_node.right != self.NULLNode:
                return self.deleteSearchInorderSuccessor(current_node.right, True)
            else:
                return current_node
        # Blijf links gaan tot een blad
        else:
            if current_node.left != self.NULLNode:
                return self.deleteSearchInorderSuccessor(current_node.left, True)
            else:
                return current_node

    def deleteItem(self, key):
        """
        Verwijdert de node dat het gegeven key bevat.
        :return: boolean
        """
        # Zoek de node die het te verwijderen item bevat en
        # vorm elke 2-knoop (behalve de wortel) op dit pad om tot 3-knoop of een 4-knoop
        if self.root.key == key:
            if self.root.left == self.NULLNode and self.root.right == self.NULLNode:
                self.root = None

        delete_node = self.deleteSearchNode(key)
        if delete_node is None:
            return False

        # Zoek de inorder successor van de node
        inosuc = self.deleteSearchInorderSuccessor(delete_node)

        # Swap de items van de nodes
        delete_node.key = inosuc.key
        delete_node.value = inosuc.value

        # verwijder inorder successor
        if inosuc.color == "red":
            if inosuc.isLeftChild():
                inosuc.parent.left = self.NULLNode
            else:
                inosuc.parent.right = self.NULLNode
        else:
            if inosuc.is3node():
                if inosuc.left.color == "red":
                    self.rightRotate(inosuc)
                    inosuc.parent.switchColor()
                    inosuc.parent.right = self.NULLNode
                else:
                    self.leftRotate(inosuc)
                    inosuc.parent.switchColor()
                    inosuc.parent.left = self.NULLNode
            elif inosuc.is4node():
                self.leftRotate(inosuc)
                inosuc.parent.parent.switchColor()
                inosuc.parent.left = self.NULLNode

        self.count -= 1
        return True

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
            if key < current_node.key and current_node.left != self.NULLNode:
                temp = self.getNode(key, current_node.left, False)
                if temp is not None:
                    return temp

            # Als de key groter is dan de key van de huidige node
            if key > current_node.key and current_node.right != self.NULLNode:
                temp = self.getNode(key, current_node.right, False)
                if temp is not None:
                    return temp

    def retrieveItem(self, key):
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
            if node.left != self.NULLNode:
                temp = self.contains(data, node.left, False)
                if temp is not None:
                    return temp
            if node.right != self.NULLNode:
                temp = self.contains(data, node.right, False)
                if temp is not None:
                    return temp

        # Als het niet gevonden is en we zitten in de eerste stap van recursie
        if start:
            return False

    def preorderTraverse(self, functionType, current_node=None, start=True):
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
        functionType(current_node.key)

        # Doorloop de linkerdeelboom van de node
        if current_node.left != self.NULLNode:
            self.preorderTraverse(functionType, current_node.left, False)

        # Doorloop de rechterdeelboom van de node
        if current_node.right != self.NULLNode:
            self.preorderTraverse(functionType, current_node.right, False)

    def inorderTraverse(self, functionType, current_node=None, start=True):
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
        if current_node.left != self.NULLNode:
            self.inorderTraverse(functionType, current_node.left, False)

        # Print de searchkey van de huidige node
        functionType(current_node.key)

        # Doorloop de rechterdeelboom van de node
        if current_node.right != self.NULLNode:
            self.inorderTraverse(functionType, current_node.right, False)

    def postorderTraverse(self, functionType, current_node=None, start=True):
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
        if current_node.left != self.NULLNode:
            self.postorderTraverse(functionType, current_node.left, False)

        # Doorloop de rechterdeelboom van de node
        if current_node.right != self.NULLNode:
            self.postorderTraverse(functionType, current_node.right, False)

        # Print de searchkey van de huidige node
        functionType(current_node.key)

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
            if current_node.parent is None or current_node.parent == self.NULLNode:
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
        if current_node.left != self.NULLNode:
            blackcountl = self.check(current_node.left, False)

        # Doorloop de rechterdeelboom van de node
        if current_node.right != self.NULLNode:
            blackcountr = self.check(current_node.right, False)

        if blackcountl != blackcountr:
            print(f"---Aantal zwarte nodes kloppen niet bij {current_node.key}---")

        if not start:
            if current_node.color == "black":
                return 1 + blackcountl
            else:
                return blackcountl

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
        if current_node.left != self.NULLNode:
            self.toDot(v, print_value, current_node.left, dot, False)
            dot.edge(str(current_node.key)+":sw", str(current_node.left.key))

        # Doorloop de rechterdeelboom van de node
        if current_node.right != self.NULLNode:
            self.toDot(v, print_value, current_node.right, dot, False)
            dot.edge(str(current_node.key)+":se", str(current_node.right.key))

        if start:
            # Slaag de rood-zwartboom op en geef die weer als gevraagt is
            dot.render(f'test-output/{name}.gv', view=v)


if __name__ == "__main__":
    t = RedBlackTree()
    print(t.isEmpty())
    print(t.insertItem(createTreeItem(8,8)))
    print(t.insertItem(createTreeItem(5,5)))
    print(t.insertItem(createTreeItem(10,10)))
    print(t.insertItem(createTreeItem(15,15)))
    print(t.isEmpty())
    print(t.retrieveItem(5)[0])
    print(t.retrieveItem(5)[1])
    t.inorderTraverse(print)
    print(t.save())
    t.load({'root': 8,'color': 'black','children':[{'root':5,'color': 'black'},{'root':10,'color': 'black'}]})
    t.insertItem(createTreeItem(15,15))
    print(t.deleteItem(0))
    print(t.save())
    print(t.deleteItem(10))
    print(t.save())

# if __name__ == "__main__":
#     folder = './test-output'
#     for filename in os.listdir(folder):
#         file_path = os.path.join(folder, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.unlink(file_path)
#             elif os.path.isdir(file_path):
#                 shutil.rmtree(file_path)
#         except Exception as e:
#             print('Failed to delete %s. Reason: %s' % (file_path, e))
#
#     boom = RedBlackTree()
#     l = list(range(0, 100))
#     shuffle(l)
#     print(l)
#     # l2 = [7, 15, 19, 10, 17, 18, 14, 16, 8, 13, 9, 12, 5, 1, 11, 0, 6, 4, 2, 3]
#     # l = [10, 49, 14, 30, 34, 25, 23, 36, 11, 5, 32, 41, 28, 19, 46, 6, 0, 13, 43, 26, 40, 2, 9, 47, 45, 39, 1, 12, 22, 38, 17, 18, 42, 35, 15, 29, 31, 27, 48, 33, 24, 37, 3, 16, 7, 20, 44, 8, 4, 21]
#     for i in l:
#         item = createTreeItem(i)
#         boom.insertItem(item)
#         # boom.toDot()
#         # print(f"{i} has been inserted")
#         # boom.check()
#
#     # boom.toDot()
#
#     d2 = boom.save()
#
#     boom2 = RedBlackTree()
#     boom2.load(d2)
#
#     boom.toDot(True)
#     boom2.toDot(True)



    # l2 = l[:]
    # shuffle(l2)
    #
    # for i in l2:
    #     print(i)
    #     boom.deleteItem(i)
    #
    #     # boom.toDot()

    # # Demo11 herverdelen met 3node parent v3
    #
    # d10 = {'root': 15, 'color': "black", 'children': [
    #         {'root': 8, 'color': "red", 'children': [
    #             {'root': 7, 'color': "black"},
    #             {'root': 10, 'color': "black", 'children': [
    #                 {'root': 9, 'color': "black"},
    #                 {'root': 11, 'color': "black"}
    #             ]}
    #         ]},
    #         {'root': 18, 'color': "black", 'children': [
    #         {'root': 17, 'color': "black"},
    #         {'root': 19, 'color': "black"}
    #     ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d10)
    #
    # boom.toDot()
    # boom.check()
    #
    # # boom.merge2node(boom.root.right)
    # print(boom.deleteSearch(18).key)
    # # boom.leftredistribute(boom.root.right.left)
    # boom.check()
    #
    #
    # boom.toDot(True)

    # Demo 10 deleteSearch test

    # boom = RedBlackTree()
    # counter = 0
    # #
    # # for i in range(100):
    # #     print(f"--------test{counter}-------")
    # #     l = list(range(0, 40))
    # #     random.shuffle(l)
    # #     print("list: ", l)
    # #     for j in l:
    # #         item = createTreeItem(j)
    # #         boom.insertItem(item)
    # #     print("check 1: ")
    # #     boom.check()
    # #     x = random.choice(l)
    # #     print("x: ", x)
    # #     print(boom.deleteSearchNode(x).key)
    # #     print("check 2: ")
    # #     boom.check()
    # #     print("--------------------")
    # #     boom.clear()
    # #     counter += 1
    #
    # # l = list(rangerange(0, 40))
    # # shuffle(l)
    # # print(l)
    # l = [4, 32, 36, 1, 7, 34, 26, 17, 10, 33, 31, 25, 9, 29, 37, 28, 18, 12, 23, 20, 13, 5, 11, 19, 8, 30, 22, 38, 15, 6, 39, 14, 0, 27, 35, 2, 16, 24, 3, 21]
    # for i in l:
    #     item = createTreeItem(i)
    #     boom.insertItem(item)
    #     # boom.toDot()
    #     # print(f"{i} has been inserted")
    #     # boom.check()
    #
    # boom.toDot()
    # boom.check()
    #
    # print(boom.deleteSearchNode(13).key)
    #
    # boom.check()
    #
    # boom.toDot(True)

    # # Demo 9 herverdelen met 3node parent v3
    #
    # d9 = {'root': "P", 'color': "black", 'children': [
    #         {'root': "O", 'color': "red", 'children': [
    #             {'root': "a", 'color': "black"},
    #                 {'root': "S", 'color': "black", 'children': [
    #                     {'root': "T", 'color': "red", 'children': [
    #                         {'root': "b", 'color': "black"},
    #                         {'root': "c", 'color': "black"}
    #                     ]},
    #                     {'root': "d", 'color': "black"}
    #                 ]}
    #         ]},
    #         {'root': "Q", 'color': "red", 'children': [
    #             {'root': "X", 'color': "black", 'children': [
    #                 {'root': "f", 'color': "black"},
    #                 {'root': "g", 'color': "black"}
    #             ]},
    #             {'root': "h", 'color': "black"}
    #         ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d9)
    #
    # boom.toDot()
    #
    # boom.leftredistribute(boom.root.right.left)
    #
    # boom.toDot(True)

    # # Demo 9 herverdelen met 3node parent v3
    #
    # d9 = {'root': "P", 'color': "black", 'children': [
    #         {'root': "R", 'color': "black", 'children': [
    #             {'root': "T", 'color': "red", 'children': [
    #                 {'root': "a", 'color': "black"},
    #                 {'root': "b", 'color': "black"}
    #             ]},
    #             {'root': "S", 'color': "red", 'children': [
    #                 {'root': "tes1", 'color': "black"},
    #                 {'root': "tes2", 'color': "black"}
    #             ]}
    #         ]},
    #         {'root': "Q", 'color': "red", 'children': [
    #             {'root': "X", 'color': "black", 'children': [
    #                 {'root': "d", 'color': "black"},
    #                 {'root': "e", 'color': "black"}
    #             ]},
    #             {'root': "f", 'color': "black"}
    #         ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d9)
    #
    # boom.toDot()
    #
    # boom.leftredistribute(boom.root.right.left)
    #
    # boom.toDot(True)

    # # Demo 8 herverdelen met 3node parent v1
    #
    # d8 = {'root': "P", 'color': "black", 'children': [
    #         {'root': "O", 'color': "red", 'children': [
    #             {'root': "a", 'color': "black"},
    #             {'root': "S", 'color': "black", 'children': [
    #                 {'root': "T", 'color': "red", 'children': [
    #                     {'root': "b", 'color': "black"},
    #                     {'root': "c", 'color': "black"}
    #                 ]},
    #                 {'root': "d", 'color': "black"}
    #             ]}
    #     ]},
    #         {'root': "X", 'color': "black", 'children': [
    #             {'root': "e", 'color': "black"},
    #             {'root': "f", 'color': "black"}
    #         ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d8)
    #
    # boom.toDot()
    #
    # print(boom.root.right.key)
    # boom.leftredistribute(boom.root.right)
    #
    # boom.toDot(True)

    # # Demo 7 herverdelen met 2node parent
    #
    # d7 = {'root': "P", 'color': "black", 'children': [
    #         {'root': "T", 'color': "black", 'children': [
    #             {'root': "a", 'color': "black"},
    #             {'root': "S", 'color': "red", 'children': [
    #                 {'root': "b", 'color': "black"},
    #                 {'root': "c", 'color': "black"}
    #             ]}
    #         ]},
    #         {'root': "X", 'color': "black", 'children': [
    #             {'root': "d", 'color': "black"},
    #             {'root': "e", 'color': "black"}
    #     ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d7)
    #
    # boom.toDot()
    #
    # boom.leftredistribute(boom.root.right)
    #
    # boom.toDot(True)

    # Demo 6 redistribute 3node to 2node with 3node parent

    # d6 = {'root': "O", 'color': "black", 'children': [
    #         {'root': "a", 'color': "black"},
    #         {'root': "P", 'color': "red", 'children': [
    #             {'root': "S", 'color': "black", 'children': [
    #                 {'root': "T", 'color': "red", 'children': [
    #                     {'root': "b", 'color': "black"},
    #                     {'root': "c", 'color': "black"}
    #                 ]},
    #                 {'root': "d", 'color': "black"}
    #             ]},
    #             {'root': "X", 'color': "black", 'children': [
    #                 {'root': "e", 'color': "black"},
    #                 {'root': "f", 'color': "black"}
    #             ]}
    #     ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d6)
    #
    # boom.toDot()
    #
    # print(boom.root.right.right.key)
    # boom.leftredistribute(boom.root.right.right)
    #
    # boom.toDot(True)

    # # Demo 5 merge2node als ouder 4node is en de te mergen node een linkerkind is en sibling rechterkind
    #
    # d5 = {'root': "M", 'color': "black", 'children': [
    #         {'root': "P", 'color': "red", 'children': [
    #             {'root': "a", 'color': "black"},
    #             {'root': "S", 'color': "black", 'children': [
    #                 {'root': "b", 'color': "black"},
    #                 {'root': "c", 'color': "black"}
    #             ]}
    #         ]},
    #         {'root': "Q", 'color': "red", 'children': [
    #             {'root': "X", 'color': "black", 'children': [
    #                 {'root': "d", 'color': "black"},
    #                 {'root': "e", 'color': "black"}
    #             ]},
    #             {'root': "f", 'color': "black"}
    #         ]}
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d5)
    #
    # boom.check()
    # boom.toDot()
    #
    # boom.merge2node(boom.root.right.left)
    # boom.check()
    #
    #
    # boom.toDot(True)

    # # Demo 4 rightRotate
    #
    # d3 = {'root': "self", 'color': "black", 'children': [
    #             {'root': "A", 'color': "black", 'children': [
    #                 {'root': "a", 'color': "black"},
    #                 {'root': "b", 'color': "black"}
    #             ]},
    #             {'root': "c", 'color': "black"}
    #         ]}
    #
    # boom = RedBlackTree()
    # boom.load(d3)
    #
    # # boom.check()
    # boom.toDot()
    #
    # # print(x.key)
    # boom.check()
    # boom.rightRotate(boom.root)
    #
    # boom.toDot(True)

    # # Demo 3 left merge 3node ouder case2
    #
    # d3 = {'root': "dummy", 'color': "black", 'children': [
    #     {'root': "M", 'color': "black", 'children': [
    #         {'root': "S", 'color': "black", 'children': [
    #             {'root': "a", 'color': "black"},
    #             {'root': "b", 'color': "black"}
    #         ]},
    #         {'root': "P", 'color': "red", 'children': [
    #             {'root': "X", 'color': "black", 'children': [
    #                 {'root': "c", 'color': "black"},
    #                 {'root': "d", 'color': "black"}
    #             ]},
    #             {'root': "e", 'color': "black"}
    #         ]}
    #     ]},
    #     None
    # ]}
    #
    # boom = RedBlackTree()
    # boom.load(d3)
    #
    # boom.check()
    # boom.toDot()
    #
    # x = boom.root.left.right.left
    # boom.merge2node(x)
    # # print(x.key)
    # boom.check()
    #
    #
    # boom.toDot(True)

    # # Demo 2
    #
    # d = {'root': "dummy", 'color': "black", 'children': [
    #     {'root': "P", 'color': "black", 'children': [
    #         {'root': "T", 'color': "black", 'children': [
    #             {'root': "a", 'color': "black"},
    #             {'root': "S", 'color': "red", 'children': [
    #                 {'root': "b", 'color': "black"},
    #                 {'root': "c", 'color': "black"}
    #             ]}
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
    # # boom.toDot()
    # #
    # # boom.leftRotate(boom.root.left.left)
    # # print(boom.root.left.left.key)
    # # boom.toDot()
    # # boom.rightRotate(boom.root.left)
    #
    # boom.toDot()
    #
    # print(boom.root.left.right.key)
    # boom.leftRotate(boom.root.left.right)
    # print(boom.root.left.right.key)
    #
    # # boom.merge2node(boom.root.left.right)
    #
    # # print(boom.root.left.right.key)
    # # print(boom.root.left.right.getLeftSibling().key)
    #
    # boom.toDot(True)

    # boom = RedBlackTree()
    #
    # # l = list(range(0, 50))
    # # shuffle(l)
    # # print(l)
    # l = [28, 45, 6, 4, 5, 16, 44, 18, 47, 46, 11, 3, 9, 23, 32, 35, 13, 43, 25, 37, 30, 17, 42, 22, 24, 19, 14, 34, 29, 41, 20, 49, 12, 40, 7, 15, 39, 1, 38, 27, 10, 2, 21, 8, 0, 48, 31, 26, 33, 36]
    #
    # for i in l:
    #     item = createTreeItem(i)
    #     boom.insertItem(item)
    #     # boom.toDot()
    #     # print(f"{i} has been inserted")
    #     boom.check()
    #
    # boom.toDot(True)


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
    # boom.rightRotate(boom.root.left)
    #
    # boom.toDot(True)