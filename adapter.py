from game import Game
import config as cfg
BET_STEP = cfg.betStep


class BlackjackAdapter:

    def __init__(self, game):
        self.game = game
        self.message = ""
        self.hide_dealer_first = False
        self.cardsDealt=False
        self._active_hand_index = 0
        self._selected_bet = BET_STEP

    @property
    def player(self):
        for participant in self.game.participants:
            if participant.name.lower() != "dealer":
                return participant
        return None

    @property
    def dealer(self):
        for participant in getattr(self.game, "participants", []):
            if participant.name.lower() == "dealer":
                return participant
        return None

    @property
    def player_name(self):
        return self.player.name

    @property
    def dealer_name(self):
        return self.dealer.name

    @property
    def player_hands(self):
        player = self.player
        if player is None:
            return []
        return player.hands

    @property
    def dealer_hand(self):
        dealer = self.dealer
        if dealer is None:
            return None
        return dealer.hands[0]

    @property
    def dealer_cards(self):
        return self.dealer_hand.cards

    @property
    def active_hand_index(self):
        self._active_hand_index = self.player.activeHandIndex
        return self._active_hand_index

    @property
    def active_hand(self):
        hands = self.player_hands
        return hands[self._active_hand_index]

    @property
    def balance(self):
        return self.player.balance
    @property
    def current_bet(self):
        hand = self.active_hand
        if (self.round_active and hand is not None) or hand.wager!=0:
            return hand.wager
        elif not self.round_active:
            return self._selected_bet
        else:
            return 0

    @property
    def round_active(self):
        return self.cardsDealt and not self._all_player_hands_finished()

    def get_hand_cards(self, hand):
        return hand.cards

    def get_hand_total(self, hand):
       return hand.value

    def get_hand_bet(self, hand):
        if (self.round_active and hand is not None and hasattr(hand, "wager") ) or hand.wager!=0:
            return hand.wager
        return self._selected_bet

    def get_hand_status_text(self, hand):
        hand.show("note")

    def is_hand_active(self, hand):
        return hand is not None and hand == self.active_hand

    def is_hand_finished(self, hand):
        return hand.isFinished

    def _all_player_hands_finished(self):
        hands = self.player_hands
        return all(self.is_hand_finished(hand) for hand in hands)

    def _advance_local_active_hand(self):
        if self.active_hand.isFinished and self.active_hand_index!=(len(self.player.hands)-1):
            self.player.activeHandIndex+=1

    def sync_message_from_game(self):
        if hasattr(self.game, "message"):
            self.message = str(self.game.message)

    def _finish_round_if_needed(self):
        if self._all_player_hands_finished():
            self.game.dealerTurn()
            self.game.checkResult()
            self.game.showResults()
            self.sync_message_from_game()

    def can_deal(self):
        return self.player.balance>=self._selected_bet and not self.round_active

    def can_hit(self):
        hand = self.active_hand
        return hand is not None and not self.is_hand_finished(hand) and self.round_active

    def can_stand(self):
        hand = self.active_hand
        return hand is not None and not self.is_hand_finished(hand) and self.round_active

    def can_double(self):
        hand = self.active_hand
        self.game.updatePossibilites(self.active_hand, self.player)
        if hand is None or self.is_hand_finished(hand) or "double" not in(self.active_hand.possibilities) or not self.round_active:
            return False
        return True

    def can_split(self):
        hand = self.active_hand
        self.game.updatePossibilites(self.active_hand,self.player)
        if hand is None or self.is_hand_finished(hand) or "split" not in(self.active_hand.possibilities) or not self.round_active:
            return False
        return True
    def cleanupIfNeeded(self):
        if self._all_player_hands_finished() and self.cardsDealt:
            self.player.activeHandIndex=0
            self.game.roundEnd()
            self.cardsDealt = False
    def increase_bet(self):
        if self.game.participants[1].balance>= BET_STEP:
            self._selected_bet += BET_STEP
        self.cleanupIfNeeded()
    def decrease_bet(self):
        self._selected_bet = max(BET_STEP, self._selected_bet - BET_STEP)
        self.cleanupIfNeeded()
    def deal(self):
        self.cleanupIfNeeded()
        self.cardsDealt=True
        self.game.roundStart(self._selected_bet)
        self.hide_dealer_first = True
        self._active_hand_index = 0
        self.sync_message_from_game()

    def hit(self):
        self.game.playerTurn(self.active_hand,self.player,"hit")
        self._advance_local_active_hand()
        self._finish_round_if_needed()
        self.sync_message_from_game()

    def stand(self):
        self.game.playerTurn( self.active_hand,self.player, "pass")
        self._advance_local_active_hand()
        self._finish_round_if_needed()
        self.sync_message_from_game()

    def double_down(self):
        self.game.playerTurn(self.active_hand,self.player, "double")
        self._advance_local_active_hand()
        self._finish_round_if_needed()
        self.sync_message_from_game()

    def split(self):
        self.game.playerTurn(self.active_hand,self.player, "split")
        self._advance_local_active_hand()
        self.sync_message_from_game()
