#!/bin/bash
CONFIG_FILE=config.yaml

for MODEL in $(yq e '.models | keys | .[]' $CONFIG_FILE); do
    NAME=$(yq e ".models.$MODEL.name" $CONFIG_FILE)
    URL=$(yq e ".models.$MODEL.url" $CONFIG_FILE)
    DEVICE=$(yq e ".models.$MODEL.device" $CONFIG_FILE)
    PORT=$(echo $URL | grep -o '[0-9]\+$')

    if [ "$DEVICE" == "cpu" ]; then
        CACHE=$(yq e ".models.$MODEL.VLLM_CPU_KVCACHE_SPACE" $CONFIG_FILE)
        CORES=$(yq e ".models.$MODEL.VLLM_CPU_OMP_THREADS_BIND" $CONFIG_FILE)

        CMD="docker run --rm -p $PORT:8000"
        CMD+=" -e VLLM_CPU_KVCACHE_SPACE=$CACHE"
        # CMD+=" -e VLLM_CPU_OMP_THREADS_BIND=$CORES"
        CMD+=" -e HF_TOKEN=${HF_TOKEN}"
        CMD+=" vllm-cpu-env"
        CMD+=" --model=$NAME --max-model-len=1024 --max-num-seqs=1"
    else
        CMD="HF_TOKEN=${HF_TOKEN} vllm serve $NAME --port $PORT --max-model-len 1024 --max-num-seqs 1"
    fi

    echo "Running: $CMD"
    eval $CMD &
done