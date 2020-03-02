#export BERT_BASE_DIR="chinese_L-12_H-768_A-12/"
export BERT_BASE_DIR="weibo_output/"
export WEIBO_DIR="weibo_senti_100k/"

vocab_file=$BERT_BASE_DIR"vocab.txt"
bert_config_file=$BERT_BASE_DIR"bert_config.json"
init_checkpoint=$BERT_BASE_DIR"model.ckpt-5999"

CUDA_VISIBLE_DEVICES=0 python -u run_classifier.py --task_name=WeiBo --do_train=False --do_eval=False --do_predict=True --data_dir=$WEIBO_DIR --vocab_file=$vocab_file --bert_config_file=$bert_config_file --init_checkpoint=$init_checkpoint --train_batch_size=32 --learning_rate=5e-5 --num_train_epochs=2.0 --max_seq_length=128 --output_dir=./weibo_output/
