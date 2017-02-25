from common.base_bot  import BaseBot
from common.constants import *
import random
import math
import numpy as np


class ExampleBot(BaseBot):

    def __init__(self, host, user_id):
        super(ExampleBot, self).__init__(host, user_id)

        self.playerIndex = None
        self.generals = None
        self.cities = []
        self.map = []
        self.all_cities = set()

    def recieve_game_start(self, data, null):
        self.player_index = data['playerIndex']
        self.replay_id = data['replay_id']
        self.chat_room = data['chat_room']
        self.usernames = data['usernames']
        self.teams = data['teams']

    def recieve_chat_message(self, chat_room, data):
        print data

    def recieve_game_update(self, data, null):
        self.cities = self.patch(self.cities, data['cities_diff'])
        self.all_cities.update(self.cities)

        self.map = self.patch(self.map, data['map_diff'])
        self.generals = data['generals']

        width = self.map[0]
        height = self.map[1]
        size = width * height

        armies = self.map[2: size + 2]

        terrain = self.map[size + 2: size + 2 + size]

        print np.reshape(armies, (width, height))
        print np.reshape(terrain, (width, height))
        print self.all_cities

        while True:
            #Pick a random tile
            index = random.randint(0, size - 2)

            if terrain[index] == self.player_index:
                row = math.floor(index / width)
                col = index % width
                end_index = index

                rand = random.random()
                if rand < 0.25 and col > 0:
                    end_index -= 1
                elif rand < 0.5 and col < width - 1:
                    end_index += 1
                elif rand < 0.75 and row < height -1:
                    end_index += width
                elif row > 0:
                    end_index -= width
                else:
                    continue

                self.send_attack(index, end_index)
                break

def main():

    host = 'http://botws.generals.io'
    username = '[Bot] Example Bot'
    user_id = 'an_incredibly_deadbeef_bot'

    bot = ExampleBot(host, user_id)
    bot.send_set_username(username)

    custom_game_id = 'super_private_game'
    bot.send_join_private(custom_game_id)
    bot.send_set_force_start(custom_game_id, True)
    bot.wait()

if __name__ == '__main__':
    main()


