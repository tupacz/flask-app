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

SESION_VOTANDO = {'nombre': 'Pato', 'voto': None, 'abierta': True, 'esAdmin': True}
SESION_YA_VOTO = {'nombre': 'Pato', 'abierta': True, 'esAdmin': False,
                  'voto': {'lista': ['Rayuela', 'Ficciones', 'El túnel', 'Cien años de soledad'], 'fecha': '2026-11-20 21:03:11'}}


def armar_cliente():
    """App de Flask con libros y votos de ejemplo en una carpeta temporal, y sesión de admin."""
    votos.RUTA_VOTOS = os.path.join(CARPETA_TEMPORAL, 'data.txt')
    votos.RUTA_LIBROS = os.path.join(CARPETA_TEMPORAL, 'books.json')
    votos.RUTA_ESTADO = os.path.join(CARPETA_TEMPORAL, 'telegram.json')
    with open(votos.RUTA_LIBROS, 'w', encoding='utf-8') as f:
        json.dump([
            {'title': 'Cien años de soledad', 'author': 'Gabriel García Márquez', 'description': 'La obra cumbre del realismo mágico.'},
            {'title': 'Rayuela', 'author': 'Julio Cortázar', 'description': 'Una novela que se puede leer en más de un orden.'},
            {'title': 'El túnel', 'author': 'Ernesto Sabato', 'description': 'Un pintor cuenta por qué mató a la única persona que lo entendía.'},
            {'title': 'Ficciones', 'author': 'Jorge Luis Borges', 'description': 'Cuentos de laberintos, espejos y bibliotecas infinitas.'},
        ], f, ensure_ascii=False)
    with open(votos.RUTA_VOTOS, 'w', encoding='utf-8') as f:
        f.write("Nombre: Ana [tg:1]; Lista: ['Rayuela', 'Ficciones', 'El túnel', 'Cien años de soledad']; fecha: 2026-11-20 21:03:11\n")
        f.write("Nombre: Beto [tg:2]; Lista: ['Rayuela', 'Cien años de soledad', 'Ficciones', 'El túnel']; fecha: 2026-11-20 21:05:00\n")
        f.write("Nombre: Caro [tg:3]; Lista: ['Ficciones', 'Rayuela', 'El túnel', 'Cien años de soledad']; fecha: 2026-11-20 21:07:00\n")
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
    cliente = armar_cliente()
    salida = os.path.join(AQUI, 'capturas')
    os.makedirs(salida, exist_ok=True)
    paginas = {
        'votar': ('/', SESION_VOTANDO),
        'votado': ('/', SESION_YA_VOTO),
        'resultado': ('/winner', None),
        'libros': ('/books-manager', None),
        'votos': ('/votes', None),
    }
    for tema in TEMAS:
        for nombre, (url, sesion) in paginas.items():
            archivo = guardar_pagina(cliente, url, tema, sesion, f'{nombre}-{tema}')
            png = os.path.join(salida, f'{nombre}-{tema}.png')
            edge('--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=500,1100',
                 '--virtual-time-budget=4000', f'--screenshot={png}', url_local(archivo))
            print(('listo  ' if os.path.exists(png) else 'FALLÓ  ') + png)


if __name__ == '__main__':
    main()
