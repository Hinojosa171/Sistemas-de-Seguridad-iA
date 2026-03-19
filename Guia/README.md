# 🔐 Sistema Inteligente de Identificación y Desencriptación de Texto usando Redes Neuronales

Un sistema web completo que utiliza inteligencia artificial para detectar automáticamente el tipo de cifrado utilizado en un texto encriptado y descifrarlo.

## 📋 Descripción General

Este proyecto combina una interfaz web interactiva, un backend API en Python con Flask, y un modelo de red neuronal entrenado para:

1. **Detectar** automáticamente qué tipo de cifrado fue utilizado en un texto
2. **Clasificar** entre 5 tipos de cifrado diferentes usando Machine Learning
3. **Desencriptar** el mensaje automáticamente según su tipo

## 🎯 Características

- 🧠 **Inteligencia Artificial**: Modelo MLP (Multilayer Perceptron) con 17 características de entrada
- 🎨 **Interfaz Moderna**: Frontend responsivo con diseño atractivo
- ⚡ **API REST**: Backend Flask con endpoint POST para análisis
- 🔒 **5 Tipos de Cifrado Soportados**:
  - Texto Plano
  - Caesar Cipher
  - ROT13
  - Base64
  - XOR
- 💻 **Todo en una Carpeta**: Estructura simple sin subcarpetas

## 📦 Estructura del Proyecto

```
sistema_seguridad_ia/
├── app.py                    # Backend Flask (API y lógica de desencriptación)
├── train_model.py            # Script para entrenar el modelo
├── index.html                # Interfaz web (HTML)
├── script.js                 # Lógica de cliente (JavaScript)
├── styles.css                # Estilos (CSS)
├── modelo_cifrado.h5         # Modelo de red neuronal entrenado
├── requirements.txt          # Dependencias de Python
└── README.md                 # Este archivo
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno

### Instalación

1. **Navega a la carpeta del proyecto**:
   ```bash
   cd c:\Users\USUARIO\Desktop\sistema_seguridad_ia
   ```

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

   Las dependencias incluyen:
   - Flask: Framework web para Python
   - Flask-CORS: Para permitir peticiones desde el frontend
   - TensorFlow/Keras: Para cargar y usar el modelo de ML
   - NumPy: Para procesamiento de datos

### Entrenamiento del Modelo (Opcional)

Si deseas reentrenar el modelo con nuevos datos:

```bash
python train_model.py
```

Este script:
- Genera datos sintéticos para 5 clases de cifrado
- Entrena una red neuronal MLP
- Guarda el modelo como `modelo_cifrado.h5`
- Toma aproximadamente 5-10 minutos

> **Nota**: El modelo ya viene preentrenado en `modelo_cifrado.h5`, así que este paso es opcional.

### Ejecución del Sistema

1. **Inicia el servidor Flask**:
   ```bash
   python app.py
   ```

   Deberías ver:
   ```
   ======================================================================
   INICIANDO SERVIDOR DE DESENCRIPTACIÓN CON IA
   ======================================================================
   ✓ Servidor iniciado en http://localhost:5000
   ✓ Frontend: Abre index.html en tu navegador
   ✓ API: POST http://localhost:5000/analizar
   ```

2. **Abre la interfaz web**:
   - Abre una nueva ventana del explorador
   - Navega a: `file:///c:/Users/USUARIO/Desktop/sistema_seguridad_ia/index.html`
   - O simplemente abre el archivo `index.html` desde tu explorador

3. **¡Listo!** Ahora puedes:
   - Escribir o pegar texto encriptado
   - Presionar "Analizar"
   - Ver los resultados instantáneamente

## 🔧 Cómo Funciona

### Flujo de Datos

```
Usuario ingresa texto cifrado (index.html)
              ↓
        script.js realiza POST
              ↓
    app.py recibe en /analizar
              ↓
      Extrae 17 características
              ↓
   Carga modelo_cifrado.h5
              ↓
  Predice tipo de cifrado (MLP)
              ↓
  Aplica función de desencriptación
              ↓
   Devuelve JSON con resultados
              ↓
  script.js muestra resultados
```

### Características del Modelo (17 features)

1. Proporción de letras
2. Proporción de dígitos
3. Proporción de caracteres especiales
4. Entropía Shannon
5-16. Frecuencia relativa de 12 caracteres más comunes
17. Longitud normalizada

## 📊 Arquitectura del Modelo

```
Entradas (17 features)
     ↓
Capa densa: 64 neuronas + ReLU
     ↓
Dropout: 0.3
     ↓
Capa densa: 32 neuronas + ReLU  
     ↓
Dropout: 0.3
     ↓
Capa salida: 5 neuronas + Softmax
     ↓
Predicción (5 clases)
```

## 🧪 Ejemplos de Prueba

### ROT13
- **Entrada**: `Uryyb Jbeyq`
- **Resultado**: `Hello World`

### Base64
- **Entrada**: `SGVsbG8gV29ybGQ=`
- **Resultado**: `Hello World`

### Caesar (Shift=3)
- **Entrada**: `Khoor Zruog`
- **Resultado**: `Hello World`

