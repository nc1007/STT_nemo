import json
import random
from math import floor

def split_data(input_file, val_ratio=0.1, test_ratio=0.05):

    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  
                data.append(json.loads(line))
    
    
    random.shuffle(data)
    
    total_samples = len(data)
    test_size = floor(total_samples * test_ratio)
    val_size = floor(total_samples * val_ratio)
    train_size = total_samples - test_size - val_size
    
    print(f"Tổng số mẫu: {total_samples}")
    print(f"Train: {train_size} mẫu ({train_size/total_samples*100:.1f}%)")
    print(f"Validation: {val_size} mẫu ({val_size/total_samples*100:.1f}%)")
    print(f"Test: {test_size} mẫu ({test_size/total_samples*100:.1f}%)")
    
    # Chia dữ liệu
    test_data = data[:test_size]
    val_data = data[test_size:test_size + val_size]
    train_data = data[test_size + val_size:]
    
    with open('train.json', 'w', encoding='utf-8') as f:
        for item in train_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
    
    with open('dev.json', 'w', encoding='utf-8') as f:
        for item in val_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
    with open('test.json', 'w', encoding='utf-8') as f:
        for item in test_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')
    
    print("\nĐã tạo thành công các file:")
    print("- train.json")
    print("- dev.json") 
    print("- test.json")

if __name__ == "__main__":
    random.seed(42)
    
    input_file = "data.json"  # Đường dẫn đến file gốc
    split_data(input_file, val_ratio=0.05, test_ratio=0.05)