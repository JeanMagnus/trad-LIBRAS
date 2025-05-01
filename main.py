import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import pyttsx3
import threading

# Inicialização da assistente de voz
engine = pyttsx3.init()
engine.setProperty('rate', 350)  # Velocidade da fala
engine.setProperty('volume', 1.0)  # Volume da fala

def speak(text):
    """Função para a assistente de voz falar uma mensagem em uma thread separada."""
    engine.say(text)
    engine.runAndWait()

# Função para falar a mensagem sem bloquear a execução do código
def speak_async(text):
    thread = threading.Thread(target=speak, args=(text,))
    thread.start()

# Mensagem inicial
speak_async("Olá! Bem-vindo ao sistema de reconhecimento de gestos. Você pode usar os seguintes comandos:")
speak_async("Pressione N para iniciar uma nova palavra.")
speak_async("Pressione P para parar de adicionar letras à palavra.")
speak_async("Pressione Q para sair do programa.")
speak_async("As letras detectadas formarão uma palavra, que será lida em voz alta quando formada.")

# Inicialização da câmera e dos módulos
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("model/keras_model.h5", "model/labels.txt")

# Configurações
offset = 20
imgSize = 300
labels = ["a", "b", "c", "d", "e", "f", "g", "i", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "y"]

# Inicializa a palavra construída e a última letra detectada
constructed_word = ""
last_letter = None
capturing_word = True  # Flag para controlar se estamos capturando a palavra ou não
finalized_word = False  # Flag para indicar que a palavra foi formada e deve ser lida

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)

    if hands and capturing_word:  # Só capturar letras se estiver "capturando a palavra"
        hand = hands[0]
        x, y, w, h = hand['bbox']

        # Criação da imagem branca e recorte da mão
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        # Obtenção da proporção e redimensionamento da imagem
        aspectRatio = h / w
        try:
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            # Classificação e exibição do resultado
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            confidence = prediction[index] * 100  # Convertendo para porcentagem

            # Adicionar a letra à palavra se for diferente da última letra e a confiança for alta
            current_letter = labels[index]
            if confidence > 90 and current_letter != last_letter:
                constructed_word += current_letter
                last_letter = current_letter

            # Exibindo letra, confiança e palavra construída no frame
            cv2.rectangle(imgOutput, (x - offset, y - offset - 50),
                          (x - offset + 200, y - offset - 50 + 50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, f'{current_letter}: {confidence:.2f}%', (x, y - 26),
                        cv2.FONT_HERSHEY_COMPLEX, 1.0, (255, 255, 255), 2)
            cv2.putText(imgOutput, f'Word: {constructed_word}', (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 1.5, (50, 255, 50), 2)

            # Desenhando o bounding box
            cv2.rectangle(imgOutput, (x - offset, y - offset),
                          (x + w + offset, y + h + offset), (255, 0, 255), 4)

            # Exibindo imagens intermediárias
            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)

        except Exception as e:
            print("Erro no processamento da imagem:", e)

    # Exibição do frame com informações
    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)

    # Limpa a palavra ao pressionar 'c' ou encerra ao pressionar 'q'
    if key == ord('c'):  # Limpa a palavra
        constructed_word = ""
        last_letter = None
        capturing_word = True  # Reinicia a captura de letras
        finalized_word = False  # Permite que a palavra seja formada novamente
        speak_async("A palavra foi limpa. Inicie a formação de uma nova palavra.")
    elif key == ord('n'):  # Inicia uma nova palavra
        constructed_word = ""
        last_letter = None
        capturing_word = True  # Reinicia a captura de letras
        finalized_word = False  # Permite que a palavra seja formada novamente
        speak_async("Iniciando uma nova palavra. Forme os gestos para começar.")
    elif key == ord('p'):  # Pausa a captura da palavra
        capturing_word = False
        finalized_word = True  # A palavra foi formada
        speak_async(f"A palavra formada foi {constructed_word}. Agora, você pode pressionar N para iniciar uma nova palavra.")
    elif key == ord('q'):  # Encerra o programa
        speak_async("Encerrando o programa. Até logo!")
        break

    # Falar a palavra formada após pressionar 'p'
    if finalized_word and constructed_word:
        speak_async(f"A palavra formada é {constructed_word}")
        finalized_word = False  # Impede que a palavra seja falada repetidamente

cap.release()
cv2.destroyAllWindows()
