# Problem Set 4A
# Name: Griffin Leonard
# Collaborators: n/a
# Time Spent: 2:00

# Part A0: Data representation
# Fill out the following variables correctly.
# If correct, the tests named data_representation should pass.
tree1 = [[4,10],5] 
tree2 = [[15,4],[[1,2],10]]
tree3 = [[12],[14,6,2],[19]]


# Part A1: Multiplication on tree leaves

def mul_tree(tree):
    """
    Recursively computes the product of all tree leaves.
    Returns an integer representing the product.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
    Outputs
       total: An int equal to the product of all leaves of the tree.

    """
    product = 1 #base value for empty list
    
    for i in range(len(tree)):
        #if vaule at index i is a list, recursively compute product
        if type(tree[i]) == list:
            tree[i] = mul_tree(tree[i])
        #multiply value at index i with the product of the values at previous indexes
        product *= tree[i]
    return product


# Part A2: Arbitrary operations on tree leaves

def sumem(a,b):
    """
    Example operator function.
    Takes in two integers, returns their sum.
    """
    return a + b

def prod(a,b):
    """
    Example operator function.
    Takes in two integers, returns their product.
    """
    return a * b

def op_tree(tree, op, base_case):
    """
    Recursively runs a given operation on tree leaves.
    Return type depends on the specific operation.

    Inputs
       tree: A list (potentially containing sublists) that
       represents a tree structure.
       op: A function that takes in two inputs and returns the
       result of a specific operation on them.
       base_case: What the operation should return as a result
       in the base case (i.e. when the tree is empty).
    """
    result = base_case #base value for empty list
    for i in range(len(tree)):
        #if vaule at index i is a list, recursively compute operation
        if type(tree[i]) == list:
            tree[i] = op_tree(tree[i],op,base_case)
        #compute operation with value at index i and the result of 
        #the operation computed for all lower indexes of i
        result = op(result,tree[i])
    return result

    
# Part A3: Searching a tree

def search_even(a, b):
    """
    Operator function that searches for even values within its inputs.

    Inputs
        a, b: integers or booleans
    Outputs
        True if either input is equal to True or even, and False otherwise
    """
    #check for Boolean values; a value of True means that 
    #search_even returned True at a lower branch
    if type(a) or type(b) == bool:
        if a or b == True:
            return True
        
    #check if either a or b is divisible by 2.
    #if so, return True. otherwise, return False
    if type(a) == int and a%2 == 0:
        return True
    elif type(b) == int and b%2 == 0:
        return True
    else:
        return False


if __name__ == '__main__':
    # You can use this part for your own testing and debugging purposes.
    # Do not erase the pass statement below.
    pass