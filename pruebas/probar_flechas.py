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

// Mantener apretado el número con el dedo: eventos táctiles (touchstart/touchmove/touchend),
// que son los que manda un teléfono. Todos salen del elemento donde se apoyó el dedo, como en un teléfono.
window.__hapticos = [];
Telegram.WebApp.HapticFeedback.impactOccurred = (fuerza) => window.__hapticos.push(fuerza);
const esperar = (ms) => new Promise(listo => setTimeout(listo, ms));
let inicioDedo = null;
function dedo(tipo, el, dy) {
  if (tipo === 'touchstart') { const c = el.getBoundingClientRect(); inicioDedo = { x: c.left + c.width / 2, y: c.top + c.height / 2 }; }
  const punto = new Touch({ identifier: 1, target: el, clientX: inicioDedo.x, clientY: inicioDedo.y + (dy || 0) });
  const evento = new TouchEvent(tipo, { bubbles: true, cancelable: true, composed: true,
    touches: tipo === 'touchend' ? [] : [punto], targetTouches: tipo === 'touchend' ? [] : [punto], changedTouches: [punto] });
  el.dispatchEvent(evento);
  return evento;
}
const titulos = () => Array.from(document.querySelectorAll('#sortable-list .libro')).map(l => l.dataset.value);
setTimeout(async () => {
  const r = window.__resultado;
  let libro = document.querySelectorAll('.libro')[3];
  let numero = libro.querySelector('.posicion');
  r.numeroNoBloqueaElScroll = getComputedStyle(libro.querySelector('.agarre')).touchAction !== 'none';

  // Dedo quieto: a los 250 ms el libro se levanta y vibra; al soltar sin mover, baja
  dedo('touchstart', numero);
  await esperar(120);
  r.noSeLevantaAntesDeTiempo = !libro.classList.contains('libro-elegido');
  await esperar(300);
  r.seLevantaAlMantener = libro.classList.contains('libro-elegido');
  r.vibraAlLevantarse = window.__hapticos.includes('medium');
  dedo('touchend', numero);
  await esperar(80);
  r.bajaAlSoltar = !libro.classList.contains('libro-elegido');

  // Dedo que se desliza enseguida: es scroll (no se bloquea) y el libro no se levanta
  window.__hapticos.length = 0;
  dedo('touchstart', numero);
  await esperar(40);
  const deslizamiento = dedo('touchmove', numero, 30);
  r.deslizarDejaScrollear = !deslizamiento.defaultPrevented;
  await esperar(400);
  r.deslizarNoLevanta = !libro.classList.contains('libro-elegido') && window.__hapticos.length === 0;
  dedo('touchend', numero, 30);
  await esperar(80);

  // Mantener y arrastrar: el libro sigue al dedo, el scroll queda bloqueado y al soltar cambia el orden
  libro = document.querySelectorAll('.libro')[1];
  numero = libro.querySelector('.posicion');
  const titulo = libro.dataset.value;
  const alto = libro.getBoundingClientRect().height;
  dedo('touchstart', numero);
  await esperar(350);
  const primerMovimiento = dedo('touchmove', numero, 8);
  r.arrastrarBloqueaScroll = primerMovimiento.defaultPrevented;
  const posiciones = [];
  const registro = [];
  const instancia = Sortable.get(document.getElementById('sortable-list'));
  instancia.option('onMove', (e) => { registro.push('move→' + e.related.dataset.value.slice(0, 6) + (e.willInsertAfter ? '+' : '-')
    + ' dedo=' + Math.round(e.originalEvent.clientY) + ' fila=' + Math.round(e.relatedRect.top) + '..' + Math.round(e.relatedRect.bottom)
    + ' arrastrado=' + Math.round(e.draggedRect.top) + '..' + Math.round(e.draggedRect.bottom) + ' t=' + Math.round(performance.now())); });
  registro.push('inicio dedo=' + Math.round(inicioDedo.y) + ' t=' + Math.round(performance.now()));
  instancia.option('onChange', (e) => { registro.push('change ' + e.newIndex); });
  // Como un dedo real: un touchmove cada 16 ms, de a 5 px, hasta bajar 3 filas (el dedo queda en el medio de una fila)
  for (let y = 8, n = 0; y <= alto * 3; y += 5, n++) {
    dedo('touchmove', numero, y);
    await esperar(16);
    if (n % 7 === 6) {
      const clon = document.querySelector('.libro-arrastrado');
      posiciones.push(clon ? Math.round(clon.getBoundingClientRect().top) : null);
    }
  }
  dedo('touchmove', numero, alto * 3);
  r.clonSigueAlDedo = posiciones.every(p => p !== null) && posiciones.every((p, i) => i === 0 || p > posiciones[i - 1]);
  const bajoDedo = document.elementFromPoint(inicioDedo.x, inicioDedo.y + alto * 3);
  r.diagnostico = JSON.stringify({ registro: registro.slice(0, 30), bajoDedo: bajoDedo && (bajoDedo.className + ' / ' + (bajoDedo.closest('.libro') || {}).className),
    filas: Array.from(document.querySelectorAll('#sortable-list > .libro')).map(l => Math.round(l.getBoundingClientRect().top)), dedoY: Math.round(inicioDedo.y + alto * 3),
    posiciones, alto, clases:Array.from(document.querySelectorAll('#sortable-list > *')).map(e => e.className) });
  // Como una persona: el dedo queda quieto un momento en el lugar elegido y recién ahí suelta
  await esperar(300);
  dedo('touchend', numero, alto * 3);
  await esperar(400);
  r.reordenaAlSoltar = titulos().indexOf(titulo) >= 3;
  r.numerosAlDia = Array.from(document.querySelectorAll('.libro .posicion')).map(p => p.textContent).join('') === titulos().map((_, i) => i + 1).join('');
  r.nadaQuedaLevantado = !document.querySelector('.libro-elegido') && !document.querySelector('.libro-arrastrado');

  document.body.setAttribute('data-resultado', JSON.stringify(r));
}, 1500);
</script>"""


def main():
    cliente = armar_cliente()
    archivo = guardar_pagina(cliente, '/', 'claro', SESION_VOTANDO, 'flechas', extra=PRUEBA)
    salida = edge('--virtual-time-budget=12000', '--dump-dom', url_local(archivo))
    m = re.search(r'data-resultado="([^"]*)"', salida.stdout)
    if not m:
        print('La página no llegó a correr la prueba:\n' + salida.stdout[-800:])
        sys.exit(1)
    import html
    import json
    resultado = json.loads(html.unescape(m.group(1)))
    orden = resultado.pop('orden')
    diagnostico = resultado.pop('diagnostico', None)
    fallas = [nombre for nombre, ok in resultado.items() if not ok]
    if fallas and diagnostico:
        # Registro del arrastre (intercambios de SortableJS con la posición del dedo y de las filas)
        print('diagnóstico:', diagnostico)
    for nombre, ok in resultado.items():
        print(('OK    ' if ok else 'FALLA ') + nombre)
    print('orden final:', orden)
    print('TODO BIEN' if not fallas else f'{len(fallas)} FALLAS: {fallas}')
    sys.exit(1 if fallas else 0)


if __name__ == '__main__':
    main()
