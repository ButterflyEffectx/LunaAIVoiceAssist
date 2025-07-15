import openai
import os
from dotenv import load_dotenv
from voice_engine import speak

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_gpt(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  
            messages=[
                {"role": "system", "content": "ตอบสั้น ๆ และดูเป็นเลขามืออาชีพ"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        reply = response.choices[0].message.content.strip()
        speak(reply)
        return reply
    except Exception as e:
        speak("ขอโทษนะคะ ลูน่าคุยกับ GPT ไม่ได้เลยตอนนี้~")
        print("GPT Error:", e)
