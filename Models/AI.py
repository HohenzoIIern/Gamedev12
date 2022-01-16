import math
from Models.GameState import GameState
from Models.findpath import astar

def state_evaluation(game_state: GameState, player_one_maximizer):
    player_one_distance = game_state.player_one_pos[0] // 2
    player_two_distance = (16 - game_state.player_two_pos[0]) // 2
    result = 0
    if player_one_maximizer:

        opponent_path_len, player_path_len = player_two_distance, player_one_distance
        if game_state.player_one_walls != 10 and game_state.player_two_walls != 10:
            previous = game_state.player_one
            game_state.player_one = True
            player_path_len = astar(game_state, False)
            game_state.player_one = previous

        result += opponent_path_len
        result -= player_one_distance
        num = 100
        if player_path_len != 0:
            num = player_path_len
        result += round(100 / num, 2)

        num_1 = 50
        if player_two_distance != 0:
            num_1 = player_two_distance
        result -= round(50 / num_1, 2)

        result += (game_state.player_one_walls - game_state.player_two_walls)
        if game_state.player_one_pos[0] == 0:
            result += 100
        if player_path_len == 0 and game_state.player_one_pos[0] != 0:
            result -= 500
        return result
    else:
        opponent_path_len, player_path_len = player_one_distance, player_two_distance
        if game_state.player_one_walls != 10 and game_state.player_two_walls != 10:
            previous = game_state.turn
            game_state.turn = 2
            player_path_len = astar(game_state, False)
            game_state.turn = previous
        result += opponent_path_len
        result -= player_two_distance
        num = 100
        if player_path_len != 0:
            num = player_path_len
        result += round(100 / num, 2)

        num_1 = 50
        if player_one_distance != 0:
            num_1 = player_one_distance
        result -= round(50 / num_1, 2)

        result += (game_state.player_two_walls - game_state.player_one_walls)
        if game_state.player_two_pos[0] == 16:
            result += 100
        if player_path_len == 0 and game_state.player_two_pos[0] != 16:
            result -= 500
        return result


def minimax(game_state: GameState, depth, alpha, beta, maximizing_player, player_one_minimax):
    if depth == 0:
        return state_evaluation(game_state, player_one_minimax)
    if maximizing_player:
        max_eval = -math.inf
        for child in game_state.get_all_child_states(player_one_minimax):
            ev = minimax(child[0], depth - 1, alpha, beta, False, player_one_minimax)
            max_eval = max(max_eval, ev)
            alpha = max(alpha, ev)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for child in game_state.get_all_child_states(player_one_minimax):
            ev = minimax(child[0], depth - 1, alpha, beta, True, player_one_minimax)
            min_eval = min(min_eval, ev)
            beta = min(beta, ev)
            if beta <= alpha:
                break
        return min_eval
