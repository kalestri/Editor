from dlist import DoubleList

class Stack:
    """
    Implementacija steka.
    """
    def __init__(self):
        """
        Inicijalizacija steka: inicijalno je prazan. Atribut u kome cuvamo 
        podatke bice dvostruko spregnuta lista.
        """
        self._list = DoubleList()
    
    def push(self, data):
        """
        Dodavanje elementa na vrh steka.
        """
        self._list.append(data)
        
    def pop(self):
        """
        Skida element sa vrha steka i vraca ga kao rezultat. Ako je stek prazan
        vraca None.
        """
        size = self._list.size()
        if size == 0:
            return None
        data = self._list.tail.data
        self._list.removeIndex(size-1)
        return data
    
    def peek(self):
        """
        Vraca element sa vrha steka bez skidanja. Ako je stek prazan vraca None.
        """
        size = self._list.size()
        if size == 0:
            return None
        return self._list.tail.data
    
    def clear(self):
        """
        Uklanja sve elemente sa steka.
        """
        self._list.clear()
    
    def values(self):
        """
        Vraca sadrzaj steka u obliku klasicne Python liste.
        """
        return self._list.values()
    
if __name__ == '__main__':
    stek = Stack()
    stek.push(1)
    stek.push(2)
    stek.push(3)
    print(stek.values())
    value = stek.peek()
    print("Peeked:", value)
    value = stek.pop()
    print("Popped:", value)
    print(stek.values())
    value = stek.pop()
    print("Popped:", value)
    print(stek.values())
    value = stek.pop()
    print("Popped:", value)
    print(stek.values())
    