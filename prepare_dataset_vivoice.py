import json
import os
import re
from collections import defaultdict
from nemo.collections.asr.parts.utils.manifest_utils import read_manifest, write_manifest
from tqdm.auto import tqdm


def write_processed_manifest(data, original_path):
    original_manifest_name = os.path.basename(original_path)
    new_manifest_name = original_manifest_name.replace(".json", "_processed.json")

    manifest_dir = os.path.split(original_path)[0]
    filepath = os.path.join(manifest_dir, new_manifest_name)
    write_manifest(filepath, data)
    print(f"Finished writing manifest: {filepath}")
    return filepath


# calculate the character set
def get_charset(manifest_data):
    charset = defaultdict(int)
    for row in tqdm(manifest_data, desc="Computing character set"):
        text = row['text']
        for character in text:
            charset[character] += 1
    return charset


# Preprocessing steps
def remove_special_characters(data):
    chars_to_ignore_regex = r"[\.\,\?\:\-!;()«»…\]\[/\*–‽+&_\\½√>€™$•¼}{~—=“\"”″‟„]"
    apostrophes_regex = r"[’'‘`ʽ']"

    data["text"] = re.sub(chars_to_ignore_regex, " ", data["text"])  # replace punctuation by space
    data["text"] = re.sub(apostrophes_regex, "'", data["text"])      # normalize apostrophes
    data["text"] = re.sub(r"'+", "'", data["text"])                  # merge multiple apostrophes
    data["text"] = re.sub(r" +", " ", data["text"])                  # merge multiple spaces
    data["text"] = data["text"].strip()
    return data


def remove_oov_characters(data):
    # Cho phép toàn bộ bảng chữ cái tiếng Việt + chữ thường/hoa + khoảng trắng + dấu nháy
    oov_regex = "[^a-zA-Zàáảãạâầấẩẫậăằắẳẵặ" \
                "èéẻẽẹêềếểễệ" \
                "ìíỉĩị" \
                "òóỏõọôồốổỗộơờớởỡợ" \
                "ùúủũụưừứửữự" \
                "ỳýỷỹỵ" \
                "đ" \
                "ÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶ" \
                "ÈÉẺẼẸÊỀẾỂỄỆ" \
                "ÌÍỈĨỊ" \
                "ÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢ" \
                "ÙÚỦŨỤƯỪỨỬỮỰ" \
                "ỲÝỶỸỴ" \
                "Đ' ]"

    data["text"] = re.sub(oov_regex, "", data["text"])
    data["text"] = re.sub(r"\s+", " ", data["text"])   # merge spaces
    data["text"] = data["text"].strip()
    return data


def normalize_case(data):
    # chuyển tất cả về chữ thường
    data["text"] = data["text"].lower()
    return data


# Processing pipeline
def apply_preprocessors(manifest, preprocessors):
    for processor in preprocessors:
        for idx in tqdm(range(len(manifest)), desc=f"Applying {processor.__name__}"):
            manifest[idx] = processor(manifest[idx])

    print("Finished processing manifest !")
    return manifest


# List of pre-processing functions (tiếng Việt)
PREPROCESSORS = [
    remove_special_characters,
    remove_oov_characters,
    normalize_case,
]


train_manifest = "train_decoded.json"
dev_manifest = "dev_decoded.json"
test_manifest = "test_decoded.json"

train_data = read_manifest(train_manifest)
dev_data = read_manifest(dev_manifest)
test_data = read_manifest(test_manifest)

# Apply preprocessing
train_data_processed = apply_preprocessors(train_data, PREPROCESSORS)
dev_data_processed = apply_preprocessors(dev_data, PREPROCESSORS)
test_data_processed = apply_preprocessors(test_data, PREPROCESSORS)

# Write new manifests
train_manifest_cleaned = write_processed_manifest(train_data_processed, train_manifest)
dev_manifest_cleaned = write_processed_manifest(dev_data_processed, dev_manifest)
test_manifest_cleaned = write_processed_manifest(test_data_processed, test_manifest)
