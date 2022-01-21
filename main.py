import math

from Models.GameState import GameState, Mappings
from Models.AI import minimax


class Game:
    def __init__(self):
        self.my_bot = True
        self.first = True
        self.second = True
        self.state = GameState()
        print("white")
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
            self.state.print_board()

            if self.check_end_state():
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
                self.my_bot = self.ai_input()
                self.state.turn = 2
            else:
                if not self.my_bot:
                    break
                else:
                    self.bot_testing(self.my_bot)
                self.state.turn = 1

    def check_end_state(self):
        if self.state.end_state():
            winner = self.state.turn
            print("The winner is P" + str(winner))
            return True
        else:
            return False

    def player_input(self, m):
        while True:
            bl = 1
            value = m
            value.strip(' ')
            if value.upper() == 'X':
                exit(0)
            elif value.upper().startswith('M'):
                value = value.replace('M', '', 1)
                value = value.replace('m', '', 1)
                [x_string, y_string] = value.split(',')
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
                value = value.replace('W', '', 1)
                value = value.replace('w', '', 1)
                [x_string, y_string, orientation] = value.split(',')
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
        if self.second:
            self.second = False
            return True
        d = {}
        for child in self.state.get_all_child_states(True):
            value = minimax(child[0], 3, -math.inf, math.inf, True, False)
            d[value] = child
        if len(d.keys()) == 0:
            return False
        k = max(d)
        winner = d[k]
        action = winner[1]
        if action is not None:
            print(action)
            if len(action) == 2:
                self.state.move(action)
                (x_string, y_string) = action
                x = ["1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9"]
                x_string = x[x_string]
                y = ["A", "S", "B", "T", "C", "U", "D", "V", "E", "W", "F", "X", "G", "Y", "H", "Z", "I"]
                y_string = y[y_string]
                # print("AI has moved")
                return 'move ' + y_string + x_string
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
                return 'wall ' + y_string + x_string + orient
        else:
            # print("AI has no moves left")
            return False

    def bot_testing(self, result):
        if not self.first:
            print(result)
            move = self.parser(input())
            self.player_input(move)
        else:
            self.first = False
        return True

    def parser(self, param):
        buff = param.split(" ")
        if buff[1] == "move" or buff[1] == "jump":
            x_string = list(buff[2])[0]
            y_string = list(buff[2])[1]
            x = {'A': 'A', 'B': 'C', 'C': 'E', 'D': 'G', 'E': 'I', 'F': 'K', 'G': 'M', 'H': 'O', 'I': 'Q'}
            x_string = x.get(str(x_string))
            y = {'1': 'A', '2': 'C', '3': 'E', '4': 'G', '5': 'I', '6': 'K', '7': 'M', '8': 'O', '9': 'Q'}
            print(str(y_string))
            y_string = y.get(str(y_string))
            print(y_string)
            return 'm' + str(y_string) + ',' + str(x_string)
        elif buff[1] == "wall":
            x_string = list(buff[2])[0]
            y_string = list(buff[2])[1]
            orient = list(buff[2])[2]
            print(y_string)
            x = {'S': 'b', 'T': 'd', 'U': 'f', 'V': 'h', 'W': 'j', 'X': 'l', 'Y': 'n', 'Z': 'p'}
            x_string = x.get(str(x_string))
            y = {'1': 'b', '2': 'd', '3': 'f', '4': 'h', '5': 'j', '6': 'l', '7': 'n', '8': 'p'}
            y_string = y.get(str(y_string))
            print('w' + str(y_string) + ',' + str(x_string) + ',' + str(orient))
            return 'w' + str(y_string) + ',' + str(x_string) + ',' + str(orient)
        else:
            return False


while True:
    game = Game()
    game.play()
    # answer = input('do you want to start again?(write yes)\n')
    # if answer != 'yes':
    #    break