### XOR
- **Entrada**: Caracteres especiales (depende del resultado XOR)
- **Resultado**: Mensaje original

### Texto Plano
- **Entrada**: `Hello World`
- **Resultado**: `Hello World`

## 🌐 API REST

### Endpoint: POST /analizar

**URL**: `http://localhost:5000/analizar`

**Solicitud**:
```json
{
  "texto_cifrado": "Uryyb Jbeyq"
}
```

**Respuesta Exitosa** (200 OK):
```json
{
  "status": "success",
  "tipo_cifrado": "ROT13",
  "mensaje_descifrado": "Hello World",
  "confianza": 0.9523,
  "texto_original": "Uryyb Jbeyq"
}
```

**Respuesta de Error** (400/500):
```json
{
  "status": "error",
  "mensaje": "Descripción del error"
}
```

### Endpoint: GET /test

Verifica que el servidor está activo.

**Respuesta**:
```json
{
  "status": "ok",
  "mensaje": "Servidor activo y funcionando",
  "modelo_cargado": true
}
```

## 🎨 Interfaz de Usuario

### Componentes

1. **Encabezado**: Título y descripción del sistema
2. **Área de Entrada**: TextArea para pegar texto cifrado
3. **Botón Analizar**: Inicia el análisis
4. **Indicador de Carga**: Muestra mientras se analiza
5. **Sección de Resultados**:
   - Tipo de cifrado detectado
   - Barra de confianza del modelo
   - Mensaje desencriptado
   - Texto original para referencia
6. **Botones de Acción**: Copiar, nuevo análisis
7. **Sección de Información**: Guía de uso y ejemplos
8. **Botones de Ejemplo**: Para cargar ejemplos preestablecidos

## 🐛 Solución de Problemas

### Problema: "Error: No se pudo conectar con el servidor Flask"

**Solución**:
1. Asegúrate de que el servidor está ejecutándose: `python app.py`
2. Verifica que esté en el puerto 5000
3. En la consola del servidor deberías ver: `Running on http://0.0.0.0:5000`

### Problema: "Modelo no cargado"

**Solución**:
1. Verifica que `modelo_cifrado.h5` existe en la carpeta del proyecto
2. Si no existe, ejecuta: `python train_model.py`
3. Reinicia el servidor Flask

### Problema: "ModuleNotFoundError: No module named 'tensorflow'"

**Solución**:
```bash
pip install -r requirements.txt --upgrade
```

### Problema: La interfaz no muestra resultados

**Solución**:
1. Abre la consola del navegador (F12)
2. Verifica si hay errores en la pestaña Console
3. Asegúrate de que el servidor Flask está activo
4. Intenta con un exemplo preestablecido

## 📝 Código Comentado

Todos los archivos incluyen comentarios detallados:

- **app.py**: Explica cada función y endpoint
- **train_model.py**: Detalles sobre generación de datos y entrenamiento
- **script.js**: Funcionalidad de cliente claramente documentada
- **index.html**: Estructura semántica bien organizada

## 🔐 Seguridad

- El modelo se carga una sola vez al iniciar el servidor (eficiente)
- Se valida la entrada del usuario
- El frontend usa CORS para comunicarse con el backend
- No se almacenan datos sensibles

## 📈 Rendimiento

- **Tiempo de análisis**: ~100-500ms (depende del servidor)
- **Precisión del modelo**: 85-95% en casos óptimos
- **Uso de memoria**: ~150-200MB (incluyendo modelo cargado)

## 🎓 Aprendizaje

Este proyecto demuestra:

1. **Machine Learning**: Clasificación multiclase con redes neuronales
2. **Extracción de Características**: Análisis de propiedades de texto
3. **Web Development**: Fullstack con Python y JS
4. **APIs REST**: Comunicación cliente-servidor
5. **Criptografía Básica**: Implementación de algoritmos de cifrado

## 🤝 Contribuciones

Para mejorar el proyecto puedes:

1. Añadir más tipos de cifrado (Vigenère, RSA, etc.)
2. Mejorar la precisión del modelo con más datos
3. Añadir más idiomas
4. Implementar interfaz de administración
5. Crear aplicación móvil

## 📚 Referencias

- [TensorFlow/Keras Documentation](https://www.tensorflow.org/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Cryptography Algorithms](https://en.wikipedia.org/wiki/Cipher)

## 📄 Licencia

Este proyecto es de código abierto y puede ser usado libremente.

## ✨ Características Futuras

- [ ] Soporte para más idiomas
- [ ] Detección de más tipos de cifrado
- [ ] Entrenamiento online del modelo
- [ ] Histórico de análisis
- [ ] Exportación de resultados (PDF, CSV)
- [ ] Interfaz de administración
- [ ] Autenticación de usuarios
- [ ] Base de datos para logs

## 📞 Contacto y Soporte

Para preguntas o problemas:

1. Verifica la sección de "Solución de Problemas"
2. Revisa los logs de la consola del servidor
3. Abre la consola del navegador (F12) para ver errores

---

**Versión**: 1.0
**Última actualización**: Marzo 2026
**Autor**: Sistema Inteligente de Identificación y Desencriptación

¡Espero que disfrutes usando el sistema! 🚀
