import math

from Models.GameState import GameState, Mappings
from Models.AI import minimax


class Game:
    def __init__(self):
        self.my_bot = True
        self.second = False
        self.state = GameState()
        res = input().split(' ').pop()
        if res == 'black':
            self.second = True
        # self.state.turn = 2
        # ans = input('You started a new game, pick your color\n black or white\n')
        # if ans == 'white':
        self.state.first_color = 'white'
        # ans = input('choose your regime\n pvp or pve\n')
        # if ans == 'pve':
        #    self.state.regime = 'pve'
        # elif ans == 'bots':
        #    self.state.regime = 'bots'
        # print("move by entering mx,y where x is the row number and y column number")
        # print("place a wall by entering wx,y,h(v) where h(v) represents the wall direction")
        # print("press x to quit")

    def play(self):
        while True:
            # self.state.print_walls_number()
            # print("\n")
            # self.state.print_board()
            if self.check_end_state():
                # print('asda')
                break

            # if self.state.regime == 'bots':
            #    self.ai_input()
            # elif self.state.regime == 'pvp':
            #    self.player_input()
            # else:
            #    if self.state.turn == 1:
            #        self.player_input()
            #    else:
            #        self.ai_input()

            if self.state.turn == 1:
                if self.second:
                    self.bot_testing(self.my_bot)
                else:
                    self.my_bot = self.ai_input()
                self.state.turn = 2
            else:
                if not self.my_bot:
                    break
                elif self.second:
                    self.my_bot = self.ai_input()
                else:
                    self.bot_testing(self.my_bot)
                self.state.turn = 1

    def check_end_state(self):
        if self.state.end_state():
            winner = self.state.turn
            # print("The winner is P" + str(winner))
            return True
        else:
            return False

    def player_input(self, m):
        while True:
            bl = 1
            value = m
            value.strip(' ')
            if value.upper() == 'exit':
                exit(0)
            elif value.upper().startswith('M'):
                buff = list(value.upper())
                x_string = buff[1]
                y_string = buff[3]
                if x_string.upper() not in Mappings.MAP.keys() or y_string.upper() not in Mappings.MAP.keys():
                    # print("Illegal move!")
                    bl = 2
                else:
                    x = Mappings.MAP[x_string.upper()]
                    y = Mappings.MAP[y_string.upper()]
                    available_moves = self.state.get_available_moves(False)
                    if (x, y) not in available_moves:
                        # print("Illegal move!")
                        bl = 2
                    else:
                        self.state.move((x, y))
                        break
            elif value.upper().startswith("W"):
                buff = list(value.upper())
                x_string = buff[1]
                y_string = buff[3]
                orientation = buff[5]
                if x_string.upper() not in Mappings.MAP.keys() or y_string.upper() not in Mappings.MAP.keys():
                    # print('Illegal wall placement!')
                    bl = 1
                else:
                    if orientation.upper() in ['V', 'H']:
                        if orientation.upper() == 'V':
                            direction = 0
                        else:
                            direction = 1

                        x = Mappings.MAP[x_string.upper()]
                        y = Mappings.MAP[y_string.upper()]
                        validation, coord = self.state.check_wall_placement((x, y), direction)
                        if validation:
                            self.state.place_wall(coord)
                            break
                        else:
                            bl = 1
                            # print('Illegal wall placement!')
            else:
                # print("Illegal command!")
                bl = 1

    def ai_input(self):
        d = {}
        for child in self.state.get_all_child_states(True):
            if self.state.turn == 1:
                value = minimax(child[0], 3, -300, 300, True, True)
            else:
                value = minimax(child[0], 3, -300, 300, True, False)
            d[value] = child
        if len(d.keys()) == 0:
            return False
        k = max(d)
        winner = d[k]
        action = winner[1]
        if action is not None:
            if len(action) == 2:
                old = self.state.move(action)
                (x_string, y_string) = action
                if (abs(x_string - old[0]) == 2 or abs(y_string - old[1]) == 2) and abs(x_string - old[0]) != abs(y_string - old[1]):
                    mod = 'move '
                else:
                    mod = 'jump '
                x = ["1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9"]
                x_string = x[x_string]
                y = ["A", "S", "B", "T", "C", "U", "D", "V", "E", "W", "F", "X", "G", "Y", "H", "Z", "I"]
                y_string = y[y_string]
                # print("AI has moved")
                print(mod + y_string + x_string)
                return mod + y_string + x_string
            else:
                self.state.place_wall(action)
                orient = ''
                if action[0] == action[2]:
                    orient = 'h'
                else:
                    orient = 'v'
                [x_string, y_string] = [action[0], action[1]]
                x = ["1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9"]
                x_string = x[x_string]
                y = ["A", "S", "B", "T", "C", "U", "D", "V", "E", "W", "F", "X", "G", "Y", "H", "Z", "I"]
                y_string = y[y_string]
                # print("AI has placed a wall")
                print('wall ' + y_string + x_string + orient)
                return 'wall ' + y_string + x_string + orient
        else:
            # print("AI has no moves left")
            return False

    def bot_testing(self, result):
        res = input()
        move = self.parser(res)
        self.player_input(move)
        return True

    def parser(self, param):
        buff = param.split(" ")
        if buff[0] == "move" or buff[0] == "jump":
            x_string = list(buff[1])[0]
            y_string = list(buff[1])[1]
            x = {'A': 'A', 'B': 'C', 'C': 'E', 'D': 'G', 'E': 'I', 'F': 'K', 'G': 'M', 'H': 'O', 'I': 'Q'}
            x_string = x.get(str(x_string))
            y = {'1': 'A', '2': 'C', '3': 'E', '4': 'G', '5': 'I', '6': 'K', '7': 'M', '8': 'O', '9': 'Q'}
            y_string = y.get(str(y_string))
            return 'm' + str(y_string) + ',' + str(x_string)
        elif buff[0] == "wall":
            x_string = list(buff[1])[0]
            y_string = list(buff[1])[1]
            orient = list(buff[1])[2]
            x = {'S': 'b', 'T': 'd', 'U': 'f', 'V': 'h', 'W': 'j', 'X': 'l', 'Y': 'n', 'Z': 'p'}
            x_string = x.get(str(x_string))
            y = {'1': 'b', '2': 'd', '3': 'f', '4': 'h', '5': 'j', '6': 'l', '7': 'n', '8': 'p'}
            y_string = y.get(str(y_string))
            return 'w' + str(y_string) + ',' + str(x_string) + ',' + str(orient)
        else:
            return False


while True:
    game = Game()
    game.play()
    # answer = input('do you want to start again?(write yes)\n')
    # if answer != 'yes':
    break
