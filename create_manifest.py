import os
import json
import soundfile as sf  

# Thư mục chứa dữ liệu
data_dir = "data_voice"

output_file = "data.json"

with open(output_file, "w", encoding="utf-8") as f_out:
    # Duyệt qua tất cả file .wav trong data_dir
    for fname in sorted(os.listdir(data_dir)):
        if fname.endswith(".wav"):
            base = os.path.splitext(fname)[0]
            wav_path = os.path.join(data_dir, fname)
            txt_path = os.path.join(data_dir, base + ".txt")

            # Bỏ qua nếu không có text
            if not os.path.exists(txt_path):
                print(f"Thiếu transcript cho {fname}, bỏ qua.")
                continue

            # Đọc transcript
            with open(txt_path, "r", encoding="utf-8") as f_txt:
                text = f_txt.read().strip()

            # Tính duration
            with sf.SoundFile(wav_path) as audio:
                duration = len(audio) / audio.samplerate

            # Tạo record
            record = {
                "audio_filepath": os.path.abspath(wav_path),
                "duration": round(duration, 3),
                "text": text
            }

            # Ghi 1 dòng JSON
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")

print(f"Đã tạo file {output_file}")