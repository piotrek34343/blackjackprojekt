"""Adapter między backendem a interfejsem. Upraszcza dostęp do danych i akcji gry."""
import config as cfg
BET_STEP = cfg.betStep


class BlackjackAdapter:
    """klasa w której adapter trzyma dane przekazywane do ui"""
    def __init__(self, game):
        self.game = game
        self.message = ""
        self.hide_dealer_first = False
        self.cardsDealt=False
        self._active_hand_index = 0
        self._selected_bet = BET_STEP
        self._insurance_taken = False
        self._insurance_available = False
        self._insurance_bet = 0

    @property
    def player(self):
        """Pobiera z game objekt player. Pomija dealera."""
        for participant in self.game.participants:
            if participant.name.lower() != "dealer":
                return participant
        return None

    @property
    def dealer(self):
        """Pobiera z game obiekt player o nazwie dealer"""
        for participant in self.game.participants:
            if participant.name.lower() == "dealer":
                return participant
        return None

    @property
    def player_hands(self):
        """Pobiera dane z game"""
        player = self.player
        if player is None:
            return []
        return player.hands

    @property
    def dealer_hand(self):
        """Pobiera dane z game"""
        dealer = self.dealer
        if dealer is None:
            return None
        return dealer.hands[0]

    @property
    def active_hand_index(self):
        """Pobiera indeks aktywnej ręki z obiektu player"""
        self._active_hand_index = self.player.activeHandIndex
        return self._active_hand_index

    @property
    def active_hand(self):
        """ustawia aktywną(aktualnie rozgrywaną) ręke na podstawie indeksu"""
        hands = self.player_hands
        return hands[self._active_hand_index]

    @property
    def balance(self):
        """Pobiera aktualne saldo z obiektu player"""
        return self.player.balance
    @property
    def current_bet(self):
        """Zwraca zakład aktywnej ręki biorąc pod uwagę stan gry"""
        hand = self.active_hand
        if (self.round_active and hand is not None) or hand.wager!=0:
            return hand.wager
        elif not self.round_active:
            return self._selected_bet
        else:
            return 0

    @property
    def round_active(self):
        """Sprawdza czy aktualnie trwa runda. Zwraca bool"""
        return self.cardsDealt and not self._all_player_hands_finished()

    def get_hand_bet(self, hand):
        """Zwraca zakład podanej ręki biorąc pod uwagę stan gry"""
        if (self.round_active and hand is not None) or hand.wager!=0:
            return hand.wager
        return self._selected_bet

    def _all_player_hands_finished(self):
        """Sprawdza czy wszystkie ręce gracza są ukończone i zwraca bool"""
        hands = self.player_hands
        return all(hand.isFinished for hand in hands)

    def _advance_player_active_hand(self):
        """Przechodzi do następnej ręki jeśli aktualna jest ukończona"""
        if self.active_hand.isFinished and self.active_hand_index!=(len(self.player.hands)-1):
            self.player.activeHandIndex+=1

    def sync_message_from_game(self):
        """Pobiera message z game"""
        if hasattr(self.game, "message"):
            self.message = str(self.game.message)

    def _finish_round_if_needed(self):
        """sprawdza czy gracz skończył swoją turę, wykonuje turę krupiera i podsumowuje gre"""
        if self._all_player_hands_finished():
            self.game.dealerTurn()
            self.game.checkResult()
            self.game.showResults()
            self.sync_message_from_game()

    def insurance_available(self):
        """sprawdza czy możliwe jest insurance"""
        self.game.updatePossibilites(self.active_hand, self.player)
        return self.active_hand is not None and self.round_active and not self._insurance_taken and "insurance" in self.active_hand.possibilities
    def can_deal(self):
        """sprawdza czy można rozpocząć rundę i rozdać karty"""
        return self.player.balance>=self._selected_bet and not self.round_active

    def can_hit(self):
        """sprawdza czy gracz może dobrać"""
        hand = self.active_hand
        return hand is not None and not hand.isFinished and self.round_active

    def can_stand(self):
        """sprawdza czy gracz może wykonać stand"""
        hand = self.active_hand
        return hand is not None and not hand.isFinished and self.round_active

    def can_double(self):
        """sprawdza czy gracz może podwoić"""
        hand = self.active_hand
        self.game.updatePossibilites(self.active_hand, self.player)
        if hand is None or hand.isFinished or "double" not in(self.active_hand.possibilities) or not self.round_active:
            return False
        return True

    def can_split(self):
        """sprawdza czy gracz może splitować"""
        hand = self.active_hand
        self.game.updatePossibilites(self.active_hand,self.player)
        if hand is None or hand.isFinished or "split" not in(self.active_hand.possibilities) or not self.round_active:
            return False
        return True
    def cleanupIfNeeded(self):
        """sprawdza czy runda się skończyła, jeśli tak przygotowuje się do następnej rundy"""
        if self._all_player_hands_finished() and self.cardsDealt:
            self.player.activeHandIndex=0
            self.game.roundEnd()
            self.cardsDealt = False
    def increase_bet(self):
        """zwiększa wybieraną stawke i wykonuje cleanup jesli na stole zostaly karty po poprzedniej rundzie"""
        if self.game.participants[1].balance>= BET_STEP:
            self._selected_bet += BET_STEP
        self.cleanupIfNeeded()
    def decrease_bet(self):
        """zmniejsza wybieraną stawke i wykonuje cleanup jesli na stole zostaly karty po poprzedniej rundzie"""
        self._selected_bet = max(BET_STEP, self._selected_bet - BET_STEP)
        self.cleanupIfNeeded()

    def take_insurance(self):
        """wykupuje ubezpieczenie"""
        if not self.insurance_available:
            return
        self.game.insuranceCheck(self.player)
        self.sync_message_from_game()
        self._insurance_taken = True

    def decline_insurance(self):
        """odrzuca ubezpieczenie(ubezpieczenie zostaje również odrzucone jeśli gracz wykona jakąkolwiek czynność)"""
        if not self.insurance_available:
            return

        self.insurance_available = False
        self.message = "Bez insurance."
    def deal(self):
        """zatwierdza stawkę(w przypadku braku zmiany jest to stawka z poprzedniej gry),
         czyści stół jeśli jest to konieczne, rozpoczyna rundę i rozdaje karty"""
        self.cleanupIfNeeded()
        self.cardsDealt=True
        self.game.roundStart(self._selected_bet)
        self.message="rozpoczęto rundę"
        self.hide_dealer_first = True
        self._active_hand_index = 0
        self._finish_round_if_needed()


    def hit(self):
        """dobiera"""
        self.game.playerTurn(self.active_hand,self.player,"hit")
        self._advance_player_active_hand()
        self._finish_round_if_needed()
        self.sync_message_from_game()

    def stand(self):
        """wykonuje stand"""
        self.game.playerTurn( self.active_hand,self.player, "pass")
        self._advance_player_active_hand()
        self._finish_round_if_needed()
        self.sync_message_from_game()

    def double_down(self):
        """podwaja"""
        self.game.playerTurn(self.active_hand,self.player, "double")
        self._advance_player_active_hand()
        self._finish_round_if_needed()
        self.sync_message_from_game()

    def split(self):
        """splituje"""
        self.game.playerTurn(self.active_hand,self.player, "split")
        self._advance_player_active_hand()
        self.sync_message_from_game()
