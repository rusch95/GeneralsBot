from socketIO_client import SocketIO, LoggingNamespace
import json
import random
import math

TILE_EMPTY = -1
TILE_MOUNTAIN = -2
TILE_FOG = -3
TILE_FOG_OBSTACLE = -4

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def patch(old, diff):
    out = []
    i = 0
    while i < len(diff):
        if diff[i]:
            out.extend(old[len(out):len(out) + diff[i]])
        i += 1
        if i < len(diff) and diff[i]:
            out.extend(diff[i + 1: i + 1 + diff[i]])
            i += diff[i]
        i += 1
    return out


class ExampleBot(object):

    def __init__(self, socket):
        self.socket = socket
        self.playerIndex = None
        self.generals = None
        self.cities = []
        self.map = []

#	def leave(self):
#        pass
#	    #self.socket.emit('leave_game')

    def on_game_start(self, data, other):
        print data
        self.player_index = data['playerIndex']
        self.replay_id = data['replay_id']
        self.chat_room = data['chat_room']
        self.usernames = data['usernames']
        self.teams = data['teams']

    def leave_game(self, data, other):
        print data
        print other
        self.socket.emit('leave_game')

    def chat_message(self, data, other):
        print data
        print other

    def game_update(self, data, other):
        self.cities = patch(self.cities, data['cities_diff'])
        self.map = patch(self.map, data['map_diff'])
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

    user_id = 'super_sexy_bot_id'
    username = '[Bot] Example Bot'

    socket = SocketIO('http://botws.generals.io')
    bot = ExampleBot(socket)
    print('Connecting to server')
    socket.on('connect', on_connect)
    socket.on('disconnect', on_disconnect)

    #Set the username for the bot
    #This should only ever be done once.
    socket.emit('set_username', user_id, username)

    custom_game_id = 'my_private_game'
    socket.emit('join_private', custom_game_id, user_id)
    socket.emit('set_force_start', custom_game_id, True)
    print 'Joined custome game at http://bot.generals.io/games/' + custom_game_id

    socket.on('game_start', bot.on_game_start)
    socket.on('game_lost', bot.leave_game)
    socket.on('game_won', bot.leave_game)
    socket.on('chat_message', bot.chat_message)
    socket.on('game_update', bot.game_update)

    socket.wait()

main()


