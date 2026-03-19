import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import base64
import string
import random

# ============================================================================
# FUNCIONES DE ENCRIPTACIÓN PARA GENERAR DATOS DE ENTRENAMIENTO
# ============================================================================

def encrypt_caesar(text, shift=3):
    """Encripta texto usando Caesar cipher"""
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += char
    return result

def encrypt_rot13(text):
    """Encripta texto usando ROT13"""
    return encrypt_caesar(text, shift=13)

def encrypt_base64(text):
    """Encripta texto usando Base64"""
    return base64.b64encode(text.encode()).decode()

def encrypt_xor(text, key=42):
    """Encripta texto usando XOR"""
    result = ""
    for char in text:
        xor_val = ord(char) ^ key
        # Evitar caracteres de control, usar valores en rango válido
        if xor_val < 32 or xor_val > 126:
            xor_val = ((xor_val - 32) % (126 - 32)) + 32
        result += chr(xor_val)
    return result

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
# GENERACIÓN DE DATOS DE ENTRENAMIENTO
# ============================================================================

def generate_training_data(samples_per_class=250, text_length=50):
    """
    Genera datos sintéticos para entrenar el modelo
    
    Clases:
    0: Texto plano
    1: Caesar
    2: ROT13
    3: Base64
    4: XOR
    """
    
    X = []
    y = []
    
    # Palabras para generar textos aleatorios
    palabras = [
        "the", "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
        "hello", "world", "python", "machine", "learning", "neural", "network",
        "security", "encryption", "algorithm", "cipher", "decode", "encode",
        "secret", "message", "invisible", "hidden", "protect", "decrypt",
        "computer", "system", "artificial", "intelligence", "data", "science"
    ]
    
    print("Generando datos de entrenamiento...")
    
    # Clase 0: Texto plano
    print(f"Clase 0: Texto plano ({samples_per_class} muestras)")
    for _ in range(samples_per_class):
        text = " ".join(random.choices(palabras, k=random.randint(4, 12)))
        features = extract_features(text)
        X.append(features)
        y.append(0)
    
    # Clase 1: Caesar (excluir shift 13 para diferenciarlo de ROT13)
    print(f"Clase 1: Caesar ({samples_per_class} muestras)")
    for _ in range(samples_per_class):
        text = " ".join(random.choices(palabras, k=random.randint(4, 12)))
        # Usar shifts que NO sean 13 (eso es ROT13)
        shift = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
        encrypted = encrypt_caesar(text, shift=shift)
        features = extract_features(encrypted)
        X.append(features)
        y.append(1)
    
    # Clase 2: ROT13
    print(f"Clase 2: ROT13 ({samples_per_class} muestras)")
    for _ in range(samples_per_class):
        text = " ".join(random.choices(palabras, k=random.randint(4, 12)))
        encrypted = encrypt_rot13(text)
        features = extract_features(encrypted)
        X.append(features)
        y.append(2)
    
    # Clase 3: Base64
    print(f"Clase 3: Base64 ({samples_per_class} muestras)")
    for _ in range(samples_per_class):
        text = " ".join(random.choices(palabras, k=random.randint(4, 12)))
        encrypted = encrypt_base64(text)
        features = extract_features(encrypted)
        X.append(features)
        y.append(3)
    
    # Clase 4: XOR
    print(f"Clase 4: XOR ({samples_per_class} muestras)")
    for _ in range(samples_per_class):
        text = " ".join(random.choices(palabras, k=random.randint(4, 12)))
        encrypted = encrypt_xor(text)
        features = extract_features(encrypted)
        X.append(features)
        y.append(4)
    
    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)

# ============================================================================
# CONSTRUCCIÓN Y ENTRENAMIENTO DEL MODELO
# ============================================================================

def build_model():
    """Construye un modelo MLP balanceado y estable"""
    model = keras.Sequential([
        # Primera capa - Input normalization
        layers.Dense(128, activation='relu', input_shape=(25,)),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        
        # Segunda capa
        layers.Dense(96, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.3),
        
        # Tercera capa
        layers.Dense(64, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.2),
        
        # Cuarta capa
        layers.Dense(48, activation='relu'),
        layers.Dropout(0.2),
        
        # Quinta capa
        layers.Dense(32, activation='relu'),
        layers.Dropout(0.1),
        
        # Capa de salida
        layers.Dense(5, activation='softmax')
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def train_and_save_model():
    """Entrena el modelo y lo guarda"""
    
    # Generar datos bien balanceados y diferenciados
    X, y = generate_training_data(samples_per_class=3000, text_length=150)
    
    # Dividir en entrenamiento y validación DESPUÉS de mezclar
    indices = np.random.permutation(len(X))
    split_idx = int(0.8 * len(X))
    
    train_indices = indices[:split_idx]
    val_indices = indices[split_idx:]
    
    X_train, X_val = X[train_indices], X[val_indices]
    y_train, y_val = y[train_indices], y[val_indices]
    
    print(f"\nDatos de entrenamiento: {X_train.shape[0]} muestras")
    print(f"Datos de validación: {X_val.shape[0]} muestras")
    
    # Construir modelo
    print("\nConstruyendo modelo...")
    model = build_model()
    
    # Entrenar con configuración mejorada
    print("Entrenando modelo con Caesar (sin shift 13) y ROT13 diferenciados...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=200,
        batch_size=64,
        verbose=1,
        shuffle=True,
        callbacks=[
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=30,
                restore_best_weights=True,
                verbose=1
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_accuracy',
                factor=0.5,
                patience=10,
                min_lr=0.00001,
                verbose=1
            )
        ]
    )
    
    # Evaluar
    print("\nEvaluando modelo...")
    test_loss, test_accuracy = model.evaluate(X_val, y_val, verbose=0)
    print(f"Precisión en validación: {test_accuracy:.4f}")
    
    # Guardar modelo
    print("\nGuardando modelo...")
    model.save('modelo_cifrado.h5')
    print("✓ Modelo guardado como 'modelo_cifrado.h5'")
    
    return model, history

if __name__ == "__main__":
    print("=" * 70)
    print("ENTRENAMIENTO DEL MODELO DE CLASIFICACIÓN DE CIFRADOS")
    print("=" * 70)
    
    model, history = train_and_save_model()
    
    print("\n" + "=" * 70)
    print("¡ENTRENAMIENTO COMPLETADO!")
    print("=" * 70)
