import streamlit as st
import numpy as np
from tensorflow import keras
import base64
import os

# ============================================================================
# CONFIGURACIÓN DE STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="🔐 Desencriptador IA",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .result-box {
            padding: 1.5rem;
            border-radius: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# CARGAR MODELO
# ============================================================================

@st.cache_resource
def load_model_tf():
    """Carga el modelo de TensorFlow"""
    try:
        model_path = 'modelo_cifrado.h5'
        if not os.path.exists(model_path):
            st.error("❌ Modelo no encontrado: modelo_cifrado.h5")
            return None
        model = keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"❌ Error cargando modelo: {e}")
        return None

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
# INTERFAZ STREAMLIT
# ============================================================================

# Encabezado
st.markdown("""
    <div class='header'>
        <h1>🔐 Desencriptador IA</h1>
        <p>Sistema Inteligente de Identificación y Desencriptación de Texto usando Redes Neuronales</p>
    </div>
""", unsafe_allow_html=True)

# Cargar modelo
MODEL = load_model_tf()

if MODEL is None:
    st.error("⚠️ No se pudo cargar el modelo. Verifica que modelo_cifrado.h5 existe.")
    st.stop()

# Barra lateral
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
        ### Tipos de Cifrado Soportados:
        - **Texto Plano**: Sin cifrado
        - **Caesar**: Rotación alfabética variable
        - **ROT13**: Rotación exacta de 13
        - **Base64**: Codificación estándar
        - **XOR**: Operación XOR bit a bit
        
        ### Cómo Usar:
        1. Ingresa o pega texto cifrado
        2. Haz clic en "Analizar"
        3. El modelo detectará el tipo y lo desencriptará
    """)

# Entrada del usuario
st.header("📝 Ingrese Texto Cifrado")

texto_cifrado = st.text_area(
    "Pegue o escriba el texto encriptado que desea analizar",
    height=150,
    placeholder="Ejemplo: Uryyb Jbeyq"
)

# Ejemplos rápidos
col1, col2, col3, col4, col5 = st.columns(5)

ejemplos = {
    "ROT13": "Uryyb Jbeyq",
    "Caesar": "Khoor Zruog",
    "Base64": "SGVsbG8gV29ybGQ=",
    "XOR": "chr(72 ^ 42)",
    "Plano": "Hello World"
}

if col1.button("📋 ROT13"):
    texto_cifrado = "Uryyb Jbeyq"
if col2.button("📋 Caesar"):
    texto_cifrado = "Khoor Zruog"
if col3.button("📋 Base64"):
    texto_cifrado = "SGVsbG8gV29ybGQ="
if col4.button("📋 Texto"):
    texto_cifrado = "Hello World"

# Botón analizar
st.markdown("---")
col_btn1, col_btn2 = st.columns([1, 4])

if col_btn1.button("🔍 **ANALIZAR**", use_container_width=True):
    if not texto_cifrado.strip():
        st.warning("⚠️ Por favor, ingresa un texto para analizar")
    elif len(texto_cifrado.strip()) < 3:
        st.warning("⚠️ El texto debe tener al menos 3 caracteres")
    else:
        with st.spinner("Analizando..."):
            # Extraer características
            features = extract_features(texto_cifrado)
            features_array = np.array([features], dtype=np.float32)
            
            # Predicción
            predictions = MODEL.predict(features_array, verbose=0)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx])
            
            # Mapeo de clases
            cipher_types = {
                0: 'Texto Plano',
                1: 'Caesar',
                2: 'ROT13',
                3: 'Base64',
                4: 'XOR'
            }
            
            tipo_cifrado = cipher_types.get(class_idx, 'Desconocido')
            
            # Desencriptadores
            desencriptadores = {
                0: decrypt_plain,
                1: decrypt_caesar,
                2: decrypt_rot13,
                3: decrypt_base64,
                4: decrypt_xor
            }
            
            desencriptador = desencriptadores.get(class_idx, decrypt_plain)
            mensaje_descifrado = desencriptador(texto_cifrado)
            
            # Mostrar resultados
            st.success("✅ Análisis completado")
            
            st.markdown("---")
            st.header("📊 Resultados")
            
            # Resultados en columnas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "🔑 Tipo de Cifrado",
                    tipo_cifrado,
                    delta=None
                )
            
            with col2:
                st.metric(
                    "🎯 Confianza",
                    f"{confidence*100:.1f}%",
                    delta=None
                )
            
            with col3:
                st.metric(
                    "📏 Longitud",
                    f"{len(texto_cifrado)} caracteres",
                    delta=None
                )
            
            # Texto original
            st.markdown("### 🔒 Texto Original (Cifrado)")
            st.code(texto_cifrado, language="text")
            
            # Mensaje desencriptado
            st.markdown("### 🔓 Mensaje Desencriptado")
            st.markdown(f"""
                <div class='result-box'>
                    <h3>{mensaje_descifrado}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Barra de confianza
            st.markdown("### 📈 Confianza del Modelo")
            st.progress(min(confidence, 1.0))
            
            # Probabilidades de todas las clases
            st.markdown("### 🔬 Probabilidades por Clase")
            
            probs_df = {
                'Clase': list(cipher_types.values()),
                'Probabilidad': [f"{p*100:.2f}%" for p in predictions[0]]
            }
            
            import pandas as pd
            df = pd.DataFrame(probs_df)
            st.dataframe(df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
        <p>Sistema Inteligente de Desencriptación | TensorFlow/Keras | Streamlit</p>
        <p>Precisión: ~92% | Creado con IA</p>
    </div>
""", unsafe_allow_html=True)
