import os
import json
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from tensorflow import keras
import base64
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# INICIALIZACIÓN DE FLASK
# ============================================================================

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

# ============================================================================
# CARGAR MODELO ENTRENADO
# ============================================================================

MODEL = None

def load_model():
    """Carga el modelo entrenado al inicio de la aplicación"""
    global MODEL
    try:
        MODEL = keras.models.load_model('modelo_cifrado.h5')
        logger.info("✓ Modelo cargado exitosamente: modelo_cifrado.h5")
    except Exception as e:
        logger.error(f"✗ Error cargando modelo: {e}")
        logger.warning("Por favor, ejecuta 'python train_model.py' primero para generar el modelo.")
        MODEL = None

# ============================================================================
# FUNCIONES DE DESENCRIPTACIÓN
# ============================================================================

def decrypt_caesar(text):
    """
    Intenta desencriptar Caesar cipher probando todos los shifts posibles
    Devuelve el resultado más probable
    """
    best_result = text
    best_score = 0
    
    # Palabras comunes en inglés para detectar el mejor resultado
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
        
        # Contar palabras comunes encontradas
        words = decrypted.lower().split()
        score = sum(1 for word in words if word in common_words)
        
        if score > best_score:
            best_score = score
            best_result = decrypted
    
    return best_result

def decrypt_rot13(text):
    """Desencripta ROT13 (es lo mismo que encriptar)"""
    return decrypt_caesar(text)

def decrypt_base64(text):
    """Desencripta Base64"""
    try:
        return base64.b64decode(text).decode('utf-8', errors='ignore')
    except:
        return text

def decrypt_xor(text, key=42):
    """Desencripta XOR"""
    return ''.join([chr(ord(char) ^ key) for char in text])

def decrypt_plain(text):
    """Texto plano, no requiere desencriptación"""
    return text

# ============================================================================
# FUNCIÓN DE EXTRACCIÓN DE CARACTERÍSTICAS
# ============================================================================

