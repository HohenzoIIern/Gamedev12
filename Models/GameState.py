import numpy as np
from copy import copy
from Models.findpath import astar


class Status:
    PLAYER_1 = 1
    PLAYER_2 = 2
    FREE_TILE = 3
    FREE_WALL = 4
    OCCUPIED_WALL = 5


class Mappings:
    MAP = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
           "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16}
    MAPR = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H", 8: "I", 9: "J",
            10: "K",
            11: "L", 12: "M", 13: "N", 14: "O", 15: "P", 16: "Q"}
    LET = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q"]


class GameState:
    def __init__(self):
        self.turn = 1
        self.regime = 'pvp'
        self.first_color = 'black'
        self.player_one_walls = 10
        self.player_two_walls = 10
        self.player_one_pos = np.array([16, 8])
        self.player_two_pos = np.array([0, 8])
        self.board = np.zeros(289, dtype=int)
        for i in range(17):
            for j in range(17):
                if i % 2 == 0 and j % 2 == 0:
                    self.board[i * 17 + j] = Status.FREE_TILE
                else:
                    self.board[i * 17 + j] = Status.FREE_WALL
        self.board[self.player_one_pos[0] * 17 + self.player_one_pos[1]] = Status.PLAYER_1
        self.board[self.player_two_pos[0] * 17 + self.player_two_pos[1]] = Status.PLAYER_2

    def print_walls_number(self):
        print('Player 1 walls: ' + str(self.player_one_walls))
        print('Player 2 walls: ' + str(self.player_two_walls))

    def is_tile_free(self, i, j):
        index = i * 17 + j
        return self.board[index] == Status.FREE_TILE

    def is_wall_free(self, i, j):
        return self.board[i * 17 + j] == Status.FREE_WALL

    def is_jump(self, move):
        if self.turn == 1:
            return abs(self.player_one_pos[0] - move[0]) == 4
        else:
            return abs(self.player_two_pos[0] - move[0]) == 4

    def is_diagonal(self, move):
        if self.turn == 1:
            return abs(self.player_one_pos[0] - move[0]) == 2 and abs(self.player_one_pos[1] - move[1]) == 2
        else:
            return abs(self.player_two_pos[0] - move[0]) == 2 and abs(self.player_two_pos[1] - move[1]) == 2

    def copy(self):
        game_state = copy(self)
        game_state.player_one_pos = copy(self.player_one_pos)
        game_state.player_two_pos = copy(self.player_two_pos)
        game_state.board = copy(self.board)
        return game_state

    def print_board(self):
        for i in range(0, len(Mappings.LET), 2):
            end_num = i + 1
            if i == 0:
                print("      {0:<2} ".format(Mappings.LET[i]),
                      end="\u001b[33m" + Mappings.LET[i + 1].lower() + "\u001b[0m")
            elif end_num <= 16:
                print("  {0:<2} ".format(Mappings.LET[i]),
                      end="\u001b[33m" + Mappings.LET[i + 1].lower() + "\u001b[0m")
            else:
                print("  {0:<3}".format(Mappings.LET[i]), end=" ")
        print()

        for i in range(17):
            if i % 2 == 0:
                print("{0:>2}  ".format(Mappings.LET[i]), end="")
            else:
                print("\u001b[33m" + "{0:>2}  ".format(Mappings.LET[i].lower()) + "\u001b[0m", end="")
            for j in range(17):
                index = i * 17 + j
                if self.board[index] == Status.FREE_TILE:
                    print("{0:4}".format(""), end="")
                elif self.board[index] == Status.PLAYER_1:
                    if self.first_color == 'black':
                        print("\u001b[30m" + "  B " + "\u001b[0m", end="")
                    else:
                        print("\u001b[0m" + "  W ", end="")
                elif self.board[index] == Status.PLAYER_2:
                    if self.first_color == 'black':
                        print("\u001b[0m" + "  W ", end="")
                    else:
                        print("\u001b[30m" + "  B " + "\u001b[0m", end="")
                else:
                    if i % 2 == 1 and j % 2 == 0:
                        if self.board[index] == Status.FREE_WALL:
                            line = ""
                            for k in range(5):
                                line += "-"
                            print(line, end="")
                        else:
                            line = ""
                            for k in range(5):
                                line += "\u2501"
                            print("\u001b[33m" + line + "\u001b[0m", end="")
                    elif i % 2 == 0 and j % 2 == 1:
                        if self.board[index] == Status.FREE_WALL:
                            print(" |", end="")
                        else:
                            print("\u001b[33m" + " \u2503" + "\u001b[0m", end="")
                    elif i % 2 == 1 and j % 2 == 1:
                        if self.board[index] == Status.FREE_WALL:
                            print("o", end="")
                        else:
                            print("\u001b[33m" + "O" + "\u001b[0m", end="")
            print()

    def check_wall_placement(self, starting_pos, orientation):

        if self.turn == 1 and self.player_one_walls == 0:
            print('Out of walls!')
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        elif self.turn == 2 and self.player_two_walls == 0:
            print('Out of walls!')
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        elif not self.is_wall_free(starting_pos[0], starting_pos[1]):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        elif orientation == 1:
            second_x = starting_pos[0]
            second_y = starting_pos[1] + 1
            third_x = starting_pos[0]
            third_y = starting_pos[1] - 1
        else:
            second_x = starting_pos[0] + 1
            second_y = starting_pos[1]
            third_x = starting_pos[0] - 1
            third_y = starting_pos[1]

        if not self.is_wall_free(second_x, second_y):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        if not self.is_wall_free(third_x, third_y):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])
        positions = np.array(
            [starting_pos[0], starting_pos[1], second_x, second_y, third_x, third_y])

        copy_state = copy(self)
        if self.turn == 1:
            res = 2
        else:
            res = 1
        if copy_state.is_wall_blocking(positions, res):
            return False, np.array([starting_pos[0], starting_pos[1], -1, -1, -1, -1])

        return True, positions

    def is_wall_blocking(self, positions, turn):
        self.place_wall(positions)
        self.turn = turn
        return not astar(self, True)

    def place_wall(self, positions):
        for i in range(0, 5, 2):
            self.board[positions[i] * 17 + positions[i + 1]] = Status.OCCUPIED_WALL
        if self.turn == 1:
            self.player_one_walls -= 1
        else:
            self.player_two_walls -= 1

    def move(self, new_pos):
        [x, y] = new_pos

        if self.turn == 1:
            old_x, old_y = self.player_one_pos
            self.player_one_pos[0] = x
            self.player_one_pos[1] = y
            self.board[x * 17 + y] = Status.PLAYER_1
        else:
            old_x, old_y = self.player_two_pos
            self.player_two_pos[0] = x
            self.player_two_pos[1] = y
            self.board[x * 17 + y] = Status.PLAYER_2

        self.board[old_x * 17 + old_y] = Status.FREE_TILE

    def end_state(self):
        return self.player_one_pos[0] == 0 or self.player_two_pos[0] == 16

    def is_goal_state(self):
        if self.turn == 1:
            return self.player_one_pos[0] == 0
        else:
            return self.player_two_pos[0] == 16

    def get_available_moves(self, include_state=True):
        result = []
        if self.top_pos(include_state) is not None:
            result.append(self.top_pos(include_state))
        if self.bottom_pos(include_state) is not None:
            result.append(self.bottom_pos(include_state))
        if self.right_pos(include_state) is not None:
            result.append(self.right_pos(include_state))
        if self.left_pos(include_state) is not None:
            result.append(self.left_pos(include_state))
        if self.jump_pos(include_state) is not None:
            result.append(self.jump_pos(include_state))
        if self.diag_r_pos(include_state) is not None:
            result.append(self.diag_r_pos(include_state))
        if self.diag_l_pos(include_state) is not None:
            result.append(self.diag_l_pos(include_state))
        return result

    def top_pos(self, include_state=True):
        if self.turn == 1:
            [i, j] = self.player_one_pos
            move = -2
            wall = -1
        else:
            i, j = self.player_two_pos
            move = 2
            wall = 1
        if 0 <= i + move <= 16 and 0 <= i + wall <= 16:
            if self.is_tile_free(i + move, j) and self.is_wall_free(i + wall, j):
                position = (i + move, j)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
        return None

    def bottom_pos(self, include_state=True):
        if self.turn == 1:
            i, j = self.player_one_pos
            move_x = 2
            wall_x = 1
        else:
            i, j = self.player_two_pos
            move_x = -2
            wall_x = -1

        if 0 <= i + move_x <= 16 and 0 <= i + wall_x <= 16:
            if self.is_wall_free(i + wall_x, j) and self.is_tile_free(i + move_x, j):
                position = (i + move_x, j)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
            return None

    def left_pos(self, include_state=True):
        if self.turn == 1:
            i, j = self.player_one_pos
            move_y = -2
            wall_y = -1
        else:
            i, j = self.player_two_pos
            move_y = 2
            wall_y = 1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            if self.is_tile_free(i, j + move_y) and self.is_wall_free(i, j + wall_y):
                position = (i, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
            return None

    def right_pos(self, include_state=True):
        if self.turn == 1:
            i, j = self.player_one_pos
            move_y = 2
            wall_y = 1
        else:
            i, j = self.player_two_pos
            move_y = -2
            wall_y = -1

        if 0 <= j + move_y <= 16 and 0 <= j + wall_y <= 16:
            if self.is_tile_free(i, j + move_y) and self.is_wall_free(i, j + wall_y):
                position = (i, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
            return None

    def jump_pos(self, include_state=True):
        if self.turn == 1:
            i, j = self.player_one_pos
            jump = -4
            move = -2
            wall1 = -1
            wall2 = -3
        else:
            i, j = self.player_two_pos
            jump = 4
            move = 2
            wall1 = 1
            wall2 = 3

        if 0 <= i + jump <= 16:
            if self.is_wall_free(i + wall1, j) and not self.is_tile_free(i + move, j) and \
                    self.is_wall_free(i + wall2, j):
                position = (i + jump, j)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
            return None

    def diag_l_pos(self, include_state=True):
        if self.turn == 1:
            i, j = self.player_one_pos
            move_x = -2
            move_y = -2
            wall_x = -1
            wall_y = -1
            occupied_x = -2
            occupied_wall = -3
        else:
            i, j = self.player_two_pos
            move_x = 2
            move_y = 2
            wall_x = 1
            wall_y = 1
            occupied_x = 2
            occupied_wall = 3

        if 0 <= i + move_x <= 16 and 0 <= j + move_y <= 16 and 0 <= i + wall_x <= 16 and 0 <= j + wall_y <= 16 and \
                0 <= i + occupied_x <= 16 and 0 <= i + occupied_wall <= 16:
            if self.is_wall_free(i + wall_x, j + wall_y) and not self.is_tile_free(i + occupied_x, j) and \
                    not self.is_wall_free(i + occupied_wall, j):
                position = (i + move_x, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
            return None

    def diag_r_pos(self, include_state=True):
        if self.turn == 1:
            i, j = self.player_one_pos
            move_x = -2
            move_y = 2
            wall_x = -1
            wall_y = 1
            occupied_x = -2
            occupied_wall = -3
        else:
            i, j = self.player_two_pos
            move_x = 2
            move_y = -2
            wall_x = 1
            wall_y = -1
            occupied_x = 2
            occupied_wall = 3

        if 0 <= i + move_x <= 16 and 0 <= j + move_y <= 16 and 0 <= i + wall_x <= 16 and 0 <= j + wall_y <= 16 and \
                0 <= i + occupied_x <= 16 and 0 <= i + occupied_wall <= 16:
            if self.is_wall_free(i + wall_x, j + wall_y) and not self.is_tile_free(i + occupied_x, j) and \
                    not self.is_wall_free(i + occupied_wall, j):
                position = (i + move_x, j + move_y)
                if include_state:
                    copy_state = self.copy()
                    copy_state.move(position)
                    if self.turn == 1:
                        copy_state.turn = 2
                    else:
                        copy_state.turn = 1
                    return copy_state, position
                else:
                    return position
            return None

    def get_child_states_with_moves(self):
        available_moves = self.get_available_moves(False)
        children = []
        for move in available_moves:
            child = self.copy()
            child.move(move)
            cost = 1000
            if self.is_jump(move):
                cost = 500
            elif self.is_diagonal(move):
                cost = 500
            if child.turn == 1:
                pos = child.player_one_pos
            else:
                pos = child.player_two_pos
            simplified_child_state = ((pos[0], pos[1]), (move[0], move[1]), cost)

            children.append((child, simplified_child_state))
        return children

    def get_all_child_states(self, ai_maximizer, include_state=True):

        children = []
        available_moves = self.get_available_moves(include_state)
        for move in available_moves:
            children.append(move)

        available_wall_placements = []
        if self.turn == 2 and not ai_maximizer:
            available_wall_placements = self.get_available_wall_placements_for_player_two(include_state)

        if self.turn == 1 and ai_maximizer:
            available_wall_placements = self.get_available_wall_placements_for_player_one(include_state)

        for wall_placement in available_wall_placements:
            children.append(wall_placement)

        return children

    def get_available_wall_placements_for_player_one(self, include_state=True):
        wall_placements = []
        if self.player_one_walls == 0:
            return wall_placements

        start_row = max(self.player_two_pos[0] - 2, 0)
        end_row = min(self.player_two_pos[0] + 3, 16)
        start_col = max(self.player_one_pos[1] - 3, 0)
        end_col = min(self.player_one_pos[1] + 3, 16)

        # horizontal
        end = end_col - 3
        if end_col == 16:
            end = end_col + 1
        start_1 = start_col + 1
        if start_col == 0:
            start_1 = start_col
            end = end_col - 2
        for i in range(start_row + 1, end_row, 2):
            for j in range(start_1, end, 2):
                if not self.is_wall_free(i, j):
                    continue
                second_y = j + 2
                third_y = j + 1
                if not start_col <= second_y <= end_col:
                    continue
                if not start_col <= third_y <= end_col:
                    continue
                if not self.is_wall_free(i, second_y):
                    continue
                if not self.is_wall_free(i, third_y):
                    continue
                positions = (i, j, i, second_y, i, third_y)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, self.turn == 2):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)
        # vertical
        start_2 = start_col
        if start_2 == 0:
            start_2 = start_col + 1
        for i in range(start_row, end_row - 3, 2):
            for j in range(start_2, end_col + 1, 2):
                if not self.is_wall_free(i, j):
                    continue
                second_x = i + 2
                third_x = i + 1
                if not start_row <= second_x <= end_row:
                    continue
                if not start_row <= third_x <= end_row:
                    continue
                if not self.is_wall_free(second_x, j):
                    continue
                if not self.is_wall_free(third_x, j):
                    continue
                positions = (i, j, second_x, j, third_x, j)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, self.turn == 2):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)

        return wall_placements

    def get_available_wall_placements_for_player_two(self, include_state=True):
        wall_placements = []
        if self.player_two_walls == 0:
            return wall_placements

        start_row = max(self.player_one_pos[0] - 3, 0)
        end_row = min(self.player_one_pos[0] + 2, 16)
        start_col = max(self.player_one_pos[1] - 3, 0)
        end_col = min(self.player_one_pos[1] + 3, 16)
        end = end_col - 3
        if end_col == 16:
            end = end_col + 1
        start_1 = start_col + 1
        if start_col == 0:
            start_1 = start_col
            end = end_col - 2
        for i in range(start_row, end_row, 2):
            for j in range(start_1, end, 2):
                if not self.is_wall_free(i, j):
                    continue
                second_y = j + 2
                third_y = j + 1
                if not start_col <= second_y <= end_col:
                    continue
                if not start_col <= third_y <= end_col:
                    continue
                if not self.is_wall_free(i, second_y):
                    continue
                if not self.is_wall_free(i, third_y):
                    continue
                positions = (i, j, i, second_y, i, third_y)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, self.turn == 2):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)

        start_2 = start_col
        if start_2 == 0 and start_row != 0:
            start_2 = start_col + 1
        if start_2 == 0 and start_row == 0:
            start_2 = start_col
        end_1 = end_col + 1
        if end_col == 16:
            end_1 = 15

        start_3 = start_row + 1
        if start_row == 0:
            start_3 = 0
        for i in range(start_3, end_row - 3, 2):
            for j in range(start_2, end_1, 2):
                if not self.is_wall_free(i, j):
                    continue
                second_x = i + 2
                third_x = i + 1
                if not start_row <= second_x <= end_row:
                    continue
                if not start_row <= third_x <= end_row:
                    continue
                if not self.is_wall_free(second_x, j):
                    continue
                if not self.is_wall_free(third_x, j):
                    continue
                positions = (i, j, second_x, j, third_x, j)
                if include_state:
                    copy_state = self.copy()
                    if not copy_state.is_wall_blocking(positions, self.turn == 2):
                        wall_placements.append((copy_state, positions))
                else:
                    wall_placements.append(positions)
        return wall_placements
