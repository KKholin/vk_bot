import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

import secret_constants
from cites import Lobby
from cities_list import cities_list

vk_session = vk_api.VkApi(token=secret_constants.TOKEN)
longpoll = VkLongPoll(vk_session)


def is_message(event):
    return event.type == VkEventType.MESSAGE_NEW and event.to_me


def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id,
                                        'message': message,
                                        'random_id': 0})


def is_start_game(event):
    start_commands = ['game', 'Города', 'Игра', 'игра',
                      'Играть', 'Играть', 'города Играть', 'Играть в города', 'играть в города']
    return event.text.lower() in start_commands


def main():
    menuBot = ['commands:''\nКак дела?', '\nВ чём сила?', '\nИграть в города']
    convertmenuBot = ' '.join(map(str, menuBot))
    players_queue = None
    lobbies = []
    users_in_game = []

    dela = ['дела по БОТовски', 'Питоновские , а у тебя?', 'print(normalno)',
            'нормас(пивас)', 'дела словно dead inside... ', 'Нормально)']

    VoprosDela = ['Как дела', 'Как дела?', 'как дела', 'Чо каво?', 'как дела?', 'd', 'как дела клатчер',
                  'Как дела клатчер?']

    for event in longpoll.listen():
        if is_message(event):
            if event.text == 'привет':
                send_message(event.user_id, 'привет! Для функций бота напиши /menu')

            elif event.text == '/menu':
                send_message(event.user_id, convertmenuBot)

            elif event.text == 'в чём сила?':
                send_message(event.user_id, 'В правде ,кто прав тот и сильней.')

            elif event.text in VoprosDela:
                OtvetDela = random.choice(dela)
                send_message(event.user_id, OtvetDela)


            elif is_start_game(event):
                if players_queue is None:
                    send_message(event.user_id, 'Ищем соперника!')
                    players_queue = event.user_id
                elif event.user_id != players_queue:
                    user1 = players_queue
                    user2 = event.user_id
                    lobbies.append(Lobby(user1, user2))
                    users_in_game.extend((user1, user2))
                    players_queue = None
                    send_message(user1, 'Игра началась!')
                    send_message(user2, 'Игра началась!')
                    send_message(lobbies[-1].get_active_player(), 'Вы ходите первым.Назовите город на любую букву!')
                elif event.user_id in users_in_game:
                    city = event.text.lower()
                    lobby = find_lobby(lobbies, event.user_id)
                    if city not in cities_list:
                        send_message(event.user_id, 'Такого города нет, либо была опечатка. \n'
                                                    'Ты проиграл. ')
                        send_message(lobby.get_inactive_player_id(), 'вы победили')
                        users_in_game.remove(event.user_id)
                        users_in_game.remove(lobby.get_inactive_player_id())
                        lobbies.remove(lobby)
                        continue
                    if not lobby.is_correct_letter(city[0].lower):
                        send_message(event.user_id, 'Не та буква, географию рано, купи букварь!')
                        continue
                    if lobby.get_activez_player_id() != event.user_id:
                        send_message(event.user_id, 'сейчас не твой ход!')
                        continue

                    lobby.change_last_letter(city)
                    lobby.used_cities.append(city)
                    lobby.change_current_turn()
                    send_message(lobby.get_active_player(), f'вам на букву: {lobby.last_letter}.\n'
                                                            f'игрок назвал город:{city}')


def find_lobby(lobbies, user_id):
    for lobby in lobbies:
        if user_id in lobby.user_ids:
            return lobby


main()
