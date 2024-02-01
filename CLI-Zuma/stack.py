"""
Provides an implementation of the Stack ADT.

Operation Time Complexities are:
  push          O(1)
  pop           O(1)
  peek          O(1)
  is_empty      O(1)
  size          O(1)
  __str__       O(n)

Documentation for each operation is described in the Stack data structure.
"""

# You should read this file, but...
###############################################################################
########################## YOU MAY NOT EDIT THIS FILE #########################
###############################################################################


class Stack:
    """
    Implements a stack using a python list to store elements.
    """
    def __init__(self):
        self.__elements = [ ]
        
    def push(self, element):
        """adds an element to the top of the stack"""
        self.__elements.append(element)
        
    def pop(self):
        """removes and returns the top of the stack"""
        return self.__elements.pop()
    
    def peek(self):
        """returns the top of the stack without removing it"""
        return self.__elements[-1]
    
    def is_empty(self):
        """returns whether the stack contains elements"""
        return len(self.__elements) == 0
    
    def size(self):
        """returns the number of items on the stack"""
        return len(self.__elements)

    def __len__(self):
        """Allows for the use of len(stack)"""
        return len(self.__elements)
    
    def __str__(self):
        """converts the stack to a string representation"""
        # elements need to be reversed because the top of the stack is
        # the end of the list.
        rev_elems = [ e for e in self.__elements ]
        rev_elems.reverse()
        return str(rev_elems)
