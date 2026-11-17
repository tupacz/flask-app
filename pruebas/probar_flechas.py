"""Toca las flechas ▲▼ en Edge headless y revisa orden, numeración, flechas deshabilitadas y foco.

Desde la raíz del repo, con el venv activado:
    python pruebas/probar_flechas.py
"""
import re
import sys

from vista_previa import SESION_VOTANDO, armar_cliente, edge, guardar_pagina, url_local

PRUEBA = """<script>
setTimeout(() => {
  const orden = () => Array.from(document.querySelectorAll('.libro')).map(l => l.dataset.value).join(', ');
  const numeros = () => Array.from(document.querySelectorAll('.libro .posicion')).map(p => p.textContent).join('');
  const r = {};
  const inicio = Array.from(document.querySelectorAll('.libro')).map(l => l.dataset.value);
  document.querySelector('.libro:last-child .subir').click();
  const tras1 = Array.from(document.querySelectorAll('.libro')).map(l => l.dataset.value);
  const n = inicio.length;
  r.ultimoSube = tras1[n - 2] === inicio[n - 1] && tras1[n - 1] === inicio[n - 2];
  document.querySelector('.libro:first-child .bajar').click();
  const tras2 = Array.from(document.querySelectorAll('.libro')).map(l => l.dataset.value);
  r.primeroBaja = tras2[0] === tras1[1] && tras2[1] === tras1[0];
  r.numeros = numeros() === Array.from({ length: tras2.length }, (_, i) => i + 1).join('');
  const libros = document.querySelectorAll('.libro');
  r.subirDelPrimeroDeshabilitado = libros[0].querySelector('.subir').disabled;
  r.bajarDelUltimoDeshabilitado = libros[libros.length - 1].querySelector('.bajar').disabled;
  r.medioHabilitadas = !libros[1].querySelector('.subir').disabled && !libros[1].querySelector('.bajar').disabled;
  r.focoSigueAlLibro = document.activeElement.getAttribute('aria-label') === 'Bajar ' + tras1[0];
  // Tocar el libro despliega su descripción; tocarlo de nuevo la oculta
  const info = libros[2].querySelector('.libro-info');
  const desc = libros[2].querySelector('.libro-desc');
  r.descripcionCerradaAlInicio = desc.hidden && info.getAttribute('aria-expanded') === 'false';
  info.click();
  r.descripcionSeAbre = !desc.hidden && info.getAttribute('aria-expanded') === 'true' && libros[2].classList.contains('abierto');
  r.ordenNoCambiaAlAbrir = orden() === tras2.join(', ');
  info.click();
  r.descripcionSeCierra = desc.hidden && info.getAttribute('aria-expanded') === 'false';
  r.orden = orden();
  window.__resultado = r;
}, 1000);

// Mantener apretado el número con el dedo (eventos táctiles simulados)
window.__hapticos = [];
Telegram.WebApp.HapticFeedback.impactOccurred = (fuerza) => window.__hapticos.push(fuerza);
const esperar = (ms) => new Promise(listo => setTimeout(listo, ms));
function dedo(tipo, el, dy) {
  const caja = el.getBoundingClientRect();
  const evento = new PointerEvent(tipo, { bubbles: true, cancelable: true, pointerType: 'touch', isPrimary: true, pointerId: 1,
                                         button: 0, clientX: caja.left + 10, clientY: caja.top + 10 + (dy || 0) });
  (tipo === 'pointerdown' ? el : document).dispatchEvent(evento);
}
setTimeout(async () => {
  const r = window.__resultado;
  const libro = document.querySelectorAll('.libro')[3];
  const numero = libro.querySelector('.posicion');
  r.numeroNoBloqueaElScroll = getComputedStyle(libro.querySelector('.agarre')).touchAction !== 'none';

  // Dedo quieto: a los 250 ms el libro se levanta y vibra
  dedo('pointerdown', numero);
  await esperar(120);
  r.noSeLevantaAntesDeTiempo = !libro.classList.contains('libro-elegido');
  await esperar(300);
  r.seLevantaAlMantener = libro.classList.contains('libro-elegido');
  r.vibraAlLevantarse = window.__hapticos.includes('medium');
  dedo('pointerup', numero);
  await esperar(50);
  r.bajaAlSoltar = !libro.classList.contains('libro-elegido');

  // Dedo que se desliza enseguida: es scroll, el libro no se levanta
  window.__hapticos.length = 0;
  dedo('pointerdown', numero);
  await esperar(40);
  dedo('pointermove', numero, 30);
  await esperar(400);
  r.deslizarNoLevanta = !libro.classList.contains('libro-elegido') && window.__hapticos.length === 0;
  dedo('pointerup', numero, 30);

  document.body.setAttribute('data-resultado', JSON.stringify(r));
}, 1500);
</script>"""


def main():
    cliente = armar_cliente()
    archivo = guardar_pagina(cliente, '/', 'claro', SESION_VOTANDO, 'flechas', extra=PRUEBA)
    salida = edge('--virtual-time-budget=8000', '--dump-dom', url_local(archivo))
    m = re.search(r'data-resultado="([^"]*)"', salida.stdout)
    if not m:
        print('La página no llegó a correr la prueba:\n' + salida.stdout[-800:])
        sys.exit(1)
    import html
    import json
    resultado = json.loads(html.unescape(m.group(1)))
    orden = resultado.pop('orden')
    fallas = [nombre for nombre, ok in resultado.items() if not ok]
    for nombre, ok in resultado.items():
        print(('OK    ' if ok else 'FALLA ') + nombre)
    print('orden final:', orden)
    print('TODO BIEN' if not fallas else f'{len(fallas)} FALLAS: {fallas}')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
