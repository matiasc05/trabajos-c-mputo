#Aylin Salazar, Matías Lizano, Emanuel Rojas, Diego Herrera, Matías Caballo y Samuel Morales
import os
import cv2
import numpy as np
import face_recognition as fr

def get_encoded_faces():
    """
    Escanea el directorio ./faces y codifica todas las caras encontradas.
    :return: un diccionario con nombres de archivo como claves y codificaciones de caras como valores.
    """
    encoded_faces = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(os.path.join(dirpath, f))
                encoding = fr.face_encodings(face)[0]
                encoded_faces[f.split(".")[0]] = encoding
    return encoded_faces 

def classify_face(im):
    """
    Encuentra todas las caras en una imagen dada y las etiqueta si se reconocen.
    :param im: ruta del archivo de la imagen.
    :return: lista de nombres de las caras reconocidas.
    """
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)

    face_locations = fr.face_locations(img)
    unknown_face_encodings = fr.face_encodings(img, face_locations)

    face_names = []

    for face_encoding in unknown_face_encodings:
        matches = fr.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        face_distances = fr.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(img, (left - 20, top - 20), (right + 20, bottom + 20), (255, 0, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(img, name, (left - 20, bottom + 15), font, 1.0, (255, 255, 255), 2)

    while True:
        cv2.imshow('Video', img)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.destroyAllWindows()
            return face_names

# Líneas finales para correr el programa:
print(classify_face("lonnis_1.jpg"))
print("Fin del programa")