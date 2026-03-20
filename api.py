"""
API REST para Desencriptador IA
Endpoints profesionales para análisis y desencriptación de texto
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from tensorflow import keras
import os
import json
from datetime import datetime

# ============================================================================
# CONFIGURACIÓN FLASK
# ============================================================================

app = Flask(__name__)
CORS(app)

# ============================================================================
# CARGAR MODELO
# ============================================================================

def load_model_tf():
    """Carga el modelo de TensorFlow"""
    try:
        model_path = 'modelo_cifrado.h5'
        if not os.path.exists(model_path):
            print("⚠️ Modelo no encontrado")
            return None
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        return None

MODEL = load_model_tf()

# Mapeo de clases
CIPHER_TYPES = {
    0: 'Plain',
    1: 'Caesar',
    2: 'ROT13',
    3: 'Base64',
    4: 'XOR'
}

# ============================================================================
# FUNCIONES DE DESENCRIPTACIÓN
# ============================================================================

def decrypt_caesar(text):
    """Intenta desencriptar Caesar cipher"""
    best_result = text
    best_score = 0
    
    common_words = {'the', 'is', 'and', 'to', 'of', 'a', 'in', 'that', 'it', 'for',
                    'was', 'with', 'be', 'have', 'this', 'from', 'at', 'by', 'on', 'are'}
    
    for shift in range(26):
        decrypted = ""
        for char in text:
            if char.isalpha():
                if char.isupper():
                    decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                else:
                    decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypted += char
        
        words = decrypted.lower().split()
        score = sum(1 for word in words if word in common_words)
        
        if score > best_score:
            best_score = score
            best_result = decrypted
    
    return best_result

def decrypt_rot13(text):
    """Desencripta ROT13"""
    return decrypt_caesar(text)

def decrypt_base64(text):
    """Desencripta Base64"""
    import base64
    try:
        return base64.b64decode(text).decode('utf-8', errors='ignore')
    except:
        return text

def decrypt_xor(text, key=42):
    """Desencripta XOR"""
    return ''.join([chr(ord(char) ^ key) for char in text])

def decrypt_plain(text):
    """Texto plano"""
    return text

# ============================================================================
# EXTRACCIÓN DE CARACTERÍSTICAS
# ============================================================================

def extract_features(text):
    """Extrae 25 características del texto"""
    features = []
    
    if len(text) == 0:
        return np.zeros(25, dtype=np.float32)
    
    letters = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    specials = sum(1 for c in text if not c.isalnum() and not c.isspace())
    spaces = sum(1 for c in text if c.isspace())
    
    features.append(letters / len(text))
    features.append(digits / len(text))
    features.append(specials / len(text))
    features.append(spaces / len(text))
    
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0
    for count in freq.values():
        p = count / len(text)
        entropy -= p * np.log2(p) if p > 0 else 0
    features.append(entropy / 8)
    
    char_freqs = sorted(freq.values(), reverse=True)
    features.append(char_freqs[0] / len(text) if len(char_freqs) > 0 else 0)
    features.append(char_freqs[1] / len(text) if len(char_freqs) > 1 else 0)
    features.append(len(freq) / len(text))
    
    printable_count = sum(1 for c in text if 32 <= ord(c) <= 126)
    features.append(printable_count / len(text))
    
    base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    base64_matches = sum(1 for c in text if c in base64_chars)
    features.append(base64_matches / len(text))
    
    uppercase = sum(1 for c in text if c.isupper())
    lowercase = sum(1 for c in text if c.islower())
    features.append(uppercase / len(text))
    features.append(lowercase / len(text))
    
    if len(char_freqs) > 1:
        avg_freq = np.mean(char_freqs)
        variance = np.var(char_freqs)
        features.append(variance / (avg_freq ** 2) if avg_freq > 0 else 0)
    else:
        features.append(0)
    
    control_chars = sum(1 for c in text if ord(c) < 32 or ord(c) > 126)
    features.append(control_chars / len(text))
    
    padding_chars = sum(1 for c in text if c in '=+/')
    features.append(padding_chars / len(text))
    
    features.append(min(len(text) / 50, 1.0))
    
    alpha_sequences = 0
    for i in range(len(text) - 1):
        if text[i].isalpha() and text[i+1].isalpha():
            alpha_sequences += 1
    features.append(alpha_sequences / len(text) if len(text) > 1 else 0)
    
    vowels = sum(1 for c in text.lower() if c in 'aeiou')
    consonants = sum(1 for c in text.lower() if c.isalpha() and c not in 'aeiou')
    features.append(vowels / len(text))
    features.append(consonants / len(text))
    
    features.append(vowels / consonants if consonants > 0 else 0)
    
    high_ascii = sum(1 for c in text if ord(c) > 127)
    features.append(high_ascii / len(text))
    
    features.append(1.0 if ' ' in text else 0)
    
    words = text.split()
    if words:
        avg_word_len = np.mean([len(w) for w in words])
        features.append(min(avg_word_len / 15, 1.0))
    else:
        features.append(0)
    
    repeated_chars = sum(1 for i in range(len(text)-1) if text[i] == text[i+1])
    features.append(repeated_chars / len(text))
    
    expected_freq = len(text) / 26
    chi_square = 0
    for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = sum(1 for char in text if char.lower() == c.lower())
        if expected_freq > 0:
            chi_square += ((observed - expected_freq) ** 2) / expected_freq
    features.append(min(chi_square / 100, 1.0))
    
    return np.array(features, dtype=np.float32)

# ============================================================================
# ENDPOINTS API
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Endpoint raíz con información de la API"""
    return jsonify({
        'nombre': 'Desencriptador IA API',
        'versión': '1.0.0',
        'descripción': 'API REST para análisis y desencriptación de texto inteligente',
        'endpoints': {
            'POST /api/analizar': 'Analiza y desencripta texto',
            'GET /api/tipos': 'Lista tipos de cifrado soportados',
            'GET /api/info': 'Información del modelo',
            'GET /api/health': 'Estado de la API'
        }
    })

