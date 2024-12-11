from tkinter import *
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import pyautogui
import numpy as np

def exibir_mensagem(mensagem):
    root = Tk()
    root.attributes('-fullscreen', True)

    label = Label(root, text=mensagem, font=("Arial", 48))
    label.place(relx=0.5, rely=0.5, anchor=CENTER)

    button = Button(root, text="Quit", command=root.destroy)
    button.place(relx=0.5, rely=1, anchor=CENTER)
    
    def mostrar():
        label.config(text="Este é nosso trabalho e como ele funciona para reconhecer pessoas", font=("Arial", 32))
    
    def mostrar2():
        label.config(text="Consiste em usar um script simples em comunicação local", font=("Arial", 32))

    def mostrar3():
        label.config(text="Este trabalho ainda está de forma experimental e espero que goste do resultado", font=("Arial", 32))

    def mostrar_webcam():
        global cap
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands()
        mp_drawing = mp.solutions.drawing_utils

        prev_mouse_x, prev_mouse_y = 0, 0

        def suavizar_ponto(ponto_atual, ponto_anterior, suavidade=0.5):
            return ponto_anterior * suavidade + ponto_atual * (1 - suavidade)
        
        def count_fingers(hand_landmarks):
            finger_tips_ids = [4, 8, 12, 16, 20]
            fingers = []
            for tip_id in finger_tips_ids:
                if tip_id == 4:
                    if hand_landmarks.landmark[tip_id].x < hand_landmarks.landmark[tip_id - 1].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            return fingers
        
        def controlar_mouse(hand_landmarks, prev_hand_landmarks):
            nonlocal prev_mouse_x, prev_mouse_y

            dedo_indicador = hand_landmarks.landmark[8]
            polegar = hand_landmarks.landmark[4]

            if prev_hand_landmarks:
                dedo_indicador.x = suavizar_ponto(dedo_indicador.x, prev_hand_landmarks.landmark[8].x)
                dedo_indicador.y = suavizar_ponto(dedo_indicador.y, prev_hand_landmarks.landmark[8].y)
                polegar.x = suavizar_ponto(polegar.x, prev_hand_landmarks.landmark[4].x)
                polegar.y = suavizar_ponto(polegar.y, prev_hand_landmarks.landmark[4].y)

            distancia = ((dedo_indicador.x - polegar.x) ** 2 + (dedo_indicador.y - polegar.y) ** 2) ** 0.5

            if distancia < 0.05:
                screen_width, screen_height = pyautogui.size()
                
                mouse_x = int(dedo_indicador.x * screen_width)
                mouse_y = int(dedo_indicador.y * screen_height)

                mouse_x = int(prev_mouse_x + (mouse_x - prev_mouse_x) * 0.2)
                mouse_y = int(prev_mouse_y + (mouse_y - prev_mouse_y) * 0.2)
                
                pyautogui.moveTo(mouse_x, mouse_y)
                
                prev_mouse_x, prev_mouse_y = mouse_x, mouse_y

           
            fingers = count_fingers(hand_landmarks)
            if fingers.count(1) == 0:
                pyautogui.click()

        def atualizar_frame():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                faces = face_cascade.detectMultiScale(frame_rgb, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame_rgb, (x, y), (x+w, y+h), (255, 0, 0), 2)

                frame_rgb.flags.writeable = False
                results = hands.process(frame_rgb)
                frame_rgb.flags.writeable = True

                prev_hand_landmarks = None
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        if prev_hand_landmarks is None:
                            prev_hand_landmarks = hand_landmarks

                        mp_drawing.draw_landmarks(frame_rgb, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        fingers_up = count_fingers(hand_landmarks).count(1)
                        cv2.putText(frame_rgb, f'Dedos: {fingers_up}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        controlar_mouse(hand_landmarks, prev_hand_landmarks)

                        prev_hand_landmarks = hand_landmarks

                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                label.imgtk = imgtk
                label.configure(image=imgtk)

            label.after(10, atualizar_frame)
        
        atualizar_frame()

    root.after(2500, mostrar)
    root.after(6000, mostrar2)
    root.after(10000, mostrar3)
    root.after(15000, mostrar_webcam)  
    root.mainloop()


mensagem = "Olá! Bem-vindo ao sistema de reconhecimento."

exibir_mensagem(mensagem)
w
