import pygame

WIDTH = 1280
HEIGHT = 720
FPS = 60


class UI:
    def __init__(self):
        self.TABLE_GREEN = (18, 102, 58)
        self.TABLE_DARK = (12, 74, 42)

        self.PANEL = (22, 55, 35)
        self.PANEL_LIGHT = (30, 68, 45)

        self.WHITE = (245, 245, 245)
        self.BLACK = (20, 20, 20)
        self.RED = (190, 50, 50)
        self.GOLD = (235, 200, 90)
        self.BLUE = (60, 110, 190)
        self.BLUE_HOVER = (85, 135, 220)
        self.ORANGE = (210, 130, 45)
        self.ORANGE_HOVER = (230, 150, 65)
        self.GRAY = (110, 110, 110)

        self.TITLE_FONT = pygame.font.SysFont("arial", 48, bold=True)
        self.BIG_FONT = pygame.font.SysFont("arial", 38, bold=True)
        self.FONT = pygame.font.SysFont("arial", 28)
        self.SMALL_FONT = pygame.font.SysFont("arial", 20)
        self.CARD_FONT = pygame.font.SysFont("arial", 30, bold=True)


def draw_text(surface, text, font, color, pos, center=False):
    img = font.render(str(text), True, color)
    rect = img.get_rect(center=pos) if center else img.get_rect(topleft=pos)
    surface.blit(img, rect)


def draw_wrapped_text(surface, text, font, color, rect, line_height=None):
    words = str(text).split()
    if not words:
        return

    if line_height is None:
        line_height = font.get_linesize()

    x, y, w, h = rect
    line = ""
    current_y = y

    for word in words:
        test_line = word if not line else f"{line} {word}"
        test_width = font.size(test_line)[0]

        if test_width <= w:
            line = test_line
        else:
            draw_text(surface, line, font, color, (x, current_y))
            current_y += line_height
            if current_y > y + h - line_height:
                return
            line = word

    if line and current_y <= y + h - line_height:
        draw_text(surface, line, font, color, (x, current_y))


class Button:
    def __init__(
        self,
        text,
        rect,
        callback,
        base_color,
        hover_color,
        text_color=(255, 255, 255),
        border_color=(255, 255, 255),
        disabled_color=(110, 110, 110),
    ):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.callback = callback
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.disabled_color = disabled_color
        self.enabled = True
        self.hovered = False

    def handle_event(self, event):
        if not self.enabled:
            return

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.callback()

    def draw(self, surface, ui):
        color = self.disabled_color if not self.enabled else (self.hover_color if self.hovered else self.base_color)
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=12)
        draw_text(surface, self.text, ui.FONT, self.text_color, self.rect.center, center=True)


def rank_to_label(rank: int) -> str:
    if rank == 1:
        return "A"
    if rank == 11:
        return "J"
    if rank == 12:
        return "Q"
    if rank == 0:
        return "K"
    return str(rank)


def suit_from_card_id(card_id: int) -> str:
    suits = ["♠", "♥", "♦", "♣"]
    idx = (card_id - 1) // 13
    idx = max(0, min(idx, 3))
    return suits[idx]


def card_to_label(card) -> str:
    return f"{rank_to_label(card.rank)}{suit_from_card_id(card.id)}"


def is_red_suit(card) -> bool:
    return suit_from_card_id(card.id) in ("♥", "♦")


def draw_card(surface, ui, x, y, card=None, hidden=False):
    rect = pygame.Rect(x, y, 92, 132)

    if hidden:
        pygame.draw.rect(surface, (35, 55, 120), rect, border_radius=12)
        pygame.draw.rect(surface, ui.WHITE, rect, 2, border_radius=12)

        for i in range(6):
            pygame.draw.line(surface, (80, 110, 180), (x + 10, y + 15 + i * 18), (x + 82, y + 15 + i * 18), 2)

        draw_text(surface, "?", ui.BIG_FONT, ui.WHITE, rect.center, center=True)
        return

    pygame.draw.rect(surface, ui.WHITE, rect, border_radius=12)
    pygame.draw.rect(surface, ui.BLACK, rect, 2, border_radius=12)

    if card is None:
        return

    label = card_to_label(card)
    color = ui.RED if is_red_suit(card) else ui.BLACK

    draw_text(surface, label, ui.CARD_FONT, color, (x + 10, y + 8))
    draw_text(surface, label, ui.CARD_FONT, color, (x + 64, y + 106), center=True)


