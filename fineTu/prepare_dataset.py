from datasets import load_dataset

# Hugging Face 토큰을 변수에 저장
token = "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"  # 여기에 자신의 Hugging Face 토큰을 입력하세요

# 데이터셋 로드
dataset = load_dataset("ziozzang/deepl_trans_DE-KO", split="train", token=token)

# 텍스트 파일로 저장
output_file = "de_ko_data.txt"
with open(output_file, "w", encoding="utf-8") as f:
    for data in dataset:
        de_text = data["DE"]
        ko_text = data["KO"]
        f.write(f"{de_text}\t{ko_text}\n")

print(f"{output_file} 파일에 저장 완료.")
