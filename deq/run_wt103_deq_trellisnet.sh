python trellisnet_train.py --cuda --n_layer 30 --d_embed 128 --nhid 300 --nout 128 --clip 0.07 --dropout 0.1 --dropouti 0.1 --dropouth 0.1 --optim Adam --lr 1e-3 --pretrain_steps 30000 --seq_len 100 --subseq_len 75 --f_thres 45 --b_thres 45 --batch_size 32 --mode 'train'


python trellisnet_train.py --cuda --n_layer 30 --d_embed 128 --nhid 300 --nout 128 --clip 0.07 --dropout 0.1 --dropouti 0.1 --dropouth 0.1 --optim Adam --lr 1e-3 --pretrain_steps 30000 --seq_len 100 --subseq_len 75 --f_thres 45 --b_thres 45 --batch_size 128 --mode 'validate' --model_dir './models/trellisnet/20191202145627/'