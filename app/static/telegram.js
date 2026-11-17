// Integración común con Telegram para todas las páginas.
// Se carga después de telegram-web-app.js y al principio del <body>.
// Referencia: https://core.telegram.org/bots/webapps
(function () {
    const tg = window.Telegram && window.Telegram.WebApp;
    const enTelegram = Boolean(tg && tg.initData);
    const raiz = document.documentElement;
    raiz.classList.add(enTelegram ? 'en-telegram' : 'fuera-de-telegram');

    const soporta = (version) => enTelegram && tg.isVersionAtLeast(version);
    const movimientoReducido = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (enTelegram) {
        tg.ready();
        tg.expand();
        // Que arrastrar un libro hacia abajo no minimice la app
        if (soporta('7.7')) tg.disableVerticalSwipes();
        // Encabezado y barra inferior de Telegram del mismo color que el fondo de la página
        if (soporta('6.1')) {
            tg.setHeaderColor('secondary_bg_color');
            tg.setBackgroundColor('secondary_bg_color');
        }
        if (soporta('7.10')) tg.setBottomBarColor('secondary_bg_color');

        // Los botones nativos pueden quedar como los dejó la página anterior: se arranca de cero
        tg.MainButton.hide();
        if (soporta('6.2')) tg.disableClosingConfirmation();

        // En las páginas internas, el botón Atrás nativo vuelve a donde indique data-volver
        const volver = document.body && document.body.dataset.volver;
        if (soporta('6.1')) {
            if (volver) {
                tg.BackButton.show();
                tg.BackButton.onClick(() => { window.location.href = volver; });
            } else {
                tg.BackButton.hide();
            }
        }
    }

    function avisar(texto) {
        return new Promise((resolver) => {
            if (soporta('6.2')) tg.showAlert(texto, () => resolver());
            else { window.alert(texto); resolver(); }
        });
    }

    function confirmar(texto) {
        return new Promise((resolver) => {
            if (soporta('6.2')) tg.showConfirm(texto, (ok) => resolver(Boolean(ok)));
            else resolver(window.confirm(texto));
        });
    }

    // tipo: 'success' | 'error' | 'warning' | 'seleccion' | 'light' | 'medium'
    function vibrar(tipo) {
        if (!soporta('6.1')) return;
        if (tipo === 'seleccion') tg.HapticFeedback.selectionChanged();
        else if (tipo === 'success' || tipo === 'error' || tipo === 'warning') tg.HapticFeedback.notificationOccurred(tipo);
        else tg.HapticFeedback.impactOccurred(tipo || 'light');
    }

    // fetch que agrega la identidad firmada por Telegram
    function fetchTelegram(url, opciones) {
        const o = Object.assign({}, opciones);
        o.headers = Object.assign({}, o.headers, { Authorization: 'tma ' + (enTelegram ? tg.initData : '') });
        return fetch(url, o);
    }

    // Botón principal: en Telegram usa el MainButton nativo; fuera, muestra el botón HTML de respaldo.
    function botonPrincipal(texto, alTocar, botonHtml) {
        if (soporta('6.0')) {
            if (botonHtml) botonHtml.hidden = true;
            tg.MainButton.setParams({ text: texto, is_visible: true, is_active: true });
            tg.MainButton.onClick(alTocar);
            return {
                cargando(si) { si ? tg.MainButton.showProgress(false) : tg.MainButton.hideProgress(); si ? tg.MainButton.disable() : tg.MainButton.enable(); },
                ocultar() { tg.MainButton.offClick(alTocar); tg.MainButton.hide(); },
            };
        }
        if (botonHtml) {
            botonHtml.hidden = false;
            botonHtml.textContent = texto;
            botonHtml.addEventListener('click', alTocar);
        }
        return {
            cargando(si) { if (botonHtml) botonHtml.disabled = si; },
            ocultar() { if (botonHtml) { botonHtml.removeEventListener('click', alTocar); botonHtml.hidden = true; } },
        };
    }

    // '2026-06-28 22:35:19' -> '28/06 a las 22:35'
    function fechaLegible(fecha) {
        const m = /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})/.exec(fecha || '');
        return m ? `${m[3]}/${m[2]} a las ${m[4]}:${m[5]}` : (fecha || '');
    }

    window.App = { tg, enTelegram, soporta, movimientoReducido, avisar, confirmar, vibrar, fetchTelegram, botonPrincipal, fechaLegible };
})();