def extract_features(text):
    """
    Extrae 25 características mejoradas del texto para mejor discriminación
    """
    features = []
    
    if len(text) == 0:
        return np.zeros(25, dtype=np.float32)
    
    # Características básicas
    letters = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    specials = sum(1 for c in text if not c.isalnum() and not c.isspace())
    spaces = sum(1 for c in text if c.isspace())
    
    features.append(letters / len(text))              # 0: proporción letras
    features.append(digits / len(text))               # 1: proporción dígitos
    features.append(specials / len(text))             # 2: proporción especiales
    features.append(spaces / len(text))               # 3: proporción espacios
    
    # Entropía Shannon mejorada
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    entropy = 0
    for count in freq.values():
        p = count / len(text)
        entropy -= p * np.log2(p) if p > 0 else 0
    features.append(entropy / 8)                      # 4: entropía normalizada
    
    # Estadísticas de frecuencias
    char_freqs = sorted(freq.values(), reverse=True)
    if len(char_freqs) > 0:
        features.append(char_freqs[0] / len(text))    # 5: freq max char
    else:
        features.append(0)
    
    if len(char_freqs) > 1:
        features.append(char_freqs[1] / len(text))    # 6: freq 2do char
    else:
        features.append(0)
    
    features.append(len(freq) / len(text))            # 7: diversidad (chars únicos / total)
    
    # Proporción de caracteres imprimibles válidos
    printable_count = sum(1 for c in text if 32 <= ord(c) <= 126)
    features.append(printable_count / len(text))      # 8: chars imprimibles válidos
    
    # Detección de patrones Base64
    base64_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    base64_matches = sum(1 for c in text if c in base64_chars)
    features.append(base64_matches / len(text))       # 9: coincidencias Base64
    
    # Proporción de caracteres en diferentes tipos
    uppercase = sum(1 for c in text if c.isupper())
    lowercase = sum(1 for c in text if c.islower())
    
    features.append(uppercase / len(text))            # 10: proporción mayúsculas
    features.append(lowercase / len(text))            # 11: proporción minúsculas
    
    # Varianza de frecuencias (patrón uniforme vs no uniforme)
    if len(char_freqs) > 1:
        avg_freq = np.mean(char_freqs)
        variance = np.var(char_freqs)
        features.append(variance / (avg_freq ** 2) if avg_freq > 0 else 0)  # 12: CV frecuencias
    else:
        features.append(0)
    
    # Números de control ASCII (caracteres especiales raros)
    control_chars = sum(1 for c in text if ord(c) < 32 or ord(c) > 126)
    features.append(control_chars / len(text))        # 13: caracteres control
    
    # Proporción de =, +, / (típicos en Base64)
    padding_chars = sum(1 for c in text if c in '=+/')
    features.append(padding_chars / len(text))        # 14: padding/encoding chars
    
    # Longitud normalizada (diferentes características para textos cortos vs largos)
    features.append(min(len(text) / 50, 1.0))         # 15: longitud relativa
    
    # Proporción de secuencias alfabéticas (ROT13, Caesar vs random)
    alpha_sequences = 0
    for i in range(len(text) - 1):
        if text[i].isalpha() and text[i+1].isalpha():
            alpha_sequences += 1
    features.append(alpha_sequences / len(text) if len(text) > 1 else 0)  # 16: secuencias alfa
    
    # Proporción de vocales vs consonantes (muy diferente en texto plano vs cifrado)
    vowels = sum(1 for c in text.lower() if c in 'aeiou')
    consonants = sum(1 for c in text.lower() if c.isalpha() and c not in 'aeiou')
    features.append(vowels / len(text))               # 17: proporción vocales
    features.append(consonants / len(text))           # 18: proporción consonantes
    
    # Ratio vocales / consonantes (muy característico del idioma)
    if consonants > 0:
        features.append(vowels / consonants)          # 19: ratio vocal/consonante
    else:
        features.append(0)
    
    # Proporción de caracteres ASCII altos (128-255) - típicos en XOR mal manejado
    high_ascii = sum(1 for c in text if ord(c) > 127)
    features.append(high_ascii / len(text))           # 20: ASCII alto
    
    # Número de espacios únicos en posiciones específicas
    if ' ' in text:
        features.append(1.0)                          # 21: tiene espacios
    else:
        features.append(0)
    
    # Longitud promedio de palabras (texto plano tiene palabras coherentes)
    words = text.split()
    if words:
        avg_word_len = np.mean([len(w) for w in words])
        features.append(min(avg_word_len / 15, 1.0))  # 22: longitud promedio palabras
    else:
        features.append(0)
    
    # Patrones de repetición
    repeated_chars = sum(1 for i in range(len(text)-1) if text[i] == text[i+1])
    features.append(repeated_chars / len(text))       # 23: repeticiones
    
    # Chi-cuadrado simplificado contra distribución esperada
    expected_freq = len(text) / 26  # Esperado para 26 letras del alfabeto
    chi_square = 0
    for c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        observed = sum(1 for char in text if char.lower() == c.lower())
        if expected_freq > 0:
            chi_square += ((observed - expected_freq) ** 2) / expected_freq
    features.append(min(chi_square / 100, 1.0))      # 24: chi-square normalizado
    
    return np.array(features, dtype=np.float32)

# ============================================================================
# MAPEO DE CLASIFICACIONES
# ============================================================================

CIPHER_TYPES = {
    0: "Texto plano",
    1: "Caesar",
    2: "ROT13",
    3: "Base64",
    4: "XOR"
}

DECRYPT_FUNCTIONS = {
    0: decrypt_plain,
    1: decrypt_caesar,
    2: decrypt_rot13,
    3: decrypt_base64,
    4: decrypt_xor
}

# ============================================================================
# RUTAS DE LA API
# ============================================================================

