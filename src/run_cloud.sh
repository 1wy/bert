#source ../cuda.rc
#source activate py3

#export BERT_BASE_DIR="chinese_L-12_H-768_A-12/"
export BERT_BASE_DIR="/mnt/aipaasdata/wxw/model/"
#export BERT_BASE_DIR="../model/"

vocab_file=$BERT_BASE_DIR"vocab.txt"
bert_config_file=$BERT_BASE_DIR"bert_config.json"
#init_checkpoint=$BERT_BASE_DIR"bert_model.ckpt"
init_checkpoint=$BERT_BASE_DIR"model.ckpt-5000"
output_dir="./"

python3 -u run_bert.py --task_name=news --do_train=False --do_eval=True --do_predict=True --vocab_file=$vocab_file --bert_config_file=$bert_config_file --init_checkpoint=$init_checkpoint --train_batch_size=32 --learning_rate=5e-5 --num_train_epochs=10.0 --max_seq_length=128 --output_dir=$output_dir
