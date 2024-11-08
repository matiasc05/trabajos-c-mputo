import random
import cv2
import face_recognition
import os
import tkinter as tk
from tkinter import messagebox

# Inicialización de variables globales
known_face_encodings = []
known_face_names = []
players = []
selected_friends = []

# Función para capturar la imagen del jugador
def capture_image(player_name):
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Captura de Foto")

    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            break
        cv2.imshow("Captura de Foto", frame)

        # Presionar la tecla `Enter` para capturar la foto
        if cv2.waitKey(1) & 0xFF == ord('\r'):
            img_name = player_name + ".jpg"
            cv2.imwrite(img_name, frame)
            messagebox.showinfo("Éxito", f"Foto guardada como: {img_name}")
            break

    cam.release()
    cv2.destroyAllWindows()

def recognize_face():
    cam = cv2.VideoCapture(0)
    messagebox.showinfo("Identificación", "Por favor, mire a la cámara para identificar su rostro.")

    while True:
        ret, frame = cam.read()
        if not ret:
            messagebox.showerror("Error", "No se pudo acceder a la cámara.")
            break

        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Desconocido"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                index = players.index(name)
                messagebox.showinfo("Resultado", f"{name}, le toca dar a {selected_friends[index]}")
                cam.release()
                cv2.destroyAllWindows()
                return

        cv2.imshow("Identificando", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

def add_player():
    player_name = player_name_entry.get()
    if player_name:
        players.append(player_name)
        player_name_entry.delete(0, tk.END)
        capture_image(player_name)
        
        player_image = face_recognition.load_image_file(player_name + ".jpg")
        player_face_encoding = face_recognition.face_encodings(player_image)[0]
        
        known_face_encodings.append(player_face_encoding)
        known_face_names.append(player_name)
        player_listbox.insert(tk.END, player_name)
    else:
        messagebox.showwarning("Aviso", "Ingrese un nombre de jugador")

def start_lottery():
    if len(players) < 4:
        messagebox.showwarning("Advertencia", "Debe haber al menos 4 jugadores.")
        return

    global selected_friends
    selected_friends = []
    for i in players:
        successLottery = True
        while successLottery:
            aleatorioNum = random.randint(0, len(players) - 1)
            if i == players[aleatorioNum] or players[aleatorioNum] in selected_friends:
                successLottery = True
            else:
                selected_friends.append(players[aleatorioNum])
                successLottery = False

    messagebox.showinfo("Sorteo Completado", "El sorteo del amigo secreto ha sido realizado.")

# Configuración de la ventana principal de tkinter
root = tk.Tk()
root.title("Sorteo de Amigo Secreto")
root.geometry("400x400")

# Entrada para el nombre del jugador
tk.Label(root, text="Nombre del Jugador:").pack()
player_name_entry = tk.Entry(root)
player_name_entry.pack()

# Botón para añadir jugador
add_player_button = tk.Button(root, text="Añadir Jugador", command=add_player)
add_player_button.pack()

# Lista de jugadores añadidos
tk.Label(root, text="Jugadores Añadidos:").pack()
player_listbox = tk.Listbox(root)
player_listbox.pack()

# Botón para iniciar el sorteo
start_lottery_button = tk.Button(root, text="Iniciar Sorteo", command=start_lottery)
start_lottery_button.pack()

# Botón para reconocimiento facial
recognize_face_button = tk.Button(root, text="Reconocimiento Facial", command=recognize_face)
recognize_face_button.pack()

# Iniciar la interfaz
root.mainloop()
