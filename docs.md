bước 1 : chuẩn bị data
bash /home/data/CUONG/NeMo/data_ahy/data.sh 1  13 
bước 2: tạo token và Tarred datasets and bucketing
sh token_Tarred.sh



* chú ý: 
  create_manifest.py: biến  data_dir = "data_voice" thay bằng tên thư mục có chức file .wav,txt