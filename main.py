from moviepy import AudioFileClip, ImageClip
from PIL import ImageGrab
import numpy as np

import pyaudio
import wave
import keyboard

OUTPUT_FILENAME = "audio.wav"
def record_audio():

    # Audio settings
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100  # Sampling rate
    CHUNK = 1024

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    print("Recording... Press 'q' to stop.")

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)
            if keyboard.is_pressed('q'):  # Press 'q' to stop recording
                print("Recording stopped.")
                break
    except KeyboardInterrupt:
        print("Recording stopped manually.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save recorded audio
    with wave.open(OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def add_static_image_to_audio(output_path):
    """Create and save a video file to `output_path` after 
    combining a static image that is located in `image_path` 
    with an audio file in `audio_path`"""
    # create the image clip object
    img = ImageGrab.grabclipboard()
    if img is None:
        raise Exception("No image found in the clipboard")
    img = np.array(img)
    image_clip = ImageClip(img)

    # create the audio clip object
    record_audio()
    audio_path = f"./{OUTPUT_FILENAME}"
    audio_clip = AudioFileClip(audio_path)

    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.with_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path)
    audio_clip.close()
    video_clip.close()

image_path = "./caesar.jpeg"
audio_path = "./caesar-ost.mp3"
output_path = "./result.mp4"

add_static_image_to_audio(output_path)