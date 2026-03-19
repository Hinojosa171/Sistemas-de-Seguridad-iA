📱 GUÍA DE DESPLIEGUE EN VERCEL
═════════════════════════════════════════════════════════════════════════════

Sistema Inteligente de Desencriptación - Deployment Vercel

═════════════════════════════════════════════════════════════════════════════

✨ OPCIÓN 1: DEPLOY AUTOMÁTICO (RECOMENDADO - 2 MINUTOS)
═════════════════════════════════════════════════════════════════════════════

Solo necesitas tu github account antes de proceder.

PASOS:

1. Ve a https://vercel.com

2. Haz clic en "Get Started" o "Sign In"
   - Selecciona "Continue with GitHub"
   - Autoriza Vercel en GitHub

3. Una vez en el dashboard de Vercel:
   - Haz clic en "New Project"
   - Elige "Import Git Repository"
   - Busca: "Sistemas-de-Seguridad-iA"
   - Selecciona el repositorio

4. Vercel detectará automáticamente:
   ✅ El archivo `vercel.json`
   ✅ La estructura del proyecto
   ✅ Las dependencias Python

5. Configura (OPCIONAL):
   - Project Name: (Vercel lo genera automáticamente)
   - Environment: Si necesitas variables, agrégalas aquí
   - Root Directory: ./ (por defecto está bien)

6. Haz clic en "Deploy"
   - Vercel compilará el proyecto (~2-5 minutos)
   - Instalará dependencias
   - Realizará el deploy automático

7. ¡Listo! Tu app estará disponible en:
   
   https://sistemas-de-seguridad-ia-[tuusername].vercel.app
   
   La URL exacta aparecerá después del deploy.

═════════════════════════════════════════════════════════════════════════════

✨ OPCIÓN 2: DEPLOY VIA CLI (3 MINUTOS)
═════════════════════════════════════════════════════════════════════════════

Si prefieres usar la terminal:

PASO 1: Instala Vercel CLI
──────────────────────────

Windows:
  npm install -g vercel

macOS/Linux:
  sudo npm install -g vercel

O si tienes scoop (Windows):
  scoop install vercel-cli


PASO 2: Autentica con GitHub
──────────────────────────

  vercel login
  
  - Elige "Continue with GitHub"
  - Autoriza en el navegador que se abre
  - Vuelve a la terminal (presiona Enter si es necesario)


PASO 3: Deploy del proyecto
──────────────────────────

  cd c:\Users\USUARIO\Desktop\sistema_seguridad_ia
  
  vercel
  
  Te preguntará:
  
  ✓ Set up and deploy "~/sistema_seguridad_ia"? 
    → yes (escribe: y + Enter)
  
  ✓ Which scope should contain your project?
    → Tu usuario de GitHub
  
  ✓ Link to existing project?
    → no (escribe: n + Enter)
  
  ✓ What's your project's name?
    → Presiona Enter o escribe un nombre
  
  ✓ In which directory is your code located?
    → ./ (presiona Enter)
  
  ✓ Want to override the settings?
    → no (escribe: n + Enter)

Vercel mostrará:
  
  ✓ Linked to [tu-nombre]/sistemas-de-seguridad-ia (created .vercel)
  ✓ Inspect: https://vercel.com/[tu-nombre]/sistemas-de-seguridad-ia/...
  ✓ Preview: https://sistemas-de-seguridad-ia-[aleatorio].vercel.app
  ✓ Production: https://sistemas-de-seguridad-ia.vercel.app


PASO 4: Abre tu app
──────────────────────────

  La URL production aparecerá en la terminal. Cópiala en tu navegador.


═════════════════════════════════════════════════════════════════════════════

🔧 CONFIGURACIÓN VERCEL EXPLICADA
═════════════════════════════════════════════════════════════════════════════

El archivo `vercel.json` contiene:

{
  "version": 2,                          # Versión Vercel 2 (actual)
  
  "public": true,                        # Proyecto público
  
  "buildCommand": "pip install -r requirements.txt",
                                         # Comando para instalar deps
  
  "functions": {
    "api/app.py": {
      "runtime": "python3.12"            # Runtime Python 3.12
    }
  },
  
  "rewrites": [
    "/api/(.*)": "/api/app.py",          # Rutas /api → app.py
    "/((?!api/.*).*)":: "/index.html"    # Otras rutas → index.html
  ]
}

Estos archivos se descargaron automáticamente cuando hiciste el `git push`.

═════════════════════════════════════════════════════════════════════════════

📊 ESTRUCTURA DE VERCEL
═════════════════════════════════════════════════════════════════════════════

Como quedó organizado tu proyecto para Vercel:

```
proyecto-root/
├── api/
│   ├── app.py              ← Backend Flask (serverless function)
│   ├── modelo_cifrado.h5   ← Red neuronal (cargada automáticamente)
│   └── wsgi.py             ← Wrapper para Vercel
├── public/                 ← Archivos estáticos (frontend)
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── vercel.json             ← Configuración Vercel (se procesa automáticamente)
├── .python-version         ← Versión Python recomendada
├── requirements.txt        ← Dependencias
└── modelo_cifrado.h5       ← Copia (respaldo)
```

