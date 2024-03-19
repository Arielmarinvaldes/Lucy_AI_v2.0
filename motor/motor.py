import io
import speech_recognition as sr
import whisper
import tempfile
import os
from pydub import AudioSegment
from voices.voices import talk

temp_file = tempfile.mkdtemp()
save_path = os.path.join(temp_file, 'temp.wav')


listener = sr.Recognizer()


def listen():
    try:
        with sr.Microphone(sample_rate=16000) as source:
            print("Escuchando...")
            talk("Escuchando...")
            listener.adjust_for_ambient_noise(source)
            audio = listener.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format='wav')

    except Exception as e:
        print(e)
        talk("Error al escuchar")
    return save_path


def recognize_audio(save_path):
    try:
        # tiny, base, small, medium, large
        audio_model = whisper.load_model('base')
        if audio_model is not None:
            # print("No se pudo cargar el modelo de reconocimiento")
            pass
        transcription = audio_model.transcribe(
            save_path, language='es', fp16=False)
        return transcription['text']

    except Exception as e:
        print("Error in recognize_audio:", e)
        return ""
