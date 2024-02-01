"""
Provides implementations of the Queue ADT. This queue is unbounded.

Operation Time Compexities are:
  enqueue       O(1)
  dequeue       O(1)
  is_empty      O(1)
  peek          O(1)
  size          O(1)
  __str__       O(n)
"""

# You should read this file, but...
###############################################################################
########################## YOU MAY NOT EDIT THIS FILE #########################
###############################################################################

    
class Queue:
    def __init__(self):
        """
        This Queue uses nodes to hold elements; allows for quick enqueue and
        dequeue. Queue size is unbounded.
        """
        self.__head = None
        self.__tail = None
        self.__size = 0
    
    def enqueue(self, element):
        """
        adds a new element to the tail of the queue.
        """
        new_node = QueueNode(element)
        if self.__size == 0:
            self.__head = new_node
        else:
            self.__tail.set_next(new_node)
            
        self.__tail = new_node
        self.__size += 1
        
    def dequeue(self):
        """
        removes and returns the head of the queue. Raises a QueueException
        if the queue is empty.
        """
        if self.__size == 0:
            raise QueueException(QueueException.DEQUEUE_EMPTY_MSSG)

        value = self.__head.get_data()
        self.__head = self.__head.get_next()
        self.__size -= 1
        if self.__size == 0:
            self.__tail = None

        return value
        
    def peek(self):
        """
        returns the head of the queue. Raises a QueueException if the queue
        is empty.
        """
        if self.__size == 0:
            raise QueueException(QueueException.PEEK_EMPTY_MSSG)
        return self.__head.get_data()

    def is_empty(self):
        """
        returns True if the queue is empty.
        """
        return self.__size == 0
    
    def size(self):
        """
        returns the size of the queue
        """
        return self.__size
    
    def __len__(self):
        """
        allows len(queue) to return the queue's size
        """
        return self.__size

    def __str__(self):
        vals = [ ]
        current = self.__head
        while current != None:
            vals.append(current.get_data())
            current = current.get_next()

        return ", ".join([str(val) for val in vals])

    
###############################################################################
# queue node
###############################################################################
class QueueNode:
    """
    Implements a node with unidirectional links, used to build a queue. 
    """
    def __init__(self, data):
        self.__data = data
        self.__next = None

    def get_next(self):
        """
        returns the node that follows us in a queue, possibly None if this node
        is the tail of the queue.
        """
        return self.__next
    
    def set_next(self, node):
        """
        changes which node follows us in a queue. May be set to None to
        denote that this is the tail of the queue.
        """
        self.__next = node

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
# exceptions
###############################################################################
class QueueException(Exception):
    """
    Should be raised when an exception occurs while interacting with a
    queue's interace.
    """
    
    # Pass these messages in as arguments when instantiating a QueueException
    # depending on the reason for raising the exception.
    PEEK_EMPTY_MSSG    = "Attempted to peek at an empty queue."
    DEQUEUE_EMPTY_MSSG = "Attempted to dequeue an empty queue."
    ENQUEUE_FULL_MSSG  = "Attempted to enqueue a queue at capacity."
    
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


###############################################################################
# testing
###############################################################################
if __name__ == "__main__":
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)
    print(queue, len(queue))
    print(queue.dequeue())
    print(queue, len(queue))
    print(queue.dequeue())
    print(queue.dequeue())
    print(queue, len(queue))
    queue.enqueue('a')
    queue.enqueue('b')
    queue.enqueue('c')
    print(queue, len(queue))
    queue.dequeue()
    queue.dequeue()
    queue.dequeue()
    queue.dequeue()
    
