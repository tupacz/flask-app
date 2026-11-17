// Página de resultados (winner.html y winner_publico.html): la boleta de quien la abre,
// las herramientas de quien organiza y el botón para cerrar o reabrir la votación.
(function () {
    const { enTelegram, fetchTelegram, avisar, confirmar, vibrar, fechaLegible } = window.App;

    function mostrarBoleta(voto) {
        const seccion = document.getElementById('tu-boleta');
        if (!seccion || !voto || !Array.isArray(voto.lista)) return;
        const ganador = seccion.dataset.ganador;
        const ol = document.getElementById('tu-boleta-lista');
        ol.innerHTML = '';
        voto.lista.forEach((titulo) => {
            const li = document.createElement('li');
            li.className = 'celda';
            li.textContent = titulo;
            if (ganador && titulo === ganador) {
                li.classList.add('es-ganador');
                const copa = document.createElement('span');
                copa.className = 'copa';
                copa.setAttribute('aria-label', 'ganador');
                copa.textContent = '🏆';
                li.appendChild(copa);
            }
            ol.appendChild(li);
        });
        document.getElementById('tu-boleta-fecha').textContent = fechaLegible(voto.fecha);
        seccion.hidden = false;
    }

    async function cargarSesion() {
        if (!enTelegram) return;
        try {
            const respuesta = await fetchTelegram('/sesion-telegram', { method: 'POST' });
            if (!respuesta.ok) return;
            const sesion = await respuesta.json();
            if (sesion.esAdmin) {
                const barra = document.getElementById('barra-admin');
                if (barra) barra.hidden = false;
            }
            mostrarBoleta(sesion.voto);
        } catch (error) {
            console.error('No se pudo cargar la sesión:', error);
        }
    }

    const botonEstado = document.getElementById('cambiar-estado');
    let cambiando = false;
    if (botonEstado) {
        botonEstado.addEventListener('click', async () => {
            if (cambiando) return;
            if (!(await confirmar(botonEstado.dataset.confirmar))) return;
            cambiando = true;
            botonEstado.disabled = true;
            try {
                const respuesta = await fetchTelegram('/estado-votacion', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ abierta: botonEstado.dataset.abrir === 'true' }),
                });
                const resultado = await respuesta.json();
                vibrar(respuesta.ok ? 'success' : 'error');
                await avisar(resultado.message || 'Hubo un error.');
                if (respuesta.ok) {
                    window.location.reload();
                    return;
                }
            } catch (error) {
                console.error('Error al cambiar el estado:', error);
                vibrar('error');
                await avisar('No se pudo conectar. Revisá tu conexión y probá de nuevo.');
            }
            cambiando = false;
            botonEstado.disabled = false;
        });
    }

    cargarSesion();
})();
