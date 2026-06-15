"""
德州扑克游戏引擎 - 单文件完整实现
"""
import random
from enum import Enum
from typing import List, Dict, Tuple


class Suit(Enum):
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'
    SPADES = '♠'


class Rank(Enum):
    TWO = ('2', 2)
    THREE = ('3', 3)
    FOUR = ('4', 4)
    FIVE = ('5', 5)
    SIX = ('6', 6)
    SEVEN = ('7', 7)
    EIGHT = ('8', 8)
    NINE = ('9', 9)
    TEN = ('10', 10)
    JACK = ('J', 11)
    QUEEN = ('Q', 12)
    KING = ('K', 13)
    ACE = ('A', 14)


class GamePhase(Enum):
    WAITING = 'waiting'
    PRE_FLOP = 'pre_flop'
    FLOP = 'flop'
    TURN = 'turn'
    RIVER = 'river'
    SHOWDOWN = 'showdown'
    FINISHED = 'finished'


class PlayerAction(Enum):
    FOLD = 'fold'
    CHECK = 'check'
    CALL = 'call'
    RAISE = 'raise'
    ALL_IN = 'all_in'


class HandRank(Enum):
    HIGH_CARD = (1, '高牌')
    ONE_PAIR = (2, '一对')
    TWO_PAIR = (3, '两对')
    THREE_OF_A_KIND = (4, '三条')
    STRAIGHT = (5, '顺子')
    FLUSH = (6, '同花')
    FULL_HOUSE = (7, '葫芦')
    FOUR_OF_A_KIND = (8, '四条')
    STRAIGHT_FLUSH = (9, '同花顺')
    ROYAL_FLUSH = (10, '皇家同花顺')


class Card:
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f"{self.rank.value[0]}{self.suit.value}"
    
    def get_value(self) -> int:
        return self.rank.value[1]


class Player:
    def __init__(self, player_id: int, username: str, first_name: str, chips: int = 1000):
        self.id = player_id
        self.username = username
        self.first_name = first_name
        self.chips = chips
        self.hand: List[Card] = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
    
    def reset(self):
        self.hand = []
        self.current_bet = 0
        self.is_folded = False
        self.is_all_in = False
    
    def bet(self, amount: int) -> int:
        actual = min(amount, self.chips)
        self.chips -= actual
        self.current_bet += actual
        if self.chips == 0:
            self.is_all_in = True
        return actual


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self):
        self.cards = [Card(s, r) for s in Suit for r in Rank]
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()
    
    def deal_many(self, count: int) -> List[Card]:
        return [self.deal() for _ in range(count)]


