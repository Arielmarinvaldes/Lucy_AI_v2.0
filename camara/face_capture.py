# import cv2
# import os
# import imutils

# person = 'Anita'
# data_path = 'Data_Face'
# person_path = data_path + '/' + person

# if not os.path.exists(person_path):
#     os.makedirs(person_path)

# capture = cv2.VideoCapture('camara\\anita.mp4')

# face_classif = cv2.CascadeClassifier('camara\\haarcascade_frontalface_default.xml')
# count = 0

# while True:
#     comp, frame = capture.read()
#     if comp == False: break
#     frame = imutils.resize(frame, width=640)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     aux_frame = frame.copy()

#     faces = face_classif.detectMultiScale(gray, 1.3, 7)

#     for (x, y, w, h) in faces:
#         cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
#         face = aux_frame[y:y+h, x:x+w]
#         face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)
#         cv2.imwrite(person_path + f'/face_{count}.jpg', face)
#         count += 1
#     cv2.imshow('frame', frame)
#     key = cv2.waitKey(1)
#     if key == 27 or count >= 300:
#         break

# capture.release()
# cv2.destroyAllWindows()

import cv2
import os
import imutils
import time

def detect_faces_and_save(person, video_path, data_path='Data_Face', max_count=300):
    person_path = os.path.join(data_path, person)

    if not os.path.exists(person_path):
        os.makedirs(person_path)

    capture = cv2.VideoCapture(video_path)

    face_classif = cv2.CascadeClassifier('camara\\haarcascade_frontalface_default.xml')
    count = 0

    while True:
        comp, frame = capture.read()
        if comp is False or count >= max_count:
            break
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        aux_frame = frame.copy()

        faces = face_classif.detectMultiScale(gray, 1.3, 7)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
            face = aux_frame[y:y+h, x:x+w]
            face = cv2.resize(face, (150,150), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(os.path.join(person_path, f'face_{count}.jpg'), face)
            count += 1
        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)
        if key == 27 or count >= max_count:
            break

    capture.release()
    cv2.destroyAllWindows()

def run():
    person_name = 'Anita'
    video_file = 'camara\\anita.mp4'
    detect_faces_and_save(person_name, video_file)


# CAPTURA DE VIDEO AL COMENZAR LA APP

# Variable para llevar el seguimiento del número de videos grabados
video_count = 1

def capture_video():
    global video_count

    # Nombre del archivo de video con el número de seguimiento
    video_filename = f'camara\\video_usuario_{video_count}.avi'

    # Inicia la captura de video
    capture = cv2.VideoCapture(0)
    video_writer = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'XVID'), 25, (640, 480))
    frames_capturados = 0

    while frames_capturados < 125:  # 5 segundos a 25 fps
        ret, frame = capture.read()
        if ret:
            video_writer.write(frame)
            frames_capturados += 1

    # Libera recursos
    capture.release()
    video_writer.release()
    cv2.destroyAllWindows()  # Cierra todas las ventanas de OpenCV

    # Incrementa el contador de videos grabados
    video_count += 1
