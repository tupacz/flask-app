"""Capturas de las pantallas con un Telegram simulado, en tema claro y oscuro, a ancho de teléfono.

Desde la raíz del repo, con el venv activado:
    python pruebas/vista_previa.py

Usa Microsoft Edge en modo headless y guarda los PNG en pruebas/capturas/ (ignorada por git).
El body se fija en 390px (Edge headless no baja de ~500px de ancho): si algo se desborda,
se ve a la derecha de la línea roja punteada. El rectángulo de abajo imita el MainButton.
"""
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
sys.path.insert(0, REPO)
os.environ.update({'BOT_TOKEN': '1:x', 'BOT_USERNAME': 'ClubBot', 'TELEGRAM_WEBHOOK_SECRET': 's', 'SECRET_KEY': 'k'})

from app import create_app, votos  # noqa: E402

EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
STATIC = os.path.join(REPO, 'app', 'static').replace('\\', '/')
CARPETA_TEMPORAL = tempfile.mkdtemp()

TEMAS = {
    'claro': {'bg_color': '#ffffff', 'secondary_bg_color': '#efeff4', 'section_bg_color': '#ffffff', 'text_color': '#000000',
              'hint_color': '#999999', 'subtitle_text_color': '#999999', 'section_header_text_color': '#6d6d72',
              'accent_text_color': '#2481cc', 'link_color': '#2481cc', 'button_color': '#2481cc', 'button_text_color': '#ffffff',
              'destructive_text_color': '#e53935', 'section_separator_color': '#c8c7cc'},
    'oscuro': {'bg_color': '#212121', 'secondary_bg_color': '#0f0f0f', 'section_bg_color': '#212121', 'text_color': '#ffffff',
               'hint_color': '#aaaaaa', 'subtitle_text_color': '#aaaaaa', 'section_header_text_color': '#8774e1',
               'accent_text_color': '#8774e1', 'link_color': '#8774e1', 'button_color': '#8774e1', 'button_text_color': '#ffffff',
               'destructive_text_color': '#ff595a', 'section_separator_color': '#3d3d3d'},
}

# Parecidos a los reales: títulos largos con emoji y descripciones de varias líneas
LIBROS_DE_EJEMPLO = [
    {'title': 'Rayuela', 'author': 'Julio Cortázar - 1963',
     'description': 'Horacio Oliveira deambula entre París y Buenos Aires buscando a la Maga. Se puede leer en más de un orden. (~600 páginas)'},
    {'title': 'Ficciones', 'author': 'Jorge Luis Borges - 1944',
     'description': 'Cuentos de laberintos, espejos y bibliotecas infinitas. (~200 páginas)'},
    {'title': 'El túnel', 'author': 'Ernesto Sabato - 1948',
     'description': 'Un pintor cuenta desde la cárcel por qué mató a la única persona que lo entendía. (~160 páginas)'},
    {'title': 'Cien años de soledad', 'author': 'Gabriel García Márquez - 1967',
     'description': 'Siete generaciones de los Buendía en Macondo, el pueblo que fundaron en medio de la selva. (~470 páginas)'},
    {'title': '¿Sueñan los androides con ovejas eléctricas? 🐑', 'author': 'Philip K. Dick - 1968',
     'description': 'En una Tierra devastada por la guerra nuclear, Rick Deckard caza androides fugados, casi idénticos a los humanos, que solo se delatan por su falta de empatía. (~235 páginas)'},
    {'title': 'Soy Leyenda 🧄', 'author': 'Richard Matheson - 1954',
     'description': 'Robert Neville es el último hombre en un mundo arrasado por una plaga que convirtió a todos en vampiros. (~168 páginas)'},
    {'title': 'Breakfast at Tiffany’s 💎', 'author': 'Truman Capote - 1958',
     'description': 'Holly Golightly vive de fiesta en fiesta en el Nueva York de los años cuarenta. (~160 páginas)'},
    {'title': 'La metamorfosis 🪲', 'author': 'Franz Kafka - 1915',
     'description': 'Gregor Samsa se despierta convertido en un insecto y su familia no sabe qué hacer con él. (~100 páginas)'},
]
TITULOS = [libro['title'] for libro in LIBROS_DE_EJEMPLO]

SESION_VOTANDO ={'nombre': 'Pato', 'voto': None, 'abierta': True, 'esAdmin': True}
SESION_YA_VOTO = {'nombre': 'Pato', 'abierta': True, 'esAdmin': False,
                  'voto': {'lista': TITULOS, 'fecha': '2026-11-20 21:03:11'}}
SESION_CERRADA = dict(SESION_YA_VOTO, abierta=False)

# Abre la descripción del quinto libro, para ver cómo queda desplegada
ABRIR_DESCRIPCION = """<script>setTimeout(() => document.querySelectorAll('.libro-info')[4].click(), 800);</script>"""