class HandEvaluator:
    @staticmethod
    def evaluate(cards: List[Card]) -> Tuple[HandRank, List[int]]:
        values = sorted([c.get_value() for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        
        is_flush = len(set(suits)) == 1
        unique_values = sorted(list(set(values)), reverse=True)
        
        is_straight = False
        straight_high = 0
        
        for i in range(len(unique_values) - 4):
            if unique_values[i] - unique_values[i + 4] == 4:
                is_straight = True
                straight_high = unique_values[i]
                break
        
        if not is_straight and set(unique_values) >= {14, 2, 3, 4, 5}:
            is_straight = True
            straight_high = 5
        
        value_counts: Dict[int, int] = {}
        for v in values:
            value_counts[v] = value_counts.get(v, 0) + 1
        
        counts = sorted(value_counts.items(), key=lambda x: (-x[1], -x[0]))
        
        if is_flush and is_straight and straight_high == 14:
            return HandRank.ROYAL_FLUSH, [14]
        if is_flush and is_straight:
            return HandRank.STRAIGHT_FLUSH, [straight_high]
        if counts[0][1] == 4:
            return HandRank.FOUR_OF_A_KIND, [counts[0][0]]
        if counts[0][1] == 3 and counts[1][1] >= 2:
            return HandRank.FULL_HOUSE, [counts[0][0], counts[1][0]]
        if is_flush:
            return HandRank.FLUSH, values[:5]
        if is_straight:
            return HandRank.STRAIGHT, [straight_high]
        if counts[0][1] == 3:
            return HandRank.THREE_OF_A_KIND, [counts[0][0]]
        if counts[0][1] == 2 and counts[1][1] == 2:
            return HandRank.TWO_PAIR, [counts[0][0], counts[1][0]]
        if counts[0][1] == 2:
            return HandRank.ONE_PAIR, [counts[0][0]]
        return HandRank.HIGH_CARD, values[:5]


class PokerGame:
    def __init__(self, room_id: str, small_blind: int = 10, big_blind: int = 20):
        self.room_id = room_id
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.players: List[Player] = []
        self.community_cards: List[Card] = []
        self.pot = 0
        self.phase = GamePhase.WAITING
        self.current_player_idx = 0
        self.dealer_idx = 0
        self.current_bet_level = 0
    
    def add_player(self, player_id: int, username: str, first_name: str, chips: int = 1000) -> bool:
        if len(self.players) >= 10:
            return False
        if any(p.id == player_id for p in self.players):
            return False
        self.players.append(Player(player_id, username, first_name, chips))
        return True
    
    def start_round(self):
        self.deck.reset()
        self.community_cards = []
        self.pot = 0
        self.phase = GamePhase.PRE_FLOP
        self.current_bet_level = 0
        
        for p in self.players:
            p.reset()
            p.hand = self.deck.deal_many(2)
        
        sb = (self.dealer_idx + 1) % len(self.players)
        bb = (self.dealer_idx + 2) % len(self.players)
        
        self.players[sb].bet(self.small_blind)
        self.players[bb].bet(self.big_blind)
        self.pot += self.small_blind + self.big_blind
        self.current_bet_level = self.big_blind
        self.current_player_idx = (bb + 1) % len(self.players)
    
    def next_phase(self):
        if self.phase == GamePhase.PRE_FLOP:
            self.phase = GamePhase.FLOP
            self.community_cards = self.deck.deal_many(3)
        elif self.phase == GamePhase.FLOP:
            self.phase = GamePhase.TURN
            self.community_cards.append(self.deck.deal())
        elif self.phase == GamePhase.TURN:
            self.phase = GamePhase.RIVER
            self.community_cards.append(self.deck.deal())
        elif self.phase == GamePhase.RIVER:
            self.phase = GamePhase.SHOWDOWN
            self.showdown()
            return
        
        self.current_bet_level = 0
        for p in self.players:
            p.current_bet = 0
        self.current_player_idx = (self.dealer_idx + 1) % len(self.players)
    
    def player_action(self, player_id: int, action: PlayerAction, amount: int = 0) -> bool:
        player = next((p for p in self.players if p.id == player_id), None)
        if not player or player.is_folded:
            return False
        if self.players[self.current_player_idx].id != player_id:
            return False
        
        if action == PlayerAction.FOLD:
            player.is_folded = True
        elif action == PlayerAction.CHECK:
            if player.current_bet < self.current_bet_level:
                return False
        elif action == PlayerAction.CALL:
            call_amt = self.current_bet_level - player.current_bet
            if call_amt > 0:
                self.pot += player.bet(call_amt)
        elif action == PlayerAction.RAISE:
            raise_amt = max(amount, self.current_bet_level + self.big_blind)
            needed = raise_amt - player.current_bet
            self.pot += player.bet(needed)
            self.current_bet_level = raise_amt
        elif action == PlayerAction.ALL_IN:
            all_in_amt = player.chips + player.current_bet
            self.pot += player.bet(player.chips)
            if all_in_amt > self.current_bet_level:
                self.current_bet_level = all_in_amt
        
        if self._is_betting_complete():
            self.next_phase()
        else:
            self._next_player()
        
        return True
    
    def _next_player(self):
        while True:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            if not self.players[self.current_player_idx].is_folded:
                break
    
    def _is_betting_complete(self) -> bool:
        active = [p for p in self.players if not p.is_folded]
        if len(active) == 1:
            return True
        return all(p.current_bet == self.current_bet_level or p.is_all_in for p in active)
    
    def showdown(self):
        active = [p for p in self.players if not p.is_folded]
        if len(active) == 1:
            active[0].chips += self.pot
            self.phase = GamePhase.FINISHED
            return
        
        best_players = []
        for player in active:
            if not best_players:
                best_players = [player]
            else:
                r1, _ = HandEvaluator.evaluate(player.hand + self.community_cards)
                r2, _ = HandEvaluator.evaluate(best_players[0].hand + self.community_cards)
                if r1.value[0] > r2.value[0]:
                    best_players = [player]
                elif r1.value[0] == r2.value[0]:
                    best_players.append(player)
        
        split = self.pot // len(best_players)
        for winner in best_players:
            winner.chips += split
        
        self.phase = GamePhase.FINISHED
    
    def get_state(self) -> dict:
        return {
            'room_id': self.room_id,
            'phase': self.phase.value,
            'community_cards': [str(c) for c in self.community_cards],
            'pot': self.pot,
            'current_bet': self.current_bet_level,
            'players': [
                {
                    'id': p.id,
                    'username': p.username,
                    'first_name': p.first_name,
                    'chips': p.chips,
                    'current_bet': p.current_bet,
                    'is_folded': p.is_folded,
                    'hand': [str(c) for c in p.hand]
                } for p in self.players
            ]
        }
