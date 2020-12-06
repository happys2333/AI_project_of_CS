import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np

# set the learning rate to the given value
def set_learning_rat(optimizer, lr):
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr

# policy value net module
class Net(nn.Module):
    def __init__(self, board_width, board_height):
        super(Net, self).__init__()

        self.board_width = board_width
        self.board_height = board_height
        #common layers
        self.conv1 = nn.Conv2d(4,32,kernel_size=3,padding=1)
        self.conv2 = nn.Conv2d(32,64,kernel_size=3,padding=1)
        self.conv3 = nn.Conv2d(64,128,kernel_size=3,padding=1)
        #action policy layers
        self.act_conv1 = nn.Conv2d(128,4,kernel_size=1)
        self.act_fc1 = nn.Linear(4*board_width*board_height, board_width*board_height)
        #state value layers
        self.val_conv1 = nn.Conv2d(128,2,kernel_size=1)
        self.val_fc1 = nn.Linear(2*board_height*board_width,64)
        self.val_fc2 = nn.Linear(64,1)

    def forward(self, state_input):
        #common layers
        x = F.relu(self.conv1(state_input))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        #action policy layers
        x_act = F.relu(self.act_fc1(x))
        x_act = x_act.view(-1, 4*self.board_width*self.board_height)
        x_act = F.log_softmax(self.act_fc1(x_act))
        #state value layers
        x_val = F.relu(self.val_fc1(x))
        x_val = x_val.view(-1,2*self.board_height*self.board_width)
        x_val = F.relu(self.val_fc1(x_val))
        x_val = F.tanh(self.val_fc2(x_val))
        return x_act,x_val

# policy value net
class PolicyValueNet():
    def __init__(self, board_width, borad_height, model_file = None, use_gpu = False):
        self.use_gpu = use_gpu
        self.borad_width = board_width
        self.borad_height = borad_height
        self.l2_const = 1e-4 #coefficient of penalty
        #the policy value net module
        if self.use_gpu:
            self.policy_value_net = Net(board_width,borad_height).cuda()
        else:
            self.policy_value_net = Net(board_width,borad_height)
        self.optimizier = optim.Adam(self.policy_value_net.parameters(), weight_decay=self.l2_const)

        if model_file:
            net_params = torch.load(model_file)
            self.policy_value_net.load_state_dict(net_params)

    #input: a batch of states
    #output: a batch of action probabilities and state values
    def policy_value(self, state_batch):
        if self.use_gpu:
            state_batch = Variable(torch.FloatTensor(state_batch).cuda())
            log_act_probs, value = self.policy_value_net(state_batch)
            act_probs = np.exp(log_act_probs.data.cup().numpy())
            return act_probs, value.data.numpy()
        else:
            state_batch = Variable(torch.FloatTensor(state_batch))
            log_act_probs, value = self.policy_value_net(state_batch)
            act_probs = np.exp(log_act_probs.data.cup().numpy())
            return act_probs, value.data.numpy()
    #input: a board
    #output: a list of (action, probability) tuples for each available action and the score of the board state
    def policy_value_fn(self,board):
        legal_positions = board.availables
        current_state = np.ascontiguousarray(board.current_state().reshape(-1,4,self.borad_width,self.borad_height))
        if self.use_gpu:
            log_act_probs, value = self.policy_value_net(Variable(torch.from_numpy(current_state)).cuda().float())
            act_probs = np.exp(log_act_probs.data.cup().numpy().flatten())
        else:
            log_act_probs, value = self.policy_value_net(Variable(torch.from_numpy(current_state)).float())
            act_probs = np.exp(log_act_probs.data.cup().numpy().flatten())
        act_probs = zip(legal_positions, act_probs[legal_positions])
        value = value.data[0][0]
        return act_probs,value
    # preform a training step
    # wrap in Variable
    def train_step(self, state_batch, mct_probs, winner_batch, lr):
        if self.use_gpu:
            state_batch = Variable(torch.FloatTensor(state_batch).cuda())
            mct_probs = Variable(torch.FloatTensor(mct_probs).cuda())
            winner_batch = Variable(torch.FloatTensor(winner_batch).cuda())
        else:
            state_batch = Variable(torch.FloatTensor(state_batch))
            mct_probs = Variable(torch.FloatTensor(mct_probs))
            winner_batch = Variable(torch.FloatTensor(winner_batch))
        # zero the parameter gradients
        self.optimizier.zero_grad()
        #set the learning rate
        set_learning_rat(self.optimizier, lr)

        #forward
        log_act_probs, value = self.policy_value_net(state_batch)
        # define the loss = (z - v)^2 - pi^T * log(p) + c//theta//^2
        # note: the L2 penalty is incorprated in optimizier
        value_loss = F.mse_loss(value.view(-1),winner_batch)
        policy_loss = -torch.mean(torch.sum(mct_probs*log_act_probs,1))
        loss  = value_loss + policy_loss
        #backward and optimize
        loss.backward()
        self.optimizier.step()
        #calculate policy entropy, for monitoring only
        entropy = -torch.mean(torch.sum(torch.exp(log_act_probs)*log_act_probs, 1))
        return loss.data[0], entropy.data[0]


    def get_policy_param(self):
        net_params = self.policy_value_net.state_dict()
        return net_params
    # save model to file
    def save_model(self, model_file):
        net_params = self.get_policy_param()
        torch.save(net_params,model_file)