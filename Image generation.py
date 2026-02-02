import time
import requests
import speech_recognition as sr

MONSTER_API_KEY = "PASTE_YOUR_MONSTER_API_KEY_HERE"
AUDIO_FILE = "input.wav"
OUTPUT_IMAGE = "generated_image.png"
def record_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        print("🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    with open(AUDIO_FILE, "wb") as f:
        f.write(audio.get_wav_data())

    return AUDIO_FILE
def speech_to_text():
    recognizer = sr.Recognizer()

    with sr.AudioFile(AUDIO_FILE) as source:
        audio = recognizer.record(source)

    text = recognizer.recognize_google(audio)
    print(" Transcribed Text:", text)
    return text
def generate_image(prompt):
    url = "https://api.monsterapi.ai/v1/generate/txt2img"
    headers = {
        "Authorization": f"Bearer {MONSTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": f"high quality, ultra realistic, {prompt}",
        "steps": 30,
        "samples": 1,
        "guidance_scale": 7.5
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    if "process_id" not in data:
        raise Exception(data)

    return data["process_id"]

def get_image_result(process_id):
    status_url = f"https://api.monsterapi.ai/v1/status/{process_id}"
    headers = {"Authorization": f"Bearer {MONSTER_API_KEY}"}

    while True:
        response = requests.get(status_url, headers=headers)
        data = response.json()

        if data["status"] == "COMPLETED":
            return data["output"][0]

        if data["status"] == "FAILED":
            raise Exception("Image generation failed")

        print(" Generating image...")
        time.sleep(3)
def save_image(image_url):
    img = requests.get(image_url).content
    with open(OUTPUT_IMAGE, "wb") as f:
        f.write(img)

    print(" Image saved as", OUTPUT_IMAGE)
def main():
    record_audio()
    prompt = speech_to_text()

    print(" Generating image...")
    pid = generate_image(prompt)
    image_url = get_image_result(pid)

    save_image(image_url)
    print(" Speech → Image complete")

if __name__ == "__main__":
    main()
