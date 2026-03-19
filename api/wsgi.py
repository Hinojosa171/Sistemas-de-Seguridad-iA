"""
WSGI wrapper para Vercel
Permite que la aplicación Flask funcione como serverless function
"""
from app import app

# Para Vercel
if __name__ == "__main__":
    app.run()
