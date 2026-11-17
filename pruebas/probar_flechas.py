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
  document.body.setAttribute('data-resultado', JSON.stringify(r));
}, 1500);
</script>"""


def main():
    cliente = armar_cliente()
    archivo = guardar_pagina(cliente, '/', 'claro', SESION_VOTANDO, 'flechas', extra=PRUEBA)
    salida = edge('--virtual-time-budget=5000', '--dump-dom', url_local(archivo))
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
