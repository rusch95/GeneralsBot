from base_bot import BaseBot
import random
import math

TILE_EMPTY = -1
TILE_MOUNTAIN = -2
TILE_FOG = -3
TILE_FOG_OBSTACLE = -4

class ExampleBot(BaseBot):

    def __init__(self, host, user_id):
        super(ExampleBot, self).__init__(host, user_id)

        self.playerIndex = None
        self.generals = None
        self.cities = []
        self.map = []

    def recieve_game_start(self, data, other):
        print data
        self.player_index = data['playerIndex']
        self.replay_id = data['replay_id']
        self.chat_room = data['chat_room']
        self.usernames = data['usernames']
        self.teams = data['teams']

    def recieve_chat_message(self, data, other):
        print data
        print other

    def recieve_game_update(self, data, other):
        self.cities = self.patch(self.cities, data['cities_diff'])
        self.map = self.patch(self.map, data['map_diff'])
        self.generals = data['generals']

        width = self.map[0]
        height = self.map[1]
        size = width * height

        armies = self.map[2: size + 2]

        terrain = self.map[size + 2: size + 2 + size]

        print len(self.map)
        print data['map_diff']

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

                self.socket.emit('attack', index, end_index)
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


