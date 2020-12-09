# -*- coding: utf-8 -*-
"""
human VS AI models
Input your move in the format: 2,3

@author: Junxiao Song
"""

from __future__ import print_function
import pickle
# from AI.game import Board, Game
from AI.game import Board, Game
from AI.mcts_pure import MCTSPlayer as MCTS_Pure
from AI.mcts_alphaZero import MCTSPlayer
# from policy_value_net_numpy import PolicyValueNetNumpy
from AI.policy_value_net_numpy import PolicyValueNetNumpy
from AI.policy_value_net_pytorch import PolicyValueNet  # Pytorch
# from policy_value_net import PolicyValueNet  # Theano and Lasagne
# from policy_value_net_tensorflow import PolicyValueNet # Tensorflow
# from policy_value_net_keras import PolicyValueNet  # Keras
from AI.w_mct_alphaZero import W_MCTSPlayer


class Human(object):
    """
    human player
    """

    def __init__(self):
        self.player = None
        self.inputt=(0,0)
        self.canInput=False

    def set_player_ind(self, p):
        self.player = p


    def give_input(self,row,column):
        self.inputt=(row,column)
        self.canInput=True

    def get_action(self, board):
        try:

            # location = input("Your move: ")
            # if isinstance(location, str):  # for python3
            #     location = [int(n, 10) for n in location.split(",")]
            while not self.canInput:
                pass

            # canInput=False
            move = board.location_to_move(self.inputt)
            # move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.availables:
            print("invalid move")
            move = self.get_action(board)
        return move

    def __str__(self):
        return "Human {}".format(self.player)


def run(AI_or_notAI):
    n = 5
    width, height = 8, 8
    # model_file = 'best_policy_8_8_5.model'
    model_file = 'worst_policy.model'
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)

        # ############### human VS AI ###################
        # load the trained policy_value_net in either Theano/Lasagne, PyTorch or TensorFlow

        # best_policy = PolicyValueNet(width, height, model_file = model_file)
        # mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)

        # load the provided model (trained in Theano/Lasagne) into a MCTS player written in pure numpy
        try:
            policy_param = pickle.load(open(model_file, 'rb'))
        except:
            policy_param = pickle.load(open(model_file, 'rb'),
                                       encoding='bytes')  # To support python3
        best_policy = PolicyValueNetNumpy(width, height, policy_param)
        if(AI_or_notAI == 'AI'):
            mcts_player = MCTSPlayer(best_policy.policy_value_fn,
                                 c_puct=5,
                                 n_playout=400)  # set larger n_playout for better performance
        else:
            mcts_player = W_MCTSPlayer(best_policy.policy_value_fn,
                                       c_puct=5,
                                       n_playout=400)  # set larger n_playout for better performance

        # uncomment the following line to play with pure MCTS (it's much weaker even with a larger n_playout)
        # mcts_player = MCTS_Pure(c_puct=5, n_playout=1000)

        # human player, input your move in the format: 2,3
        human = Human()

        # set start_player=0 for human first
        game.start_play(human, mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')

if __name__ == '__main__':
    Ai_or_notAI = 'notAI'#选择智能还是智障
    run(Ai_or_notAI)
