################################################################################
## 6.0002 Fall 2018
## Problem Set 1
## Written By: habadio, mkebede
## Name: Griffin Leonard
## Collaborators: Kaden DiMarco
## Time: 7:00
## Late Days Used: 1

import operator

# Problem 1
class State():
    """
    A class representing the election results for a given state. 
    Assumes there are no ties between dem and gop votes. The party with a 
    majority of votes receives all the Electoral College (EC) votes for 
    the given state.
    """
    def __init__(self, name, dem, gop, ec):
        """
        Parameters:
        name - the 2 letter abbreviation of a state
        dem - number of Democrat votes cast
        gop - number of Republican votes cast
        ec - number of EC votes a state has 

        Attributes:
        self.name - str, the 2 letter abbreviation of a state
        self.winner - str, the winner of the state, "dem" or "gop"
        self.margin - int, difference in votes cast between the two parties, a positive number
        self.ec - int, number of EC votes a state has
        """
        self.name = name
        if dem > gop:
            self.winner = 'dem'
        else:
            self.winner = 'gop'
        self.margin = abs(dem-gop)
        self.ec = ec

    def get_name(self):
        """
        Returns:
        str, the 2 letter abbreviation of the state  
        """
        return self.name

    def get_ecvotes(self):
        """
        Returns:
        int, the number of EC votes the state has 
        """
        return self.ec

    def get_margin(self):
        """
        Returns: 
        int, difference in votes cast between the two parties, a positive number
        """
        return self.margin

    def get_winner(self):
        """
        Returns:
        str, the winner of the state, "dem" or "gop"
        """
        return self.winner

    def __str__(self):
        """
        Returns:
        str, representation of this state in the following format,
        "In <state>, <ec> EC votes were won by <winner> by a <margin> vote margin."
        """
        return str('In',self.get_name()+',',self.get_ecvotes(),'EC votes were won by', self.get_winner(),'by a',self.get_margin(),'vote margin.')
        
    def __eq__(self, other):
        """
        Determines if two State instances are the same.
        They are the same if they have the same state name, winner, margin and ec votes
        Note: Allows you to check if State_1 == State_2

        Param:
        other - State object to compare against  

        Returns:
        bool, True if the two states are the same, False otherwise
        """
        if self.get_name() == other.get_name() and self.get_winner() == other.get_winner() and self.get_margin() == other.get_margin() and self.get_ecvotes() == other.get_ecvotes():       
            return True
        else:
            return False

# Problem 2
def load_election_results(filename):
    """
    Reads the contents of a file, with data given in the following tab-delimited format,
    State   Democrat_votes    Republican_votes    EC_votes 

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a list of State instances
    """
    #open the file and skip over the first line
    f = open(filename, 'r')
    f.readline()
    
    #iterate through remaining lines and create a State for each
    states = []
    for line in f:
        data = line.split()
        state = State(data[0],int(data[1]),int(data[2]),int(data[3]))
        states.append(state)
    
    return states

# Problem 3
def find_winner(election):
    """
    Finds the winner of the election based on who has the most amount of EC votes.
    Note: In this simplified representation, all of EC votes from a state go
    to the party with the majority vote.

    Parameters:
    election - a list of State instances 

    Returns:
    a tuple, (winner, loser) of the election i.e. ('dem', 'gop') if Democrats won, else ('gop', 'dem')
    """
    #count up the total EC votes for each party
    dem, gop = 0,0
    for state in election:
        if state.get_winner() == 'dem':
            dem += state.get_ecvotes()
        else:
            gop += state.get_ecvotes()
            
    #winner is state with more total EC votes
    if dem > gop:
        return ('dem','gop')
    else:
        return ('gop','dem')

def states_lost(election):
    """
    Finds the list of States that were lost by the losing candidate (states won by the winning candidate).
    
    Parameters:
    election - a list of State instances 

    Returns:
    A list of State instances lost by the loser (won by the winner)
    """
    winner = find_winner(election)[0] #a string (either 'dem' or 'gop')
    
    #make list of states that winner of election won 
    states = []
    for state in election:
        if state.get_winner() == winner:
            states.append(state)
    
    return states        

