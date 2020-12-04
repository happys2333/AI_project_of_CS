import numpy as np
import copy


def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class TreeNode(object):
    """
    own value: Q
    prior probability: P
    visit-count-adjusted prior score u
    """

    def __init__(self, parent, prior_p):
        self._parent = parent  # type: TreeNode
        self._children = {} #type: TreeNode
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prior_p

    def expand(self, action_priors):
        """
        Expand tree by creating new children.
        :param action_priors: a list of tuples of actions and their prior probability
        """

        for action, prob in action_priors:
            if action not in self._children:
                self._children[action] = TreeNode(self, prob)

    def select(self, c_puct):
        """select action among children that gives maximum action value Q plus bonus u(p)
        Return: A tuple of (action, next_node)
        """
        return max(self._children.items(), key=lambda act_node: act_node[1].get_value(c_puct))

    def update(self, leaf_value):
        """
        update node valued from leaf evaluation
        leaf_value: the value of subtree evaluation from the current player's perspective
        """
        self._n_visits += 1;

        self._Q += 1.0 * (leaf_value - self._Q) / self._n_visits

    def update_recursive(self, leaf_value):
        """applied recursively for all ancestors"""

        if self._parent:
            self._parent.updata_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):

        self._u = (c_puct + self._P * np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q+self._u;

    def is_leaf(self):
        return self._children=={}

    def is_root(self):
        return self._parent is None


    class MCTS(object):

        def __init__(self,policy_value_fn,c_puct=5,n_playout=10000):

            self._root=TreeNode(None,1.0)
            self._policy=policy_value_fn
            self._c_puct=c_puct
            self._n_playout=n_playout


        def _playout(self,state):

            node=self._root
            while(True):
                if node.is_leaf():break

                action,node=node.select(self._c_puct)

                state.do_move(action)  # Change to our code

            action_probs,leaf_value=self._policy(state)

            end,winner=state.game_end()

            if not end:
                node.expand(action_probs)

            else:
                if winner==-1:
                    leaf_value=0.0;
                else:
                    leaf_value=(1.0 if winner==state.get_current_player() else -1.0)

            node.update_recursive(-leaf_value)

        def get_move_probs(self,state,temp=1e-3):

            for n in range(self._n_playout):
                state_copy=copy.deepcopy(state)
                self._playout(state_copy)

            act_visits=[(act,node._n_visits)
                        for act,node in self._root._children.items()]
            acts,visits=zip(*act_visits)
            act_probs=softmax(1.0/temp *np.log(np.array(visits) + 1e-10))

            return acts,act_probs

        def update_with_move(self,last_move):

            if last_move in self._root._children:
                self._root=self._root._children[last_move]
                self._root._parent=None
            else:
                self._root=TreeNode(None,1.0)

