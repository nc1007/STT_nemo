#!/bin/bash

# Script thiết lập môi trường STT_nemo
# Cách dùng:
#   ./setup.sh start stop
# Ví dụ:
#   ./setup.sh 1 5   # chạy từ bước 1 đến 5

START=${1:-1}
STOP=${2:-99}

step=1

run_step () {
  if [ $step -ge $START ] && [ $step -le $STOP ]; then
    echo ">>> Bước $step: $1"
    eval "$2"
  fi
  step=$((step+1))
}

# Bước 1: Tạo môi trường conda
run_step "Tạo môi trường conda tên STT_nemo với Python 3.10" \
"conda create -n STT_nemo python=3.10 -y"

# Bước 2: Kích hoạt môi trường conda
run_step "Kích hoạt môi trường conda" \
"eval \"\$(conda shell.bash hook)\" && conda activate STT_nemo"

# Bước 3: Clone repository NeMo
run_step "Clone repository NeMo" \
"git clone https://github.com/NVIDIA-NeMo/NeMo.git"

# Bước 4: Chuyển vào thư mục NeMo
run_step "Chuyển vào thư mục NeMo" \
"cd NeMo"

# Bước 5: Cài đặt dependencies
run_step "Cài đặt các dependencies" \
"pip install -r requirements.txt"

# Bước 6: Cài đặt bộ toolkit cho NeMo
run_step "Cài đặt bộ toolkit cho NeMo" \
"pip install nemo_toolkit[all]"

# Bước 7: Quay lại thư mục cha NeMo
run_step "Chuyển vào thư mục cha NeMo" \
"cd .."

# Bước 8: Tạo và xử lý manifest
run_step "Chạy create_manifest.py" \
"python ./create_manifest.py"
# buước 9
run_step "Chạy split_manifest.py" \
"python ./split_manifest.py"
#bước 10
run_step "Tạo thư mục train/dev/test" \
"mkdir -p train dev test"

# Bước 11: Chạy decode_resample.py
run_step "Chạy decode_resample.py cho train/dev/test" \
"python ./decode_resample.py \
  --manifest=train.json \
  --destination_folder=./train && \
python ./decode_resample.py \
  --manifest=dev.json \
  --destination_folder=./dev && \
python ./decode_resample.py \
  --manifest=test.json \
  --destination_folder=./test"

# Bước 12: Chuẩn bị dataset
run_step "Chạy prepare_dataset_vivoice.py" \
"python ./prepare_dataset_vivoice.py"

# Bước 13: Thông báo hoàn tất
run_step "Hoàn tất thiết lập" \
"echo 'Thiết lập hoàn tất! Môi trường STT đã sẵn sàng.'"