CÓMO FUNCIONA:

1. Vercel detecta los archivos de configuración
2. Crea serverless functions de Python en `/api`
3. Sirve archivos estáticos desde `/public`
4. Ruta `/api/analizar` → Función Python
5. Ruta raíz `/` o cualquier otra → index.html (SPA)

═════════════════════════════════════════════════════════════════════════════

🚀 DESPUÉS DEL DEPLOY
═════════════════════════════════════════════════════════════════════════════

Tu aplicación estará en vivo en:

  🌐 https://sistemas-de-seguridad-ia-[tu-nombre].vercel.app

Pruébalo:

1. Abre la URL en tu navegador
2. Escribe texto cifrado (ej: "Uryyb Jbeyq")
3. Haz clic en "Analizar"
4. ¡Disfruta del desencriptador en la nube! ☁️

═════════════════════════════════════════════════════════════════════════════

⚙️ UPDATES Y CAMBIOS POSTERIORES
═════════════════════════════════════════════════════════════════════════════

Vercel Deploys Automáticamente:

Cada vez que hagas push a GitHub, Vercel:

1. ✅ Detecta automáticamente los cambios
2. ✅ Vuelve a compilar el proyecto
3. ✅ Ejecuta tests (si existen)
4. ✅ Hace el deploy automático

Simplemente haz:

  git add .
  git commit -m "tu mensaje"
  git push origin main

¡Y Vercel se encargará del resto!


ACTUALIZAR APP LOCALMENTE + PUSH:

  1. Edita el código localmente
  2. Prueba en http://localhost:5000
  3. git add .
  4. git commit -m "descripción del cambio"
  5. git push origin main
  6. Vercel deployará automáticamente 🚀


═════════════════════════════════════════════════════════════════════════════

📋 SOLUCIÓN DE PROBLEMAS
═════════════════════════════════════════════════════════════════════════════

❌ Error: "Module not found: app"
Solución: Verifica que `/api/app.py` exista y tenga la aplicación Flask

❌ Error: "TensorFlow not installed"
Solución: Verifica `requirements.txt` incluya TensorFlow>=2.10.0

❌ Error: "Model file not found"
Solución: Verifica que `modelo_cifrado.h5` esté en `/api` y en raíz

❌ API no responde
Solución: Verifica que el `script.js` use `/api` en producción (ya está configurado)

❌ Deploy falla
Solución: 
  - Revisa los logs en Vercel Dashboard
  - Verifica que el repositorio esté actualizado
  - Intenta redeploy manual en Vercel Dashboard


═════════════════════════════════════════════════════════════════════════════

💡 COSAS EXTRA (OPCIONALES)
═════════════════════════════════════════════════════════════════════════════

1. DOMINIO PERSONALIZADO

   En Vercel Dashboard:
   - Ve a tu proyecto
   - Settings → Domains
   - Agrega tu dominio
   - Sigue el setup de DNS

   Ej: https://desencriptador.tudominio.com


2. VARIABLES DE ENTORNO

   Si necesitas agregar variables (API keys, etc):
   - Vercel → Settings → Environment Variables
   - Agrega: NOMBRE_VARIABLE = valor
   - Vercel redeploy automáticamente


3. CUSTOM ANALYTICS

   Vercel incluye analytics gratuitos:
   - Dashboard → Analytics
   - Ve estadísticas de tu aplicación


4. ROLLBACK A VERSION ANTERIOR

   Si algo sale mal:
   - Vercel → Deployments
   - Haz click en una versión anterior
   - Promote to Production


═════════════════════════════════════════════════════════════════════════════

✅ CHECKLIST FINAL
═════════════════════════════════════════════════════════════════════════════

Antes de hacer deploy, verifica:

✓ Código en GitHub (https://github.com/Hinojosa171/Sistemas-de-Seguridad-iA)
✓ vercel.json existe en raíz
✓ /api/app.py existe
✓ /public/index.html existe
✓ modelo_cifrado.h5 en /api y en raíz
✓ requirements.txt tiene todas las dependencias
✓ .gitignore excluye .venv y __pycache__
✓ Los commits están en main branch


═════════════════════════════════════════════════════════════════════════════

📞 SOPORTE
═════════════════════════════════════════════════════════════════════════════

Documentación oficial Vercel:
  https://vercel.com/docs

Documentación Python en Vercel:
  https://vercel.com/docs/concepts/functions/serverless-functions/python

Comunidad Vercel Discord:
  https://discord.gg/vercel

═════════════════════════════════════════════════════════════════════════════

¡Tu aplicación estará en la nube en menos de 5 minutos! 🚀☁️

═════════════════════════════════════════════════════════════════════════════
