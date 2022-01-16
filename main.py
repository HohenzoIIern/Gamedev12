import math

from Models.GameState import GameState, Mappings
from Models.AI import minimax

class Game:
    def __init__(self):
        self.state = GameState()
        ans = input('You started a new game, pick your color\n black or white\n')
        if ans == 'white':
            self.state.first_color = 'white'
        ans = input('choose your regime\n pvp or pve\n')
        if ans == 'pve':
            self.state.regime = 'pve'
        elif ans == 'bots':
            self.state.regime = 'bots'
        print("move by entering mx,y where x is the row number and y column number")
        print("place a wall by entering wx,y,h(v) where h(v) represents the wall direction")
        print("press x to quit")

    def play(self):
        while True:
            self.state.print_walls_number()
            print("\n")
            self.state.print_board()

            if self.check_end_state():
                break

            if self.state.regime == 'bots':
                self.ai_input()
            elif self.state.regime == 'pvp':
                self.player_input()
            else:
                if self.state.turn == 1:
                    self.player_input()
                else:
                    self.ai_input()

            if self.state.turn == 1:
                self.state.turn = 2
            else:
                self.state.turn = 1

    def check_end_state(self):
        if self.state.end_state():
            winner = self.state.turn
            print("The winner is P" + str(winner))
            return True
        else:
            return False

    def player_input(self):
        while True:
            value = input("Enter move: ")
            value.strip(' ')
            if value.upper() == 'X':
                exit(0)
            elif value.upper().startswith('M'):
                value = value.replace('M', '', 1)
                value = value.replace('m', '', 1)
                [x_string, y_string] = value.split(',')
                if x_string.upper() not in Mappings.MAP.keys() or y_string.upper() not in Mappings.MAP.keys():
                    print("Illegal move!")
                else:
                    x = Mappings.MAP[x_string.upper()]
                    y = Mappings.MAP[y_string.upper()]
                    available_moves = self.state.get_available_moves(False)
                    if (x, y) not in available_moves:
                        print("Illegal move!")
                    else:
                        self.state.move((x, y))
                        break
            elif value.upper().startswith("W"):
                value = value.replace('W', '', 1)
                value = value.replace('w', '', 1)
                [x_string, y_string, orientation] = value.split(',')
                if x_string.upper() not in Mappings.MAP.keys() or y_string.upper() not in Mappings.MAP.keys():
                    print('Illegal wall placement!')
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
                            print('Illegal wall placement!')
            else:
                print("Illegal command!")

    def ai_input(self):
        d = {}
        for child in self.state.get_all_child_states(True):
            value = minimax(child[0], 3, -math.inf, math.inf, True, False)
            d[value] = child
        if len(d.keys()) == 0:
            return None
        k = max(d)
        winner = d[k]
        action = winner[1]
        if action is not None:
            if len(action) == 2:
                self.state.move(action)
                print("AI has moved")
            else:
                self.state.place_wall(action)
                print("AI has placed a wall")
            return True
        else:
            print("AI has no moves left")
            return False


while True:
    game = Game()
    game.play()
    answer = input('do you want to start again?(write yes)\n')
    if answer != 'yes':
        break
