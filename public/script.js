/**
 * Script principal para el Sistema Inteligente de Desencriptación
 * Maneja la interacción entre el usuario y el backend Flask
 */

// ============================================================================
// CONFIGURACIÓN
// ============================================================================

// Detecta si está en producción (Vercel) o desarrollo (localhost)
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const API_URL = isDevelopment ? 'http://localhost:5000' : '/api';
const ENDPOINT_ANALIZAR = `${API_URL}/analizar`;

// Elementos del DOM
const textoCifradoInput = document.getElementById('textoCifrado');
const btnAnalizar = document.getElementById('btnAnalizar');
const btnLimpiar = document.getElementById('btnLimpiar');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultadosSection = document.getElementById('resultadosSection');
const errorSection = document.getElementById('errorSection');
const btnCopiar = document.getElementById('btnCopiar');
const btnNuevoAnalisis = document.getElementById('btnNuevoAnalisis');
const btnDescartar = document.getElementById('btnDescartar');
const exampleBtns = document.querySelectorAll('.example-btn');

// ============================================================================
// FUNCIONES PRINCIPALES
// ============================================================================

/**
 * Realiza la petición al backend para analizar el texto cifrado
 */
async function analizarTexto() {
    const textoCifrado = textoCifradoInput.value.trim();
    
    // Validación
    if (!textoCifrado) {
        mostrarError('Por favor, ingresa un texto cifrado para analizar.');
        return;
    }
    
    if (textoCifrado.length < 3) {
        mostrarError('El texto debe tener al menos 3 caracteres.');
        return;
    }
    
    // Mostrar indicador de carga
    mostrarCarga();
    
    try {
        // Realizar petición POST al backend
        const response = await fetch(ENDPOINT_ANALIZAR, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                texto_cifrado: textoCifrado
            })
        });
        
        // Parsear respuesta
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.mensaje || 'Error en la respuesta del servidor');
        }
        
        if (data.status !== 'success') {
            throw new Error(data.mensaje || 'Error desconocido');
        }
        
        // Mostrar resultados
        mostrarResultados(data);
        
    } catch (error) {
        // Manejar errores
        console.error('Error:', error);
        mostrarError(`Error al conectar con el servidor: ${error.message}. 
                     Asegúrate de que el servidor Flask está ejecutándose en http://localhost:5000`);
    } finally {
        // Ocultar indicador de carga
        ocultarCarga();
    }
}

/**
 * Muestra los resultados del análisis en la página
 */
function mostrarResultados(data) {
    // Establecer valores en los elementos
    document.getElementById('tipoCifrado').textContent = data.tipo_cifrado;
    document.getElementById('mensajeDescifrado').textContent = data.mensaje_descifrado;
    document.getElementById('textoOriginal').textContent = data.texto_original;
    
    // Mostrar confianza con barra de progreso
    const confianza = Math.round(data.confianza * 100);
    document.getElementById('confidencePercent').textContent = `${confianza}%`;
    document.getElementById('confidenceFill').style.width = `${confianza}%`;
    
    // Actualizar color de la barra según confianza
    const confidenceBar = document.getElementById('confidenceFill');
    if (confianza >= 80) {
        confidenceBar.style.backgroundColor = '#4CAF50'; // Verde
    } else if (confianza >= 60) {
        confidenceBar.style.backgroundColor = '#FFC107'; // Amarillo
    } else {
        confidenceBar.style.backgroundColor = '#f44336'; // Rojo
    }
    
    // Ocultar error si había alguno
    ocultarError();
    
    // Mostrar sección de resultados
    resultadosSection.classList.remove('hidden');
    
    // Scroll suave a resultados
    resultadosSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Muestra un mensaje de error
 */
function mostrarError(mensaje) {
    document.getElementById('errorMessage').textContent = mensaje;
    errorSection.classList.remove('hidden');
    resultadosSection.classList.add('hidden');
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

/**
 * Oculta el mensaje de error
 */
function ocultarError() {
    errorSection.classList.add('hidden');
}

/**
 * Muestra el indicador de carga
 */
function mostrarCarga() {
    loadingIndicator.classList.remove('hidden');
    btnAnalizar.disabled = true;
}

/**
 * Oculta el indicador de carga
 */
function ocultarCarga() {
    loadingIndicator.classList.add('hidden');
    btnAnalizar.disabled = false;
}

/**
 * Limpia el textarea y los resultados
 */
function limpiar() {
    textoCifradoInput.value = '';
    resultadosSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    textoCifradoInput.focus();
}

/**
 * Copia el mensaje desencriptado al portapapeles
 */
function copiarMensaje() {
    const mensajeDescifrado = document.getElementById('mensajeDescifrado').textContent;
    
    if (mensajeDescifrado && mensajeDescifrado !== '-') {
        navigator.clipboard.writeText(mensajeDescifrado).then(() => {
            // Cambiar texto del botón temporalmente
            const textoOriginal = btnCopiar.innerHTML;
            btnCopiar.innerHTML = '<span>✓ ¡Copiado!</span>';
            
            setTimeout(() => {
                btnCopiar.innerHTML = textoOriginal;
            }, 2000);
        }).catch(err => {
            alert('Error al copiar al portapapeles');
        });
    }
}

/**
 * Carga un ejemplo en el textarea
 */
function cargarEjemplo(evento) {
    const ejemplo = evento.target.getAttribute('data-example');
    if (ejemplo) {
        textoCifradoInput.value = ejemplo;
        textoCifradoInput.focus();
    }
}

// ============================================================================
// EVENT LISTENERS
// ============================================================================

// Botón Analizar
btnAnalizar.addEventListener('click', analizarTexto);

// Botón Limpiar
btnLimpiar.addEventListener('click', limpiar);

// Botón Copiar
btnCopiar.addEventListener('click', copiarMensaje);

// Botón Nuevo Análisis
btnNuevoAnalisis.addEventListener('click', limpiar);

// Botón Descartar Error
btnDescartar.addEventListener('click', ocultarError);

// Permitir pulsar Enter en el textarea para analizar
textoCifradoInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
        analizarTexto();
    }
});

