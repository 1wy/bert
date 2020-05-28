#source ../cuda.rc
source activate py3

python pull_push_data.py pull
aipaas login -u wxw -p wy123456
aipaas airun "./run_cloud.sh" --gpu 1 -u wxw -p wy123456 -w ./ -o ../output
python pull_push_data.py push