@app.route('/api/analizar', methods=['POST'])
def analizar():
    """
    Endpoint principal: Analiza texto cifrado
    
    Body JSON:
    {
        "texto": "Uryyb Jbeyq"
    }
    
    Response:
    {
        "exito": true,
        "tipo_cifrado": "ROT13",
        "confianza": 0.92,
        "descifrado": "Hello World",
        "probabilidades": {...}
    }
    """
    try:
        if MODEL is None:
            return jsonify({
                'exito': False,
                'error': 'Modelo no disponible'
            }), 500
        
        datos = request.get_json()
        
        # Validaciones
        if not datos or 'texto' not in datos:
            return jsonify({
                'exito': False,
                'error': 'Campo "texto" requerido'
            }), 400
        
        texto = str(datos['texto']).strip()
        
        if len(texto) < 3:
            return jsonify({
                'exito': False,
                'error': 'El texto debe tener al menos 3 caracteres'
            }), 400
        
        # Extraer características y predecir
        features = extract_features(texto)
        features_array = np.array([features], dtype=np.float32)
        predictions = MODEL.predict(features_array, verbose=0)
        
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        # Desencriptar
        desencriptadores = {
            0: decrypt_plain,
            1: decrypt_caesar,
            2: decrypt_rot13,
            3: decrypt_base64,
            4: decrypt_xor
        }
        
        desencriptador = desencriptadores.get(class_idx, decrypt_plain)
        mensaje_descifrado = desencriptador(texto)
        
        # Preparar probabilidades
        probabilidades = {
            CIPHER_TYPES[i]: float(predictions[0][i]) 
            for i in range(len(CIPHER_TYPES))
        }
        
        return jsonify({
            'exito': True,
            'tipo_cifrado': CIPHER_TYPES[class_idx],
            'confianza': round(confidence, 4),
            'descifrado': mensaje_descifrado,
            'longitud_original': len(texto),
            'timestamp': datetime.now().isoformat(),
            'probabilidades': probabilidades
        }), 200
    
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 500

@app.route('/api/tipos', methods=['GET'])
def tipos():
    """
    Endpoint: Lista tipos de cifrado soportados
    
    Response:
    {
        "tipos": ["Plain", "Caesar", "ROT13", "Base64", "XOR"],
        "total": 5
    }
    """
    return jsonify({
        'tipos': list(CIPHER_TYPES.values()),
        'total': len(CIPHER_TYPES),
        'descripcion': {
            'Plain': 'Texto sin cifrado',
            'Caesar': 'Rotación alfabética variable',
            'ROT13': 'Rotación fija de 13 caracteres',
            'Base64': 'Codificación estándar Base64',
            'XOR': 'Operación XOR bit a bit'
        }
    }), 200

@app.route('/api/info', methods=['GET'])
def info():
    """
    Endpoint: Información del modelo
    
    Response:
    {
        "modelo": "modelo_cifrado.h5",
        "arquitectura": "Redes Neuronales (MLP)",
        "características": 25,
        "clases": 5,
        "precisión": "~92%"
    }
    """
    return jsonify({
        'modelo': 'modelo_cifrado.h5',
        'framework': 'TensorFlow/Keras',
        'arquitectura': 'Red Neuronal Multicapa (MLP)',
        'características_entrada': 25,
        'clases_salida': 5,
        'precisión_aproximada': '92%',
        'capas_ocultas': [128, 96, 64],
        'entrenamiento': 'Dataset cifrado heterogéneo',
        'archivo_disponible': os.path.exists('modelo_cifrado.h5')
    }), 200

@app.route('/api/health', methods=['GET'])
def health():
    """
    Endpoint: Verificar estado de la API
    
    Response:
    {
        "estado": "operacional",
        "modelo_cargado": true,
        "versión": "1.0.0"
    }
    """
    return jsonify({
        'estado': 'operacional' if MODEL is not None else 'error',
        'modelo_cargado': MODEL is not None,
        'versión': '1.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def no_encontrado(error):
    return jsonify({
        'exito': False,
        'error': 'Endpoint no encontrado'
    }), 404

@app.errorhandler(405)
def metodo_no_permitido(error):
    return jsonify({
        'exito': False,
        'error': 'Método HTTP no permitido'
    }), 405

# ============================================================================
# EJECUTAR
# ============================================================================

if __name__ == '__main__':
    print("🚀 Iniciando API Desencriptador IA...")
    print("📡 URL: http://localhost:5000")
    print("📚 Documentación: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
