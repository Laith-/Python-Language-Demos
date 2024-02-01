"""
Provides an implementation of the Doubly Linked List ADT.

Operation Time Complexities are:                Quality of Life Analogue:
  add        O(1)
  append     O(1)                                     
  pop        O(n); O(1) at head and tail
  insert     O(n); O(1) at head and tail
  index      O(n); O(1) at head and tail          __index__     same as index
  peek       O(1)
  remove     O(n)
  contains   O(n)                                 __contains__  same as contains
  length     O(1)                                 __len__       same as length
  is_empty   O(1)
  __str__    O(n)
  sort       ??? -- you must implement
                                                  __iter__      O(n)

Documentation for each operation is described in the DoublyLinkedList data
structure.

NOTE: This implementation of a DLL has numerous 'quality of life' improvements
to it. You may iterate over it using a for loop, and reference specific elements
by index using square brackets. See 'quality of life' documentation below.
"""


class DoublyLinkedList:
    """
    Implements a doubly linked list. Notable features of DLL are that they have
    O(1) time complexity for adding and removing at index 0 and -1. 
    """
    ###########################################################################
    # initialization
    ###########################################################################
    def __init__(self):
        self.__head = None  # the first node in the SLL
        self.__tail = None  # the last node in the SLL

        # size is cached so we don't have to recalculate it every time we
        # need it. Recalculating is O(n), whereas cacheing is O(1)
        self.__size = 0

        
    ###########################################################################
    # public interface -- must be completed for the assignment
    ###########################################################################
    def sort(self):
        """
        Reorganizes the list contents so they are sorted in ascending order.
        Assume contents can be compared with the logical operators, >, <, and ==
        """
        pass # delete pass and replace with your code


    ###########################################################################
    # private methods -- you may define your own private methods here.
    ###########################################################################

    
            
    ###########################################################################
    # public interface -- you may not edit these methods.
    ###########################################################################
    def add(self, element):
        """
        adds a new element to the head of the list
        """
        new_head = DLLNode(element)
        self.__connect(new_head, self.__head)
        self.__head = new_head
        self.__size += 1 

        # if the list is len==1, then the new head is also the tail
        if self.__size == 1:
            self.__tail = self.__head

            
    def append(self, element):
        """
        adds the element to the tail of the list
        """
        new_tail = DLLNode(element)
        self.__connect(self.__tail, new_tail)
        self.__tail = new_tail
        self.__size += 1

        # if the list is len==1, then the new tail is also the new head
        if self.__size == 1:
            self.__head = self.__tail

            
    def remove(self, element):
        """
        removes the first occurrence of element. Raises an exception if the
        element does not exist in the list.
        """
        current = self.__head
        found = False
        while current != None and not found:
            if current.get_data() == element:
                self.__connect(current.get_previous(), current.get_next())
                self.__size -= 1
                found = True
            else:
                current = current.get_next()
            
        if not found:
            raise LinkedListException(
                LinkedListException.LIST_NOCONTAINS_MSSG % str(element))
        
        # fix our head and tail if they were removed
        elif self.__size == 0:
            self.__head = self.__tail = None
        elif self.__head == current:
            self.__head = current.get_next()
        elif self.__tail == current:
            self.__tail = current.get_previous()

            
    def contains(self, element):
        """
        returns True if element is in the list, False otherwise
        """
        current = self.__head
        while current != None:
            if current.get_data() == element:
                return True
            current = current.get_next()
        return False


    def peek(self):
        """
        returns the head of the list
        """
        return self.index(0)
    
    
    def index(self, pos):
        """
        returns the element at the specified position in the list. Raises an
        exception if the position is out of bounds.
        """
        assert pos >= 0, "Index out of bounds, %d." % pos
        assert pos < self.__size, "Index out of bounds, %d." % pos
        assert self.__size > 0, "Index out of bounds, %d." %  pos

        data = None
        # special case: indexing the tail
        if pos == self.__size-1:
            data = self.__tail.get_data()
        else:
            current = self.__head
            times_to_traverse = pos
            while times_to_traverse > 0:
                current = current.get_next()
                times_to_traverse -= 1
            data = current.get_data()

        return data

    
    def insert(self, pos, element):
        """
        places element at index pos of the list, raises an exception if the
        position is out of bounds.
        """
        assert pos >= 0, "Index out of bounds, %d." % pos
        assert pos <= self.__size, "Index out of bounds, %d." % pos
        
        # special case: adding to the tail
        if pos == self.__size:
            self.append(element)

        # special case: adding to the head
        elif pos == 0:
            self.add(element)

        # everything in between; can only excute if we have 3 or more elements
        # in the list.
        else:
            current = self.__head
            times_to_traverse = pos
            while times_to_traverse > 0:
                current = current.get_next()
                times_to_traverse -= 1

            node = DLLNode(element)
            prev = current.get_previous()
            next = current
            self.__connect(prev, node)
            self.__connect(node, next)
            self.__size += 1

        
    def pop(self, pos=None):
        """
        removes and returns the element at the specified index, defaulting to
        the tail of the list. Raises an exception if the position is
        out of bounds.
        """
        if pos != None:
            assert pos >= 0, "Index out of bounds, %d." % pos
            assert pos < self.__size, "Index out of bounds, %d." % pos
            assert self.__size > 0, "Index out of bounds, %d." %  pos
        else:
            pos = self.__size - 1

        data = None
        
        # special case: pop the tail
        if pos == self.__size - 1:
            data = self.__tail.get_data()
            self.__tail = self.__tail.get_previous()
            self.__connect(self.__tail, None)
            self.__size -= 1
            if self.__size == 1:
                self.__head = self.__tail
                
        # special case: pop the head
        elif pos == 0:
            data = self.__head.get_data()
            self.__head = self.__head.get_next()
            self.__connect(None, self.__head)
            self.__size -= 1
            if self.__size == 1:
                self.__tail = self.__head

        # everything between the head and the tail; can only execute if
        # the list has 3 or more elements. Otherwise, one of the previous two
        # cases would have been executed
        else:
            current = self.__head
            times_to_traverse = pos
            while times_to_traverse > 0:
                current = current.get_next()
                times_to_traverse -= 1
                
            data = current.get_data()
            self.__connect(current.get_previous(), current.get_next())

            self.__size -= 1

        # check if list is now empty
        if self.__size == 0:
            self.__tail = self.__head = None
                
        return data

    
    def is_empty(self):
        """
        returns True if list is empty, False otherwise
        """
        return self.__size == 0

    
    def length(self):
        """
        returns number of elements in the list
        """
        return self.__size

    
    def __str__(self):
        """
        return an unofficial string representation of the list
        """
        strs = [ ]
        node = self.__head
        while node is not None:
            strs.append(str(node.get_data()))
            node = node.get_next()
        return ", ".join(strs)

    
    def __repr__(self):
        """
        return an official string representation of the list
        """
        strs = [ ]
        node = self.__head
        while node is not None:
            strs.append(repr(node.get_data()))
            node = node.get_next()
        return "[ " + ", ".join(strs) + " ]"
    

    ###########################################################################
    # qualiity of life methods -- do not edit these.
    ###########################################################################
    def __contains__(self, element):
        """
        implementing this method allows for the 'in' operator to be applied
        to the data structure. e.g., if 7 in list:
        """
        return self.contains(element)
    
    def __len__(self):
        """
        implementing this method allows len() to be applied to the list
        """
        return self.__size
    
    def __getitem__(self, pos):
        """
        implementing this method allows use of square brackets for indexing 
        specific elements.
           e.g., value = linked_list[0]
        """        
        return self.index(pos)

    def __iter__(self):
        """
        Implementiing this method allows for iteration over the list with
        a for loop, among other things:
          e.g., for value in linked_list:
                  print(value)
        """
        current = self.__head        
        while current != None:
            # not sure what yield does? Here are some introductions:
            # https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
            # https://www.geeksforgeeks.org/use-yield-keyword-instead-return-keyword-python/
            yield current.get_data()
            current = current.get_next()
            
        
    ###########################################################################
    # private methods -- do not edit these.
    ###########################################################################
    def __connect(self, first, second):
        """
        Helper method that connects two nodes to each other, first being
        the earlier node and second being the latter node. Allows nodes to be
        None, signifying that the other is the head or tail of the list.
        """
        if first is not None:
            first.set_next(second)
        if second is not None:
            second.set_previous(first)


            
