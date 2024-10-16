import requests
import tkinter as tk
from tkinter import messagebox, Text, Scrollbar
import re

# Google Translate API 정보

# API_KEY = "" 본인의 키를 입력
url = "https://translation.googleapis.com/language/translate/v2"

def clean_text(text):
    """모든 문장을 한 문장으로 인식"""
    # 모든 줄을 결합하고, 불필요한 공백을 제거
    one_line_text = ' '.join(text.split())
    
    # 정규 표현식을 사용하여 문장을 구분
    sentences = re.split(r'(?<=[.!?]) +', one_line_text)
    
    # 비어있지 않은 문장만 반환
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def translate_segment(segment):
    """텍스트 세그먼트를 번역"""
    params = {
        "q": segment,
        "target": "ko",  # 목적 언어 코드 설정
        "format": "text",
        "key": API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        result = response.json()
        if 'data' in result:
            return result['data']['translations'][0]['translatedText']
    return "번역 오류 발생"

def process_text(input_text):
    """원본 텍스트를 정리하고 번역하여 재조립"""
    segments = clean_text(input_text)
    translated_segments = []

    for segment in segments:
        segment = segment.strip()
        if segment:
            translated_segment = translate_segment(segment)
            # 줄바꿈을 추가하여 번역된 문장을 리스트에 추가
            translated_segments.append(translated_segment + '\n')

    # 모든 번역된 문장을 하나의 문자열로 결합
    return ''.join(translated_segments)

def translate_and_display():
    input_text = text_entry.get("1.0", tk.END).strip()
    if input_text:
        translated_text = process_text(input_text)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated_text)
    else:
        messagebox.showwarning("입력 오류", "번역할 텍스트를 입력하세요.")

# GUI 설정
app = tk.Tk()
app.title("완벽한 번역기")
app.geometry("600x400")

# 입력 텍스트 박스
text_entry = Text(app, wrap="word", height=10)
text_entry.pack(padx=10, pady=10, fill="both", expand=True)

# 번역 버튼
translate_button = tk.Button(app, text="번역하기", command=translate_and_display)
translate_button.pack(pady=10)

# 결과 출력 텍스트 박스
output_frame = tk.Frame(app)
output_frame.pack(padx=10, pady=10, fill="both", expand=True)

output_text = Text(output_frame, wrap="word", height=10)
output_text.pack(side="left", fill="both", expand=True)

# 스크롤바 추가
scrollbar = Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=scrollbar.set)

app.mainloop()

