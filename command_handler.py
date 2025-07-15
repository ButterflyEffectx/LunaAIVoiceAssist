import datetime
import webbrowser as wb
import wikipedia

from voice_engine import speak
from screenshot import capture_screen, open_image_and_prompt
from github_tools import create_repo
from gpt_chat import ask_gpt
from spotify_control import next_song, previous_song, pause_song, resume_song

COMMANDS = {
    "time": ["บอกเวลา", "ตอนนี้กี่โมง", "เวลา"],
    "screenshot": ["แคปหน้าจอ", "ถ่ายหน้าจอ", "บันทึกหน้าจอ"],
    "github": ["สร้าง github", "สร้างกิตฮับ", "สร้างกิทฮับ", "สร้างกินฮับ", "ภาษาอังกฤษฮับ", "ทำกิทฮับ", "กิตฮับ", "กิทฮับ", "กิท", "ภาษาอังกฤษ hub", "สร้าง gif hub", "สร้างกินหัก", "ภาษาอังกฤษหัก", "สร้างกินครับ", "ภาษาอังกฤษหา", "สร้างภาษาอังกฤษครับ", "สร้างอังกฤษ", "ช่างกันหัก"],
    "youtube": ["เปิด youtube", "เปิดยูทูป"],
    "search": ["ค้นหา", "เสิร์ช", "ค้นหาใน chrome"],
    "greeting": ["สวัสดี", "หวัดดี"],
    "next_song": ["เปลี่ยนเพลง", "ข้ามเพลง", "เพลงต่อไป", "skip เพลง"],
    "prev_song": ["ย้อนเพลง", "เพลงก่อนหน้า", "previous", "เพลงที่แล้ว", "ย้อนกลับ"],
    "pause_song": ["หยุดเพลง", "พอสเพลง", "หยุดเล่น", "pause"],
    "resume_song": ["เล่นเพลง", "เปิดเพลง", "เล่นต่อ", "resume"],
}

def detect_command(cmd: str):
    """
    ตรวจสอบคำสั่งจากข้อความ cmd โดยเทียบกับ keywords ใน COMMANDS
    คืนค่า key ของคำสั่ง หรือ None ถ้าไม่เจอ
    """
    cmd_lower = cmd.lower()
    for key, keywords in COMMANDS.items():
        for kw in keywords:
            if kw in cmd_lower:
                return key
    return None

def handle_command(cmd: str):
    """
    ฟังก์ชันหลักสำหรับจัดการคำสั่ง
    """
    command_type = detect_command(cmd)
    if command_type == "time":
        from datetime import datetime
        now = datetime.now().strftime("%H:%M")
        speak(f"ตอนนี้เวลา {now} นาฬิกาครับ")
    
    elif command_type == "github":
        try:
            create_repo()
            speak("สร้าง GitHub repository เรียบร้อย")
        except Exception as e:
            speak("เกิดข้อผิดพลาดในการสร้าง repository")
            print(f"Error: {e}")

    elif command_type == "screenshot":
        screenshot_path = capture_screen()
        open_image_and_prompt(screenshot_path)
        speak("แคปหน้าจอเรียบร้อยแล้ว")
      

    elif command_type == "youtube":
        speak("กำลังเปิด YouTube ให้ครับ")
        open_youtube()
    
    elif command_type == "next_song":
        next_song()
        
    elif command_type == "prev_song":
        previous_song()
        
    elif command_type == "pause_song":
        pause_song()

    elif command_type == "resume_song":
        resume_song()

    elif command_type == "search":
        speak("กำลังค้นหาให้ครับ")
        do_search()

    elif command_type == "greeting":
        speak("สวัสดีครับ ยินดีให้บริการครับ")

    else:
        # ใช้ GPT ตอบคำถามที่ไม่อยู่ใน command
        speak("ขอเช็คข้อมูลให้ก่อนนะครับ...")
        ask_gpt(cmd)

# ตัวอย่างฟังก์ชันสมมติที่ใช้ใน handle_command (ต้องเขียนเพิ่มเอง)


def capture_screenshot():
    # โค้ดแคปหน้าจอจริง ๆ
    path = r"C:\Users\onyou\Pictures\LunaScreenshots\screenshot.png"
    print(f"Capturing screenshot and saving to {path}")
    return path

def open_image(path):
    # โค้ดเปิดภาพในเครื่อง (Windows ตัวอย่าง)
    import os
    os.startfile(path)

def open_youtube():
    import webbrowser
    webbrowser.open("https://www.youtube.com")

def do_search():
    import webbrowser
    # ค้นหาขั้นต้น
    webbrowser.open("https://www.google.com")

def speak(text):
    # ฟังก์ชันพูดข้อความ
    print(f"Luna 💬: {text}")