###############################################################################
# Doubly Linked Node: do not edit
###############################################################################
class DLLNode:
    """
    Implements a node with double links (forward, backward), used to build 
    doubly linked lists.
    """
    def __init__(self, data, prev=None, next=None):
        """
        Initialize one node for a DLL
          data    : the value that the DLL stores
          next    : the next node in the list (possibly None)
          prev    : the previous node in the list (possbly None)
        """
        self.__data = data
        self.__prev = prev
        self.__next = next

        if prev != None:
            prev.set_next(self)
        if next != None:
            next.set_previous(self)

    def get_next(self):
        """
        returns the node that follows us in a DLL, possibly None if this node
        is the tail of the list.
        """
        return self.__next
    
    def set_next(self, node):
        """
        changes which node follows us in the DLL. May be set to None to
        denote that this is the tail of the list.
        """
        self.__next = node

    def get_previous(self):
        """
        returns the node that precedes us in a DLL, possibly None if this node
        is the head of the list.
        """
        return self.__prev
    
    def set_previous(self, node):
        """
        changes which node precedes us in the DLL. May be set to None to
        denote that this is the head of the list.
        """
        self.__prev = node

    def get_data(self):
        """
        returns the value that we hold
        """
        return self.__data

    def set_data(self, data):
        """
        sets the value that we hold
        """
        self.__data = data


###############################################################################
# Custom exceptions: do not edit
###############################################################################
class LinkedListException(Exception):
    """
    Should be raised when an exception occurs while interacting with a DLL's
    interface.
    """
    # Pass these messages in as arguments when instantiating a QueueException
    # depending on the reason for raising the exception.
    LIST_EMPTY_MSSG      = "Tried to remove element from an empty list."
    LIST_INDEX_MSSG      = "List index out of bounds, %d."
    LIST_NOCONTAINS_MSSG = "Tried to remove element, %s, not in list."
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


###############################################################################
# Testing
###############################################################################
if __name__ == "__main__":
    list = DoublyLinkedList()

    # you should test that your sort method works properly, here.
    ############
    # FINISH ME
    ############
