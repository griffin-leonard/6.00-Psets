# Problem Set 4
# Name: Griffin Leonard
# Collaborators: n/a
# Time Spent: 11:00
# Late Days Used: 2

import matplotlib.pyplot as plt
import numpy as np
from ps4_classes import BlackJackCard, CardDecks, Busted


#############
# PROBLEM 1 #
#############
class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """
    
    hit = 'hit'
    stand = 'stand'

    def __init__(self, deck):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
        card deck (this deck itself contains one or more standard card decks)

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck
                      
        Important: You MUST deal out the first four cards in the following order:
            player, dealer, player, dealer
        """
        self.deck = deck
        self.player = [deck.deal_card()]
        self.dealer = [deck.deal_card()]
        self.player.append(deck.deal_card())
        self.dealer.append(deck.deal_card())

    # You can call the method below like this:
    #   BlackJackHand.best_val(cards)
    @staticmethod
    def best_val(cards):
        """
        Finds the best sum of point values given a list of cards, where the
        "best sum" is defined as the highest point total not exceeding 21.

        Remember that an Ace can have value 1 or 11.
        Hint: If you have one Ace, give it a value of 11 by default. If the sum
        point total exceeds 21, then give it a value of 1. What should you do
        if cards has more than one Ace?

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        #create count for number of Aces and the value of the cards
        total = 0
        aces = 0
        for c in cards:
            if c.get_rank() == 'A':
                aces += 1
            total += c.get_val()
        
        #if Aces cause player to bust, change the value of the Aces to 1
        while total > 21 and aces != 0:
            aces -= 1
            total -= 10
            
        return total
        
    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        return self.player

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        return self.dealer

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        return self.dealer[0]

    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        used for testing, DO NOT MODIFY
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    # Strategy 1
    def mimic_dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        if self.best_val(self.get_player_cards()) < 17:
            return 'hit'
        return 'stand'

    # Strategy 2
    def peek_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        if self.best_val(self.get_player_cards()) < self.best_val(self.get_dealer_cards()):
            return 'hit'
        return 'stand'

    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        if self.best_val(self.get_player_cards()) >= 17:
            return 'stand'
        elif self.best_val(self.get_player_cards()) >= 12 and self.get_dealer_upcard().get_val() <= 6:
            return 'stand'
        return 'hit'

    def play_player(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player. The player
        will be dealt a new card until they stand or bust.

        Parameter:
        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)

        This function does not return anything. Instead, it:
            - Adds a new card to self.player each time the player hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the player's hand is greater than 21.
        """
        if self.best_val(self.get_player_cards()) > 21:
            raise Busted()
        if strategy(self) == 'hit':
            self.player.append(self.deck.deal_card())
            self.play_player(strategy)

    def play_dealer(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17, or they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the dealer's hand is greater than 21.
        """
        if self.best_val(self.get_dealer_cards()) > 21:
            raise Busted()
        if self.best_val(self.get_dealer_cards()) < 17:
            self.dealer.append(self.deck.deal_card())
            self.play_dealer()

    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.

        Useful for debugging. DO NOT MODIFY. 
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

#############
# PROBLEM 2 #
#############


def play_hand(deck, strategy, bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on their inital bet.

    Note: If the dealer gets a blackjack (i.e. first two cards equal 21),
    and the player does not, the dealer automatically wins the game.

    The player will get:

        - 2.5 times their original bet if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.
        - 2 times their original bet if the player wins after getting more
          cards or the dealer busts.
        - the original amount they bet if the game ends in a tie. If the
          player and dealer both get blackjack from their first two cards, this
          is also a tie.
        - 0 if the dealer wins or the player busts.

    Parameters:

        deck - an instance of CardDeck
        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        bet - float, the amount that the player bets (default=1.0)

    Returns:

        float, the amount the player gets back
    """
    #play the player's and dealer's hand
    hand = BlackJackHand(deck)    
    
    #check if player or dealer has blackjack
    if hand.best_val(hand.get_player_cards()) == 21 and hand.best_val(hand.get_dealer_cards()) < 21:
        return 2.5*bet #if the player gets blackjack
    elif hand.best_val(hand.get_player_cards()) < 21 and hand.best_val(hand.get_dealer_cards()) == 21:
        return 0.0
    elif hand.best_val(hand.get_player_cards()) == 21 and hand.best_val(hand.get_dealer_cards()) == 21:
        return bet

    #try playing the hand and check if the player or dealer busts
    try:
        hand.play_player(strategy)
    except Busted: #if the player busts the dealer wins
        return 0.0
    try:
        hand.play_dealer()
    except Busted: #if the dealer busts the player wins
        return 2*bet
    
    #if the player and dealer don't bust, check who wins
    if hand.best_val(hand.get_player_cards()) == hand.best_val(hand.get_dealer_cards()):
        return bet #if there's a tie
    elif hand.best_val(hand.get_player_cards()) > hand.best_val(hand.get_dealer_cards()):
        return 2*bet #if the player wins
    return 0.0 #if the dealer wins

#############
# PROBLEM 3 #
#############


def run_simulation(strategy, bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False):
    """
    Runs a simulation and generates a box plot reflecting the distribution of
    player's rates of return across all trials.

    The box plot displays the distribution of data based on the five number
    summary: minimum, first quartile, median, third quartile, and maximum.
    We also want to show the average on the box plot. You can do this by
    specifying another parameter: plt.boxplot(results, showmeans=True)

    For each trial:

        - instantiate a new CardDeck with the num_decks and type BlackJackCard
        - for each hand in the trial, call play_hand and keep track of how
          much money the player receives across all the hands in the trial
        - calculate the player's rate of return, which is
            100*(total money received-total money bet)/(total money bet)

    Parameters:

        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.mimic_dealer_strategy)
        bet - float, the amount that the player bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials
    """
    returnRate = []
    
    #for each trial create a new deck and a counter for money bet and won
    for trial in range(num_trials):
        deck = CardDecks(num_decks,BlackJackCard)
        totalBet = 0.0
        totalWon = 0.0
        #play each hand and update the money counters
        for n in range(num_hands):
            totalBet += bet
            totalWon += play_hand(deck,strategy,bet)
        #add the rate of return to the list
        returnRate.append(100*(totalWon-totalBet)/totalBet)
    
    #create boxplot
    if show_plot:
        plt.figure()
        plt.boxplot(returnRate,showmeans=True)
        plt.title('Player ROI on Playing '+str(num_hands)+' Hands ('+strategy.__name__+')\n(Mean = '\
                  +str(sum(returnRate)/num_trials)+', SD = '+str(np.std(returnRate))+')')
        plt.ylabel('% Return')
        plt.xticks([])
        
    return (returnRate,sum(returnRate)/num_trials,np.std(returnRate))


def run_all_simulations(strategies):
    """
    Runs the simulation for each strategy in strategies and generates a single
    graph with one box plot for each strategy. Each box plot should reflect the
    distribution of rates of return for each strategy.

    Make sure to label each plot with the name of the strategy.

    Parameters:

        strategies - list of strategies to simulate
    """
    #get the rates of return for each strategy 
    results = []
    for strat in strategies:
        results.append(run_simulation(strat)[0])
    
    #create boxplot
    plt.figure()
    plt.boxplot(results,showmeans=True)
    plt.title('Player ROI Using Different Strategies')
    plt.ylabel('% Return')
    stratText = [s.__name__ for s in strategies]
    ticks = [x+1 for x in range(len(strategies))]
    plt.xticks(ticks,stratText)

if __name__ == '__main__':
    # uncomment to test each strategy separately
#    run_simulation(BlackJackHand.mimic_dealer_strategy, show_plot=True)
#    run_simulation(BlackJackHand.peek_strategy, show_plot=True)
#    run_simulation(BlackJackHand.simple_strategy, show_plot=True)

    # uncomment to run all simulations
#    run_all_simulations([BlackJackHand.mimic_dealer_strategy,
#                         BlackJackHand.peek_strategy, BlackJackHand.simple_strategy])
    pass