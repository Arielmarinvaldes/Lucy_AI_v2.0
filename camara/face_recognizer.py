import cv2
import os
import threading as tr
import winsound
import sys
import numpy as np
import time
from voices.voices import talk


def reconocimiento(rec):
    rec = rec.replace('reconocimiento', '').strip()
    if rec == 'activado.':
        talk("Activando reconocimiento")
        face_rec(0)
    elif 'desactivado.':
        talk("Desactivando reconocimiento")
        face_rec(1)

intrusos_path = 'C:\\Users\\amval\\OneDrive\\Escritorio\\whisper-python-assistant-main\\intrusos'
data_path = 'Data_Face'

if os.path.exists(data_path):
    print("Cargando rostros de 'Data_Face'.")
else:
    print("La carpeta 'Data_Face' no se encontró en la ubicación especificada.")


# Crear el reconocedor de rostros LBPH
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

try:
    # Leyendo el modelo
    face_recognizer.read('C:\\Users\\amval\\OneDrive\\Escritorio\\whisper-python-assistant-main\\LBPHFaceModel.xml')
    print("Modelo cargado correctamente.")
except cv2.error as e:
    print(f"Error al cargar el modelo: {e}")
    


face_classif = cv2.CascadeClassifier('camara\\haarcascade_frontalface_default.xml')

def face_rec(state):
    # Inicialización de la cámara
    capture = cv2.VideoCapture(0)
    recognized = False
    unknown_detected = False

    while True:
        comp, frame = capture.read()
        if not comp:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = gray.copy()

        faces = face_classif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = aux_frame[y:y + h, x:x + w]
            face = cv2.resize(face, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(face)

            cv2.putText(frame, f'{result}', (x, y - 5), 1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)

            # LBPHFace
            if result[1] < 76:
                recognized = True
                cv2.putText(frame, f'{data_path[result[0]]}', (x, y - 25), 2, 1.1,
                            (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                nombre_rostro = data_path[result[0]]
                talk(f'Bienvenido {nombre_rostro}')
                time.sleep(2) # Agrega un retraso para permitir que el mensaje se reproduzca

            else:
                unknown_detected = True
                alarma_song(0) # Activa la alarma
                cv2.putText(frame, 'Desconocido', (x, y - 20), 1, 0.8, (0, 0, 255), 1,
                            cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                talk('Rostro Desconocido')
                
                # Tomar la foto del rostro desconocido
                img_name = f'imagen_{np.random.randint(100000)}.jpg'  # Generar un nombre aleatorio para la imagen
                img_path = os.path.join(intrusos_path, img_name)
                cv2.imwrite(img_path, frame)
                print(f"Se ha guardado la imagen del rostro desconocido: {img_name}")

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        
        if key == 27 or recognized or unknown_detected:
            break
    
    # Liberación de recursos
    capture.release()
    cv2.destroyAllWindows()
    # sys.exit()
    
    return 'reconocido' if recognized else 'desconocido'  # Retorna 'no_reconocido' cuando no se reconoce ningún rostro


def alarma_song(state):
    if state == 0:
        winsound.PlaySound("sonido\\repeating-alarm-tone-metal-detector.wav", winsound.SND_FILENAME)


def thread_alarma_song(state):
    ta = tr.Thread(target=alarma_song, args=(state,))
    ta.start()
