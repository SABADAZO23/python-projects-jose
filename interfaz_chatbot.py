import tkinter as tk
from tkinter import ttk, scrolledtext
import json
import string
import unicodedata
import random
from datetime import datetime

class ChatbotInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot STEAM UNAL")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Cargar intents
        try:
            with open(r"C:\Users\USUARIO\Documents\Visual 2\Chat_bot\intents.json", encoding="utf-8") as file:
                self.intents = json.load(file)
        except Exception as e:
            print(f"Error al cargar intents: {e}")
            return

        # Crear el marco principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Área de título
        self.title_frame = ttk.Frame(self.main_frame)
        self.title_frame.pack(fill=tk.X, pady=5)
        
        self.title_label = ttk.Label(
            self.title_frame, 
            text="Chatbot STEAM UNAL",
            font=('Helvetica', 16, 'bold')
        )
        self.title_label.pack()

        # Área de chat
        self.chat_frame = ttk.Frame(self.main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Crear área de texto con scroll
        self.chat_area = scrolledtext.ScrolledText(
            self.chat_frame,
            wrap=tk.WORD,
            font=('Roboto', 11),
            bg='white'
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        # Marco para entrada y botón
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(fill=tk.X, pady=5)

        # Campo de entrada
        self.input_field = ttk.Entry(
            self.input_frame,
            font=('Roboto', 11)
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_field.bind("<Return>", self.send_message)

        # Botón de enviar
        self.send_button = ttk.Button(
            self.input_frame,
            text="Enviar",
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)

        # Mostrar mensaje inicial
        self.display_bot_message(
            "¡Hola! Soy  Locotron, tu asistente del aula STEAM.\n"
            "Puedes preguntarme sobre:\n"
            "- Las aulas STEAM\n"
            "- La Universidad Nacional\n"
            "- Impresoras 3D\n"
            "- Coordinadores y personal\n"
        )

    def limpiar_texto(self, texto):
        texto = texto.lower()
        texto = ''.join(c for c in unicodedata.normalize('NFD', texto)
                       if unicodedata.category(c) != 'Mn')
        texto = ''.join(c if c not in string.punctuation else ' ' for c in texto)
        return ' '.join(texto.split())

    def obtener_palabras_clave(self, texto):
        stop_words = {
            'que', 'cual', 'quien', 'como', 'donde', 'cuando', 'por', 'para',
            'con', 'los', 'las', 'el', 'la', 'un', 'una', 'unos', 'unas', 'y',
            'o', 'pero', 'si', 'no', 'en', 'de', 'a', 'e', 'i', 'u', 'es', 'son',
            'esta', 'estas', 'este', 'estos', 'hay', 'tiene', 'tienen', 'me',
            'te', 'se', 'mi', 'tu', 'su', 'del', 'al', 'lo', 'le'
        }
        return [p for p in self.limpiar_texto(texto).split() if p not in stop_words]

    def calcular_similitud(self, palabras_pregunta, palabras_patron):
        set_pregunta = set(palabras_pregunta)
        set_patron = set(palabras_patron)
        palabras_comunes = set_pregunta.intersection(set_patron)
        
        if not palabras_comunes:
            return 0
        
        precision = len(palabras_comunes) / len(set_patron)
        recall = len(palabras_comunes) / len(set_pregunta)
        
        if precision + recall == 0:
            return 0
        return 2 * (precision * recall) / (precision + recall)

    def encontrar_mejor_respuesta(self, pregunta):
        palabras_pregunta = self.obtener_palabras_clave(pregunta)
        mejor_score = 0
        mejor_intent = None
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                palabras_patron = self.obtener_palabras_clave(pattern)
                score = self.calcular_similitud(palabras_pregunta, palabras_patron)
                
                if score > mejor_score:
                    mejor_score = score
                    mejor_intent = intent
        
        if mejor_score < 0.2:
            return "Lo siento, no entiendo tu pregunta. ¿Podrías reformularla?"
        
        return random.choice(mejor_intent['responses'])

    def display_message(self, message, sender):
        self.chat_area.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        
        # Insertar tiempo
        self.chat_area.insert(tk.END, f"\n[{timestamp}] ")
        
        # Insertar remitente
        if sender == "user":
            self.chat_area.insert(tk.END, "Tú: ", "user")
        else:
            self.chat_area.insert(tk.END, "Locotron: ", "bot")
        
        # Insertar mensaje
        self.chat_area.insert(tk.END, f"{message}\n")
        
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def display_bot_message(self, message):
        self.display_message(message, "bot")

    def display_user_message(self, message):
        self.display_message(message, "user")

    def send_message(self, event=None):
        message = self.input_field.get().strip()
        if not message:
            return
        
        # Mostrar mensaje del usuario
        self.display_user_message(message)
        
        # Obtener y mostrar respuesta del bot
        response = self.encontrar_mejor_respuesta(message)
        self.display_bot_message(response)
        
        # Limpiar campo de entrada
        self.input_field.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = ChatbotInterface(root)
    
    # Configurar estilos
    style = ttk.Style()
    style.configure('TFrame', background='#f0f0f0')
    style.configure('TLabel', background='#f0f0f0')
    style.configure('TButton', padding=5)
    
    # Configurar tags para el chat
    app.chat_area.tag_configure("user", foreground="blue")
    app.chat_area.tag_configure("bot", foreground="green")
    
    root.mainloop()

if __name__ == "__main__":
    main() 