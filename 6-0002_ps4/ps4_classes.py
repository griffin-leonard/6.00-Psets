"""
Helper classes for Blackjack Simulation
"""
import random


class Card:
    """
    Representation of a playing card.
    """
    # possible ranks are Ace, the numbers 2 through 10, Jack, Queen, and King
    rank_names = ('2', '3', '4', '5', '6', '7', '8', '9', '10',
                  'J', 'Q', 'K', 'A')
    # possible suits are clubs, diamonds, hearts, and spades
    suit_names = ('C', 'D', 'H', 'S')

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return self.rank + self.suit


class BlackJackCard(Card):
    """
    Representation of a blackjack playing card.
    """

    def get_val(self):
        """
        Returns the maximum point value of the card in a game of blackjack.
        """
        rank = self.get_rank()
        if rank == 'A':
            return 11
        if rank in ('J', 'Q', 'K'):
            return 10
        else:
            return int(rank)


class CardDecks:
    """
    Representation of a card deck consisting of one or more standard card decks.
    """

    def __init__(self, num_decks, card_type):
        self.val = []
        for _ in range(num_decks):
            self.val += CardDecks.create_deck(card_type)
        random.shuffle(self.val)

    @staticmethod
    def create_deck(card_type):
        result = []
        for r in Card.rank_names:
            for s in Card.suit_names:
                result.append(card_type(r, s))
        return result

    def deal_card(self):
        try:
            return self.val.pop()
        except:
            raise ValueError('Deck Empty')

    def num_cards_left(self):
        return len(self.val)


class Busted(Exception):
    """
    Raised when a player goes bust (value of cards in hand exceeds 21)
    """
    pass
