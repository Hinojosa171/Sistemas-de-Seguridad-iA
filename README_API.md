# 📡 Documentación API REST - Desencriptador IA

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API
```bash
python api.py
```

### 3. La API estará en
```
http://localhost:5000
```

---

## 📚 Endpoints Disponibles

### 1️⃣ Información (GET /)
Obtiene información general de la API

**URL:** `http://localhost:5000/`

**Método:** `GET`

**Response:**
```json
{
  "nombre": "Desencriptador IA API",
  "versión": "1.0.0",
  "endpoints": {...}
}
```

---

### 2️⃣ Analizar Texto (POST /api/analizar)
**Endpoint principal** - Detecta tipo de cifrado y desencripta

**URL:** `http://localhost:5000/api/analizar`

**Método:** `POST`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "texto": "Uryyb Jbeyq"
}
```

**Response (Éxito):**
```json
{
  "exito": true,
  "tipo_cifrado": "ROT13",
  "confianza": 0.9234,
  "descifrado": "Hello World",
  "longitud_original": 11,
  "timestamp": "2026-03-19T10:30:45.123456",
  "probabilidades": {
    "Plain": 0.0123,
    "Caesar": 0.0234,
    "ROT13": 0.9234,
    "Base64": 0.0234,
    "XOR": 0.0175
  }
}
```

**Ejemplos CURL:**

```bash
# ROT13
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"Uryyb Jbeyq"}'

# Caesar
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"Khoor Zruog"}'

# Base64
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"SGVsbG8gV29ybGQ="}'

# Texto Plano
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"Hello World"}'
```

---

### 3️⃣ Listar Tipos de Cifrado (GET /api/tipos)
Lista todos los tipos de cifrado soportados

**URL:** `http://localhost:5000/api/tipos`

**Método:** `GET`

**Response:**
```json
{
  "tipos": ["Plain", "Caesar", "ROT13", "Base64", "XOR"],
  "total": 5,
  "descripcion": {
    "Plain": "Texto sin cifrado",
    "Caesar": "Rotación alfabética variable",
    "ROT13": "Rotación fija de 13 caracteres",
    "Base64": "Codificación estándar Base64",
    "XOR": "Operación XOR bit a bit"
  }
}
```

**CURL:**
```bash
curl http://localhost:5000/api/tipos
```

---

### 4️⃣ Información del Modelo (GET /api/info)
Detalles técnicos del modelo de IA

**URL:** `http://localhost:5000/api/info`

**Método:** `GET`

**Response:**
```json
{
  "modelo": "modelo_cifrado.h5",
  "framework": "TensorFlow/Keras",
  "arquitectura": "Red Neuronal Multicapa (MLP)",
  "características_entrada": 25,
  "clases_salida": 5,
  "precisión_aproximada": "92%",
  "capas_ocultas": [128, 96, 64],
  "entrenamiento": "Dataset cifrado heterogéneo",
  "archivo_disponible": true
}
```

**CURL:**
```bash
curl http://localhost:5000/api/info
```

---

### 5️⃣ Health Check (GET /api/health)
Verifica que la API está operacional

**URL:** `http://localhost:5000/api/health`

**Método:** `GET`

**Response:**
```json
{
  "estado": "operacional",
  "modelo_cargado": true,
  "versión": "1.0.0",
  "timestamp": "2026-03-19T10:30:45.123456"
}
```

**CURL:**
```bash
curl http://localhost:5000/api/health
```

---

## 🔧 Uso desde JavaScript (Frontend)

### Ejemplo básico con Fetch

```javascript
async function analizarTexto(texto) {
  const response = await fetch('http://localhost:5000/api/analizar', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ texto: texto })
  });
  
  const resultado = await response.json();
  return resultado;
}

// Uso
analizarTexto('Uryyb Jbeyq').then(data => {
  console.log('Tipo:', data.tipo_cifrado);
  console.log('Confianza:', data.confianza);
  console.log('Descifrado:', data.descifrado);
});
```

### Ejemplo con React

```jsx
import React, { useState } from 'react';

function AnalizadorIA() {
  const [texto, setTexto] = useState('');
  const [resultado, setResultado] = useState(null);
  const [cargando, setCargando] = useState(false);

  async function analizar() {
    setCargando(true);
    try {
      const response = await fetch('http://localhost:5000/api/analizar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ texto })
      });
      const data = await response.json();
      setResultado(data);
    } catch (error) {
      console.error('Error:', error);
    }
    setCargando(false);
  }

  return (
    <div>
      <textarea value={texto} onChange={e => setTexto(e.target.value)} />
      <button onClick={analizar} disabled={cargando}>
        {cargando ? 'Analizando...' : 'Analizar'}
      </button>
      
      {resultado && (
        <div>
          <h3>Tipo: {resultado.tipo_cifrado}</h3>
          <p>Confianza: {(resultado.confianza * 100).toFixed(2)}%</p>
          <p>Descifrado: {resultado.descifrado}</p>
        </div>
      )}
    </div>
  );
}

export default AnalizadorIA;
```

---

## 🐍 Uso desde Python

```python
import requests

def analizar_texto(texto):
    url = 'http://localhost:5000/api/analizar'
    payload = {'texto': texto}
    
    response = requests.post(url, json=payload)
    resultado = response.json()
    
    return resultado

# Uso
resultado = analizar_texto('Uryyb Jbeyq')
print(f"Tipo: {resultado['tipo_cifrado']}")
print(f"Confianza: {resultado['confianza']}")
print(f"Descifrado: {resultado['descifrado']}")
```

---

## ⚠️ Códigos de Error

| Código | Descripción |
|--------|-------------|
| 200 | Análisis exitoso |
| 400 | Solicitud inválida (falta "texto") |
| 404 | Endpoint no encontrado |
| 405 | Método HTTP no soportado |
| 500 | Error interno del servidor |

---

## 🔒 CORS Habilitado

La API tiene CORS habilitado para permitir solicitudes desde diferentes dominios.

Para usar desde un dominio diferente:
```javascript
fetch('http://localhost:5000/api/analizar', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ texto: 'Uryyb Jbeyq' })
});
```

---

## 📊 Ejemplos de Prueba

### ROT13: "Uryyb Jbeyq"
```bash
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"Uryyb Jbeyq"}'
```

### Caesar: "Khoor Zruog"
```bash
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"Khoor Zruog"}'
```

### Base64: "SGVsbG8gV29ybGQ="
```bash
curl -X POST http://localhost:5000/api/analizar \
  -H "Content-Type: application/json" \
  -d '{"texto":"SGVsbG8gV29ybGQ="}'
```

---

## 🚀 Desplegar en Producción

Para producción, usa **Gunicorn**:

```bash
pip install gunicorn

# Ejecutar con 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 api:app
```

O con **Docker**:

```dockerfile
FROM python:3.12

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api:app"]
```

---

## 📝 Notas

- El modelo ocupa ~410MB
- TensorFlow se carga en memoria al iniciar
- Máximo 25 características extraídas por texto
- Precisión aproximada: 92%
- Tiempos de respuesta: <200ms típicamente

