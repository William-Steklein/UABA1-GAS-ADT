"""
ADT voor dubbel gelinkte circulaire ketting
"""

class LCNode:
    def __init__(self, item=None, next_node=None, prev_node=None):
        self.item = item
        self.next = next_node
        self.prev = prev_node


class LinkedChain:
    def __init__(self):
        self.head = None
        self.count = 0

    def load(self, DGCLijst):
        """
        Laadt de dubbel gelinkte circulaire ketting uit een lijst.
        :param DGCLijst: lijst met items
        :return: None
        """
        # Creëer van elk item in de lijst een DGCNode
        nodes = []
        for item in DGCLijst:
            self.count += 1
            nodes.append(LCNode(item))

        # Laat de headpointer naar de eerste node wijzen
        self.head = nodes[0]

        # Laat de eerste node naar de laatste wijzen en de laatste naar de eerste
        self.head.prev = nodes[-1]
        nodes[-1].next = self.head

        # Laat elke node (behalve de eerste en de laatste) naar zijn volgende en vorige wijzen
        prev_node = self.head
        for n in nodes[1:]:
            prev_node.next = n
            n.prev = prev_node
            prev_node = n

    def save(self):
        """
        Slaagt de dubbel gelinkte circulaire ketting op in een lijst.
        :return: lijst
        """
        # Return een lege lijst als de ketting leeg is
        if self.head is None:
            return []

        # Creëer een lege lijst en zet de eerste node als de huidige node
        DGCLijst = []
        node = self.head

        # Doorloop alle nodes en voeg die toe aan de DGCLijst
        while True:
            DGCLijst.append(node.item)
            node = node.next
            if node == self.head:
                return DGCLijst

    def print(self):
        """
        Print de dubbel gelinkte circulaire kettin op het scherm.
        :return: None
        """
        print(self.save())

    def insert(self, n, newItem):
        """
        Voegt het element 'newItem' toe op positie n in de dubbel gelinkte circulaire kettin.
        :param newItem: waarde
        :param n: index
        :return: None
        """
        # Als de gegeven index groter is dan de lengte van de ketting
        if abs(n) > self.getLength() + 1:
            return False
        n -= 1
        # Als de ketting
        if self.head is None:
                new_node = LCNode(newItem)
                new_node.next = new_node
                new_node.prev = new_node
                self.head = new_node

                # Verhoog de count met 1
                self.count += 1

                # succes
                return True

        # Als de index 0 is of - lengte van de ketting - 1 (vooraan in de ketting)
        elif n == 0 or n == -self.count - 1:
            n = 0
            # Neem de laatste node in de lijst
            current_node = self.head.prev
        elif n > 0:
            # Zoek de node dat op positie n + 1 staat
            current_node = self.head
            for i in range(n - 1):
                current_node = current_node.next
        else:
            current_node = self.head.prev
            for i in range(-n - 1):
                current_node = current_node.prev

        # Creëer een nieuwe node
        new_node = LCNode(newItem)
        # Laat de next pointer naar het eerstvolgende element wijzen
        new_node.next = current_node.next
        # en de prev pionter naar het vorige element wijzen
        new_node.prev = current_node

        # Laat de next pointer van het laatste element wijzen naar de nieuwe node
        current_node.next = new_node
        # Laat de prev pointer van de node voor de nieuwe node naar de nieuwe node wijzen
        new_node.next.prev = new_node

        # Laat de headpointer naar de nieuwe node wijzen als de gegeven index 0 is
        if n == 0:
            self.head = new_node

        # Verhoog de count met 1
        self.count += 1

        # succes
        return True

    def delete(self, item):
        """
        Verwijdert het element met item als waarde uit de dubbel gelinkte circulaire ketting
        :param item: value
        :return: boolean
        """
        # Zoek de te verwijderen node
        current_node = self.findNode(item)
        if current_node is None:
            return False

        # Als de te verwijderen node de eerste in de ketting is
        if current_node == self.head:
            self.head = current_node.next

        # Laat de pointer van de vorige en de volgende node niet meer naar current_node wijzen,
        # maar naar de volgende/vorige in de ketting
        current_node.prev.next = current_node.next
        current_node.next.prev = current_node.prev

        # Verlaag de count met 1
        self.count -= 1

        return True

    def findNode(self, item):
        """
        Geeft de node die item als waarde bevat terug.
        :param item: value
        :return: LCNode
        """
        # Doorloop alle nodes
        current_node = self.head
        while True:
            # Return de node als item gelijk is aan de waarde van de node
            if current_node.item == item:
                return current_node

            # Ga naar de volgende node
            current_node = current_node.next

            # Als current_node gelijk is aan de eerste stop met doorlopen
            if current_node == self.head:
                return None

    def retrieveNode(self, index):
        """
        Geeft de node die op plaats index staat terug.
        :param index: index van de lijst
        :return: LCNode
        """
        if self.head is None:
            return None

        # Doorloop de nodes tot aan index
        current_node = self.head
        for i in range(index):
            current_node = current_node.next

        return current_node

    def retrieve(self, index):
        """
        Geeft het element op positie n terug
        :param index: index van de lijst
        :return: value
        """
        index -= 1
        node = self.retrieveNode(index)
        if node is not None:
            return node.item, True
        else:
            return None, False

    def isEmpty(self):
        """
        Bepaalt of de ketting leeg is.
        :return: boolean
        """
        if self.head is None:
            return True
        return False

    def getLength(self):
        """
        Geeft de lengte van de ketting terug.
        :return: int
        """
        return self.count

    def clear(self):
        # Laat de headpointer wijzen naar None en zet de counter terug op 0
        self.head = None
        self.count = 0

        # succes
        return True

if __name__ == "__main__":
    l = LinkedChain()
    for i in range(1, 11):
        l.insert(1, i)

    l.clear()
    l.print()



# inginious testing
# if __name__ == "__main__":
#     l = LinkedChain()
#     print(l.isEmpty())
#     print(l.getLength())
#     print(l.retrieve(4)[1])
#     print(l.insert(4,500))
#     print(l.isEmpty())
#     print(l.insert(1,500))
#     print(l.retrieve(1)[0])
#     print(l.retrieve(1)[1])
#     print(l.save())
#     print(l.insert(1,600))
#     print(l.save())
#     l.load([10,-9,15])
#     l.insert(3,20)
#     print(l.delete(0))
#     print(l.save())
#     print(l.delete(10))
#     print(l.save())

# True
# 0
# False
# False
# True
# True
# 500
# True
# [500]
# True
# [600, 500]
# False
# [10, -9, 20, 15]
# True
# [-9, 20, 15]