# Constants
suits = 'CDHS'
ranks = '23456789TJQKA'

from abc import ABCMeta, abstractmethod
class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """

    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit

    def __repr__(self):
        return self.card

    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()

    def __ge__(self, other): return self.value() >= other.value()

    def __lt__(self, other): return self.value() < other.value()

    def __le__(self, other): return self.value() <= other.value()

    def __eq__(self, other): return self.value() == other.value()

    def __ne__(self, other): return self.value() != other.value()

####################################   1번    ############################3
class PKCard(Card):
    """Card for Poker game
    """
    suits = 'CDHS'
    ranks = '23456789TJQKA'

    def __init__(self, suit_ranks):
        self.card = suit_ranks

    def value(self):
        return self.ranks.index(self.card[0])


if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')
    print(f'{c1} {c2} {c3}')

    # comparison
    print(c1 > c2 == c3)

    # sorting
    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards)



#####################################  2번  #################################
import random
class Deck:
    def __init__(self, cls):
        """Create a deck of 'cls' card class
        """
        self.cards = [cls(str(rank)+str(suit)) for suit in cls.suits for rank in cls.ranks]

    def __str__(self):
        return "{}".format(self.cards)

    def shuffle(self):
        return random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def __len__(self):
        return len(self.cards)

    def __getitem__(self,idx):
        return self.cards[idx]
if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)



################################## 3번  #################################

import random

class Hands:
    def __init__(self, cardss):
        self.cards = cardss
        if len(self.cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = sorted(self.cards, reverse=True)

        self.order = {'straight flush': 9, 'four of a kind': 8, 'full house': 7, 'flush': 6, 'straight': 5,
                      'three pair': 4,
                      'two pair': 3, 'one pair': 2, None: 1}
        self.result = ()
        self.output=["I win, You lose", "You win, I lose", "tie-breaking"]

    def is_flush(self):
        a = []
        for i in self.cards:
            a.append(i[1])
        if len(set(a)) == 1:
            return 'flush'
        else:
            return None

    def is_straight(self):
        a = []
        for i in self.cards:
            a.append(i[0])
        a.sort(reverse=True)
        if (a[0] - 1 == a[1] and a[1] - 1 == a[2] and a[2] - 1 == a[3] and a[3] - 1 == a[4]):
            return 'straight'
        else:
            return None

    def classify_by_rank(self, d_cards):
        a = dict()
        for i in d_cards:
            a[i[0]] = []
        for j in d_cards:
            a[j[0]].append(j[1])

        return a

    def find_a_kind(self):
        cards_by_ranks = self.classify_by_rank(self.cards)
        b = cards_by_ranks.values()
        c = list(map(len, b))
        c = list(map(str, c))
        if '3' in c and '2' in c:
            return 'full house'
        elif '2' in c:
            if c.count('2') == 1:
                return 'one pair'
            elif c.count('2') == 2:
                return 'two pair'
        elif '3' in c:
            return 'three pair'
        elif '4' in c:
            return 'four of a kind'
        else:
            return None


    def straight_flush(self):
        if self.is_straight() == 'straight' and self.is_flush() == 'flush':
            return 'straight flush'
        else:
            return None

    def tell_hand_ranking(self):
        if self.is_flush() != None:
            self.result = (self.order[self.is_flush()], self.cards)

        if self.is_straight() != None:
            self.result = (self.order[self.is_straight()], self.cards)

        if self.find_a_kind() != None:
            self.result = (self.order[self.find_a_kind()], self.cards)

        if self.straight_flush() != None:
            self.result = (self.order[self.straight_flush()], self.cards)

        if self.is_flush() == None and self.is_straight() == None and self.find_a_kind() == None and self.straight_flush() == None:
            self.result = (self.order[None], self.cards)

        return self.result

    def pairs(self, my_sort, you_sort, index_range):
        for i in range(0, index_range):
            if my_sort[i][0] > you_sort[i][0]:
                return self.output[0]
            elif my_sort[i][0] < you_sort[i][0]:
                return self.output[1]
            else:
                pass
        return self.output[2]

    def compare(self, other):
        self.tell_hand_ranking()
        other.tell_hand_ranking()
        print(self.result)
        print(other.result)
        if self.result[0] > other.result[0]: return self.output[0]
        elif self.result[0] == other.result[0]: return self.tie_breadking(other) #무승부면 자세히 비교
        else: return self.output[1]

    def tie_breadking(self, other):
        if self.result[0] not in self.order.values(): return False

        if self.result[0] == 9 or self.result[0] == 5: #straight_flush, straight
            if self.result[1][0][0] > other.result[1][0][0]: return self.output[0]
            elif self.result[1][0][0] == other.result[1][0][0]: return self.output[2]
            else: return self.output[1]

        elif self.result[0] == 6 or self.result[0] == 1: #flush, None
            for i in range(5):
                if self.result[1][i][0] > other.result[1][i][0]: return self.output[0]
                elif self.result[1][i][0] == other.result[1][i][0]: pass
                else: return self.output[1]
            return self.output[2]
        else:
            my_sort=self.classify_by_rank(self.cards)
            you_sort=self.classify_by_rank(other.cards)
            my_sort=sorted(my_sort.items(), key=lambda x: len(x[1]), reverse=True)
            you_sort=sorted(you_sort.items(), key=lambda x: len(x[1]), reverse=True)

            if self.result[0]==8 or self.result[0]==7 or self.result[0]==4: #four card, full house, three pair
                if my_sort[0][0]>you_sort[0][0]: return self.output[0]
                elif  my_sort[0][0]<you_sort[0][0]: return self.output[1]
                else: return False

            if self.result[0]==3: #two pair
                return self.pairs(my_sort, you_sort, 3)

            if self.result[0]==2: #one pair
                return self.pairs(my_sort, you_sort, 4)




if __name__ == '__main__':
    my = ([(5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S')],
          [(5, 'S'), (6, 'S'), (7, 'S'), (8, 'S'), (9, 'S')],  # 스트레이트플러시

          [(2, 'H'), (2, 'D'), (2, 'S'), (2, 'C'), (8, 'S')],  # 포카드

          [(3, 'D'), (3, 'S'), (3, 'H'), (5, 'H'), (5, 'D')],  # 풀하우스

          [(8, 'D'), (3, 'D'), (4, 'D'), (6, 'D'), (5, 'D')],  # 플러시
          [(11, 'D'), (3, 'D'), (4, 'D'), (6, 'D'), (5, 'D')],
          [(11, 'D'), (3, 'D'), (4, 'D'), (10, 'D'), (5, 'D')],
          [(11, 'D'), (3, 'D'), (9, 'D'), (10, 'D'), (5, 'D')],
          [(11, 'D'), (3, 'D'), (9, 'D'), (10, 'D'), (7, 'D')],
          [(11, 'D'), (2, 'D'), (9, 'D'), (10, 'D'), (7, 'D')],

          [(7, 'H'), (3, 'D'), (4, 'S'), (6, 'D'), (5, 'D')],  # 스트레이트
          [(7, 'H'), (3, 'D'), (4, 'S'), (6, 'D'), (5, 'D')],

          [(7, 'H'), (7, 'D'), (7, 'S'), (6, 'C'), (5, 'D')],  # 3페어

          [(7, 'H'), (7, 'D'), (6, 'S'), (6, 'C'), (5, 'D')],  # 2페어
          [(7, 'H'), (7, 'D'), (6, 'S'), (6, 'C'), (5, 'D')],
          [(7, 'H'), (7, 'D'), (6, 'S'), (6, 'C'), (5, 'D')],

          [(7, 'H'), (7, 'D'), (12, 'S'), (6, 'C'), (5, 'D')],  # 1페어
          [(7, 'H'), (7, 'D'), (12, 'S'), (6, 'C'), (5, 'D')],
          [(7, 'H'), (7, 'D'), (12, 'S'), (6, 'C'), (5, 'D')],
          [(7, 'H'), (7, 'D'), (12, 'S'), (6, 'C'), (5, 'D')],

          [(7, 'H'), (2, 'D'), (13, 'S'), (6, 'C'), (5, 'D')],  # 노페어
          [(7, 'H'), (2, 'D'), (13, 'S'), (6, 'C'), (5, 'D')],
          [(7, 'H'), (2, 'D'), (13, 'S'), (11, 'C'), (5, 'D')],
          [(7, 'H'), (2, 'D'), (13, 'S'), (11, 'C'), (5, 'D')],
          [(7, 'H'), (2, 'D'), (13, 'S'), (11, 'C'), (5, 'D')],
          [(7, 'H'), (2, 'D'), (13, 'S'), (11, 'C'), (5, 'D')])

    you = ([(6, 'D'), (7, 'D'), (8, 'D'), (9, 'D'), (10, 'D')],
           [(5, 'D'), (6, 'D'), (7, 'D'), (8, 'D'), (9, 'D')],

           [(4, 'D'), (4, 'S'), (4, 'C'), (4, 'H'), (8, 'S')],

           [(7, 'D'), (7, 'S'), (7, 'C'), (9, 'S'), (9, 'S')],

           [(11, 'S'), (9, 'S'), (2, 'S'), (7, 'S'), (10, 'S')],
           [(11, 'S'), (9, 'S'), (2, 'S'), (7, 'S'), (10, 'S')],
           [(11, 'S'), (9, 'S'), (2, 'S'), (7, 'S'), (10, 'S')],
           [(11, 'S'), (9, 'S'), (2, 'S'), (7, 'S'), (10, 'S')],
           [(11, 'S'), (9, 'S'), (2, 'S'), (7, 'S'), (10, 'S')],
           [(11, 'S'), (9, 'S'), (2, 'S'), (7, 'S'), (10, 'S')],

           [(8, 'H'), (7, 'K'), (4, 'D'), (6, 'D'), (5, 'D')],
           [(7, 'K'), (3, 'C'), (4, 'H'), (6, 'K'), (5, 'S')],
           [(9, 'K'), (9, 'C'), (9, 'H'), (1, 'K'), (3, 'S')],

           [(9, 'K'), (9, 'C'), (3, 'H'), (1, 'K'), (3, 'S')],
           [(7, 'C'), (7, 'S'), (3, 'S'), (3, 'C'), (2, 'D')],
           [(7, 'H'), (7, 'D'), (6, 'S'), (6, 'C'), (7, 'D')],

           [(4, 'H'), (4, 'D'), (6, 'S'), (9, 'C'), (3, 'D')],
           [(7, 'S'), (7, 'C'), (6, 'S'), (9, 'C'), (3, 'D')],
           [(7, 'S'), (7, 'C'), (8, 'S'), (12, 'C'), (3, 'D')],
           [(7, 'S'), (7, 'C'), (6, 'S'), (12, 'C'), (3, 'D')],

           [(3, 'H'), (9, 'D'), (12, 'C'), (2, 'C'), (11, 'D')],
           [(3, 'H'), (9, 'D'), (13, 'C'), (2, 'C'), (11, 'D')],
           [(3, 'H'), (9, 'D'), (13, 'C'), (2, 'C'), (11, 'D')],
           [(3, 'H'), (7, 'D'), (13, 'C'), (2, 'C'), (11, 'D')],
           [(3, 'H'), (7, 'D'), (13, 'C'), (5, 'C'), (11, 'D')],
           [(5, 'H'), (7, 'D'), (13, 'C'), (2, 'C'), (11, 'D')])

    for i in range(0, 26): print(Hands(my[i]).compare(Hands(you[i])))