def ec_votes_reqd(election, total=538):
    """
    Finds the number of additional EC votes required by the loser to change election outcome.
    Note: A party wins when they earn half the total number of EC votes plus 1.

    Parameters:
    election - a list of State instances 
    total - total possible number of EC votes

    Returns:
    int, number of additional EC votes required by the loser to change the election outcome
    """
    loser = find_winner(election)[1] #a string (either 'dem' or 'gop')
    
    #count up the total EC votes for the losing party
    votes = 0
    for state in election:
        if state.get_winner() == loser:
            votes += state.get_ecvotes()
    
    #votes needed to change outcome is total/2+1 minus the number of votes the losing party has
    return total//2 +1 -votes
                                         
# Problem 4
def greedy_election(lost_states, ec_votes_needed):
    """
    Finds a subset of lost_states that would change an election outcome if
    voters moved into those states. First chooses the states with the smallest 
    win margin, i.e. state that was won by the smallest difference in number of voters. 
    Continues to choose other states up until it meets or exceeds the ec_votes_needed. 
    Should only return states that were originally lost by the loser (won by the winner) in the election.

    Parameters:
    lost_states - a list of State instances that were lost by the loser of the election
    ec_votes_needed - int, number of EC votes needed to change the election outcome
    
    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    #sort lost_states by each state's margin attribute
    sorted_states = sorted(lost_states, key=operator.attrgetter('margin'))
    
    #add states to the list of swing states until ec_votes_needed is reached
    votes = 0
    swing_states = []
    for state in sorted_states:
        if votes < ec_votes_needed:
            votes += state.get_ecvotes()
            swing_states.append(state)
        else:
            break
    
    return swing_states
        

# Problem 5
def dp_move_max_voters(lost_states, ec_votes, memo = None, answer = True):
    """
    Finds the largest number of voters needed to relocate to get at most ec_votes
    for the election loser. Analogy to the knapsack problem:
    Given a list of states each with a weight(#ec_votes) and value(#margin),
    determine the states to include in a collection so the total weight(#ec_votes)
    is less than or equal to the given limit(ec_votes) and the total value(#voters displaced)
    is as large as possible.

    Parameters:
    lost_states - a list of State instances that were lost by the loser 
    ec_votes - int, the maximum number of EC votes 
    memo - dictionary, an OPTIONAL parameter for memoization (don't delete!).
    Note: If you decide to use the memo make sure to override the default value when it's first called.

    Returns:
    A list of State instances such that the maximum number of voters need to be relocated
    to these states in order to get at most ec_votes 
    The empty list, if no possible states
    """
    #for first time function is called
    if memo == None:
        memo = {}
    
    if (len(lost_states), ec_votes) in memo:
        result = memo[(len(lost_states), ec_votes)]
    elif lost_states == [] or ec_votes == 0:
        result = (0, ())
    elif lost_states[0].get_ecvotes() > ec_votes:
        #explore right branch only (don't chooose state) if weight exceeds max weight (ec_votes)
        result = dp_move_max_voters(lost_states[1:], ec_votes, memo, answer = False)
    else:
        nextState = lost_states[0]
        #explore left branch (choose state)
        withVal, withToTake =\
                 dp_move_max_voters(lost_states[1:],
                            ec_votes - nextState.get_ecvotes(), memo, answer = False)
        withVal += nextState.get_margin()
        #explore right branch (don't chooose state)
        withoutVal, withoutToTake = dp_move_max_voters(lost_states[1:], ec_votes, memo, answer = False)
        #choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextState,))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(lost_states), ec_votes)] = result
    
    #if final answer, returns a list of states. otherwise returns a tuple to use for memoization
    if answer:
        return result[1]
    else:
        return result
    
def move_min_voters(lost_states, ec_votes_needed):
    """
    Finds a subset of lost_states that would change an election outcome if
    voters moved into those states. Should minimize the number of voters being relocated. 
    Only return states that were originally lost by the loser (won by the winner)
    of the election.
    Hint: This problem is simply the complement of dp_move_max_voters

    Parameters:
    lost_states - a list of State instances that the loser of the election lost
    ec_votes_needed - int, number of EC votes needed to change the election outcome

    Returns:
    A list of State instances such that the election outcome would change if additional
    voters relocated to those states (also can be referred to as our swing states)
    The empty list, if no possible swing states
    """
    #find total EC votes loser has
    votes = sum([state.get_ecvotes() for state in lost_states])
    
    #make a list of states that's the complement of states found by dp_move_max_voters
    max_voters = dp_move_max_voters(lost_states, votes-ec_votes_needed)
    min_voters = [state for state in lost_states if state not in max_voters]

    return min_voters

#Problem 6
def flip_election(election, swing_states):
    """
    Finds a way to shuffle voters in order to flip an election outcome. 
    Moves voters from states that were won by the losing candidate (any state not in lost_states), 
    to each of the states in swing_states. To win a swing state, must move (margin + 1) new voters into that state. 
    Also finds the number of EC votes gained by this rearrangement, as well as the minimum number of 
    voters that need to be moved.

    Parameters:
    election - a list of State instances representing the election 
    swing_states - a list of State instances where people need to move to flip the election outcome 
                   (result of move_min_voters or greedy_election)
    
    Return:
    A tuple that has 3 elements in the following order:
        - a dictionary with the following (key, value) mapping: 
            - Key: a 2 element tuple, (from_state, to_state), the 2 letter abbreviation of the State 
            - Value: int, number of people that are being moved 
        - an int, the total number of EC votes gained by moving the voters 
        - an int, the total number of voters moved 
    None, if it is not possible to sway the election
    """
    lost_states = states_lost(election)
    won_states = [state for state in election if state not in lost_states]
    
    #sort state lists by increasing margin
    sortedSwingStates = sorted(swing_states, key=operator.attrgetter('margin'))
    sortedWonStates = sorted(won_states, key=operator.attrgetter('margin'))
    #map state names to margins as to not mutate states in sortedWonStates
    stateMargins = {state.get_name():state.get_margin() for state in sortedWonStates}
    
    stateDict = {}
    totalEC = 0
    voters = 0
    for swingState in sortedSwingStates:
        for wonState in sortedWonStates:
            #only move people when there are enough to change the outcome of state without losing/tying previous states
            if stateMargins[wonState.get_name()] > swingState.get_margin() +1:
                stateDict.update({(wonState.get_name(), swingState.get_name()):swingState.get_margin()+1})
                totalEC += swingState.get_ecvotes()
                voters += swingState.get_margin()+1
                stateMargins[wonState.get_name()] -= swingState.get_margin()+1
                break
    
    #only return tuple if the election outcome has actually changed
    if totalEC < ec_votes_reqd(election):
        return None
    else:
        return (stateDict,totalEC,voters)

if __name__ == "__main__":
    pass
    # Uncomment the following lines to test each of the problems

#    # tests Problem 1 and Problem 2 
#    election2012 = load_election_results("2012_results.txt")
#
#    # tests Problem 3  
#    winner, loser = find_winner(election2012)
#    lost_states = states_lost(election2012)
#    names_lost_states = [state.get_name() for state in lost_states]
#    ec_votes_needed = ec_votes_reqd(election2012)
#    print("Winner:", winner, "\nLoser:", loser)
#    print("EC votes needed:",ec_votes_needed)
#    print("States lost by the loser: ", names_lost_states, "\n")
#
#    # tests Problem 4
#    print("greedy_election")
#    greedy_swing = greedy_election(lost_states, ec_votes_needed)
#    names_greedy_swing = [state.get_name() for state in greedy_swing]
#    voters_greedy = sum([state.get_margin()+1 for state in greedy_swing])
#    ecvotes_greedy = sum([state.get_ecvotes() for state in greedy_swing])
#    print("Greedy swing states results:", names_greedy_swing)
#    print("Greedy voters displaced:", voters_greedy, "for a total of", ecvotes_greedy, "Electoral College votes.", "\n")
#
#    # tests Problem 5: dp_move_max_voters
#    print("dp_move_max_voters")
#    total_lost = sum(state.get_ecvotes() for state in lost_states)
#    move_max = dp_move_max_voters(lost_states, total_lost-ec_votes_needed)
#    max_states_names = [state.get_name() for state in move_max]
#    max_voters_displaced = sum([state.get_margin()+1 for state in move_max])
#    max_ec_votes = sum([state.get_ecvotes() for state in move_max])
#    print("States with the largest margins:", max_states_names)
#    print("Max voters displaced:", max_voters_displaced, "for a total of", max_ec_votes, "Electoral College votes.", "\n")
#
#    # tests Problem 5: move_min_voters
#    print("move_min_voters")
#    swing_states = move_min_voters(lost_states, ec_votes_needed)
#    swing_state_names = [state.get_name() for state in swing_states]
#    min_voters = sum([state.get_margin()+1 for state in swing_states])
#    swing_ec_votes = sum([state.get_ecvotes() for state in swing_states])
#    print("Complementary knapsack swing states results:", swing_state_names)
#    print("Min voters displaced:", min_voters, "for a total of", swing_ec_votes, "Electoral College votes. \n")