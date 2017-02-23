from socketIO_client import SocketIO, LoggingNamespace
import urllib
import logging

TILE_EMPTY = -1
TILE_MOUNTAIN = -2
TILE_FOG = -3
TILE_FOG_OBSTACLE = -4

logging.basicConfig(level=logging.INFO)

class BaseBot(object):

    def __init__(self, host, user_id):
        self.socket = SocketIO('http://botws.generals.io')
        self.bind_recieve_callbacks()

        self.user_id = user_id

        self.playerIndex = None
        self.generals = None
        self.cities = []
        self.map = []


        self.user_id = user_id

    def bind_recieve_callbacks(self):
        self.socket.on('connect', self.on_connect)
        self.socket.on('disconnect', self.on_disconnect)
        self.socket.on('reconnect', self.on_reconnect)
        self.socket.on('game_start', self.recieve_game_start)
        self.socket.on('game_lost', self.recieve_game_lost)
        self.socket.on('game_won', self.recieve_game_won)
        self.socket.on('chat_message', self.recieve_chat_message)
        self.socket.on('game_update', self.recieve_game_update)
        self.socket.on('stars', self.recieve_stars)
        self.socket.on('rank', self.recieve_rank)

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_reconnect(self):
        pass

    def recieve_game_start(self, data, null):
        pass

    def recieve_game_update(self, data, null):
        pass

    def recieve_game_lost(self, data, null):
        pass

    def recieve_game_won(self, data, null):
        pass

    def recieve_chat_message(self, chat_room, data):
        pass

    def recieve_stars(self, data, null):
        pass

    def recieve_rank(self, data, null):
        pass

    def send_set_username(self, username):
        #Enforce username bot requirement
        self.socket.emit('set_username', self.user_id, username)

    def send_play(self):
        self.socket.emit('play', self.user_id)

    def send_join_1v1(self):
        self.socket.emit('join_1v1', self.user_id)

    def send_join_private(self, custom_game_id):
        self.socket.emit('join_private', custom_game_id, self.user_id)
        logging.info('Join the same custom game at http://bot.generals.io/games/' +
                      urllib.quote(custom_game_id))

    def send_set_custom_team(self, custom_game_id, team):
        self.socket.emit('set_custom_team', custom_game_id, team)

    def send_join_team(self, team_id):
        self.socket.emit('join_team', team_id, self.user_id)
        logging.info('Join the same 2v2 team at http://bot.generals.io/teams/' +
                     urllib.quote(team_id))

    def send_leave_team(self, team_id):
        self.socket.emit('leave_team', team_id)

    def send_cancel(self):
        self.socket.emit('cancel')

    def send_set_force_start(self, queue_id, doForce):
        self.socket.emit('set_force_start', queue_id, doForce)

    def send_attack(self, start, end, is50=False):
        self.socket.emit('attack', start, end, is50)

    def send_clear_moves(self):
        self.socket.emit('clear_moves')

    def send_ping_tile(self, index):
        self.socket.emit('ping_tile', index)

    def send_chat_message(self, chat_room, text):
        self.socket.emit('chat_message', chat_room, text)

    def send_leave_game(self):
        self.socket.emit('leave_game')

    def send_stars_and_rank(self):
        self.socket.emit('stars_and_rank', self.user_id)

    def patch(self, old, diff):
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

    def wait(self):
        self.socket.wait()

