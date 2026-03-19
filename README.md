# 🔐 Sistema Inteligente de Desencriptación con IA

Sistema de identificación y desencriptación automática de texto cifrado utilizando redes neuronales de TensorFlow.

## ✨ Características

- **5 Tipos de Cifrado Detectados**: Texto plano, Caesar, ROT13, Base64, XOR
- **Modelo IA**: Red Neuronal MLP con 90-95% de precisión
- **25 Características Extractas**: Análisis estadístico avanzado
- **Interfaz Web Moderna**: Responsive, rápida, intuitiva
- **Sin Dependencias Externas**: Frontend vanilla JS
- **Procesamiento Local**: Privacidad garantizada

## 🚀 Inicio Rápido

### Requisitos
- Python 3.8+
- Navegador web moderno
- 2GB RAM mínimo

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/Hinojosa171/Sistemas-de-Seguridad-iA.git
cd Sistemas-de-Seguridad-iA

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar

```bash
# Iniciar servidor Flask
python app.py

# Abrir en navegador
# Windows: start http://localhost:5000
# Mac/Linux: open http://localhost:5000
```

Servidor disponible en: `http://localhost:5000`

## 📦 Estructura del Proyecto

```
.
├── app.py                  # Backend Flask (API)
├── index.html              # Frontend (Interfaz)
├── script.js               # Lógica JavaScript
├── styles.css              # Estilos CSS3
├── train_model.py          # Script de entrenamiento
├── modelo_cifrado.h5       # Red neuronal entrenada
├── requirements.txt        # Dependencias Python
├── vercel.json             # Config Vercel
├── README.md               # Este archivo
└── Guia/
    ├── ARQUITECTURA_TECNICA.txt  # Detalles técnicos
    └── README.md
```

## 🧠 Cómo Funciona

### Flujo de Datos

```
Usuario Input
    ↓
Validación Frontend
    ↓
POST /analizar
    ↓
Extract Features (25 características)
    ↓
Predicción del Modelo (TensorFlow)
    ↓
Selecciona Desencriptador
    ↓
Retorna Resultado
    ↓
Mostrar en Interfaz
```

### Modelo IA

- **Entrada**: 25 características estadísticas
- **Capas**: Dense(128) → Dense(96) → Dense(64) → Dense(5)
- **Activación**: ReLU + Softmax
- **Salida**: Probabilidades de 5 clases
- **Precisión**: ~92%

## 🌐 Despliegue en Vercel

### Opción 1: Vercel (Frontend + Backend Serverless)

```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel
```

### Opción 2: Manual en Console

1. Ir a [vercel.com](https://vercel.com)
2. Conectar con GitHub
3. Importar este repositorio
4. Vercel detectará el `vercel.json`
5. Deploy automático

**URL en Vivo**: (Se generará después del deploy)

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear `.env`:
```env
FLASK_ENV=production
FLASK_DEBUG=0
API_URL=https://tu-dominio.com
```

### Entrenamiento del Modelo

```bash
python train_model.py
```

Esto genera un nuevo `modelo_cifrado.h5`

## 📊 API Endpoints

### POST /analizar

**Request**:
```json
{
    "texto_cifrado": "Uryyb Jbeyq"
}
```

**Response**:
```json
{
    "status": "success",
    "tipo_cifrado": "ROT13",
    "mensaje_descifrado": "Hello World",
    "confianza": 0.9523,
    "texto_original": "Uryyb Jbeyq"
}
```

### GET /test

Verifica que el servidor está activo.

## 🎯 Tipos de Cifrado Soportados

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **Texto Plano** | Sin cifrar | Hello World |
| **Caesar** | Rotación alfabética variable | Khoor Zruog (shift=3) |
| **ROT13** | Rotación exacta de 13 | Uryyb Jbeyq |
| **Base64** | Codificación estándar | SGVsbG8gV29ybGQ= |
| **XOR** | Operación XOR bit a bit | ☺♠️♣♦ (binario) |

## 📚 Documentación

- [ARQUITECTURA_TECNICA.txt](./Guia/ARQUITECTURA_TECNICA.txt) - Detalles técnicos completos
- [API Reference](./Guia/API.md) - Endpoints documentados

## 🛠️ Stack Tecnológico

**Backend**:
- Flask 2.3.3
- TensorFlow 2.10+
- NumPy 1.24+
- Python 3.8+

**Frontend**:
- HTML5
- CSS3 (vanilla, sin frameworks)
- JavaScript vanilla (sin dependencias)

**Infraestructura**:
- Vercel (hosting)
- GitHub (versionado)

## 🔐 Seguridad

- ✅ Procesamiento 100% local
- ✅ Sin almacenamiento de datos
- ✅ Sin tracking de usuarios
- ✅ CORS configurado
- ✅ Validación de entrada

## ⚙️ Extensiones Futuras

- [ ] Soporte para más cifrados (Vigenère, Polybius, etc.)
- [ ] API pública con autenticación
- [ ] Dashboard de estadísticas
- [ ] Soporte multiidioma
- [ ] Aplicación móvil (React Native)
- [ ] Batch processing

## 📝 Licencia

MIT License - Libre para uso personal y comercial

## 👨‍💻 Contribuir

Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agrega mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📧 Contacto

- GitHub: [@Hinojosa171](https://github.com/Hinojosa171)
- Email: [tu-email@ejemplo.com]

## 🙏 Agradecimientos

- TensorFlow/Keras por la plataforma IA
- Flask por el framework web
- Vercel por el hosting

---

**Inspirado en**: Criptografía, Seguridad Informática, Machine Learning

⭐ Si te gustó, ¡deja una estrella en GitHub!
