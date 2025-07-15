import os
import subprocess
from github import Github
from voice_engine import speak, speak_with_emotion
import webbrowser
import tkinter as tk
from tkinter import simpledialog
import speech_recognition as sr

def listen_yes_no(prompt=""):
    """ถามคำถามแล้วรอฟังคำตอบเป็นเสียง -> คืนค่า True/False"""
    speak(prompt)
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        response = r.recognize_google(audio, language="th-TH").lower()
        print("คุณตอบว่า:", response)
        if "ใช่" in response or "ได้" in response or "โอเค" in response or "ทั้งหมด" in response:
            return True
        elif "ไม่" in response:
            return False
        else:
            speak("ขอโทษค่ะ ลูน่าฟังไม่เข้าใจ คิดว่าเป็น ไม่ นะคะ")
            return False
    except:
        speak("ลูน่าฟังไม่ชัดเลยค่ะ จะถือว่าเป็น ไม่ นะคะ")
        return False


def create_repo():
    speak("รับทราบค่ะ กำลังสร้าง repository")

    root = tk.Tk()
    root.withdraw()

    # STEP 1: ใส่ชื่อ repo
    repo_name = simpledialog.askstring("ชื่อ Repository", "ใส่ชื่อ repo ที่ต้องการสร้าง:")
    if not repo_name:
        speak("คุณยังไม่ได้ใส่ชื่อ repo นะคะ")
        return

    # STEP 2: ถามด้วยเสียงว่า public หรือ private
    is_public = listen_yes_no("ต้องการให้ repository เป็น public ใช่ไหมคะ")

    try:
        token = os.getenv("GITHUB_API_KEY")
        if not token:
            speak("ไม่มี GitHub API key นะคะ กรุณาตั้ง environment variable ให้ถูกต้อง")
            return
        g = Github(token)
        user = g.get_user()
        repo = user.create_repo(repo_name, private=not is_public)
        speak(f"สร้าง repository {repo_name} เรียบร้อยแล้วค่ะ")
    except Exception as e:
        speak("เหมือนจะพบปัญหาในการสร้าง repo ค่ะ")
        print(f"Error: {e}")
        return

    # STEP 3: ใส่ path โปรเจกต์
    path = simpledialog.askstring("Path ของโปรเจกต์", "ใส่ path ของโปรเจกต์ที่ต้องการอัพขึ้น GitHub:")
    if not path or not os.path.isdir(path):
        speak("path นี้ไม่มีอยู่จริงนะคะ")
        return

    os.chdir(path)
    subprocess.run(["git", "init"])

    check_remote = subprocess.run(["git", "remote"], capture_output=True, text=True)
    if "origin" in check_remote.stdout.split():
        speak("เจอ origin เดิมอยู่ ลูน่าจะลบทิ้งให้ค่ะ")
        subprocess.run(["git", "remote", "remove", "origin"])

    subprocess.run(["git", "remote", "add", "origin", repo.clone_url])
    speak("เชื่อมต่อกับ repository เรียบร้อยแล้วค่ะ")

    # STEP 4: ถามด้วยเสียงว่าจะ add ไฟล์ทั้งหมดมั้ย
    add_all = listen_yes_no("ต้องการเพิ่มไฟล์ทั้งหมดเลยมั้ยคะ")

    if add_all:
        subprocess.run(["git", "add", "."])
    else:
        file_list = simpledialog.askstring("ไฟล์ที่ต้องการ add", "ใส่ชื่อไฟล์แยกด้วยช่องว่าง เช่น main.py index.html:")
        if file_list:
            subprocess.run(["git", "add"] + file_list.split())
        else:
            speak("ยังไม่ได้เลือกไฟล์ไหนเลยค่ะ")
            return

    # STEP 5: commit message
    commit_message = simpledialog.askstring("Commit Message", "ใส่ข้อความ commit:")
    if not commit_message:
        speak("คุณไม่ได้ใส่ commit message ค่ะ")
        return
    subprocess.run(["git", "commit", "-m", commit_message])

    # STEP 6: ถามด้วยเสียงว่าจะใช้ master มั้ย
    use_master = listen_yes_no("ต้องการ push ไปที่ branch master ใช่ไหมคะ")

    if use_master:
        subprocess.run(["git", "branch", "-M", "master"])
        subprocess.run(["git", "push", "-u", "origin", "master"])
    else:
        branch_name = simpledialog.askstring("ชื่อ Branch", "ใส่ชื่อ branch ที่ต้องการ:")
        if not branch_name:
            speak("ยังไม่ได้ใส่ชื่อ branch เลยนะคะ")
            return
        subprocess.run(["git", "checkout", "-b", branch_name])
        subprocess.run(["git", "push", "-u", "origin", branch_name])

    speak("อัปโหลดเสร็จแล้วค่ะ ลูน่าจะเปิด browser ให้เลยนะคะ")
    webbrowser.open(repo.html_url)

if __name__ == "__main__":
    create_repo()
