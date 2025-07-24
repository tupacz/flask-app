from dotenv import load_dotenv
load_dotenv()  # Cargar variables antes de importar la app

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
