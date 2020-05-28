#source ../cuda.rc
source activate py3

python pull_push_data.py pull
aipaas airun "./run_cloud.sh" -u wxw -p wy123456 -w ./
python pull_push_data.py push
