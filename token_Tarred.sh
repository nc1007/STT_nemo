#!/bin/bash

# Script to process ASR text tokenizer
python NeMo/scripts/tokenizers/process_asr_text_tokenizer.py  \
  --manifest=dev_decoded_processed.json,train_decoded_processed.json \
  --vocab_size=1024 \
  --data_root=tokenizer_bpe_maxlen_4 \
  --tokenizer=spe \
  --spe_type=bpe \
  --spe_character_coverage=1.0 \
  --spe_max_sentencepiece_length=4

python NeMo/scripts/speech_recognition/convert_to_tarred_audio_dataset.py \
  --manifest_path=train_decoded_processed.json \
  --target_dir=train_tarred_1bk \
  --num_shards=1024 \
  --max_duration=11.0 \
  --min_duration=1.0 \
  --shuffle \
  --shuffle_seed=1 \
  --sort_in_shards \
  --workers=-1
