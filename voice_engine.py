from gtts import gTTS
import pygame
import os
import tempfile
import time
import re
from pydub import AudioSegment
from pydub.effects import normalize

# กำหนด path ffmpeg
AudioSegment.converter = r"C:\Users\onyou\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\Users\onyou\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin\ffprobe.exe"

def preprocess_text(text):
    """ปรับปรุงข้อความให้เหมาะสำหรับการพูด"""
    text = re.sub(r'([,.!?])', r'\1 ', text)
    text = re.sub(r'\.', '.  ', text)
    text = re.sub(r'([!?])', r'\1  ', text)
    text = re.sub(r'(\d+)', r' \1 ', text)
    return text.strip()

def speak(text, speed=1.15, pitch_adjustment=1.07):
    """
    พูดข้อความด้วยเสียงผู้หญิงแหลม สดใส
    - speed: เพิ่มความเร็วเล็กน้อย (1.15 = สดใส)
    - pitch_adjustment: ปรับเสียงให้แหลมขึ้น (1.07 = เสียงผู้หญิงการ์ตูน)
    """
    print(f"Luna 💬: {text}")
    
    processed_text = preprocess_text(text)
    temp_dir = tempfile.gettempdir()
    now = int(time.time())
    temp_mp3_path = os.path.join(temp_dir, f"luna_temp_{now}.mp3")
    temp_processed_path = os.path.join(temp_dir, f"luna_processed_{now}.mp3")

    try:
        # สร้างเสียงด้วย Google TTS
        tts = gTTS(text=processed_text, lang='th', slow=False)
        tts.save(temp_mp3_path)

        if not os.path.exists(temp_mp3_path):
            print("Error: ไม่สามารถสร้างไฟล์ TTS ได้")
            return

        # โหลดไฟล์เสียง
        sound = AudioSegment.from_file(temp_mp3_path)

        # ปรับ pitch ให้แหลมขึ้น
        bright_voice = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * pitch_adjustment)
        }).set_frame_rate(sound.frame_rate)

        # Normalize และปรับความเร็วให้สดใส
        final_sound = normalize(bright_voice)
        final_sound = final_sound.apply_gain(-2)  # ลดเสียงเล็กน้อย
        final_sound = final_sound.fade_in(30).fade_out(30)

        # ปรับความเร็ว
        if speed != 1.0:
            final_sound = final_sound.speedup(playback_speed=speed)

        # Export ไฟล์
        final_sound.export(temp_processed_path, format="mp3", parameters=["-q:a", "2"])

        if not os.path.exists(temp_processed_path):
            print("Error: ไม่สามารถสร้างไฟล์เสียงที่ปรับปรุงแล้วได้")
            return

        # เล่นเสียง
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load(temp_processed_path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
        time.sleep(0.1)

    except Exception as e:
        print(f"Error in speak function: {e}")

    finally:
        try:
            if os.path.exists(temp_mp3_path):
                os.remove(temp_mp3_path)
            if os.path.exists(temp_processed_path):
                os.remove(temp_processed_path)
        except Exception as e:
            print(f"Warning: ไม่สามารถลบไฟล์ temp ได้: {e}")

def speak_with_emotion(text, emotion="happy"):
    """
    พูดด้วยอารมณ์ (ปรับจาก happy เป็นพื้นฐานเสียงผู้หญิงใส ๆ)
    """
    if emotion == "happy":
        speak(text, speed=1.15, pitch_adjustment=1.07)
    elif emotion == "serious":
        speak(text, speed=1.05, pitch_adjustment=0.96)
    elif emotion == "calm":
        speak(text, speed=1.0, pitch_adjustment=0.92)
    else:
        speak(text)

# ทดสอบ
if __name__ == "__main__":
    speak_with_emotion("สวัสดีค่ะ ลูน่ามาแล้ววว พร้อมช่วยทุกเรื่องเลยนะคะ!", "happy")
