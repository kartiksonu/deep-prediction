import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import torch.nn as nn
from TCN.tcn import TemporalConvNetwork, TimeDistributedLayer
from TCN.trellisnet import TrellisNet
from TCN.utils import WeightDrop


class LSTMModel(nn.Module):
    def __init__(self,):
        super(LSTMModel,self).__init__()
        self.encoder_lstm=nn.LSTMCell(input_size=2,hidden_size=64)
        self.embedding_pos=nn.Linear(64,2)
        self.decoder_lstm=nn.LSTMCell(input_size=64,hidden_size=64)


    def forward(self,input_traj):
        self.h,self.c=(torch.zeros(input_traj.shape[0],64),torch.zeros(input_traj.shape[0],64))
        for i in range(20):
            self.h,self.c=self.encoder_lstm(input_traj[:,i,:],(self.h,self.c))
        out=[]
        for i in range(30):
            self.h,self.c=self.decoder_lstm(self.h,(self.h,self.c))
            out.append(self.embedding_pos(self.h))
        pred_traj=torch.stack(out,dim=1)
        return pred_traj


# TCN Model
class TCNModel(nn.Module):
    def __init__(self, input_size, output_size, num_channels, kernel_size, dropout, embedding_size=64):
        super(TCNModel, self).__init__()
        self.input_embedding = nn.Linear(2, embedding_size)
        self.tcn = TemporalConvNetwork(input_size, num_channels, kernel_size=kernel_size, dropout=dropout)
        self.output_embedding = nn.Linear(embedding_size, 2)
        self.tdst_output = TimeDistributedLayer(nn.Linear(20, 30), batch_first=True)

    
    def forward(self, x):
        x = self.input_embedding(x)
        x = self.tcn(x)
        x = self.tdst_output(x)
        x = x.permute(0,2,1)
        out = self.output_embedding(x)
        return out


# Trellis Network Model
class TrellisNetModel(nn.Module):
    def __init__(self):
        super(TrellisNetModel, self).__init__()

    def forward(self, inputs, hidden):
        raise NotImplementedError

    def init_hidden(self, bsz):
        raise NotImplementedError


class Social_Model(nn.Module):
    def __init__(self):
        super(Social_Model,self).__init__()
        self.agent_encoder=nn.LSTM(input_size=2,hidden_size=64,batch_first=True)
        self.neighbour_encoder=nn.LSTM(input_size=2,hidden_size=64,batch_first=True)
        self.decoder_lstm=nn.LSTMCell(input_size=128,hidden_size=128)
        self.embedding_pos=nn.Linear(128,2)

    def forward(self,input_dict):
        agent_traj=input_dict['agent_traj']
        neighbour_traj=input_dict['neighbour_traj']
        agent_embedding,_=self.agent_encoder(agent_traj)
        agent_embedding=agent_embedding[:,-1,:]
        # import pdb; pdb.set_trace()
        neighbour_embedding=[]
        pred_traj=[]
        for batch_index in range(len(neighbour_traj)):
            curr_neighbours_traj=neighbour_traj[batch_index]
            out=self.neighbour_encoder(curr_neighbours_traj)[0][:,-1,:]
            out=torch.mean(out,dim=0)
            neighbour_embedding.append(out)
        neighbour_embedding=torch.stack(neighbour_embedding,dim=0)
        self.h=torch.cat([agent_embedding,neighbour_embedding],dim=1)
        self.c=torch.zeros(self.h.shape)
        # import pdb; pdb.set_trace()
        for _ in range(30):
            self.h,self.c=self.decoder_lstm(self.h,(self.h,self.c))
            pred_traj.append(self.embedding_pos(self.h))
        pred_traj=torch.stack(pred_traj,dim=1)
        return pred_traj