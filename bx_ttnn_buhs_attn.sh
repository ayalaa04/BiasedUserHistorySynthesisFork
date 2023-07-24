git checkout BiasedUserHistorySynthesis
TOKENIZERS_PARALLELISM=False CUDA_VISIBLE_DEVICES=0 taskset -c 0-32 python3  main.py --dataset=bx --dataset_dir=$DATASETS_DIR --device=gpu --batch_size=1024 --print_freq=128 --lr=1e-4 --epochs=50 --margin=1 --num_negatives=10 --warm_threshold=0.001 --num_workers=32 --sampling_bias=True --sampling_softmax_temp=1.0 --set_embedding_model=mha --num_heads=1 --projection_dim=96 --test_freq=4 --fanouts=10
git checkout BaseModel