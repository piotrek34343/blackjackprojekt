import sys
import pygame
import game as g

from adapter import BlackjackAdapter
from ui import (
    WIDTH,
    HEIGHT,
    FPS,
    UI,
    create_menu_buttons,
    create_game_buttons,
    update_game_button_states,
    draw_menu,
    draw_game,
)


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Blackjack")
    clock = pygame.time.Clock()

    ui = UI()
    game = g.Game()
    backend = BlackjackAdapter(game)

    state = "menu"

    def start_game():
        nonlocal state
        state = "game"

    def back_to_menu():
        nonlocal state
        state = "menu"

    def quit_game():
        pygame.quit()
        sys.exit()

    menu_buttons = create_menu_buttons(ui, start_game, quit_game)
    game_buttons = create_game_buttons(ui, backend, back_to_menu)

    running = True
    while running:
        clock.tick(FPS)
        update_game_button_states(game_buttons, backend)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "menu":
                for button in menu_buttons:
                    button.handle_event(event)

            elif state == "game":
                for button in game_buttons.values():
                    button.handle_event(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        back_to_menu()
                    elif event.key == pygame.K_RETURN:
                        backend.deal()
                    elif event.key == pygame.K_h:
                        backend.hit()
                    elif event.key == pygame.K_s:
                        backend.stand()
                    elif event.key == pygame.K_x:
                        backend.double_down()
                    elif event.key == pygame.K_p:
                        backend.split()

        if state == "menu":
            draw_menu(screen, ui, menu_buttons)
        elif state == "game":
            draw_game(screen, ui, backend, game_buttons)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()