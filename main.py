from voice_engine import speak
from listen_engine import listen
from command_handler import handle_command

WAKE_WORDS = ["luna", "รูน่า", "ดูหน้า", "อยู่หน้า", "ทูน่า", "หนูนา", "ลูน่า"]

def detect_wake_word(command: str):
    """ตรวจสอบและคืนคำสั่งหลังจาก wake word ถ้าพบ"""
    for word in WAKE_WORDS:
        if word in command:
            return command.replace(word, "").strip()
    return None

def main():
    print("🚀 เริ่มต้นระบบ Luna Assistant")
    speak("ลูน่าเริ่มต้นระบบพร้อมรับคำสั่งแล้วค่ะ")

    while True:
        try:
            command = listen()
            if command:
                print(f"📝 คำสั่งที่ได้ยิน: '{command}'")

                clean_cmd = detect_wake_word(command)
                if clean_cmd is not None:
                    print("✅ ตรวจพบ wake word")
                    print(f"🔧 คำสั่งที่ประมวลผล: '{clean_cmd}'")

                    if clean_cmd:
                        handle_command(clean_cmd)
                    else:
                        speak("มีอะไรให้ช่วยไหมครับ")
                else:
                    print("❌ ไม่พบ wake word")

        except KeyboardInterrupt:
            print("\n🛑 หยุดระบบ Luna Assistant")
            speak("ลาก่อนครับ")
            break

        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาด: {e}")
            speak("เกิดข้อผิดพลาดครับ")

if __name__ == "__main__":
    main()
