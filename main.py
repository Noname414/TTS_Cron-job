import logging
from google import genai
from google.genai import types
import wave

# Set up the wave file to save the output:
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
   with wave.open(filename, "wb") as wf:
      wf.setnchannels(channels)
      wf.setsampwidth(sample_width)
      wf.setframerate(rate)
      wf.writeframes(pcm)
      logging.info(f"Audio saved to {filename}")

def generate_audio(script):
    client = genai.Client()
    prompt = "以中文Podcast方式朗誦以下對話，並以主持人林冠傑和林欣潔的口吻："+script

    response = client.models.generate_content(
    model="gemini-2.5-pro-preview-tts",
    contents=prompt,
    config=types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
                speaker_voice_configs=[
                types.SpeakerVoiceConfig(
                    speaker='林冠傑',
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Charon',
                        )
                    )
                ),
                types.SpeakerVoiceConfig(
                    speaker='林欣潔',
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name='Zephyr',
                        )
                    )
                ),
                ]
            )
        )
    )
    )

    data = response.candidates[0].content.parts[0].inline_data.data

    file_name='out.wav'
    wave_file(file_name, data) # Saves the file to current directory

if __name__ == "__main__":
    logging.info("Generating audio...")
    with open('2507.05257v1_script.txt', 'r', encoding='utf-8') as file:
        script = file.read()
    generate_audio(script)
    logging.info("Audio generated successfully!")