// Botones de ejemplos
exampleBtns.forEach(btn => {
    btn.addEventListener('click', cargarEjemplo);
});

// ============================================================================
// INICIALIZACIÓN
// ============================================================================

// Verificar conexión con el servidor al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    verificarServidor();
    textoCifradoInput.focus();
});

/**
 * Verifica que el servidor Flask está disponible
 */
async function verificarServidor() {
    try {
        const response = await fetch(`${API_URL}/test`, {
            method: 'GET'
        });
        
        if (response.ok) {
            console.log('✓ Servidor Flask conectado y activo');
        } else {
            console.warn('⚠️ Servidor Flask no está respondiendo correctamente');
            mostrarError('Advertencia: El servidor Flask puede no estar disponible. Asegúrate de ejecutar "python app.py" antes de usar la aplicación.');
        }
    } catch (error) {
        console.error('✗ Error conectando con servidor:', error);
        mostrarError(`Error: No se pudo conectar con el servidor Flask en ${API_URL}. 
                     Por favor, asegúrate de: 
                     1. Tener las dependencias instaladas (pip install -r requirements.txt)
                     2. Ejecutar el backend (python app.py)
                     3. El servidor Flask debe estar en http://localhost:5000`);
    }
}

/**
 * Manejo de errores global
 */
window.addEventListener('error', (event) => {
    console.error('Error global:', event.error);
});

// ============================================================================
// FUNCIONES AUXILIARES
// ============================================================================

/**
 * Función para debug - simular respuesta del servidor (para testing)
 */
function debugSimularRespuesta() {
    console.log('%cFunction debug available', 'color: green; font-size: 12px;');
    console.log('Use: simulateResponse() to test the app');
}

function simulateResponse() {
    const mockData = {
        status: 'success',
        tipo_cifrado: 'ROT13',
        mensaje_descifrado: 'Hello World',
        confianza: 0.95,
        texto_original: 'Uryyb Jbeyq'
    };
    
    mostrarCarga();
    setTimeout(() => {
        ocultarCarga();
        mostrarResultados(mockData);
    }, 1000);
}

// ============================================================================
// LOG DE INICIALIZACIÓN
// ============================================================================

console.log('%c=== Sistema Inteligente de Desencriptación ===', 'color: #4CAF50; font-size: 14px; font-weight: bold;');
console.log('%cBackend esperado:', 'color: #2196F3; font-weight: bold;');
console.log(`%c${API_URL}`, 'color: #FF9800; font-size: 12px;');
console.log('%cPara iniciar el servidor, ejecuta:', 'color: #2196F3; font-weight: bold;');
console.log('%cpython app.py', 'color: #FF9800; font-size: 12px;');
console.log('%cPara entrenar el modelo, ejecuta:', 'color: #2196F3; font-weight: bold;');
console.log('%cpython train_model.py', 'color: #FF9800; font-size: 12px;');
