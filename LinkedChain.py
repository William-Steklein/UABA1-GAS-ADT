"""
ADT contract voor circulaire dubbelgelinkte ketting
"""

class LCNode:
    def __init__(self, item=None, next_node=None, prev_node=None):
        """
        Creëer een knoop voor een circulaire dubbelgelinkte ketting.
        :param item: waarde
        :param next_node: volgende knoop
        :param prev_node: vorige knoop
        """
        self.item = item
        self.next = next_node
        self.prev = prev_node


class LinkedChain:
    def __init__(self):
        """
        Creëert een lege circulaire dubbelgelinkte ketting.
        """
        self.head = None
        self.count = 0

    def load(self, LC_lijst):
        """
        Laadt de circulaire dubbelgelinkte ketting uit een lijst.
        :param LC_lijst: lijst met items
        :return: None
        """
        # Creëer van elk item in de lijst een DGCNode
        nodes = []
        for item in LC_lijst:
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
        Slaagt de circulaire dubbelgelinkte ketting op in een lijst.
        :return: lijst
        """
        # Return een lege lijst als de ketting leeg is
        if self.head is None:
            return []

        # Creëer een lege lijst en zet de eerste node als de huidige node
        LC_lijst = []
        node = self.head

        # Doorloop alle nodes en voeg die toe aan de LC_lijst
        while True:
            LC_lijst.append(node.item)
            node = node.next
            if node == self.head:
                return LC_lijst

    def print(self):
        """
        Print de circulaire dubbelgelinkte ketting op het scherm.
        :return: None
        """
        print(self.save())

    def isEmpty(self):
        """
        Bepaalt of de circulaire dubbelgelinkte ketting leeg is.
        :return: boolean
        """
        if self.head is None:
            return True
        return False

    def getLength(self):
        """
        Geeft de lengte van de circulaire dubbelgelinkte ketting terug.
        :return: int
        """
        return self.count

    def insert(self, n, newItem):
        """
        Voegt het element 'newItem' toe op positie n in de circulaire dubbelgelinkte ketting.
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

    def delete(self, n):
        """
        Verwijdert het element op positie n uit de circulaire dubbelgelinkte ketting.
        :param n: positie van het element
        :return: boolean
        """
        if n <= 0:
            return False

        n -= 1

        # Zoek de te verwijderen node
        current_node = self.retrieveNode(n)
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

    def retrieveNode(self, n):
        """
        Geeft de knoop die op positie n staat in de circulaire dubbelgelinkte ketting terug.
        :param n: positie van de node
        :return: LCNode
        """
        if self.head is None:
            return None

        # Doorloop de nodes tot aan index
        current_node = self.head
        for i in range(n):
            current_node = current_node.next

        return current_node

    def retrieve(self, n):
        """
        Geeft het element op positie n terug in de circulaire dubbelgelinkte ketting.
        :param n: positie van de item
        :return: value
        """
        n -= 1
        node = self.retrieveNode(n)
        if node is not None:
            return node.item, True
        else:
            return None, False

    def clear(self):
        """
        Wist de circulaire dubbelgelinkte ketting.
        :return: success (boolean)
        """
        # Laat de headpointer wijzen naar None en zet de counter terug op 0
        self.head = None
        self.count = 0

        # succes
        return True

if __name__ == "__main__":
    l = LinkedChain()

    for i in range(10):
        l.insert(1, i)
    print(l.save())

    l.delete(11)

    print(l.save())


    # print(l.isEmpty())
    # print(l.getLength())
    # print(l.retrieve(4)[1])
    # print(l.insert(4,500))
    # print(l.isEmpty())
    # print(l.insert(1,500))
    # print(l.retrieve(1)[0])
    # print(l.retrieve(1)[1])
    # print(l.save())
    # print(l.insert(1,600))
    # print(l.save())
    # l.load([10,-9,15])
    # l.insert(3,20)
    # print(l.delete(0))
    # print(l.save())
    # print(l.delete(1))
    # print(l.save())