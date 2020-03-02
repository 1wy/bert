source ../cuda.rc
source activate py3.6

export BERT_BASE_DIR="chinese_L-12_H-768_A-12/"
#export BERT_BASE_DIR="finnews/CloseRet_t-2_t+1/output/"
export DATA_DIR="finnews/CloseRet_t_t+1/"
#export DATA_DIR="finnews1001-1907"

vocab_file=$BERT_BASE_DIR"vocab.txt"
bert_config_file=$BERT_BASE_DIR"bert_config.json"
init_checkpoint=$BERT_BASE_DIR"bert_model.ckpt"
#init_checkpoint=$BERT_BASE_DIR"model.ckpt-4871"
output_dir=$DATA_DIR"output/"

CUDA_VISIBLE_DEVICES=0 python -u run_classifier.py --task_name=Weibo --do_train=True --do_eval=False --do_predict=True --data_dir=$DATA_DIR --vocab_file=$vocab_file --bert_config_file=$bert_config_file --init_checkpoint=$init_checkpoint --train_batch_size=32 --learning_rate=5e-5 --num_train_epochs=2.0 --max_seq_length=128 --output_dir=$output_dir