@app.route('/', methods=['GET'])
def home():
    """Ruta principal - sirve el archivo index.html"""
    return send_from_directory('.', 'index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    """
    Endpoint principal para analizar y desencriptar texto
    
    Recibe JSON con:
    {
        "texto_cifrado": "texto encriptado aquí"
    }
    
    Devuelve JSON con:
    {
        "tipo_cifrado": "Nombre del cifrado detectado",
        "mensaje_descifrado": "Texto desencriptado",
        "confianza": 0.95,
        "status": "success"
    }
    """
    try:
        # Verificar que el modelo está cargado
        if MODEL is None:
            return jsonify({
                'status': 'error',
                'mensaje': 'Modelo no cargado. Por favor, ejecuta train_model.py primero.'
            }), 500
        
        # Obtener datos de la petición
        data = request.get_json()
        
        if not data or 'texto_cifrado' not in data:
            return jsonify({
                'status': 'error',
                'mensaje': 'Se requiere un campo "texto_cifrado" en el JSON'
            }), 400
        
        texto_cifrado = data['texto_cifrado']
        
        if not texto_cifrado or len(texto_cifrado.strip()) == 0:
            return jsonify({
                'status': 'error',
                'mensaje': 'El texto cifrado no puede estar vacío'
            }), 400
        
        # Extraer características
        features = extract_features(texto_cifrado)
        
        # Realizar predicción
        features_batch = np.expand_dims(features, axis=0)
        predicciones = MODEL.predict(features_batch, verbose=0)
        
        # Obtener clase predicha y confianza
        clase_predicha = np.argmax(predicciones[0])
        confianza = float(predicciones[0][clase_predicha])
        
        # Obtener nombre del cifrado
        tipo_cifrado = CIPHER_TYPES.get(clase_predicha, "Desconocido")
        
        # Desencriptar usando la función correspondiente
        decrypt_func = DECRYPT_FUNCTIONS.get(clase_predicha, decrypt_plain)
        mensaje_descifrado = decrypt_func(texto_cifrado)
        
        # Devolver resultado
        return jsonify({
            'status': 'success',
            'tipo_cifrado': tipo_cifrado,
            'mensaje_descifrado': mensaje_descifrado,
            'confianza': round(confianza, 4),
            'texto_original': texto_cifrado
        })
    
    except Exception as e:
        logger.error(f"Error en /analizar: {str(e)}")
        return jsonify({
            'status': 'error',
            'mensaje': f'Error al procesar la petición: {str(e)}'
        }), 500

@app.route('/test', methods=['GET'])
def test():
    """Endpoint de prueba para verificar que el servidor está activo"""
    return jsonify({
        'status': 'ok',
        'mensaje': 'Servidor activo y funcionando',
        'modelo_cargado': MODEL is not None
    })

@app.route('/styles.css', methods=['GET'])
def serve_css():
    """Sirve el archivo CSS"""
    return send_from_directory('.', 'styles.css')

@app.route('/script.js', methods=['GET'])
def serve_js():
    """Sirve el archivo JavaScript"""
    return send_from_directory('.', 'script.js')

# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Manejo de rutas no encontradas"""
    return jsonify({
        'status': 'error',
        'mensaje': 'Ruta no encontrada. Usa POST /analizar'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores internos"""
    return jsonify({
        'status': 'error',
        'mensaje': 'Error interno del servidor'
    }), 500

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("INICIANDO SERVIDOR DE DESENCRIPTACIÓN CON IA")
    print("=" * 70)
    
    # Cargar modelo
    load_model()
    
    # Iniciar servidor
    print("\n✓ Servidor iniciado en http://localhost:5000")
    print("✓ Frontend: Abre index.html en tu navegador")
    print("✓ API: POST http://localhost:5000/analizar")
    print("\n" + "=" * 70)
    
    app.run(debug=True, port=5000, host='0.0.0.0')
