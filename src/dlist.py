class DoubleList:
    """
    Dvostruko spregnuta lista.
    """
    def __init__(self):
        """
        Inicijalizacija liste: lista je na pocetku prazna. To se oznacava tako
        sto referenca na prvi element liste (self.head) ima vrednost None, i
        referenca na poslednji element liste (self.tail) ima vrednost None.
        """
        self.head = None
        self.tail = None
    
    def insert(self, data):
        """
        Ubacivanje novog elementa u listu, na njen pocetak. Podatak koji se
        upisuje dat je parametrom data.
        """
        newNode = _DoubleListNode(data)
        # next mora pokazivati na stari pocetak liste
        newNode.next = self.head
        # ako je lista prazna, dobice prvi element, pa tail treba da pokazuje na njega
        if self.tail is None:
            self.tail = newNode
        # ako lista nije prazna, stari prvi treba uvezati sa novim prvim
        if self.head is not None:
            self.head.prev = newNode
        # head mora pokazivati na novi prvi element
        self.head = newNode
        
    def insertIndex(self, i, data):
        """
        Ubacivanje novog elementa u listu, izmenju elemenata sa indeksima i-1 i i. Podatak koji se
        upisuje dat je parametrom data. 
        """
        # moramo ici sekvencijalno kroz listu dok ne dodjemo do i-tog elementa
        curNode = self.head
        # trebace nam brojac pozicija u listi
        pos = 0
        while curNode is not None and pos < i:
            curNode = curNode.next
            pos = pos + 1
        if curNode is not None:
            newNode = _DoubleListNode(data)
            
            # XXX
            prevNode = curNode.prev
            newNode.next = curNode
            curNode.prev = newNode
            
            # XXX
            newNode.prev = prevNode
            if newNode.prev is not None:
                newNode.prev.next = newNode
            else:
                self.head = newNode
        
    def append(self, data):
        """
        Dodavanje novog elementa na kraj liste. Podatak koji se upisuje dat je
        parametrom data.
        """
        newNode = _DoubleListNode(data)
        # prev mora pokazivati na stari kraj liste
        newNode.prev = self.tail
        # ako je lista prazna, dobice prvi element, pa head treba da pokazuje na njega
        if self.head is None:
            self.head = newNode
        # ako lista nije prazna, stari poslednji treba uvezati sa novim poslednjim
        if self.tail is not None:
            self.tail.next = newNode
        # tail mora pokazivati na poslednji element
        self.tail = newNode
            
    def exists(self, data):
        """
        Trazenje datog podatka u listi. Funkcija vraca True ako je podatak 
        pronadjen, inace vraca False. Trazeni podatak dat je parametrom data.
        """
        curNode = self.head
        while curNode is not None and curNode.data != data:
            curNode = curNode.next
        return curNode is not None

    def remove(self, data):
        """
        Uklanja prvi nadjeni element sa vrednoscu data iz liste.
        """
        # ako je lista prazna, ne radi nista
        if self.head is None:
            return

        # ako treba izbaciti prvi element:
        if self.head.data == data:
            # head pomeramo na sledeci u listi
            self.head = self.head.next
            # ako lista ima vise od jednog elementa, head nece biti None
            if self.head is not None:
                # referenca na prethodni element za prvi element mora biti None
                self.head.prev = None
            else:
                # ovo znaci da lista ima tacno jedan element, koji smo izbacili;
                # head je postao None, i tail treba da postane None
                self.tail = None
            return
        
        # ako se ne izbacuje prvi element, u petlji ga trazimo medju narednim
        # elementima
        curNode = self.head.next
        while curNode is not None and curNode.data != data:
            curNode = curNode.next
        if curNode is not None:
            # sada curNode pokazuje na element koji treba izbaciti
            curNode.prev.next = curNode.next
            if curNode.next is not None:
                curNode.next.prev = curNode.prev
            # ako uklanjamo poslednji element iz liste, treba pomeriti tail
            if curNode == self.tail:
                self.tail = curNode.prev
                
    def removeIndex(self, i):
        """
        Uklanja i-ti element iz liste.
        """
        if self.head is None:
            return
        if i == 0:
            self.head = self.head.next
            if self.head is not None:
                self.head.prev = None   
            return
        curNode = self.head.next
        pos = 1
        while curNode is not None and pos < i:
            curNode = curNode.next
            pos = pos + 1
        if curNode is not None:
            curNode.prev.next = curNode.next
            if curNode.next is not None:
                curNode.next.prev = curNode.prev
            if curNode == self.tail:
                self.tail = curNode.prev
        
    def values(self):
        """
        Vraca sadrzaj liste u obliku klasicne Python liste
        """
        retVal = []
        curNode = self.head
        while curNode is not None:
            retVal.append(curNode.data)
            curNode = curNode.next
        return retVal
    
    def index(self, i):
        """
        Vraca podatak iz liste koji se nalazi na i-toj poziciji. Pozicije
        se broje od 0. Ako lista ima manje od i+1 elemenata, vraca None.
        """
        # moramo ici sekvencijalno kroz listu dok ne dodjemo do i-tog elementa
        curNode = self.head
        # trebace nam brojac pozicija u listi
        pos = 0
        while curNode is not None and pos < i:
            curNode = curNode.next
            pos = pos + 1
        if curNode is None:
            return None
        else:
            return curNode.data
    
    def size(self):
        """
        Vraca broj elemenata liste.
        """
        count = 0
        curNode = self.head
        while curNode is not None:
            curNode = curNode.next
            count = count + 1
        return count

    def clear(self):
        """
        Uklanja sve elemente iz liste.
        """
        self.head = self.tail = None
    
class _DoubleListNode:
    """
    Element dvostruko spregnute liste. Ima tri atributa: data cuva podatak
    koji predstavlja element liste; next cuva referencu na sledeci element
    u listi; prev cuva referencu na prethodni element u listi.

    Kod poslednjeg elementa liste next je None. Kod prvog elementa liste
    prev je None.
    """
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

if __name__ == '__main__':
    # napravimo dvostruko spregnutu listu; inicijalno je prazna
    dlist = DoubleList()
    # dodajemo elemente na njen kraj
    dlist.append(1)
    dlist.append(2)
    dlist.append(3)
    dlist.append(4)
    dlist.append(5)
    dlist.append(6)
    # sada bi u listi trebalo da ima 6 elemenata, sa vrednostima 1,2,3,4,5,6
    print(dlist.size())
    print(dlist.values())
    # uklonimo broj 7 iz liste (takvog nema)
    dlist.remove(7)
    # sada bi sadrzaj liste trebalo da bude nepromenjen
    print(dlist.values())
    # uklonimo broj 6 iz liste (poslednji)
    dlist.remove(6)
    # sada bi lista trebalo da glasi 1,2,3,4,5
    print(dlist.values())
    # uklonimo broj 1 iz liste (prvi)
    dlist.remove(1)
    # sada bi lista trebalo da glasi 2,3,4,5
    print(dlist.values())
    # uklonimo broj 3 iz liste (iz sredine)
    dlist.remove(3)
    # sada bi lista trebalo da glasi 2,4,5
    print(dlist.values())
    # da proveravamo da li u listi postoji broj 4
    print(dlist.search(4))
    # vrati element sa indeksom 1 (trebalo bi dobiti 4)
    print(dlist.index(1))
    # vrati element sa indeksom 53 (trebalo bi dobiti None)
    print(dlist.index(53))