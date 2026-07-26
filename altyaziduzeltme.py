# srt_kaydir.py
import re
from datetime import timedelta

SRT_DOSYASI = "altyazi2.srt"
YENI_SRT = "altyazi2_fixed.srt"
KAYMA_SANIYE = -14.0  # Altyazıyı 14 saniye öne çeker

def adjust_timestamp(ts):
    h, m, s_ms = ts.split(':')
    s, ms = s_ms.split(',')
    td = timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))
    new_td = td + timedelta(seconds=KAYMA_SANIYE)
    if new_td.total_seconds() < 0:
        new_td = timedelta(seconds=0)
    tot_sec = int(new_td.total_seconds())
    hours = tot_sec // 3600
    minutes = (tot_sec % 3600) // 60
    seconds = tot_sec % 60
    millis = int((new_td.microseconds) / 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

def fix_line(match):
    start, end = match.group(1), match.group(2)
    return f"{adjust_timestamp(start)} --> {adjust_timestamp(end)}"

with open(SRT_DOSYASI, "r", encoding="utf-8") as f:
    content = f.read()

fixed_content = re.sub(
    r'(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})', 
    fix_line, 
    content
)

with open(YENI_SRT, "w", encoding="utf-8") as f:
    f.write(fixed_content)

print("2. Bölüm altyazısı -14 saniye kaydırıldı!")