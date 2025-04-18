import nltk
import random
import json
from nltk.stem import WordNetLemmatizer

# Descargar recursos de NLTK (asegúrate de que 'wordnet' esté disponible)
nltk.download('wordnet')

# Cargar el archivo JSON con las intenciones
try:
    with open(r"C:\Users\USUARIO\Documents\Visual 2\Chat_bot\intents.json", encoding="utf-8") as file:
        intents = json.load(file)
except FileNotFoundError:
    print("Error: No se encontró el archivo 'intents.json'. Verifica la ruta.")
    exit()
except json.JSONDecodeError:
    print("Error: El archivo 'intents.json' no tiene un formato válido.")
    exit()

# Inicializar el lematizador de NLTK
lemmatizer = WordNetLemmatizer()

# Función para lematizar las palabras (llevarlas a su forma base)
def lemmatize_sentence(sentence):
    return [lemmatizer.lemmatize(word.lower()) for word in sentence.split()]

# Crear una lista de patrones y respuestas
patterns = []
responses = []
intent_tags = []

try:
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            patterns.append(pattern.lower())  # Convertir patrones a minúsculas
            responses.append(intent['responses'])
            intent_tags.append(intent['intent'])
except KeyError as e:
    print(f"Error: Falta la clave {e} en el archivo 'intents.json'.")
    exit()

# Función para encontrar la intención del usuario
def classify_intent(user_input):
    user_input_words = lemmatize_sentence(user_input.lower())  # Convertir entrada a minúsculas
    
    max_score = 0
    best_intent = None

    for i, pattern in enumerate(patterns):
        # Tokenizar y comparar palabras
        pattern_words = lemmatize_sentence(pattern)
        score = len(set(user_input_words).intersection(pattern_words)) / len(pattern_words)

        if score > max_score:
            max_score = score
            best_intent = intent_tags[i]

    return best_intent

# Función para obtener una respuesta basada en la intención
def get_response(intent):
    for i, intent_obj in enumerate(intents['intents']):
        if intent_obj.get('intent') == intent:  # Usar .get() para evitar KeyError
            return random.choice(intent_obj.get('responses', []))
    return "Lo siento, no entiendo tu intención."

# Función principal del chatbot
def chatbot():
    print("Hola, soy tu chatbot. Escribe 'salir' para finalizar.")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":  # Convertir entrada a minúsculas para comparación
            print("Chatbot: ¡Hasta luego!")
            break

        intent = classify_intent(user_input)
        if intent:
            response = get_response(intent)
        else:
            response = "Lo siento, no entiendo lo que quieres decir."
        print(f"Chatbot: {response}")

# Ejecutar el chatbot
if __name__ == "__main__":
    chatbot()