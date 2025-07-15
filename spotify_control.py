import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from voice_engine import speak

# เตรียม environment สำหรับ OAuth (สามารถใส่ไว้ใน .env ก็ได้)
os.environ["SPOTIPY_CLIENT_ID"] = ""
os.environ["SPOTIPY_CLIENT_SECRET"] = ""
os.environ["SPOTIPY_REDIRECT_URI"] = ""

# ข้ามเพลง
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from voice_engine import speak

def get_spotify_client():
    scope = "user-modify-playback-state user-read-playback-state"
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

def next_song():
    try:
        sp = get_spotify_client()
        playback = sp.current_playback()
        if not playback:
            speak("ลูน่าไม่เจอว่า Spotify เปิดอยู่เลยค่ะ")
            return
        if not playback.get("is_playing"):
            speak("ยังไม่มีเพลงเล่นอยู่ ลองกดเล่นก่อนนะคะ~")
            return
        sp.next_track()
        speak("ข้ามเพลงให้เรียบร้อยแล้วค่า~ 🎶")
    except Exception as e:
        speak("มีปัญหาตอนข้ามเพลงนะคะ")
        print(f"Error: {e}")

def previous_song():
    try:
        sp = get_spotify_client()
        playback = sp.current_playback()
        if not playback:
            speak("ลูน่าไม่เจอว่า Spotify เปิดอยู่เลยค่ะ")
            return
        if not playback.get("is_playing"):
            speak("ยังไม่มีเพลงเล่นอยู่นะคะ")
            return
        sp.previous_track()
        speak("ย้อนเพลงให้เรียบร้อยแล้วค่ะ 🎵")
    except Exception as e:
        speak("มีปัญหาตอนย้อนเพลงนะคะ")
        print(f"Error: {e}")

def resume_song():
    """เล่นเพลงต่อ ถ้ามีการ pause อยู่"""
    try:
        sp = get_spotify_client()
        playback = sp.current_playback()
        if playback and not playback.get("is_playing"):
            sp.start_playback()
            speak("เปิดเพลงต่อให้แล้วนะคะ 🎼")
        else:
            speak("ตอนนี้มีเพลงกำลังเล่นอยู่แล้วค่ะ")
    except Exception as e:
        speak("ลูน่าไม่สามารถเปิดเพลงให้ได้นะคะ")
        print(f"Error: {e}")

def pause_song():
    """หยุดเพลงชั่วคราว"""
    try:
        sp = get_spotify_client()
        playback = sp.current_playback()
        if playback and playback.get("is_playing"):
            sp.pause_playback()
            speak("หยุดเพลงให้แล้วนะคะ 🛑")
        else:
            speak("ไม่มีเพลงที่เล่นอยู่ในตอนนี้ค่ะ")
    except Exception as e:
        speak("เกิดปัญหาตอนหยุดเพลงค่ะ")
        print(f"Error: {e}")
