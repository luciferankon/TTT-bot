import numpy as np

import torch
from torch.nn import MSELoss

from board import play_random_move, Board, play_games
from neural import (TTTNet, NetContext, create_qneural_player,
                            get_q_values, play_training_games_x,
                            play_training_games_o)

policy_net = TTTNet()
target_net = TTTNet()
sgd = torch.optim.SGD(policy_net.parameters(), lr=0.1)
loss = MSELoss()
net_context = NetContext(policy_net, target_net, sgd, loss)

with torch.no_grad():
    board = Board(np.array([1, -1, -1, 0, 1, 1, 0, 0, -1]))
    q_values = get_q_values(board, net_context.target_net)
    print(f"Before training q values = {q_values}")

print("Training learning X vs random")
play_training_games_x(net_context=net_context, o_strategies=[play_random_move])

print("Training learning O vs random")
play_training_games_o(net_context=net_context, x_strategies=[play_random_move])


with torch.no_grad():
    play_qneural_move = create_qneural_player(net_context)

    print("Playing qneural vs random:")
    print("-----------------------------")
    play_games(2, play_qneural_move, play_random_move)
    print("\n")
    print("Playing random vs qneural:")
    print("----------------------------")
    play_games(2, play_random_move, play_qneural_move)
    print("\n")

    print("Playing qneural vs qneural:")
    print("----------------------------")
    play_games(2, play_qneural_move, play_qneural_move)

    board = Board(np.array([1, -1, -1, 0, 1, 1, 0, 0, -1]))
    q_values = get_q_values(board, net_context.target_net)
    print(f"After training q values = {q_values}")

