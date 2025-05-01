# 🤟 Sistema de Reconhecimento de Gestos em LIBRAS com Feedback de Voz

Este projeto permite o reconhecimento de gestos manuais da Língua Brasileira de Sinais (LIBRAS) em tempo real, com auxílio de visão computacional, e utiliza uma assistente de voz para guiar o usuário e ler a palavra formada com os gestos.

Tal projeto rendeu um artigo sobre o tema, que pode ser lido [aqui](/docs/Promovendo%20Acessibilidade%20com%20Inteligência%20Artificial_%20Desenvolvimento%20de%20um%20Sistema%20para%20Tradução%20de%20LIBRAS.docx%20(1).pdf).

## 🧠 Tecnologias Utilizadas

- Python 3.x  
- OpenCV  
- [cvzone](https://github.com/cvzone/cvzone)  
- NumPy  
- pyttsx3 (síntese de voz)  
- TensorFlow / Keras (modelo treinado)

## 🧩 Funcionalidades

- Detecta gestos manuais da LIBRAS em tempo real.
- Classifica cada gesto e monta uma palavra.
- Feedback por voz utilizando a biblioteca `pyttsx3`.
- Interface com comandos por teclado para iniciar, limpar ou finalizar a palavra.
- Leitura em voz alta da palavra formada.

## 🎮 Controles

- `N`: Inicia a formação de uma nova palavra.  
- `P`: Pausa a captura de letras e fala a palavra formada.  
- `C`: Limpa a palavra atual.  
- `Q`: Encerra o programa.

## 📦 Requisitos

- Webcam funcional
- Python 3.7 ou superior

### Instalação de dependências

```bash
pip install opencv-python numpy pyttsx3 cvzone
```

> Observação: a biblioteca `cvzone` inclui o módulo de detecção de mãos e o classificador usado para prever a letra.

## 📁 Estrutura do Projeto

```
.
├── model/
│   ├── keras_model.h5      # Modelo treinado com Keras
│   └── labels.txt          # Rótulos das classes (letras)
├── main.py                 # Script principal com o código do sistema
└── README.md               # Este arquivo
```

## 📌 Letras Reconhecidas

Atualmente, o sistema reconhece as seguintes letras:

```
a, b, c, d, e, f, g, i, l, m, n, o, p, q, r, s, t, u, v, w, y
```

## 📤 Treinamento do Modelo

O modelo `keras_model.h5` e o arquivo `labels.txt` podem ser criados utilizando a plataforma [Teachable Machine](https://teachablemachine.withgoogle.com/) do Google. Exporte o modelo no formato Keras e salve-o na pasta `model/`.

## 🔊 Assistente de Voz

A assistente de voz é baseada em `pyttsx3`, uma biblioteca offline de texto para fala, que funciona em Windows, macOS e Linux.

## 🛠️ Execução

Após configurar o ambiente e os arquivos, basta executar:

```bash
python main.py
```
