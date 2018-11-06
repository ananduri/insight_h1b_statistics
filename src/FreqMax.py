from collections import namedtuple

KeyValue = namedtuple('KeyValue', ('key', 'value'))

class DblNode:
    '''Node for doubly linked list'''
    def __init__(self, datum):
        self.datum = datum
        self.next = None
        self.prev = None

class FreqMax:
    '''
    Data structure used to track most frequent keys in a list.
    
    Supports reading in a list of n keys in O(n) time
    and returning the k most frequent keys in O(k) time.
    
    This is superior time complexity compared to using a max-heap,
    where reading in the list would take O(n log n) time and
    returning the k most frequent keys would take O(k log n) time.
    
    This data structure consists of 
    1. A doubly linked list, where each node contains a key 
       along with the number of times the key has been seen.
       The list is kept in order according to 
       the frequency of the keys.
    2. A dict mapping from keys to the node containing that key
       in the linked list.
    3. A dict mapping from a frequency to the last node in
       the linked list containing that key.
       This is useful for re-ordering the linked list
       when incrementing the frequency of a key.
    
    Methods
    -------
    add(key)
        Updates the data structure so that the frequency of key
        is increased by 1. If the key hasn't been seen yet,
        a new node is created for the key with a frequency of 1.
        This method does not return anything.
    
    getmax(k=1)
        Returns a generator containing the top k most frequently seen
        keys in sorted order. If k is greater than the number of keys 
        in the data structure, then all the keys are returned
        in sorted order, and no warning is raised.
    
        On the other hand, if there are multiple keys with
        the smallest frequency out of the top k keys' frequencies,
        then return all of those keys. In this case the returned
        generator will contain more than k keys.
    
    getmaxgrouped(k=1)
        Return a list of lists containing the top k most frequently
        seen keys. There will be k lists in the returned list.
        Each of those lists will contain at least 1 key.
        If there are multiple keys with the same frequency,
        then the list with that frequency will contain all
        of those keys, in an arbitrary order.
    
    display()
        Prints out a view of the data structure
        that is useful for debugging.
    '''
    
    def __init__(self):
        self.dblist = None
        self.nodes = {}
        self.gaps = {}
        
    def display(self):
        node = self.dblist
        while node is not None:
            print(node.datum, end='')
            if self.gaps[node.datum.value] == node:
                print('   <-- gap: {0}'.format(node.datum.value))
            else:
                print('')
            node = node.next
        
    def add(self, key):
        if key in self.nodes:
            node = self.nodes[key]
            old_value = node.datum.value
            node.datum = node.datum._replace(value=old_value+1)
            
            # if node is a 'gap', update the gaps dict before splicing:
            if self.gaps[old_value] == node:
                if node.prev and node.prev.datum.value == old_value:
                    self.gaps[old_value] = node.prev
                else:
                    del self.gaps[old_value]
                    
            # if linked list is now out of order,
            # splice node to the closest location
            # that restores order

            if node.prev is None or node.datum.value < node.prev.datum.value:
                self.gaps[node.datum.value] = node
                return
            
            # first find the node that will precede 
            # the spliced in node
            target_value = node.datum.value  # note: this is the updated value
            
            if target_value > self.dblist.datum.value:
                # splice node to head of list
                node.prev.next = node.next
                if node.next: node.next.prev = node.prev
                new_child = self.dblist
                node.prev = None
                node.next = new_child
                new_child.prev = node
                self.dblist = node
                self.gaps[node.datum.value] = node
                return

            while target_value not in self.gaps:
                target_value += 1
            new_parent = self.gaps[target_value]
            
            if node.prev != new_parent:            
                # splice node out
                node.prev.next = node.next
                if node.next: node.next.prev = node.prev
                    
                # splice node in, after new_parent
                new_parent.next.prev = node 
                node.next = new_parent.next
                node.prev = new_parent
                new_parent.next = node
            
            self.gaps[node.datum.value] = node                
        else:
            # add new node to tail of linked list
            node = DblNode(KeyValue(key, 1))
            self.nodes[key] = node
            if not self.gaps:
                self.gaps[1] = node
                self.dblist = node
                return
            self.gaps[1].next = node
            node.prev = self.gaps[1]
            self.gaps[1] = node
            
    def getmax(self, k=1):
        def g(count, node):
            while count > 0 and node is not None:
                yield node.datum.key
                node = node.next
                count -= 1
            # check for tied keys that were not included
            while node is not None and node.next.datum.value == node.datum.value:
                yield node.datum.key
            
        return g(k, self.dblist)
        
    def getmaxgrouped(self, k=1):
        node, count = self.dblist, k
        keys = []
        while count > 0 and node is not None:
            currkeys = []
            currkeys.append(node.datum)
            while node.next is not None and node.next.datum.value == node.datum.value:
                node = node.next
                currkeys.append(node.datum)
            keys.append(currkeys)
            node = node.next
            count -= 1
        
        return keys
