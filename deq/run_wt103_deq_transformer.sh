python transformer_train.py --cuda --n_layer 5 --eval_n_layer 24 --d_embed 128 --d_model 128 --n_head 10 --d_head 70 --d_inner 8000 --dropout 0.05 --dropatt 0.0 --optim Adam --lr 0.00025 --warmup_step 16000 --pretrain_steps 16000 --eval-interval 5000 --max_step 300000 --tgt_len 30 --mem_len 50 --eval_tgt_len 30 --wnorm --f_thres 30 --b_thres 40 --subseq_len 75 --batch_size 128 --mode 'train'