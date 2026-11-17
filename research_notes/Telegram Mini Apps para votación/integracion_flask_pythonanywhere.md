# Integración Flask + PythonAnywhere para convertir la app de votación en una Telegram Mini App (estado a noviembre de 2026)

Notas de método (para quien redacte el informe):

- "Verificado" significa que abrí la página fuente en esta sesión (17/11/2026). Cuando un dato viene solo de un resumen de buscador o de mi conocimiento previo lo marco como tal.
- El validador de `initData` de la sección 2 lo ejecuté localmente (Python 3.13) contra un vector de prueba público con token y hash reales y pasó. El resto del código Flask solo fue chequeado con `py_compile` (Flask no está instalado en la máquina local), no ejecutado.
- Leí el código actual del repo. Difiere de lo que dice el CLAUDE.md en dos puntos que importan acá: el admin ya no usa un `prompt()` con contraseña embebida sino `/login` con cookie de sesión de Flask (`SESSION_COOKIE_SAMESITE='Lax'`, contraseña en variable `ADMIN_PASSWORD` o `app/admin_password.txt`), y `index.html` ya guarda en `localStorage` que el dispositivo votó. `app/__init__.py` ya tiene un helper `_leer_secreto(nombre_env, archivo)` y `.gitignore` ya ignora `.env`, `app/secret_key.txt` y `app/admin_password.txt`.

## 1. ¿Cuál es la conversión mínima viable? ¿Qué funciona sin cambios y qué se rompe?

### Takeaway
La conversión mínima no requiere tocar el backend: crear un bot en @BotFather, apuntar el botón de menú o la Main Mini App a `https://tupac.pythonanywhere.com/` y agregar el `<script>` de Telegram en el `<head>`. La app sigue funcionando igual (nombre tipeado, mismo `/submit`); lo que no se gana todavía es identidad verificada, y lo que puede fallar es el gesto de arrastre contra el gesto de cerrar de Telegram.

