from enum import StrEnum


class GameStates(StrEnum):
    START_MENU = "start_menu"
    KEYBOARD_MENU = "keyboard_menu"
    GAME_OVER = "game_over"
    WIN = "win_game_over"
    GAME = "game"
