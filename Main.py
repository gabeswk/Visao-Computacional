from tkinter import *
import cv2
from PIL import Image, ImageTk
import mediapipe as mp
import pyautogui
import threading
import time

# Otimização extrema do PyAutoGUI
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False # Cuidado: Desativa o canto de segurança (cantos da tela)

# Variáveis globais para compartilhar dados entre a Câmera e a Janela
frame_global = None
rodando = True
detectou_mao = False

def iniciar_logica_camera():
    global frame_global, rodando, detectou_mao

    # Tenta forçar 60 FPS (depende se a webcam suporta, se não, vai no máximo possível)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60) 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    mp_hands = mp.solutions.hands
    # Agora detecta 2 mãos (max_num_hands=2)
    hands = mp_hands.Hands(
        max_num_hands=2,
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    mp_drawing = mp.solutions.drawing_utils

    # Variáveis de controle de movimento
    prev_mouse_x, prev_mouse_y = 0, 0
    screen_width, screen_height = pyautogui.size()
    
    # Controle de clique e desenho
    ultimo_clique = 0
    frame_count = 0
    faces_detectadas = []
    
    # Suavização separada para cada mão (0 e 1) se necessário, 
    # mas aqui usaremos uma global para o mouse
    landmarks_anteriores = None

    def suavizar_valor(atual, anterior, fator=0.5):
        return anterior * fator + atual * (1 - fator)

    def count_fingers(hand_landmarks):
        finger_tips_ids = [4, 8, 12, 16, 20]
        fingers = []
        
        # Polegar (lógica básica)
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Outros dedos
        for tip_id in finger_tips_ids[1:]:
            if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    while rodando:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        
        # --- LÓGICA DE ROSTO (Otimizada: Roda a cada 10 frames) ---
        if frame_count % 10 == 0:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detectadas = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(30, 30))
        
        # Desenha rostos (apenas visual, não trava o mouse)
        for (x, y, w, h) in faces_detectadas:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # --- LÓGICA DE MÃOS ---
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = hands.process(frame_rgb)
        frame_rgb.flags.writeable = True # Volta a ser desenhável

        detectou_mao = False # Reseta status

        if results.multi_hand_landmarks:
            detectou_mao = True
            
            # Itera sobre todas as mãos encontradas (máximo 2)
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                dedo_indicador = hand_landmarks.landmark[8]
                polegar = hand_landmarks.landmark[4]
                
                # --- LÓGICA DE MOVIMENTO (PINÇA) ---
                distancia = ((dedo_indicador.x - polegar.x) ** 2 + (dedo_indicador.y - polegar.y) ** 2) ** 0.5
                
                # Se fizer pinça, move o mouse
                if distancia < 0.05:
                    x_atual = dedo_indicador.x
                    y_atual = dedo_indicador.y

                    if landmarks_anteriores:
                        x_suave = suavizar_valor(x_atual, landmarks_anteriores.landmark[8].x, 0.6)
                        y_suave = suavizar_valor(y_atual, landmarks_anteriores.landmark[8].y, 0.6)
                    else:
                        x_suave, y_suave = x_atual, y_atual

                    mouse_x = int(x_suave * screen_width)
                    mouse_y = int(y_suave * screen_height)

                    # Move se houver deslocamento real
                    if abs(mouse_x - prev_mouse_x) > 3 or abs(mouse_y - prev_mouse_y) > 3:
                        try:
                            pyautogui.moveTo(mouse_x, mouse_y)
                            prev_mouse_x, prev_mouse_y = mouse_x, mouse_y
                        except:
                            pass # Evita crash se mouse sair da tela

                    # Atualiza referência para suavização
                    landmarks_anteriores = hand_landmarks

                # --- LÓGICA DE CLIQUE (MÃO FECHADA) ---
                fingers = count_fingers(hand_landmarks)
                fingers_count = fingers.count(1)

                # Feedback visual dos dedos na tela
                cv2.putText(frame, f'Dedos: {fingers_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if fingers_count == 0:
                    tempo_atual = time.time()
                    if tempo_atual - ultimo_clique > 0.6: # Delay para não dar clique duplo acidental
                        pyautogui.click()
                        ultimo_clique = tempo_atual
                        cv2.putText(frame, "CLICK!", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        # Atualiza a variável global para a interface gráfica ler
        # Convertemos para RGB aqui para o Tkinter usar depois
        frame_global = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_count += 1

    cap.release()

def exibir_mensagem(mensagem):
    root = Tk()
    root.attributes('-fullscreen', True)

    label_msg = Label(root, text=mensagem, font=("Arial", 48))
    label_msg.place(relx=0.5, rely=0.5, anchor=CENTER)

    label_video = Label(root)
    label_video.place(relx=0.5, rely=0.5, anchor=CENTER)
    label_video.place_forget()

    def fechar_app():
        global rodando
        rodando = False
        root.destroy()

    button = Button(root, text="Sair (Pressione ESC se travar)", command=fechar_app, font=("Arial", 14), bg="red", fg="white")
    button.place(relx=0.5, rely=0.95, anchor=CENTER)
    
    # Tecla de emergência para fechar
    root.bind('<Escape>', lambda e: fechar_app())

    def mostrar():
        label_msg.config(text="Reconhecimento de 2 mãos ativado.", font=("Arial", 32))
    
    def mostrar2():
        label_msg.config(text="FPS desbloqueado via Threading.", font=("Arial", 32))

    def mostrar3():
        label_msg.config(text="Iniciando câmera de alto desempenho...", font=("Arial", 32))

    def iniciar_loop_video():
        label_msg.place_forget()
        label_video.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Inicia a thread da câmera em paralelo
        t = threading.Thread(target=iniciar_logica_camera)
        t.daemon = True # Mata a thread se o programa fechar
        t.start()
        
        atualizar_interface()

    def atualizar_interface():
        # Esta função roda no loop do Tkinter e só busca a imagem pronta
        if frame_global is not None:
            img = Image.fromarray(frame_global)
            imgtk = ImageTk.PhotoImage(image=img)
            label_video.imgtk = imgtk
            label_video.configure(image=imgtk)
        
        # Tenta atualizar o mais rápido que o Tkinter conseguir (10ms)
        root.after(10, atualizar_interface)



    root.after(00, iniciar_loop_video)  
    root.mainloop()

mensagem = "Olá! Carregando Sistema Otimizado..."
exibir_mensagem(mensagem)