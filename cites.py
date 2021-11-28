import random


class Lobby:
    def __init__(self, user1, user2):
        self.user_ids = [user1, user2]
        self.current_turn = random.randint(0, 1)
        self.used_cities = []
        self.last_letter = None


    def get_active_player(self):  # проверка что первая буква города равна последней букве прошлого города
        return self.user_ids[self.current_turn]

    def is_correct_letter(self, letter):
        return self.last_letter is None or self.last_letter == letter


    def is_unused_city(self, city):
        NocorrectName = ['ы', 'ь', 'ё']
        for letter in city[::-1]:
            if letter not in NocorrectName:
                break

    def change_current_turn(self):
        self.current_turn = 1- self.current_turn
    def get_inactive_player_id(self):
        return self.user_ids[1 - self.current_turn]