def armar_cliente():
    """App de Flask con libros y votos de ejemplo en una carpeta temporal, y sesión de admin."""
    votos.RUTA_VOTOS = os.path.join(CARPETA_TEMPORAL, 'data.txt')
    votos.RUTA_LIBROS = os.path.join(CARPETA_TEMPORAL, 'books.json')
    votos.RUTA_ESTADO = os.path.join(CARPETA_TEMPORAL, 'telegram.json')
    with open(votos.RUTA_LIBROS, 'w', encoding='utf-8') as f:
        json.dump(LIBROS_DE_EJEMPLO, f, ensure_ascii=False)
    with open(votos.RUTA_VOTOS, 'w', encoding='utf-8') as f:
        for i, nombre in enumerate(['Ana', 'Beto', 'Caro']):
            orden = TITULOS[i:] + TITULOS[:i]
            f.write(f"Nombre: {nombre} [tg:{i + 1}]; Lista: {orden}; fecha: 2026-11-20 21:0{i}:00\n")
    cliente = create_app().test_client()
    with cliente.session_transaction() as s:
        s['admin'] = True
    return cliente


def telegram_simulado(tema, sesion):
    """Reemplazo de telegram-web-app.js: tema, MainButton dibujado y /sesion-telegram respondido sin servidor."""
    variables = ''.join(f"--tg-theme-{k.replace('_', '-')}:{v};" for k, v in TEMAS[tema].items())
    return f"""<style>:root{{{variables}}} body{{width:390px;outline:1px dashed red}} #mb{{width:390px}}</style>
<script>
window.Telegram = {{ WebApp: {{
  initData: 'user=x', initDataUnsafe: {{}}, themeParams: {{}},
  isVersionAtLeast: () => true, ready(){{}}, expand(){{}}, disableVerticalSwipes(){{}},
  setHeaderColor(){{}}, setBackgroundColor(){{}}, setBottomBarColor(){{}},
  enableClosingConfirmation(){{}}, disableClosingConfirmation(){{}},
  BackButton: {{ show(){{}}, hide(){{}}, onClick(){{}} }},
  MainButton: {{ setParams(p){{ const b=document.createElement('div'); b.id='mb'; b.textContent=p.text;
      b.style.cssText='position:fixed;left:0;bottom:0;padding:14px;text-align:center;font:600 17px system-ui;background:var(--tg-theme-button-color);color:var(--tg-theme-button-text-color)';
      if(document.body) document.body.appendChild(b); }},
      hide(){{}}, onClick(){{}}, offClick(){{}}, showProgress(){{}}, hideProgress(){{}}, enable(){{}}, disable(){{}} }},
  HapticFeedback: {{ selectionChanged(){{}}, notificationOccurred(){{}}, impactOccurred(){{}} }},
  showAlert(t,c){{c&&c()}}, showConfirm(t,c){{c&&c(true)}},
}} }};
const _fetch = window.fetch;
window.fetch = async (url, o) => url === '/sesion-telegram'
  ? new Response(JSON.stringify({json.dumps(sesion)}), {{status: 200}})
  : _fetch(url, o);
</script>"""


def guardar_pagina(cliente, url, tema, sesion, nombre, extra=''):
    """Renderiza la página con Telegram simulado y la guarda como HTML local. Devuelve la ruta."""
    html = cliente.get(url).get_data(as_text=True)
    html = html.replace('<script src="https://telegram.org/js/telegram-web-app.js"></script>', telegram_simulado(tema, sesion or {}))
    html = html.replace('/static/', f'file:///{STATIC}/')
    html = html.replace('</body>', extra + '</body>')
    archivo = os.path.join(CARPETA_TEMPORAL, f'{nombre}.html')
    with open(archivo, 'w', encoding='utf-8') as f:
        f.write(html)
    return archivo


def edge(*argumentos):
    return subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--allow-file-access-from-files', *argumentos],
                          capture_output=True, text=True, encoding='utf-8', timeout=60)


def url_local(archivo):
    return 'file:///' + archivo.replace(os.sep, '/')


def main():
    admin = armar_cliente()
    publico = create_app().test_client()
    salida = os.path.join(AQUI, 'capturas')
    os.makedirs(salida, exist_ok=True)
    # nombre: (url, sesión que responde /sesion-telegram, html extra, cliente, votación abierta)
    paginas = {
        'votar': ('/', SESION_VOTANDO, '', admin, True),
        'votar-descripcion': ('/', SESION_VOTANDO, ABRIR_DESCRIPCION, admin, True),
        'votado': ('/', SESION_YA_VOTO, '', publico, True),
        'quienes-votaron': ('/winner', SESION_YA_VOTO, '', publico, True),
        'resultado': ('/winner', None, '', admin, True),
        'resultado-cerrada': ('/winner', SESION_CERRADA, '', publico, False),
        'libros': ('/books-manager', None, '', admin, True),
        'votos': ('/votes', None, '', admin, True),
    }
    for tema in TEMAS:
        for nombre, (url, sesion, extra, cliente, abierta) in paginas.items():
            votos.guardar_estado({'abierta': abierta})
            archivo = guardar_pagina(cliente, url, tema, sesion, f'{nombre}-{tema}', extra)
            png = os.path.join(salida, f'{nombre}-{tema}.png')
            edge('--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=500,1100',
                 '--virtual-time-budget=4000', f'--screenshot={png}', url_local(archivo))
            print(('listo  ' if os.path.exists(png) else 'FALLÓ  ') + png)


if __name__ == '__main__':
    main()