### Cited Findings
- La página oficial hoy se titula "Telegram Mini Apps" (la URL sigue siendo `/bots/webapps` y el objeto JS sigue siendo `window.Telegram.WebApp`). Los tutoriales que hablan de "Web Apps" o "Web App Bots" son anteriores al cambio de nombre. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Inicialización: agregar en `<head>`, antes de cualquier otro script, `<script src="https://telegram.org/js/telegram-web-app.js?65"></script>`; al cargarse queda disponible `window.Telegram.WebApp`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Botón de menú: se configura en @BotFather con `/setmenubutton` o *Bot Settings > Menu Button* (texto + URL); por usuario se puede cambiar con el método `setChatMenuButton`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Main Mini App: se configura en @BotFather (*/mybots > bot > Bot Settings > Configure Mini App*). Se abre con `https://t.me/botusername?startapp`, `?startapp=command` y `&mode=compact` (media pantalla). — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Mini Apps por link directo: `https://t.me/botusername/appname` (con `?startapp=...` opcional); se pueden lanzar "in any chat" y exponen `chat_type` y `chat_instance`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Telegram documenta siete formas de lanzamiento (botón de teclado, botón inline, botón de menú, Main Mini App, modo inline, link directo, menú de adjuntos). El botón de menú se comporta igual que el botón inline: entrega datos básicos del usuario y un `query_id`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- El lanzamiento desde un botón de teclado (`KeyboardButton.web_app`) es el único que permite `sendData` y la página describe `WebAppInitData` como vacío en ese caso (igual que en modo inline). `sendData` está limitado a 4096 bytes y cierra la Mini App. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- `ready()` avisa a Telegram que la app puede mostrarse; hay que llamarlo apenas cargan los elementos esenciales, si no el placeholder se oculta recién al terminar de cargar toda la página. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- La última versión de Bot API al momento de la consulta es 10.4 (9 de noviembre de 2026); el changelog de Mini Apps que alcancé a leer llega a Bot API 10.1 (11 de junio de 2026). — [core.telegram.org/bots/api](https://core.telegram.org/bots/api), [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)

### Inferences
- Pasos mínimos concretos: (1) `/newbot` en @BotFather y guardar el token; (2) `/setmenubutton` con la URL `https://tupac.pythonanywhere.com/` y/o habilitar la Main Mini App para tener el link `https://t.me/<bot>?startapp` que se pega en el grupo del club; (3) una línea de `<script>` en `app/templates/index.html`; (4) llamar `Telegram.WebApp.ready()` y `expand()`.
- Funciona sin cambios (es una página HTTPS común dentro de un webview): el render Jinja, el `fetch('/submit')` al mismo origen, SortableJS, el CDN de jsDelivr.
- No conviene usar el botón de teclado (`KeyboardButton`) como forma de entrada: es justo el modo en el que `initData` llega vacío, así que no serviría para identificar al votante.
- Riesgos de la versión mínima: (a) el arrastre vertical puede disparar el gesto de minimizar/cerrar (ver sección 7); (b) la identidad sigue siendo el nombre tipeado, así que no mejora el control de voto único; (c) `index.html` carga `sortablejs@latest`, conviene fijar una versión para que un release nuevo no cambie el comportamiento táctil dentro del webview.
- En Telegram Web (web.telegram.org) las Mini Apps se muestran dentro de un iframe; ahí una cookie `SameSite=Lax` no viaja, por lo que el login de admin por cookie probablemente no funcione en ese cliente (sí en las apps móviles y de escritorio, donde el webview es de primer nivel). No lo verifiqué; es razonamiento sobre el comportamiento estándar de cookies.

### Gaps
- No verifiqué en un dispositivo real si `alert()` y `confirm()` nativos (que `index.html` usa hoy) funcionan en todos los clientes de Telegram; la recomendación segura es reemplazarlos por `showAlert`/`showConfirm` cuando se está dentro de Telegram (sección 8).
- No verifiqué si `localStorage` persiste entre sesiones en todos los clientes (la app lo usa para recordar "este dispositivo ya votó"). Con identidad por `user.id` deja de ser crítico.
- La página oficial no dice explícitamente si un botón de menú o un botón inline `web_app` se pueden usar dentro de grupos; solo afirma que los links directos funcionan en cualquier chat. Ese punto lo cubre otro investigador.
- No encontré en la página oficial la fecha exacta del cambio de nombre "Web Apps" → "Mini Apps".

## 2. ¿Cómo validar `Telegram.WebApp.initData` en Python/Flask sin dependencias? ¿Qué librerías lo traen hecho y están mantenidas?

### Takeaway
Alcanzan `hmac`, `hashlib` y `urllib.parse` de la librería estándar: unas 25 líneas, sin llamadas de red. La implementación de abajo fue ejecutada contra un vector real y rechaza datos manipulados, token incorrecto y `auth_date` vencido. La firma Ed25519 (`signature`) es para terceros que no tienen el token y exige una dependencia criptográfica; esta app no la necesita.

### Cited Findings
- Algoritmo oficial: `initData` es un query string; el *data-check-string* es la cadena de todos los campos recibidos (sin `hash`), ordenados alfabéticamente, en formato `key=value` y unidos con salto de línea. `secret_key = HMAC_SHA256(<bot_token>, "WebAppData")` (la constante `WebAppData` es la **clave**, el token es el mensaje) y se compara `hex(HMAC_SHA256(data_check_string, secret_key))` con `hash`. También hay que revisar `auth_date` para rechazar datos viejos. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- La documentación comunitaria precisa dos detalles que suelen causar bugs: el resultado del primer HMAC se usa como bytes crudos (no en hex) y el segundo se codifica en hex. — [docs.telegram-mini-apps.com/platform/init-data](https://docs.telegram-mini-apps.com/platform/init-data)
- Validación para terceros (Ed25519): el campo `signature` es la firma Ed25519 en base64url del data-check-string, que en este caso se arma anteponiendo `<bot_id>:WebAppData` y un salto de línea, y excluyendo `hash` y `signature`. Clave pública de producción: `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d`; de test: `40055058a4ee38156a06562e52eece92a771bcd8346a8c4615cb7376eddf72ec`. Solo requiere el `bot_id`, no el token. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- La firma puede venir sin padding base64; hay que agregar `=` si el decodificador lo exige. El texto de esa página dice que el separador es punto y coma pero su ejemplo usa dos puntos (`7342037359:WebAppData`), que coincide con la documentación oficial. — [docs.telegram-mini-apps.com/platform/init-data](https://docs.telegram-mini-apps.com/platform/init-data)
- Campos de `initData`: `auth_date`, `hash`, `user`, `query_id`, `start_param`, `chat_type`, `chat_instance`, `chat`, `receiver`, `can_send_after`. En `user`, `id` y `first_name` están siempre; `last_name`, `username`, `language_code`, `is_premium`, `allows_write_to_pm` son opcionales. — [docs.telegram-mini-apps.com/platform/init-data](https://docs.telegram-mini-apps.com/platform/init-data)
- `telegram-webapp-auth` 3.2.1 (publicada el 21/06/2026, Python >=3.10): `TelegramAuthenticator(secret_key).validate(init_data, expr_in=timedelta(minutes=5))`, `generate_secret_key(token)`, errores `ExpiredInitDataError` / `InvalidInitDataError`, y `validate_third_party()` para Ed25519. Su única dependencia obligatoria es `cryptography>=48.0.0`. — [pypi.org/project/telegram-webapp-auth](https://pypi.org/project/telegram-webapp-auth/)
- `init-data-py` 1.0.1 (publicada el 18/10/2026, Python >=3.10): `validate_by_hash(query_string, bot_token, expires_in=3600)`, `is_valid_by_hash(...)`, `parse(...)`, `sign(UnsignedInitData(user=User(...)), bot_token)` para tests, y `validate_by_signature(query_string, bot_id)` con el extra `ed25519` (que instala `cryptography>=41.0`). Sin dependencias obligatorias. Vencimiento por defecto: un día. En 1.0 el parámetro `lifetime` de la serie 0.2.x pasó a llamarse `expires_in`. — [pypi.org/project/init-data-py](https://pypi.org/project/init-data-py/)
- `aiogram` 3.32.0 (Python >=3.11, Bot API 10.4) depende de `aiohttp`, `pydantic`, `aiofiles`, `magic-filter`, `certifi` y `typing-extensions`. — [pypi.org/project/aiogram](https://pypi.org/project/aiogram/)
- `python-telegram-bot` 22.8 (Python >=3.10, Bot API 10.0) depende de `httpx`. — [pypi.org/project/python-telegram-bot](https://pypi.org/project/python-telegram-bot/)
- `pyTelegramBotAPI` 4.37.1 (Python >=3.11, Bot API 10.3) depende de `requests` y `aiohttp`. — [pypi.org/project/pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- Existen gists de Python con validadores basados en `hmac`/`hashlib`/`urllib.parse`. — [gist de nukdokplex](https://gist.github.com/nukdokplex/79438159cb4e757c15ded719e1a83163), [gist de draincoder](https://gist.github.com/draincoder/f86f4ed8020738ced5f9f4eebea2b2e6) (no revisé su código)

### Implementación de referencia (verificada localmente)

```python
# app/telegram_auth.py  -- solo librería estándar
import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl


class InitDataInvalido(Exception):
    pass


def validar_init_data(init_data, bot_token, max_edad_seg=86400):
    """Valida Telegram.WebApp.initData. Devuelve un dict con los campos
    (con `user` ya convertido a dict) o lanza InitDataInvalido."""
    if not init_data:
        raise InitDataInvalido("initData vacío")
    try:
        # parse_qsl decodifica el percent-encoding; el data-check-string
        # se arma con los valores ya decodificados.
        pares = dict(parse_qsl(init_data, keep_blank_values=True, strict_parsing=True))
    except ValueError:
        raise InitDataInvalido("initData mal formado")

    hash_recibido = pares.pop("hash", None)
    if not hash_recibido:
        raise InitDataInvalido("falta hash")

    # Todos los campos restantes (incluido `signature`), ordenados, key=value, unidos con \n
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(pares.items()))

    # clave = "WebAppData", mensaje = token (el orden invertido es el bug más común)
    clave_secreta = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculado = hmac.new(clave_secreta, data_check_string.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(calculado.encode(), hash_recibido.encode()):
        raise InitDataInvalido("hash incorrecto")

    try:
        auth_date = int(pares.get("auth_date", ""))
    except ValueError:
        raise InitDataInvalido("auth_date inválido")
    if max_edad_seg and time.time() - auth_date > max_edad_seg:
        raise InitDataInvalido("initData vencido")

    try:
        pares["user"] = json.loads(pares["user"]) if "user" in pares else None
    except ValueError:
        raise InitDataInvalido("user inválido")
    return pares
```

Resultado de la prueba local (token `5768337691:AAH5YkoiEuPk8-FZa32hStHTqXiLPtAEhx8`, `initData` con `auth_date=1662771648` y `hash=c501b71e...e2b2`, usuario id 279058397):

- vector conocido: válido, devuelve `user.id == 279058397`
- mismo vector con `max_edad_seg=3600`: rechazado por vencido
- vector con un dígito del id cambiado: rechazado ("hash incorrecto")
- token con un carácter de más: rechazado
- ida y vuelta firmando datos propios con nombre no ASCII ("José Ñandú") y un campo `signature` presente: válido

### Inferences
- Para esta app conviene la función propia: cero dependencias, el mismo estilo que el resto del código y ninguna llamada de red (clave en PythonAnywhere gratuito). Si se prefiere una librería, `init-data-py` es la más liviana (sin dependencias obligatorias y con `sign()` para armar datos de prueba); `telegram-webapp-auth` obliga a instalar `cryptography`.
- Las dos librerías específicas tuvieron releases en 2026 (junio y octubre), así que se las puede considerar mantenidas. Instalar `aiogram` o `python-telegram-bot` solo para validar `initData` es desproporcionado.
- La verificación Ed25519 no se puede hacer con la librería estándar de Python (las dos librerías que la ofrecen la delegan en `cryptography`). No aporta nada cuando el backend es el dueño del token.
- Sobre `auth_date`: es el momento en que se abrió la Mini App, y `initData` no se renueva mientras la app sigue abierta. Con un límite de 5 minutos (el del ejemplo de `telegram-webapp-auth`) alguien que tarda en ordenar los libros recibiría un error; para una votación entre amigos, 24 horas (el default de `init-data-py`) es un valor razonable. El voto único lo garantiza el `user.id`, no la frescura.
- Al validar, el campo `signature` debe quedar dentro del data-check-string del HMAC (solo se excluye `hash`). La implementación de arriba lo hace y la prueba de ida y vuelta lo cubre; conviene además confirmarlo con un `initData` real de un cliente actual.

### Gaps
- El vector de prueba lo tomé de memoria (es el que usa el ecosistema tma.js / init-data-golang); no volví a abrir la página donde está publicado. Lo que sí está comprobado es que el HMAC calculado coincide con el hash del vector, cosa que no puede ocurrir por azar.
- No verifiqué en esta sesión la API exacta de `aiogram.utils.web_app` (de memoria: `check_webapp_signature` y `safe_parse_webapp_init_data`) ni la de `pyTelegramBotAPI` (de memoria: `telebot.util.validate_web_app_data` y `parse_web_app_data`). Confirmar en su documentación antes de citarlas.
- No verifiqué si `python-telegram-bot` incluye un validador de `initData`; hasta donde sé, su ejemplo `webappbot.py` usa `sendData` con botón de teclado y no valida `initData`.
- No obtuve la fecha de publicación de las últimas versiones de `aiogram`, `python-telegram-bot` y `pyTelegramBotAPI` (la respuesta de PyPI se truncó), solo sus números de versión y la versión de Bot API que declaran.

## 3. ¿Cómo enviar `initData` al backend y usar el id de Telegram en lugar del nombre tipeado? ¿Cómo mantener la app usable fuera de Telegram?

### Takeaway
La convención extendida es mandar el string crudo en el header `Authorization: tma <initData>` en cada request; el servidor lo valida y usa `user.id` como clave de voto único. Si el header no viene (navegador común), la app puede seguir con el flujo actual de nombre tipeado, idealmente controlado por una opción de configuración.

### Cited Findings
- Convención: el cliente envía el `initData` crudo en `Authorization: tma <initData>`; el servidor lee el header, comprueba que el esquema sea `tma`, extrae los datos y valida la firma. — [docs.telegram-mini-apps.com/platform/init-data](https://docs.telegram-mini-apps.com/platform/init-data)
- Telegram indica enviar `Telegram.WebApp.initData` al backend del bot para validarlo; recién después de validar se pueden usar los datos. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- `user.id` y `first_name` vienen siempre dentro de `user`; `username` y `last_name` son opcionales. — [docs.telegram-mini-apps.com/platform/init-data](https://docs.telegram-mini-apps.com/platform/init-data)
- Una guía de terceros advierte no confiar en `initDataUnsafe` para autorizar (sirve solo para mostrar) y señala que al abrir la página en una pestaña común `initData` puede quedar vacío. — resumen de buscador sobre [teleclaw.com](https://teleclaw.com/blog/telegram-miniapp-tutorial) y [simplifylabs.io](https://simplifylabs.io/blog/how-to-create-telegram-mini-app/) (no abrí las páginas; baja confianza)

### Código propuesto (no ejecutado; solo `py_compile`)

Backend, dentro de `app/routes.py`:

```python
from flask import abort, current_app, request
from app.telegram_auth import InitDataInvalido, validar_init_data


def usuario_telegram():
    """dict `user` validado; None si el request no trae initData;
    corta con 401 si lo trae y es inválido."""
    auth = request.headers.get('Authorization', '')
    esquema, _, crudo = auth.partition(' ')
    if esquema.lower() != 'tma' or not crudo:
        return None
    token = current_app.config.get('BOT_TOKEN')
    if not token:
        abort(503, description='Falta configurar BOT_TOKEN en el servidor.')
    try:
        datos = validar_init_data(crudo, token)
    except InitDataInvalido as e:
        abort(401, description=str(e))
    return datos.get('user')
```

Uso en `/submit` (esquema):

```python
user = usuario_telegram()
if user:
    marca = f"[tg:{user['id']}]"                      # clave de voto único
    nombre = ' '.join(filter(None, [user.get('first_name'), user.get('last_name')]))
    nombre = nombre.replace(';', ',').replace("'", '’')  # no romper el parser de data.txt
    name = f"{nombre} {marca}"
    ya_voto = marca in file_contents
elif current_app.config.get('SOLO_TELEGRAM'):
    return jsonify({'message': 'Abrí la votación desde Telegram.'}), 403
else:
    name = data['name']                               # flujo actual
    ya_voto = name in file_contents
```

Frontend, en `index.html`:

```javascript
const tg = window.Telegram && window.Telegram.WebApp;
const enTelegram = Boolean(tg && tg.initData);   // cadena vacía fuera de Telegram

if (enTelegram) {
    const u = tg.initDataUnsafe.user || {};      // solo para mostrar, nunca para autorizar
    const campo = document.getElementById('name');
    campo.value = [u.first_name, u.last_name].filter(Boolean).join(' ');
    campo.readOnly = true;
}

async function enviarVoto(orderedList, name) {
    const headers = { 'Content-Type': 'application/json' };
    if (enTelegram) headers['Authorization'] = 'tma ' + tg.initData;
    return fetch('/submit', { method: 'POST', headers, body: JSON.stringify({ name, orderedList }) });
}
```

### Inferences
- Header contra cuerpo JSON: funcionalmente equivalentes. El header tiene la ventaja de servir igual para cualquier ruta (por ejemplo, un `/winner` reservado al admin identificado por Telegram) sin cambiar el formato de cada cuerpo.
- Guardar el id sin romper los cuatro parsers duplicados: incrustarlo en el nombre con delimitadores, por ejemplo `Nombre: Ana García [tg:123456789]; Lista: [...]; fecha: ...`. No contiene `; ` ni `', '`, mantiene `data.txt` como única fuente de verdad (el editor `/votes` sigue sirviendo para anular un voto) y la búsqueda por subcadena `"[tg:123456789]"` es exacta gracias a los corchetes. Costo: `nombres_de_votantes()` y la vista pública deberían quitar la marca con una expresión regular antes de mostrar. Alternativa: un archivo aparte (`votantes_tg.json`), que se desincroniza cuando el admin edita `data.txt` a mano.
- Los nombres de Telegram son texto libre: pueden traer `; ` o comillas simples y romper el parseo de `data.txt` (pitfall ya anotado en CLAUDE.md), por eso hay que sanearlos antes de escribir.
- El chequeo actual `if name in file_contents` es por subcadena sobre todo el archivo (un nombre "Ana" choca con "Mariana" y con títulos de libros). Pasar a `[tg:<id>]` elimina ese problema para los votos hechos desde Telegram.
- Modo mixto: mientras `SOLO_TELEGRAM` esté apagado, cualquiera puede seguir votando por navegador con un nombre inventado, así que la garantía de un voto por persona solo vale si se exige Telegram. Para un club de amigos puede alcanzar con dejar el modo mixto durante la transición.
- El admin también puede identificarse por Telegram: una lista `ADMIN_TG_IDS` en la configuración y `usuario_telegram()['id'] in ADMIN_TG_IDS` reemplazaría a la contraseña dentro de Telegram y evita el problema de la cookie en Telegram Web. Como `/winner` es una navegación GET (sin header propio), habría que pedir el resultado por `fetch` con el header o pasar `initData` por POST.

### Gaps
- La página oficial no documenta qué valor tiene `Telegram.WebApp.initData` fuera de Telegram. Por conocimiento del script, el objeto existe igual y `initData` es una cadena vacía; conviene confirmarlo abriendo la página en Chrome con la consola.
- No revisé línea por línea los parsers de `voting_condorcet.py`, `voting_irv.py` y `kek.py` para confirmar que el nombre se usa solo como etiqueta; hay que verificarlo antes de adoptar el sufijo `[tg:id]`.
- No ejecuté el código Flask de esta sección (Flask no está instalado localmente).

## 4. PythonAnywhere: allowlist, proxy, webhooks, long polling y cambios 2025-2026

### Takeaway
Para la Mini App en sí PythonAnywhere no impone ningún obstáculo: validar `initData` no hace llamadas salientes. Si además se quiere un bot que responda, la cuenta gratuita alcanza usando webhook sobre la web app existente (el long polling exige tareas always-on, que son pagas); `api.telegram.org` está en la allowlist y las llamadas salientes pasan por el proxy `proxy.server:3128`.

### Cited Findings
- `api.telegram.org` figura en la allowlist de cuentas gratuitas, junto con `core.telegram.org`, `oauth.telegram.org` y varios hosts `*.web.telegram.org`. — [pythonanywhere.com/whitelist](https://www.pythonanywhere.com/whitelist/)
- Las cuentas gratuitas solo pueden acceder a sitios de la allowlist y lo hacen a través de un proxy HTTP en `proxy.server:3128`. "Most Python libraries recognise and use the setting that we supply"; `requests` no necesita configuración, otras librerías hay que configurarlas a mano y algunas no funcionan a través del proxy. Las cuentas pagas tienen acceso irrestricto. — [help.pythonanywhere.com/pages/403ForbiddenError](https://help.pythonanywhere.com/pages/403ForbiddenError/)
- Límites vigentes de la cuenta gratuita: 100 segundos de CPU, 512 MiB de disco, una web app con un solo web worker que vence al mes, y dos consolas. Las cuentas creadas antes del 15/01/2026 (08/01/2026 en el sistema EU) conservan además una base MySQL y una tarea programada diaria. — [help.pythonanywhere.com/pages/FreeAccountsFeatures](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/)
- Anuncio del 15/12/2025: desde enero de 2026 las cuentas gratuitas dejan de tener soporte directo (pasa a foros y ayuda comunitaria); para usuarios nuevos, las tareas programadas y MySQL pasan al plan Developer; las web apps sin uso vencen al mes en lugar de a los tres meses. El plan Hacker de USD 5/mes se podía congelar hasta el 8/1 (EU) o 15/1 (US); después el plan pago base cuesta USD 10/mes. — [blog.pythonanywhere.com/221](https://blog.pythonanywhere.com/221/)
- Las tareas always-on solo funcionan en cuentas pagas ("this will only work in paid accounts"). — [help.pythonanywhere.com/pages/AlwaysOnTasks](https://help.pythonanywhere.com/pages/AlwaysOnTasks/)
- Staff de PythonAnywhere (giles, 25/06/2024): un bot corriendo en una consola no queda 24/7 porque los servidores de consolas se reinician por mantenimiento cada uno o dos días; recomienda webhooks. Staff (fjl, julio de 2025): un puerto propio (5000) no es accesible desde afuera; el bot tiene que desplegarse como web app. — [foro PythonAnywhere, tema 34784](https://www.pythonanywhere.com/forums/topic/34784/)
- El tutorial oficial de PythonAnywhere (2017, con `telepot` + Flask) lleva una nota de 2020 que decía que el webhook ya no funcionaba en cuentas gratuitas porque Telegram dejó de aceptar certificados wildcard, y una actualización del 20/06/2024 que dice que "should work on free accounts again". — [blog.pythonanywhere.com/148](https://blog.pythonanywhere.com/148/)
- Ese tutorial pone el webhook en una ruta con un secreto impredecible y, para cuentas gratuitas, configura a mano el proxy `http://proxy.server:3128` porque `telepot` no toma el proxy del entorno. — [blog.pythonanywhere.com/148](https://blog.pythonanywhere.com/148/)
- Reporte del 28/03/2026 en cuenta gratuita: "Cannot connect to api.telegram.org:443"; el staff respondió que el dominio ya está en la allowlist y el hilo no registra solución. En el mismo hilo (julio de 2025) un usuario copió código de proxy para `python-telegram-bot` antiguo y obtuvo `AttributeError: module 'telegram' has no attribute 'utils'`. — [foro PythonAnywhere, tema 34784](https://www.pythonanywhere.com/forums/topic/34784/)
- `setWebhook`: `url` debe ser HTTPS; `secret_token` (1 a 256 caracteres, solo `A-Z`, `a-z`, `0-9`, `_` y `-`) se reenvía en el header `X-Telegram-Bot-Api-Secret-Token` de cada request; puertos soportados 443, 80, 88 y 8443; `max_connections` de 1 a 100 (40 por defecto); `drop_pending_updates` descarta lo pendiente. Mientras haya un webhook configurado no se puede usar `getUpdates`. — [core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- Al atender un webhook se puede invocar un método de Bot API en el cuerpo de la respuesta (JSON con el campo `method`); no se puede saber si esa llamada tuvo éxito ni obtener su resultado. — [core.telegram.org/bots/api](https://core.telegram.org/bots/api)

### Código propuesto (no ejecutado; solo `py_compile`)

Webhook que contesta `/start` sin hacer ninguna llamada saliente:

```python
@main.route('/tg-webhook', methods=['POST'])
def tg_webhook():
    secreto = current_app.config.get('TG_WEBHOOK_SECRET') or ''
    recibido = request.headers.get('X-Telegram-Bot-Api-Secret-Token', '')
    if not secreto or not hmac.compare_digest(recibido.encode(), secreto.encode()):
        abort(403)
    update = request.get_json(silent=True) or {}
    msg = update.get('message') or {}
    if (msg.get('text') or '').startswith('/start'):
        return jsonify({
            'method': 'sendMessage',
            'chat_id': msg['chat']['id'],
            'text': 'Tocá el botón para votar.',
            'reply_markup': {'inline_keyboard': [[
                {'text': 'Votar', 'web_app': {'url': 'https://tupac.pythonanywhere.com/'}}
            ]]},
        })
    return '', 200
```

Registro del webhook, una sola vez (desde una consola Bash de PythonAnywhere o desde la PC):

```bash
curl "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=https://tupac.pythonanywhere.com/tg-webhook" \
  -d "secret_token=<SECRETO>" \
  -d "max_connections=1" \
  -d 'allowed_updates=["message"]'
```

### Inferences
- Para lo que pide una Mini App de votación, la cuenta gratuita no es limitante: la página se sirve por HTTPS, la validación es local y el webhook entra por la misma web app. El único requisito de red aparece si el servidor quiere mandar mensajes (por ejemplo, avisar al grupo "ya votaron 5"), y ese destino está en la allowlist.
- Responder dentro del propio webhook (campo `method`) evita por completo el proxy y la allowlist para el caso `/start`, a costa de no enterarse si el envío falló.
- El error "Cannot connect to api.telegram.org:443" con el dominio ya permitido apunta a una librería que no usa el proxy por sí sola. El formato del mensaje coincide con el de `aiohttp` (base de `aiogram` y del modo async de `pyTelegramBotAPI`), que por defecto ignora las variables de proxy del entorno. No está confirmado en el hilo.
- Con un solo web worker, un request lento (por ejemplo una llamada saliente a Telegram sin timeout) bloquea toda la app, incluida la votación. Conviene poner `timeout` corto en cualquier llamada saliente y `max_connections=1` en el webhook.
- Dos consejos desactualizados que siguen circulando: (a) "los webhooks no funcionan en PythonAnywhere gratuito" (nota de 2020, revertida en 2024); (b) código de proxy con `telegram.utils.request.Request`, que pertenece a `python-telegram-bot` anterior a la v20 y ya no existe.
- La web app gratuita vence al mes (antes eran tres): si nadie entra al panel a extenderla, el link del bot deja de responder. Vale un recordatorio mensual.
- No sé si la cuenta `tupac` es gratuita o paga; al ser anterior a 2026, si es gratuita conserva la tarea programada diaria y MySQL.

### Gaps
- La confirmación más reciente de que el webhook de Telegram funciona con un subdominio `*.pythonanywhere.com` gratuito es de junio de 2024; no encontré una confirmación explícita de 2025-2026. Se comprueba en un minuto con `getWebhookInfo` después de `setWebhook`.
- La página de ayuda no explica el mecanismo exacto por el que se "suministra" el proxy (presumiblemente variables de entorno `http_proxy`/`https_proxy`). Si es así, `urllib.request` de la librería estándar también lo tomaría solo; hay que probarlo con tres líneas en una consola de PythonAnywhere.
- No verifiqué la forma actual de configurar el proxy en `pyTelegramBotAPI` (de memoria: `telebot.apihelper.proxy = {'https': 'http://proxy.server:3128'}`) ni en `python-telegram-bot` v22 (de memoria: `ApplicationBuilder().proxy(...)`); `httpx`, hasta donde sé, sí respeta las variables de entorno.
- La página de la allowlist llegó truncada; no pude confirmar si `t.me` o `telegram.org` (de donde el navegador del usuario, no el servidor, baja `telegram-web-app.js`) están listados. No hace falta: esa descarga la hace el cliente.

## 5. ¿Qué librería de bots es la más liviana para un Flask síncrono en PythonAnywhere?

### Takeaway
Ninguna: para dos o tres métodos de Bot API (`setWebhook`, `sendMessage`, quizá `answerWebAppQuery`) alcanza con llamadas HTTP directas usando `urllib.request` o `requests`. Si se quiere una librería, `pyTelegramBotAPI` es la única de las tres grandes con modo síncrono; `python-telegram-bot` y `aiogram` son asíncronas y encajan mal en WSGI.

### Cited Findings
- `pyTelegramBotAPI` 4.37.1: "Both synchronous and asynchronous", Bot API 10.3, Python >=3.11, dependencias obligatorias `requests` y `aiohttp`. — [pypi.org/project/pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- `python-telegram-bot` 22.8: construida sobre `asyncio` desde la v20.0, declara que no busca ser thread-safe, Bot API 10.0, Python >=3.10, dependencia `httpx`. — [pypi.org/project/python-telegram-bot](https://pypi.org/project/python-telegram-bot/)
- `aiogram` 3.32.0: "Modern and fully asynchronous framework", Bot API 10.4, Python >=3.11 y <3.16, dependencias `aiohttp`, `pydantic`, `aiofiles`, `magic-filter`, `certifi`, `typing-extensions`. — [pypi.org/project/aiogram](https://pypi.org/project/aiogram/)
- En PythonAnywhere `requests` funciona a través del proxy sin configuración; otras librerías requieren configuración manual. — [help.pythonanywhere.com/pages/403ForbiddenError](https://help.pythonanywhere.com/pages/403ForbiddenError/)
- Un hilo del foro de PythonAnywhere (abril de 2020) muestra el patrón `pyTelegramBotAPI` + Flask: bot creado con `threaded=False`, ruta POST en `/{secreto}`, `remove_webhook()` seguido de `set_webhook(url=...)`. Los problemas del hilo fueron errores de tipeo en nombres de métodos y no recargar la web app. — [foro PythonAnywhere, tema 27319](https://www.pythonanywhere.com/forums/topic/27319/)
- El tutorial oficial de PythonAnywhere usa `telepot`; el staff aclaró en 2025 que las instrucciones corresponden a una versión específica de esa librería y que hay que instalar esa versión o adaptar el código. — [blog.pythonanywhere.com/148](https://blog.pythonanywhere.com/148/), [foro PythonAnywhere, tema 34784](https://www.pythonanywhere.com/forums/topic/34784/)

### Helper sin dependencias (no ejecutado contra la red)

```python
import json
import urllib.request


def tg_api(token, metodo, **params):
    """Llama a un método de Bot API. Devuelve el JSON de respuesta."""
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/{metodo}',
        data=json.dumps(params).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.load(resp)

# tg_api(token, 'sendMessage', chat_id=-100123, text='Ya votaron 5 de 8')
```

### Inferences
- Comparación para un WSGI síncrono con un solo worker:

| Opción | Dependencias nuevas | Encaje con Flask/WSGI | Comentario |
|---|---|---|---|
| `urllib.request` | ninguna | directo | hay que escribir a mano cada llamada; depende de que el proxy de PythonAnywhere se tome del entorno (por verificar) |
| `requests` | 1 | directo | PythonAnywhere documenta que funciona con su proxy sin tocar nada |
| `pyTelegramBotAPI` (sync) | `requests` + `aiohttp` | bueno, con `threaded=False` | decoradores cómodos si el bot crece; exige Python >=3.11 |
| `python-telegram-bot` 22 | `httpx` | incómodo | hay que envolver cada llamada en `asyncio.run()`; pensada para su propio event loop |
| `aiogram` 3 | `aiohttp`, `pydantic` y otras | malo | framework async completo; `aiohttp` no toma el proxy solo |

- El helper de `urllib` es coherente con la premisa del proyecto (Flask como única dependencia). Si falla por el proxy en la cuenta gratuita, la salida de menor costo es `requests`.
- `telepot` (el del tutorial oficial) no es una opción en 2026: el propio staff admite que el tutorial está atado a una versión vieja.

### Gaps
- No verifiqué contra documentación actual el motivo de `threaded=False` en `pyTelegramBotAPI` bajo WSGI (de memoria: evita que la librería lance hilos propios que el worker puede cortar).
- No probé `urllib.request` detrás del proxy de PythonAnywhere.
- No sé qué versión de Python usa hoy la web app en PythonAnywhere; `pyTelegramBotAPI` y `aiogram` actuales exigen 3.11 o superior.

## 6. ¿Hace falta un webhook (o un backend de bot) para que la Mini App funcione?

### Takeaway
No. La Mini App es una URL asociada al bot en @BotFather; el servidor solo necesita el token para verificar el HMAC de `initData`, sin hablar con Telegram. El webhook solo hace falta si el bot debe reaccionar a mensajes (por ejemplo responder `/start`), y enviar mensajes por iniciativa propia requiere llamadas salientes pero tampoco webhook.

### Cited Findings
- El botón de menú y la Main Mini App se configuran en @BotFather con una URL; no se menciona ningún requisito de backend del bot para abrirlas. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- La validación consiste en calcular HMAC-SHA-256 con el token sobre los datos recibidos; no interviene ninguna llamada a Bot API. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Lanzada desde botón inline, botón de menú o menú de adjuntos, la Mini App recibe un `query_id` que se puede usar con `answerWebAppQuery` para enviar un mensaje en nombre del usuario. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- `sendData` solo existe para lanzamientos desde botón de teclado y entrega los datos al bot como mensaje de servicio (`web_app_data`), lo que sí exige que el bot reciba updates. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Con un webhook configurado no se puede usar `getUpdates`. — [core.telegram.org/bots/api](https://core.telegram.org/bots/api)

### Inferences
- Tres niveles posibles: (1) sin backend de bot: Mini App + validación de `initData`; (2) solo llamadas salientes (`sendMessage` al grupo cuando alguien vota o cuando se cierra la votación); (3) webhook para responder `/start` con un botón. El nivel 1 ya resuelve identidad y voto único.
- Sin webhook, si alguien abre el chat privado con el bot y toca "Iniciar", el bot no contesta nada; el botón de menú igual aparece. Para un grupo de amigos alcanza, y el webhook de la sección 4 lo mejora con unas 20 líneas.
- Como esta app persiste el voto por `fetch` a su propio backend, `sendData` no hace falta, y eso es bueno porque obligaría al modo de lanzamiento en el que `initData` llega vacío.

### Gaps
- `savePreparedInlineMessage` (para que el usuario comparta un mensaje desde la Mini App) quedó fuera de lo verificado; lo cubre la investigación de funciones para grupos.

## 7. Arrastrar y soltar dentro del webview de Telegram

### Takeaway
El conflicto es real y está reconocido por Telegram: un arrastre vertical puede interpretarse como el gesto de minimizar o cerrar. La solución oficial desde Bot API 7.7 es `disableVerticalSwipes()`, combinada con `expand()` y, en SortableJS, un `handle` más un pequeño `delay` táctil. No encontré ningún reporte público específico de SortableJS dentro de Telegram, y hay al menos un reporte de que en iOS el problema persistía.

### Cited Findings
- Bot API 7.7 (7 de julio de 2024) agregó `isVerticalSwipesEnabled`, `enableVerticalSwipes()` y `disableVerticalSwipes()`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Según la documentación oficial, deshabilitar los swipes verticales es útil cuando la Mini App usa gestos que pueden chocar con los de minimizar y cerrar; aun deshabilitados, el usuario puede minimizar y cerrar deslizando el encabezado de la Mini App. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps) (texto citado en el resumen del buscador; no lo extraje literal en mi lectura)
- Causa descripta por desarrolladores: el colapso ocurre cuando el documento no es desplazable o cuando `window.scrollY` vale cero; en ese estado un deslizamiento hacia abajo achica la app en lugar de desplazar el contenido. El truco anterior a 7.7 era forzar `height: calc(100vh + 1px)` y hacer `window.scrollTo(0, 1)` en `touchstart`; el autor actualizó el artículo indicando usar `disableVerticalSwipes` en su lugar. — [dev.to/nimaxin](https://dev.to/nimaxin/how-to-fix-the-telegram-mini-app-scrolling-collapse-issue-a-handy-trick-1abe)
- Reportes en los comentarios de ese artículo: un desarrollador (julio de 2024) dijo que el truco dejó de funcionar al expandir a pantalla completa y que `disableVerticalSwipes()` fue "a huge win", pero que en iOS seguía viendo el comportamiento viejo; otro (12/11/2024) informó que el problema persistía en iOS y estaba resuelto en Android. Nadie respondió sobre iOS. — [dev.to/nimaxin](https://dev.to/nimaxin/how-to-fix-the-telegram-mini-app-scrolling-collapse-issue-a-handy-trick-1abe)
- Un artículo sobre errores comunes señala que en juegos e interfaces de arrastre los usuarios creen que la app se colgó cuando un deslizamiento hacia abajo la cierra, y recomienda `disableVerticalSwipes()` en pantallas con gestos propios. — [adsgram.ai](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them) (resumen de buscador; no abrí la página)
- Un PR público aplica el patrón `ready()` → `expand()` → `disableVerticalSwipes()` más `overscroll-behavior: none` en `html` y `body`. — [github.com/zmarvel909m77/MCee77/pull/8](https://github.com/zmarvel909m77/MCee77/pull/8) (resumen de buscador; repo personal, evidencia débil)
- La documentación comunitaria también describe una alternativa por CSS para que el webview no pase los swipes a Telegram, y advierte verificar que el usuario no quede atrapado al deshabilitar el gesto. — [docs.telegram-mini-apps.com/platform/swipe-behavior](https://docs.telegram-mini-apps.com/platform/swipe-behavior) (resumen de buscador)
- Opciones de SortableJS según su README: `delay` (milisegundos antes de que empiece el ordenamiento), `delayOnTouchOnly` (aplica el delay solo con touch), `touchStartThreshold` (movimiento mínimo que cancela un arrastre demorado; sugiere 3 a 5 px porque algunas pantallas disparan `touchmove` sin que el dedo se mueva), `handle` (zona del ítem desde la que se puede arrastrar), `forceFallback` (usa la implementación propia en vez del drag and drop HTML5 nativo, para un comportamiento consistente entre dispositivos), `fallbackTolerance` (píxeles antes de considerar arrastre; sugiere 3 a 5), `fallbackOnBody`. — [github.com/SortableJS/Sortable](https://github.com/SortableJS/Sortable)
- En otro webview embebido (VS Code) el drag HTML5 nativo se cancelaba y se resolvió con `forceFallback: true`, que sigue eventos de puntero. — [PR en guilletin63/vscode-gh-projects](https://github.com/guilletin63/vscode-gh-projects/pull/12) (resumen de buscador; no es Telegram)
- `HapticFeedback` existe desde Bot API 6.1 con `impactOccurred`, `notificationOccurred` y `selectionChanged`. `expand()` lleva la Mini App a la altura máxima disponible (`isExpanded` lo confirma). — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)

### Configuración propuesta (no probada en dispositivo)

```javascript
const tg = window.Telegram && window.Telegram.WebApp;
const enTelegram = Boolean(tg && tg.initData);

if (enTelegram) {
    tg.ready();
    tg.expand();
    if (tg.isVersionAtLeast('7.7')) tg.disableVerticalSwipes();
}

const sortable = new Sortable(document.getElementById('sortable-list'), {
    animation: 150,
    handle: '.agarre',            // ícono ≡ a la derecha; el resto del ítem deja scrollear
    delay: 120,
    delayOnTouchOnly: true,
    touchStartThreshold: 5,
    forceFallback: true,
    fallbackTolerance: 3,
    onStart() { if (enTelegram) tg.HapticFeedback.impactOccurred('light'); },
    onChange() { if (enTelegram) tg.HapticFeedback.selectionChanged(); },
    onEnd() { if (enTelegram) tg.HapticFeedback.impactOccurred('soft'); },
});
```

```css
html, body { overscroll-behavior: none; }
.agarre { touch-action: none; padding: 12px; cursor: grab; }
```

### Inferences
- Orden de defensa recomendado: (1) `expand()` + `disableVerticalSwipes()`; (2) `handle` con `touch-action: none`, para que el dedo sobre el texto del libro siga desplazando la lista y solo el agarre inicie el arrastre; (3) `delay` táctil corto para distinguir tocar de arrastrar; (4) `forceFallback: true` para no depender del drag HTML5 del webview.
- Con una lista más alta que la pantalla, el `handle` es lo que evita el conflicto entre scroll y arrastre, problema clásico de iOS con o sin Telegram.
- Como el reporte de iOS quedó sin resolver en la fuente, la prueba en un iPhone real es el paso de verificación más importante de toda la conversión. Los reportes son de 2024; no encontré confirmación posterior de que iOS esté corregido.
- Plan B si el arrastre resulta poco confiable en algún cliente: botones "subir" y "bajar" por ítem como alternativa accesible; no dependen de gestos.
- Los clientes anteriores a Bot API 7.7 ignoran `disableVerticalSwipes`; por eso la guarda con `isVersionAtLeast('7.7')`. A fines de 2026 debería ser una minoría (suposición, sin dato).

### Gaps
- No encontré issues de SortableJS, hilos de Stack Overflow ni posts que traten específicamente SortableJS dentro de una Telegram Mini App. La recomendación combina la guía oficial de Telegram con las opciones documentadas de SortableJS; falta validación empírica.
- No pude confirmar la última versión publicada de SortableJS para recomendar un número exacto al reemplazar `@latest`.
- No verifiqué si `isVersionAtLeast` figura en la porción de la página oficial que leí (lo conozco como método estándar de `Telegram.WebApp`).
- No hay datos sobre el comportamiento en Telegram Desktop ni en Telegram Web con mouse; presumiblemente no hay conflicto porque no existe gesto de swipe.

## 8. Adaptación de la interfaz: tema, botón principal, confirmaciones

### Takeaway
Con variables CSS `--tg-theme-*` y unos pocos métodos de `Telegram.WebApp` la página adopta el aspecto del cliente sin frameworks ni build. Todo se puede aplicar de forma condicional para que fuera de Telegram siga viéndose como hoy.

### Cited Findings
- Variables CSS de tema: `--tg-theme-bg-color`, `--tg-theme-text-color`, `--tg-theme-hint-color`, `--tg-theme-link-color`, `--tg-theme-button-color`, `--tg-theme-button-text-color`, `--tg-theme-secondary-bg-color`, `--tg-theme-header-bg-color`, `--tg-theme-bottom-bar-bg-color`, `--tg-theme-accent-text-color`, `--tg-theme-section-bg-color`, `--tg-theme-section-header-text-color`, `--tg-theme-section-separator-color`, `--tg-theme-subtitle-text-color`, `--tg-theme-destructive-text-color`; además `--tg-color-scheme`, `--tg-viewport-height`, `--tg-viewport-stable-height`, `--tg-safe-area-inset-*` y `--tg-content-safe-area-inset-*`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Botón inferior: Bot API 7.10 renombró la clase `MainButton` a `BottomButton` y agregó `hasShineEffect` y `position`; 9.5 agregó `iconCustomEmojiId`. Métodos: `setText`, `onClick` (alias de `onEvent('mainButtonClicked', ...)`), `show`/`hide`, `enable`/`disable`, `showProgress(leaveActive)`, `hideProgress`, `setParams`. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- `showConfirm()` y `enableClosingConfirmation()` existen desde Bot API 6.2. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Eventos: `themeChanged` (leer `themeParams` y `colorScheme`), `viewportChanged` (con `isStateStable`), `mainButtonClicked`. `viewportStableHeight` es la altura a usar para fijar elementos al borde inferior. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)

### Código propuesto (no probado en dispositivo)

```css
body {
    background: var(--tg-theme-bg-color, #ffffff);
    color: var(--tg-theme-text-color, #222222);
}
.libro {
    background: var(--tg-theme-secondary-bg-color, #f3f3f3);
    border-bottom: 1px solid var(--tg-theme-section-separator-color, #dddddd);
}
.autor { color: var(--tg-theme-hint-color, #777777); }
button.enviar {
    background: var(--tg-theme-button-color, #2481cc);
    color: var(--tg-theme-button-text-color, #ffffff);
}
```

```javascript
if (enTelegram) {
    document.getElementById('boton-enviar').hidden = true;   // se reemplaza por el botón nativo
    tg.enableClosingConfirmation();                           // evita perder el orden por cerrar sin querer

    tg.MainButton.setText('Enviar mi voto');
    tg.MainButton.show();
    tg.MainButton.onClick(() => {
        tg.showConfirm('¿Confirmás este orden? No se puede cambiar después.', async (ok) => {
            if (!ok) return;
            tg.MainButton.showProgress();
            try {
                const resp = await enviarVoto(sortable.toArray(), '');
                const cuerpo = await resp.json();
                tg.HapticFeedback.notificationOccurred(resp.ok ? 'success' : 'error');
                tg.showAlert(cuerpo.message);
                if (resp.ok) { tg.disableClosingConfirmation(); tg.MainButton.hide(); }
            } finally {
                tg.MainButton.hideProgress();
            }
        });
    });
}
```

### Inferences
- Los valores por defecto en `var(--tg-theme-..., #valor)` hacen que el mismo CSS sirva dentro y fuera de Telegram, sin detectar nada en JS.
- `Telegram.WebApp.MainButton` sigue siendo el nombre del objeto para el botón principal aunque la clase se llame `BottomButton` desde 7.10; los tutoriales que dicen "MainButton" siguen siendo válidos.
- Reemplazar `confirm()` y `alert()` por `showConfirm` y `showAlert` solo dentro de Telegram mantiene el comportamiento actual en el navegador.
- El campo de nombre puede ocultarse dentro de Telegram y mostrarse un saludo ("Votás como Ana"), tomado de `initDataUnsafe.user` únicamente para mostrar.
- `sortable.toArray()` en el ejemplo es ilustrativo: hay que usar la misma función con la que `index.html` arma hoy `orderedList`.

### Gaps
- No verifiqué en la página la versión en la que se agregó `showAlert` ni la existencia de `disableClosingConfirmation` (conocimiento previo: ambas son 6.2+).
- Las variables de tema más nuevas pueden no existir en clientes viejos; por eso los valores por defecto.

## 9. Seguridad y almacenamiento: token, concurrencia, ¿SQLite?

### Takeaway
El token del bot es ahora el secreto más importante (con él se puede fabricar `initData` de cualquier usuario); debe vivir fuera de git, y el repo ya tiene el mecanismo para eso. Con un único web worker en la cuenta gratuita, la escritura en archivo plano no corre riesgo real de concurrencia; pasar a SQLite es una mejora opcional, no un requisito.

### Cited Findings
- El hash de `initData` se calcula con una clave derivada del token del bot, de modo que quien tenga el token puede generar datos válidos. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- PythonAnywhere recomienda guardar las variables en un archivo `.env` y cargarlas con `python-dotenv` desde el archivo WSGI, antes de importar la app; los cambios se aplican recién al recargar la web app. — [ayuda de PythonAnywhere: variables de entorno para web apps](https://helpdev.pythonanywhere.com/pages/environment-variables-for-web-apps) (contenido tomado del resumen del buscador; la página devolvió 404 al intentar abrirla)
- La cuenta gratuita ejecuta la web app con un solo web worker. — [help.pythonanywhere.com/pages/FreeAccountsFeatures](https://help.pythonanywhere.com/pages/FreeAccountsFeatures/)
- El `secret_token` del webhook permite verificar que el request viene de Telegram mediante el header `X-Telegram-Bot-Api-Secret-Token`. — [core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- El tutorial de PythonAnywhere protegía el webhook poniéndolo en una ruta con un secreto impredecible, porque la app es públicamente accesible. — [blog.pythonanywhere.com/148](https://blog.pythonanywhere.com/148/)

### Inferences
- Opción sin dependencias y consistente con el repo: reutilizar `_leer_secreto` en `app/__init__.py`:

```python
app.config['BOT_TOKEN'] = _leer_secreto('BOT_TOKEN', os.path.join(base_dir, 'bot_token.txt'))
app.config['TG_WEBHOOK_SECRET'] = _leer_secreto(
    'TG_WEBHOOK_SECRET', os.path.join(base_dir, 'tg_webhook_secret.txt'), generar=True)
```

  y agregar `app/bot_token.txt` y `app/tg_webhook_secret.txt` a `.gitignore` (hoy ignora `.env`, `app/secret_key.txt` y `app/admin_password.txt`). En PythonAnywhere el archivo se crea a mano una vez, o se define `os.environ['BOT_TOKEN']` en el archivo WSGI, que vive fuera del repo.
- La vía `.env` + `python-dotenv` que recomienda PythonAnywhere agrega una dependencia; no hace falta dado el helper existente.
- Si el token se filtra (por ejemplo, por un commit accidental), hay que revocarlo en @BotFather y cargar el nuevo; los `initData` firmados con el anterior dejan de validar.
- Concurrencia: `/submit` abre el archivo en `a+`, lee todo, busca el duplicado y agrega una línea. No es atómico, pero con un solo worker los requests se atienden de a uno, así que dos votos simultáneos no se pisan. En un plan pago con varios workers sí existiría la carrera (dos votos del mismo usuario podrían pasar el chequeo a la vez).
- El riesgo de datos más concreto no es la concurrencia sino los que ya figuran en CLAUDE.md: `app/data/` está versionado y un deploy puede pisar votos, y `/submit-data` reescribe el archivo entero.
- SQLite (módulo `sqlite3` de la librería estándar) daría voto único atómico con una restricción `UNIQUE` sobre el id de Telegram y eliminaría el parser duplicado en cuatro archivos, pero obliga a reescribir `/votes`, los scripts de conteo y a sacar el archivo de la base del repo. Para 8 a 15 votantes el archivo plano con la marca `[tg:id]` es suficiente; SQLite se justifica si se quiere historial de varias votaciones o varias rondas.
- Con `initData` validado, el webhook protegido por `secret_token` y `/submit` aceptando solo JSON, no aparecen superficies nuevas más allá del token. La validación debe hacerse siempre en el servidor; `initDataUnsafe` en el cliente es solo cosmético.

### Gaps
- No pude abrir la página de ayuda de variables de entorno de PythonAnywhere (404 en las URL probadas); el contenido citado viene del resumen del buscador.
- No verifiqué documentación de PythonAnywhere sobre rendimiento o bloqueo de SQLite en su sistema de archivos.
- No verifiqué en esta sesión el comando exacto de @BotFather para revocar el token (de memoria: `/revoke`).

## 10. Desarrollo local

### Takeaway
Hay tres caminos: probar directamente contra el deploy en PythonAnywhere (lo más simple), exponer `localhost:5000` con un túnel HTTPS (por ejemplo un Quick Tunnel de cloudflared, sin cuenta), o usar el entorno de test de Telegram, que acepta URLs HTTP sin TLS. Para depurar hay inspección de webview en Android, iOS, Telegram Desktop beta y macOS beta.

### Cited Findings
- Entorno de test: es independiente del principal, requiere una cuenta nueva y un bot nuevo creado con @BotFather dentro de ese entorno. Ingreso: en iOS, tocar 10 veces el ícono de Ajustes > Accounts > Login to another account > Test; en Telegram Desktop, Settings > mantener Shift + Alt y clic derecho en "Add Account" > "Test Server"; en macOS, 10 clics en Ajustes para abrir el menú Debug y ⌘ + clic en "Add Account". Las llamadas a Bot API usan `https://api.telegram.org/bot<token>/test/METHOD_NAME`. En este entorno se permiten links HTTP sin TLS para probar Mini Apps. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Depuración en Android: activar depuración USB, en Ajustes de Telegram mantener presionado dos veces el número de versión, elegir "Enable WebView Debug" y abrir `chrome://inspect/#devices` en Chrome. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Depuración en Telegram Desktop (Windows y Linux): usar la versión Beta, Settings > Advanced > Experimental settings > habilitar webview inspection, y clic derecho > Inspect dentro del webview. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Depuración en iOS: 10 toques en Ajustes, activar "Allow Web View Inspection", conectar por USB y usar Safari > Develop en una Mac. En macOS: versión Beta, 5 clics en Ajustes, "Debug Mini Apps", clic derecho > Inspect Element. — [core.telegram.org/bots/webapps](https://core.telegram.org/bots/webapps)
- Quick Tunnel de Cloudflare: `cloudflared tunnel --url http://localhost:8080` (cambiando el puerto), sin cuenta ni dominio propio; genera un subdominio aleatorio de `trycloudflare.com` que cambia en cada ejecución; sin garantía de disponibilidad, máximo 200 requests en curso y sin soporte de SSE. — [developers.cloudflare.com](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/)
- Una guía de terceros indica que fuera del entorno de test Telegram no carga Mini Apps por HTTP plano y que el desarrollo local necesita un túnel. — resumen de buscador sobre [teleclaw.com](https://teleclaw.com/blog/telegram-miniapp-tutorial) y [simplifylabs.io](https://simplifylabs.io/blog/how-to-create-telegram-mini-app/) (no abrí las páginas)
- `init-data-py` incluye `sign(UnsignedInitData(user=User(...)), bot_token)` para fabricar `initData` firmado en tests. — [pypi.org/project/init-data-py](https://pypi.org/project/init-data-py/)

### Inferences
- Flujo recomendado para este proyecto en Windows: `python run.py` (puerto 5000) y, en otra terminal, `cloudflared tunnel --url http://localhost:5000`; pegar la URL `https://<algo>.trycloudflare.com` en un **segundo bot de desarrollo** (`/setmenubutton`) para no tocar el bot real. Como la URL cambia en cada arranque, hay que actualizarla en @BotFather cada vez.
- El backend se puede probar sin Telegram: una función de 5 líneas que firme datos propios con el token de desarrollo (la usé para verificar el validador) permite hacer `curl` o tests con un header `Authorization: tma ...` válido:

```python
def firmar_init_data(campos, bot_token):   # solo para pruebas
    dcs = "\n".join(f"{k}={v}" for k, v in sorted(campos.items()))
    clave = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    firma = hmac.new(clave, dcs.encode(), hashlib.sha256).hexdigest()
    return urllib.parse.urlencode({**campos, "hash": firma})
```

- En Windows la opción de depuración más cómoda es Telegram Desktop Beta con inspección de webview; para el arrastre táctil hay que usar un teléfono (Android + `chrome://inspect` es lo más accesible sin Mac).
- El entorno de test evita el túnel (acepta `http://`), pero el teléfono tiene que alcanzar la PC por la red local y hay que crear cuenta y bot de test; para un proyecto chico el túnel o el deploy directo suelen costar menos.
- Usar un bot de desarrollo aparte también evita que el token de producción ande por la máquina local.

### Gaps
- La página oficial no detalla cómo entrar al entorno de test desde Android.
- No verifiqué el estado actual de ngrok (dominio estático gratuito, página intermedia de advertencia en el plan free) ni si esa página interfiere con el webview de Telegram; por eso el ejemplo usa cloudflared, cuya documentación sí abrí.
- La documentación de Cloudflare leída no dice explícitamente que la URL generada sea HTTPS (lo es en la práctica, por conocimiento previo).

## 11. Tutoriales y repos de Flask + Telegram Mini App (idealmente en PythonAnywhere)

### Takeaway
No encontré ningún tutorial ni repositorio que combine Flask, Telegram Mini App y PythonAnywhere, ni uno de Flask + Mini App de calidad suficiente para recomendar. El material útil está repartido: documentación oficial de Telegram, el tutorial oficial de PythonAnywhere para el webhook (viejo pero con el patrón correcto) y librerías o gists de validación.

### Cited Findings
- Dos búsquedas dirigidas (Flask + Mini App + `initData`; Flask + PythonAnywhere + `telegram-web-app.js`) no devolvieron ningún tutorial ni repo específico de Flask; los resultados fueron guías genéricas, artículos para React y un ejemplo en Node.js con Telegraf. — resultados de búsqueda del 17/11/2026, por ejemplo [ejemplo de Telegraf](https://github.com/feathers-studio/telegraf-docs/blob/master/examples/mini-apps/README.md) y [artículo React en DEV](https://dev.to/serhii_a9c08345ac360cf5c8/build-a-telegram-mini-app-with-react-initdata-validation-twa-devsdk-and-mainbutton-47b4)
- Tutorial oficial de PythonAnywhere "Building a simple Telegram bot using PythonAnywhere" (2/1/2017, actualizado el 20/6/2024): bot con Flask y webhook en ruta secreta, proxy para cuentas gratuitas. Es un bot de chat, no una Mini App, y usa `telepot`. — [blog.pythonanywhere.com/148](https://blog.pythonanywhere.com/148/)
- Hilo "Running a Telegram Bot" del foro de PythonAnywhere (2024 a 2026): recorrido real de un principiante con consolas, módulos faltantes, puerto 5000, proxy y webhook; sirve como lista de tropiezos. — [foro PythonAnywhere, tema 34784](https://www.pythonanywhere.com/forums/topic/34784/)
- Documentación comunitaria de Mini Apps: formato de `initData`, convención del header `tma`, validación por hash y por firma. Recomienda librerías de validación solo para JavaScript y Go, no para Python. — [docs.telegram-mini-apps.com/platform/init-data](https://docs.telegram-mini-apps.com/platform/init-data)
- Librerías Python de validación con release en 2026: `init-data-py` y `telegram-webapp-auth`. — [pypi.org/project/init-data-py](https://pypi.org/project/init-data-py/), [pypi.org/project/telegram-webapp-auth](https://pypi.org/project/telegram-webapp-auth/)
- Gists con validadores en Python puro. — [nukdokplex](https://gist.github.com/nukdokplex/79438159cb4e757c15ded719e1a83163), [draincoder](https://gist.github.com/draincoder/f86f4ed8020738ced5f9f4eebea2b2e6) (no revisados)
- Artículo en Habr sobre qué es una Mini App. — [habr.com/en/articles/935718](https://habr.com/en/articles/935718) (apareció en resultados; no lo abrí)

### Inferences
- La falta de un tutorial Flask + PythonAnywhere + Mini App no indica dificultad: las piezas son independientes y chicas (una etiqueta `<script>`, una función de validación de unas 25 líneas, una ruta de webhook opcional). Las secciones 2, 3, 4 y 7 de estas notas cubren ese hueco con código adaptado a este repo.
- Orden de lectura sugerido para el desarrollador: (1) página oficial de Mini Apps (inicialización, validación, testing); (2) `docs.telegram-mini-apps.com/platform/init-data`; (3) blog 148 de PythonAnywhere solo por el patrón del webhook, ignorando `telepot`; (4) página 403/proxy de la ayuda de PythonAnywhere si aparecen errores de conexión.
- Resumen de consejos desactualizados a filtrar en cualquier tutorial: el nombre "Web Apps"; `sendData` con botón de teclado como forma principal de devolver datos (no entrega `initData`); trucos de scroll para evitar el colapso (reemplazados por `disableVerticalSwipes` desde 7.7); "PythonAnywhere gratis no admite webhooks de Telegram" (revertido en 2024); vencimiento de la web app a los tres meses y plan Hacker de USD 5 (cambiaron en enero de 2026); `telepot`; el proxy vía `telegram.utils.request` de `python-telegram-bot` anterior a v20; el parámetro `lifetime` de `init-data-py` 0.2.x.

### Gaps
- No busqué en YouTube ni en comunidades en ruso o español más allá de lo que devolvió el buscador; puede existir material no indexado en estas búsquedas.
- No revisé los ejemplos oficiales de `python-telegram-bot` (`webappbot.py`) ni de `aiogram` (ejemplo de web app con aiohttp); hasta donde sé ninguno usa Flask.
- Los ejemplos reales de apps de votación en Telegram los cubre otro investigador (`ejemplos_y_experiencia.md` en la misma carpeta).