def draw_hand(surface, ui, cards, start_x, y, hide_first=False):
    if not cards:
        draw_text(surface, "(brak kart)", ui.SMALL_FONT, ui.WHITE, (start_x, y + 40))
        return

    spacing = 105
    for i, card in enumerate(cards):
        hidden = hide_first and i == 0
        draw_card(surface, ui, start_x + i * spacing, y, card=card, hidden=hidden)


def draw_table_background(surface, ui):
    surface.fill(ui.TABLE_GREEN)
    pygame.draw.ellipse(surface, ui.TABLE_DARK, (70, 110, WIDTH - 140, HEIGHT - 220), 6)


def create_menu_buttons(ui, start_callback, quit_callback):
    return [
        Button(
            "Start",
            (WIDTH // 2 - 130, 370, 260, 60),
            start_callback,
            ui.BLUE,
            ui.BLUE_HOVER,
        ),
        Button(
            "Wyjście",
            (WIDTH // 2 - 130, 450, 260, 60),
            quit_callback,
            ui.RED,
            (215, 80, 80),
        ),
    ]


def create_game_buttons(ui, adapter, back_to_menu):
    return {
        "minus": Button("- Bet", (120, 620, 110, 48), adapter.decrease_bet, ui.BLUE, ui.BLUE_HOVER),
        "plus": Button("+ Bet", (245, 620, 110, 48), adapter.increase_bet, ui.BLUE, ui.BLUE_HOVER),
        "deal": Button("Deal", (370, 620, 120, 48), adapter.deal, ui.ORANGE, ui.ORANGE_HOVER),
        "hit": Button("Hit", (505, 620, 110, 48), adapter.hit, ui.BLUE, ui.BLUE_HOVER),
        "stand": Button("Stand", (630, 620, 120, 48), adapter.stand, ui.BLUE, ui.BLUE_HOVER),
        "double": Button("Double", (765, 620, 140, 48), adapter.double_down, ui.BLUE, ui.BLUE_HOVER),
        "split": Button("Split", (920, 620, 120, 48), adapter.split, ui.BLUE, ui.BLUE_HOVER),
        "menu": Button("Menu", (1055, 620, 120, 48), back_to_menu, ui.RED, (215, 80, 80)),
        "insurance": Button("Insurance", (370, 568, 180, 42),adapter.take_insurance,(140, 90, 180), (170, 120, 210),),
        "no_insurance": Button("No Insurance", (565, 568, 180, 42),adapter.decline_insurance,(140, 90, 180), (170, 120, 210),),
    }


def update_game_button_states(buttons, adapter):
    buttons["minus"].enabled = not adapter.round_active
    buttons["plus"].enabled = not adapter.round_active
    buttons["deal"].enabled = adapter.can_deal()
    buttons["hit"].enabled = adapter.can_hit()
    buttons["stand"].enabled = adapter.can_stand()
    buttons["double"].enabled = adapter.can_double()
    buttons["split"].enabled = adapter.can_split()
    buttons["menu"].enabled = True
    buttons["insurance"].enabled = adapter.insurance_available()
    buttons["no_insurance"].enabled = adapter.insurance_available()


def draw_menu(surface, ui, buttons):
    draw_table_background(surface, ui)

    draw_text(surface, "BLACKJACK", ui.TITLE_FONT, ui.GOLD, (WIDTH // 2, 170), center=True)
    draw_text(surface, "Projekt", ui.FONT, ui.WHITE, (WIDTH // 2, 225), center=True)

    info_rect = pygame.Rect(WIDTH // 2 - 260, 265, 520, 70)
    pygame.draw.rect(surface, ui.PANEL, info_rect, border_radius=16)
    pygame.draw.rect(surface, ui.WHITE, info_rect, 2, border_radius=16)
    draw_text(surface, "Start uruchamia stół. Wyjście zamyka program.", ui.SMALL_FONT, ui.WHITE, info_rect.center, center=True)

    for button in buttons:
        button.draw(surface, ui)


def draw_player_hands(surface, ui, adapter, y=410):
    hands = adapter.player_hands

    if not hands:
        draw_text(surface, "(brak rąk gracza)", ui.SMALL_FONT, ui.WHITE, (90, y + 40))
        return

    panel_width = 280
    panel_height = 250
    gap = 20

    total_width = len(hands) * panel_width + (len(hands) - 1) * gap
    start_x = max(40, (WIDTH - total_width) // 2)

    for idx, hand in enumerate(hands):
        x = start_x + idx * (panel_width + gap)

        is_active = adapter.is_hand_active(hand)
        bg_color = (40, 90, 60) if is_active else ui.PANEL
        border_color = ui.GOLD if is_active else ui.WHITE

        panel_rect = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(surface, bg_color, panel_rect, border_radius=16)
        pygame.draw.rect(surface, border_color, panel_rect, 3 if is_active else 2, border_radius=16)

        draw_text(surface, f"Hand {idx + 1}", ui.FONT, ui.WHITE, (x + 14, y + 12))
        draw_text(surface, f"Bet: ${adapter.get_hand_bet(hand)}", ui.SMALL_FONT, ui.WHITE, (x + 14, y + 48))
        draw_text(surface, f"Suma: {adapter.get_hand_total(hand)}", ui.SMALL_FONT, ui.WHITE, (x + 14, y + 74))

        status_text = adapter.get_hand_status_text(hand)
        if status_text:
            draw_text(surface, status_text, ui.SMALL_FONT, ui.GOLD, (x + 14, y + 98))

        cards = adapter.get_hand_cards(hand)
        card_spacing = 46 if len(cards) <= 4 else 36
        cards_start_x = x + 12
        cards_y = y + 110

        for i, card in enumerate(cards):
            draw_card(surface, ui, cards_start_x + i * card_spacing, cards_y, card=card, hidden=False)


def draw_game(surface, ui, adapter, buttons):
    draw_table_background(surface, ui)

    top_rect = pygame.Rect(20, 20, WIDTH - 40, 88)
    pygame.draw.rect(surface, ui.PANEL, top_rect, border_radius=16)
    pygame.draw.rect(surface, ui.WHITE, top_rect, 2, border_radius=16)

    draw_text(surface, "BLACKJACK", ui.BIG_FONT, ui.GOLD, (40, 36))

    hand_count = len(adapter.player_hands)
    if hand_count > 0:
        active_label = f"{adapter.active_hand_index + 1}/{hand_count}"
    else:
        active_label = "-"

    draw_text(surface, f"Saldo: ${adapter.balance}", ui.FONT, ui.WHITE, (760, 34))
    draw_text(surface, f"Aktywna ręka: {active_label}", ui.SMALL_FONT, ui.WHITE, (760, 68))
    draw_text(surface, f"Bet: ${adapter.current_bet}", ui.SMALL_FONT, ui.WHITE, (1010, 68))

    draw_text(surface, adapter.dealer_name, ui.FONT, ui.WHITE, (90, 135))
    dealer_total = "?" if adapter.hide_dealer_first and adapter.round_active else adapter.get_hand_total(adapter.dealer_hand)
    draw_text(surface, f"Suma: {dealer_total}", ui.SMALL_FONT, ui.WHITE, (90, 170))
    draw_hand(
        surface,
        ui,
        adapter.dealer_cards,
        90,
        195,
        hide_first=adapter.hide_dealer_first and adapter.round_active,
    )

    draw_text(surface, adapter.player_name, ui.FONT, ui.WHITE, (90, 385))
    draw_player_hands(surface, ui, adapter, y=350)

    status_rect = pygame.Rect(860, 170, 320, 135)
    pygame.draw.rect(surface, ui.PANEL_LIGHT, status_rect, border_radius=16)
    pygame.draw.rect(surface, ui.WHITE, status_rect, 2, border_radius=16)

    draw_text(surface, "Status", ui.FONT, ui.GOLD, (880, 185))
    draw_wrapped_text(
        surface,
        adapter.message,
        ui.FONT,
        ui.WHITE,
        (880, 225, 280, 70),
        line_height=30,
    )
    # insurance panel

    ins_rect = pygame.Rect(340, 540, 440, 100)
    pygame.draw.rect(surface, ui.PANEL_LIGHT, ins_rect, border_radius=12)
    pygame.draw.rect(surface, ui.GOLD, ins_rect, 2, border_radius=12)
    if adapter.insurance_available():
        draw_text(
            surface, "Dealer pokazuje Asa — Insurance?",
            ui.SMALL_FONT, ui.GOLD, (ins_rect.centerx, ins_rect.y + 12), center=True,)
        buttons["insurance"].draw(surface, ui)
        buttons["no_insurance"].draw(surface, ui)
    bottom_rect = pygame.Rect(20, 595, WIDTH - 40, 100)
    pygame.draw.rect(surface, ui.PANEL, bottom_rect, border_radius=16)
    pygame.draw.rect(surface, ui.WHITE, bottom_rect, 2, border_radius=16)

    for button in buttons.values():
        button.draw(surface, ui)

    draw_text(
        surface,
        "ENTER = Deal | H = Hit | S = Stand | X = Double | P = Split | ESC = Menu",
        ui.SMALL_FONT,
        ui.WHITE,
        (25, 700),
    )