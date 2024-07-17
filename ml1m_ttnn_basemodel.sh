git checkout BaseModel
TOKENIZERS_PARALLELISM=False CUDA_VISIBLE_DEVICES=0 taskset -c 0-32 python3 main.py --dataset=ml --dataset_dir=$DATASETS_DIR --device=gpu --batch_size=1024 --print_freq=128 --lr=2e-4 --epochs=100 --margin=1 --num_negatives=20 --warm_threshold=0.2 --num_workers=32 

TOKENIZERS_PARALLELISM=False python3 main.py --dataset=ml --dataset_dir=/Users/bibi/Desktop/my_rec_sys/BiasedUserHistorySynthesisFork/DATASET/ --device=cpu --batch_size=1024 --print_freq=128 --lr=2e-4 --epochs=100 --margin=1 --num_negatives=20 --warm_threshold=0.2 --num_workers=8