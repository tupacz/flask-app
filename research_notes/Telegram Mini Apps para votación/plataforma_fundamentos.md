# Plataforma Telegram Mini Apps: fundamentos (estado al 17 de noviembre de 2026)

Nota de método. Las fuentes primarias son la documentación oficial de Telegram, consultada el 17/11/2026. La versión vigente del Bot API es la **10.4 (9 de noviembre de 2026)**. Los datos marcados "(verificado en texto crudo)" fueron contrastados con el HTML descargado de core.telegram.org y no solo con un resumen automático. Los identificadores de API quedan en inglés tal como figuran en la documentación.

## 1. Qué es exactamente una Mini App y qué requisitos tiene

### Takeaway
Una Mini App es una página web común (HTML, CSS y JavaScript) que Telegram carga dentro de un WebView propio y que siempre está atada a un bot. No existe sin bot. La página incluye el script `telegram-web-app.js`, que le da el objeto `window.Telegram.WebApp` para hablar con el cliente de Telegram. "Web Apps" y "Bot Web Apps" son nombres viejos que sobreviven en los identificadores (`web_app`, `WebAppInfo`, `WebAppInitData`).

### Cited Findings
- Definición oficial: las Mini Apps permiten crear interfaces con JavaScript que se abren dentro de Telegram y "pueden reemplazar por completo a cualquier sitio web". Soportan autorización transparente, pagos y notificaciones por medio del bot. — [Telegram Mini Apps (oficial)](https://core.telegram.org/bots/webapps)
- "Web Apps" es el nombre anterior. Algunos nombres de la API como `web_app` y `WebAppInfo` lo conservan. — [Bot Features (oficial)](https://core.telegram.org/bots/features)
- Técnicamente "son aplicaciones web típicas que se muestran en un WebView". El desarrollador entrega una URL y Telegram la carga. Son un agregado de los bots, así que no se puede crear una Mini App sin bot. — [docs.telegram-mini-apps.com, About](https://docs.telegram-mini-apps.com/platform/about)
- El script se incluye en el `<head>` antes que cualquier otro script. Etiqueta exacta hoy (verificado en texto crudo): `<script src="https://telegram.org/js/telegram-web-app.js?65"></script>`. — [Telegram Mini Apps, "Initializing Mini Apps"](https://core.telegram.org/bots/webapps)
- En producción solo se aceptan enlaces HTTPS válidos. En el entorno de prueba se aceptan enlaces HTTP sin TLS e incluso direcciones IP. — [docs.telegram-mini-apps.com, Creating New App](https://docs.telegram-mini-apps.com/platform/creating-new-app) y [Telegram Mini Apps, "Testing Mini Apps"](https://core.telegram.org/bots/webapps)
- El bot se crea con `/newbot` en @BotFather (nombre, username de 5 a 32 caracteres terminado en "bot", y devuelve el token). — [Bot Features](https://core.telegram.org/bots/features)
- Clientes que soportan Mini Apps y su identificador en `Telegram.WebApp.platform`: Android (`android`), iOS (`ios`), macOS (`macos`), Telegram Desktop (`tdesktop`), Telegram Web A (`weba`), Telegram Web K (`web`). Cada cliente se desarrolla por separado y el comportamiento puede diferir. — [docs.telegram-mini-apps.com, About](https://docs.telegram-mini-apps.com/platform/about)
- Telegram afirma que más de 500 millones de sus 950 millones de usuarios usan Mini Apps cada mes. — [Bot Features](https://core.telegram.org/bots/features) (la cifra de 950 millones es de 2024, así que el dato puede estar desactualizado)
- Novedad de 2026: existe **Telegram Serverless**, que permite alojar el backend del bot y el front-end de la Mini App en infraestructura de Telegram (`https://app<app_id>.tgcloud.ai/`). Solo admite módulos JavaScript en un sandbox V8, sin paquetes npm, con una base tipo SQLite por bot. Se activa en @BotFather (bot > Serverless). La página registra una actualización del 6 de octubre de 2026 que sumó el hosting de Mini Apps y los endpoints. — [Telegram Serverless (oficial)](https://core.telegram.org/bots/serverless)

### Inferences
- Para un desarrollador Flask, la Mini App es una ruta Flask más servida por HTTPS (PythonAnywhere ya da HTTPS). Lo único nuevo es el script de Telegram en el template y la validación de `initData` en el servidor.
- El número `?65` del script es un parámetro de cache-busting que Telegram va subiendo. Los tutoriales viejos muestran números menores o ninguno. Conviene copiar siempre la etiqueta de la documentación oficial vigente.
- Telegram Serverless no sirve para un backend en Python porque solo ejecuta JavaScript. Es una alternativa, no un requisito.

### Gaps
- La página de Serverless no indica precios, cuotas ni si está en beta. Tampoco dice en qué versión del Bot API apareció el objeto `Telegram.WebApp.Serverless` (la documentación lo marca solo como "NEW").
- No encontré una lista oficial de los valores posibles de `platform`. La lista de arriba es de la documentación comunitaria.

## 2. Formas de lanzar una Mini App y en qué se diferencian

### Takeaway
La documentación oficial enumera siete formas de lanzamiento (más una octava para solicitudes de ingreso a chats, agregada en Bot API 10.1). Cambian tres cosas según la forma: qué trae `initData`, si la app puede mandar algo al chat, y en qué tipos de chat está disponible. Dato clave para grupos: los botones `web_app` (teclado e inline) solo funcionan en chats privados con el bot, así que en un grupo la vía práctica es un enlace directo `t.me/bot/app?startapp=...` o `t.me/bot?startapp=...`, que además entrega `chat_type` y `chat_instance`.

### Cited Findings
- "Telegram soporta actualmente siete formas de lanzar Mini Apps": Main Mini App desde el botón del perfil, botón de teclado, botón inline, botón de menú, modo inline, enlace directo y menú de adjuntos (verificado en texto crudo). — [Telegram Mini Apps, "Implementing Mini Apps"](https://core.telegram.org/bots/webapps)

| Forma | Cómo se configura | Qué recibe la app | Qué puede hacer |
|---|---|---|---|
| Botón de teclado (reply keyboard) | `KeyboardButton` con campo `web_app` | `initData` **vacío** | `Telegram.WebApp.sendData(data)` (hasta 4096 bytes). Envía un mensaje de servicio `web_app_data` al bot y cierra la app. Es la única forma que admite `sendData` |
| Botón inline | `InlineKeyboardButton` con campo `web_app` | `user` (ID, nombre, username, `language_code`) y `query_id` | El bot llama a `answerWebAppQuery` con el `query_id` para mandar un mensaje en nombre del usuario y cerrar la app |
| Botón de menú | `/setmenubutton` o Bot Settings > Menu Button en @BotFather, o el método `setChatMenuButton` (`MenuButtonWebApp`) | Igual que el botón inline | Igual que el botón inline |
| Main Mini App | Se configura en @BotFather. Botón "Launch app" en el perfil y enlace `https://t.me/botusername?startapp` | `start_param` y parámetro GET `tgWebAppStartParam` si `startapp` no está vacío. `chat_type` y `chat_instance` | Uso compartido por varios miembros de un chat. No puede escribir en el chat |
| Modo inline | `InlineQueryResultsButton` con `web_app` en `answerInlineQuery` | `initData` **vacío** | `switchInlineQuery(query[, choose_chat_types])` devuelve al usuario al modo inline. No tiene acceso al chat |
| Enlace directo | `https://t.me/botusername/appname` | `start_param`, `tgWebAppStartParam`, `chat_type`, `chat_instance` | Sin acceso al chat. Para enviar mensajes el usuario debe pasar por modo inline y elegir un resultado |
| Menú de adjuntos | `/setattach` o Bot Settings > Configure Attachment Menu | `user`, `receiver` (solo chats privados), `chat` (grupos, supergrupos, canales), `start_param` (vía `startattach`), `query_id` | `answerWebAppQuery` manda un mensaje al chat desde donde se abrió |
| Solicitud de ingreso (10.1) | Bot configurado como "guard bot". Método `sendChatJoinRequestWebApp` | `chat_join_request_query_id`, datos del usuario y del chat | `answerChatJoinRequestQuery` resuelve la solicitud |

Fuente de toda la tabla: [Telegram Mini Apps, "Implementing Mini Apps"](https://core.telegram.org/bots/webapps)

- Restricción de chats del botón de teclado (verificado en texto crudo): "The Web App will be able to send a 'web_app_data' service message. Available in private chats only." — [Bot API, KeyboardButton](https://core.telegram.org/bots/api)
- Restricción del botón inline (verificado en texto crudo): "Available only in private chats between a user and the bot. Not supported for messages sent on behalf of a business account and ephemeral messages." — [Bot API, InlineKeyboardButton](https://core.telegram.org/bots/api)
- `MenuButtonWebApp` acepta, en lugar de la URL, un enlace t.me a una Mini App del bot, y en ese caso se abre como si el usuario hubiera tocado el enlace (desde Bot API 7.6). — [Bot API, MenuButtonWebApp](https://core.telegram.org/bots/api) y [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- El objeto `WebAppInitData` está vacío si la Mini App se lanzó desde un botón de teclado o desde modo inline. — [Telegram Mini Apps, WebAppInitData](https://core.telegram.org/bots/webapps)
- `chat_type` puede valer `sender`, `private`, `group`, `supergroup` o `channel`. `chat_instance` es un identificador global del chat. Ambos se devuelven solo en lanzamientos por enlace directo. — [Telegram Mini Apps, WebAppInitData](https://core.telegram.org/bots/webapps)
- Con `chat_type` y `chat_instance` las Mini Apps pueden seguir el contexto del chat, lo que permite "uso concurrente y compartido por varios miembros" (pizarras, pedidos grupales, juegos multijugador). — [Telegram Mini Apps, "Direct Link Mini Apps"](https://core.telegram.org/bots/webapps)
- Formatos de enlace exactos (verificado en texto crudo): `https://t.me/botusername?startapp`, `https://t.me/botusername?startapp=command`, `https://t.me/botusername?startapp=command&mode=compact`, `https://t.me/botusername/appname`, `https://t.me/botusername/appname?startapp=command`, `https://t.me/botusername/appname?startapp=command&mode=compact`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Desde Bot API 7.6 las Mini Apps de enlace directo abren a altura completa por defecto y el usuario no puede reducirlas. `mode=compact` las abre a media pantalla. La Main Mini App se comporta igual y el modo también se puede cambiar en @BotFather. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Parámetro de inicio: caracteres permitidos A-Z, a-z, 0-9, `_` y `-`. La documentación comunitaria da un máximo de 512 caracteres y la expresión `/^[\w-]{0,512}$/`, y recomienda base64url para otros contenidos. — [docs.telegram-mini-apps.com, Start Parameter](https://docs.telegram-mini-apps.com/platform/start-parameter)
- El menú de adjuntos está disponible solo para grandes anunciantes de Telegram Ad Platform. Todos los bots pueden probarlo en el entorno de prueba (verificado en texto crudo). — [Telegram Mini Apps, "Attachment Menu"](https://core.telegram.org/bots/webapps)
- Acceso desde la pantalla de inicio del teléfono (Bot API 8.0): `addToHomeScreen()` pide al usuario crear el acceso directo y `checkHomeScreenStatus()` devuelve `unsupported`, `unknown`, `added` o `missed`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Los bots con Main Mini App aparecen en la pestaña "Apps" de la búsqueda para los usuarios que ya los abrieron. — [Telegram Mini Apps, "Launching the main Mini App"](https://core.telegram.org/bots/webapps)
- `can_send_after` indica cuántos segundos hay que esperar antes de poder usar `answerWebAppQuery`. — [Telegram Mini Apps, WebAppInitData](https://core.telegram.org/bots/webapps)
- Conflicto interno de la documentación oficial: la tabla de `WebAppInitData` describe `start_param` como "el valor del parámetro `startattach`, devuelto solo al lanzar desde el menú de adjuntos por enlace", pero las secciones de Main Mini App y enlace directo dicen que `startapp` también llega en `start_param` y en `tgWebAppStartParam`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)

### Inferences
- En un grupo no sirven los botones `web_app`. Lo que funciona es publicar un enlace `t.me/<bot>/<app>?startapp=<id>` o `t.me/<bot>?startapp=<id>` (como texto o como botón inline de tipo `url`). En ese caso la app recibe `user`, `start_param`, `chat_type` y `chat_instance`, todo firmado dentro de `initData`.
- `chat_instance` identifica el chat de forma opaca. No es el `chat.id` del Bot API, así que sirve para agrupar votos por chat pero no para llamar a métodos del bot sobre ese chat.
- Como las formas por enlace directo no pueden escribir en el chat, cualquier anuncio de resultados lo tiene que mandar el bot por su cuenta (con `sendMessage` desde el servidor) o el usuario con `shareMessage` o modo inline.
- La descripción de `start_param` en la tabla de campos parece haber quedado vieja. En la práctica `startapp` llega en ambos lugares, como indican las secciones narrativas y la documentación comunitaria.

### Gaps
- La documentación oficial de Mini Apps no fija la longitud máxima de `startapp`. La página Bot Features da 64 caracteres para los deep links `start` y `startgroup`, y la documentación comunitaria da 512 para `startapp`. No pude confirmar el valor de 512 en una fuente oficial.
- `mode=fullscreen` no aparece en la página oficial de Mini Apps. No verifiqué si está documentado en otra página de Telegram (por ejemplo la de enlaces t.me).
- No verifiqué qué recibe exactamente la app cuando se abre desde el acceso directo de la pantalla de inicio.

## 3. Qué expone `window.Telegram.WebApp` (telegram-web-app.js)

### Takeaway
El objeto `Telegram.WebApp` da datos de arranque (`initData`), tema y viewport, botones nativos, popups, vibración, almacenamiento en tres variantes, sensores, y métodos para compartir, pagar y navegar. Cada método indica desde qué versión del Bot API existe y se debe proteger con `isVersionAtLeast()` porque los clientes viejos no lo tienen.

### Cited Findings
- **Campos principales**: `initData` (string crudo), `initDataUnsafe` (objeto `WebAppInitData`), `version`, `platform`, `colorScheme`, `themeParams`, `isActive` (8.0+), `isExpanded`, `viewportHeight`, `viewportStableHeight`, `headerColor`, `backgroundColor`, `bottomBarColor`, `isClosingConfirmationEnabled`, `isVerticalSwipesEnabled`, `isFullscreen`, `isOrientationLocked`, `safeAreaInset`, `contentSafeAreaInset`, `BackButton`, `MainButton`, `SecondaryButton`, `SettingsButton`, `HapticFeedback`, `CloudStorage`, `BiometricManager`, `Accelerometer`, `DeviceOrientation`, `Gyroscope`, `LocationManager`, `DeviceStorage`, `SecureStorage`, `Serverless` (marcado "NEW"). — [Telegram Mini Apps, "Initializing Mini Apps"](https://core.telegram.org/bots/webapps)
- Advertencia oficial sobre `initDataUnsafe` (verificado en texto crudo): "Data from this field should not be trusted. You should only use data from initData on the bot's server and only after it has been validated." — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Ciclo de vida**: `ready()` avisa a Telegram que la app ya se puede mostrar y oculta el placeholder de carga (hay que llamarlo lo antes posible). `expand()` lleva la app a la altura máxima. `close()` la cierra. `isVersionAtLeast(version)` compara versiones. `onEvent(eventType, eventHandler)` y `offEvent(...)` manejan eventos. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Apariencia**: `setHeaderColor(color)` (6.1+), `setBackgroundColor(color)` (6.1+), `setBottomBarColor(color)` (7.10+). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Cierre y gestos**: `enableClosingConfirmation()` y `disableClosingConfirmation()` (6.2+), `enableVerticalSwipes()` y `disableVerticalSwipes()` (7.7+). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Pantalla completa y orientación** (8.0+): `requestFullscreen()`, `exitFullscreen()`, `lockOrientation()`, `unlockOrientation()`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Pantalla de inicio** (8.0+): `addToHomeScreen()`, `checkHomeScreenStatus([callback])`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Envío de datos y navegación**: `sendData(data)` (solo botón de teclado, hasta 4096 bytes), `switchInlineQuery(query[, choose_chat_types])` (6.7+, tipos `users`, `bots`, `groups`, `channels`), `openLink(url[, options])` (opción `try_instant_view` 6.4+), `openTelegramLink(url)` (desde 7.0 ya no cierra la app), `openInvoice(url[, callback])` (6.1+). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Compartir** : `shareToStory(media_url[, params])` (7.8+), `shareMessage(msg_id[, callback])` (8.0+), `downloadFile(params[, callback])` (8.0+). El `msg_id` de `shareMessage` debe pertenecer a un `PreparedInlineMessage` obtenido antes con el método del Bot API `savePreparedInlineMessage` (verificado en texto crudo). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Emoji status** (8.0+): `setEmojiStatus(custom_emoji_id[, params, callback])`, `requestEmojiStatusAccess([callback])`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Popups nativos** (6.2+): `showPopup(params[, callback])`, `showAlert(message[, callback])`, `showConfirm(message[, callback])`. Límites de `showPopup`: `title` 0 a 64 caracteres, `message` 1 a 256, de 1 a 3 botones, `id` y `text` de cada botón 0 a 64 (verificado en texto crudo). — [Telegram Mini Apps, PopupParams](https://core.telegram.org/bots/webapps)
- **Otros**: `showScanQrPopup(params[, callback])` y `closeScanQrPopup()` (6.4+), `readTextFromClipboard([callback])` (6.4+), `requestWriteAccess([callback])` y `requestContact([callback])` (6.9+), `hideKeyboard()` (9.1+), `requestChat(req_id[, callback])` (9.6+). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Botones inferiores**: `Telegram.WebApp.MainButton` y `Telegram.WebApp.SecondaryButton` son ambos de la clase `BottomButton` (la clase `MainButton` fue renombrada a `BottomButton` en Bot API 7.10). Campos: `type`, `text`, `color`, `textColor`, `isVisible`, `isActive`, `isProgressVisible`, `hasShineEffect` (7.10+), `position` (7.10+), `iconCustomEmojiId` (9.5+). Métodos: `setText`, `onClick`, `offClick`, `show`, `hide`, `enable`, `disable`, `showProgress`, `hideProgress`, `setParams`. — [Telegram Mini Apps, BottomButton](https://core.telegram.org/bots/webapps)
- **`BackButton`**: campo `isVisible` y métodos `onClick`, `offClick`, `show`, `hide` (6.1+). **`SettingsButton`**: lo mismo (7.0+). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **`HapticFeedback`** (6.1+): `impactOccurred`, `notificationOccurred`, `selectionChanged`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **`CloudStorage`** (6.9+): `setItem`, `getItem`, `getItems`, `removeItem`, `removeItems`, `getKeys`. Límites (verificado en texto crudo): hasta 1024 claves, clave de 1 a 128 caracteres con solo A-Z, a-z, 0-9, `_` y `-`, valor de 0 a 4096 caracteres. — [Telegram Mini Apps, CloudStorage](https://core.telegram.org/bots/webapps)
- **`DeviceStorage`** (9.0+): almacenamiento local por dispositivo, parecido a `localStorage`, hasta 5 MB por usuario y bot. Métodos `setItem`, `getItem`, `removeItem`, `clear`. — [Telegram Mini Apps, DeviceStorage](https://core.telegram.org/bots/webapps)
- **`SecureStorage`** (9.0+): usa Keychain en iOS y Keystore en Android, hasta 10 ítems por usuario y bot. Métodos `setItem`, `getItem`, `restoreItem`, `removeItem`, `clear`. — [Telegram Mini Apps, SecureStorage](https://core.telegram.org/bots/webapps)
- **`BiometricManager`** (7.2+): `init`, `requestAccess`, `authenticate`, `updateBiometricToken`, `openSettings`. **`LocationManager`** (8.0+): `init`, `getLocation`, `openSettings`. **`Accelerometer`, `DeviceOrientation`, `Gyroscope`** (8.0+): `start` y `stop`, con `refresh_rate` de 20 a 1000 ms. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **`Serverless`**: `call(name[, input][, callback])` llama a un endpoint de una Mini App alojada en Telegram Serverless. Cada llamada viaja con el `initData`, que la plataforma valida antes de ejecutar el endpoint. — [Telegram Mini Apps, Serverless](https://core.telegram.org/bots/webapps)
- **`ThemeParams`** (colores `#RRGGBB`, todos opcionales): `bg_color`, `text_color`, `hint_color`, `link_color`, `button_color`, `button_text_color`, `secondary_bg_color` (6.1+), `header_bg_color`, `accent_text_color`, `section_bg_color`, `section_header_text_color`, `subtitle_text_color`, `destructive_text_color` (7.0+), `section_separator_color` (7.6+), `bottom_bar_bg_color` (7.10+). — [Telegram Mini Apps, ThemeParams](https://core.telegram.org/bots/webapps)
- **Variables CSS** que el script define: `--tg-color-scheme`, `--tg-viewport-height`, `--tg-viewport-stable-height`, la familia `--tg-theme-*` (por ejemplo `--tg-theme-bg-color`, `--tg-theme-text-color`, `--tg-theme-button-color`, `--tg-theme-secondary-bg-color`), `--tg-safe-area-inset-top|bottom|left|right` y `--tg-content-safe-area-inset-top|bottom|left|right`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- `viewportStableHeight` no cambia durante gestos o animaciones y se actualiza al terminar (evento `viewportChanged` con `isStateStable=true`). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- `safeAreaInset` cubre las zonas del sistema (notch, indicador de inicio) y `contentSafeAreaInset` cubre la interfaz propia de Telegram. Importan sobre todo en pantalla completa. — [Adsgram, errores comunes en Mini Apps (ago. 2026, actualizado oct. 2026)](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Eventos** de `onEvent`: `themeChanged`, `viewportChanged`, `mainButtonClicked`, `backButtonClicked`, `settingsButtonClicked`, `invoiceClosed` (6.1+), `popupClosed` (6.2+), `qrTextReceived`, `clipboardTextReceived` (6.4+), `writeAccessRequested`, `contactRequested` (6.9+), `biometricManagerUpdated`, `biometricAuthRequested`, `biometricTokenUpdated` (7.2+), `scanQrPopupClosed` (7.7+), `secondaryButtonClicked` (7.10+), y en 8.0+ `activated`, `deactivated`, `safeAreaChanged`, `contentSafeAreaChanged`, `fullscreenChanged`, `fullscreenFailed`, `homeScreenAdded`, `homeScreenChecked`, `accelerometer*`, `deviceOrientation*`, `gyroscope*`, `locationManagerUpdated`, `locationRequested`, `shareMessageSent`, `shareMessageFailed`, `emojiStatusSet`, `emojiStatusFailed`, `emojiStatusAccessRequested`, `fileDownloadRequested`. — [Telegram Mini Apps, "Events Available for Mini Apps"](https://core.telegram.org/bots/webapps)
- Algunos métodos solo funcionan como respuesta a una interacción del usuario (por ejemplo `openLink` y los `openSettings` de biometría y ubicación). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Para `downloadFile` el servidor debe responder con `Content-Disposition: attachment; filename="<file_name>"` y `Access-Control-Allow-Origin: https://web.telegram.org` (verificado en texto crudo). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)

### Inferences
- "BottomButton" no es un campo de `Telegram.WebApp` sino el nombre de la clase. En el código se sigue escribiendo `Telegram.WebApp.MainButton` y `Telegram.WebApp.SecondaryButton`.
- Para una app de votación con lista arrastrable conviene llamar `ready()`, `expand()` y `disableVerticalSwipes()` al iniciar, porque el gesto vertical de cerrar compite con el arrastre de SortableJS. `enableClosingConfirmation()` evita perder un orden a medio armar. `MainButton` reemplaza al botón "Enviar" propio y `HapticFeedback` da respuesta táctil al soltar un ítem.
- `CloudStorage` es por usuario y por bot, así que sirve para preferencias o un borrador del voto pero no para guardar los votos de todos. Eso sigue yendo al servidor.

### Gaps
- No relevé los parámetros finos de cada método (por ejemplo los campos de `StoryShareParams` o `DownloadFileParams`). Están en la página oficial.
- La documentación no dice cuánto tiempo persiste `CloudStorage` ni si expira. Solo da límites de tamaño.

## 4. Identificación del usuario y validación de `initData` en el servidor

### Takeaway
El usuario llega identificado sin login: `Telegram.WebApp.initData` es un query string firmado por Telegram que incluye `user` (JSON), `auth_date`, `hash` y `signature`. El servidor debe recalcular el `hash` con HMAC-SHA256 usando el token del bot y descartar datos viejos mirando `auth_date`. Desde Bot API 8.0 existe además una firma Ed25519 que un tercero puede verificar con la clave pública de Telegram sin conocer el token.

### Cited Findings
- **Campos de `WebAppInitData`**: `query_id`, `chat_join_request_query_id` (10.1), `user`, `receiver`, `chat`, `chat_type`, `chat_instance`, `start_param`, `can_send_after`, `auth_date` (Unix time de apertura), `hash`, `signature` (firma de todos los parámetros salvo `hash`, pensada para terceros). — [Telegram Mini Apps, WebAppInitData](https://core.telegram.org/bots/webapps)
- **Campos de `WebAppUser`**: `id` (entero de hasta 52 bits significativos, entra en un entero de 64 bits o un double), `is_bot` (solo en `receiver`), `first_name`, `last_name` (opcional), `username` (opcional), `language_code` (opcional, solo en `user`), `is_premium` (opcional), `added_to_attachment_menu` (opcional), `allows_write_to_pm` (opcional), `photo_url` (opcional, .jpeg o .svg). — [Telegram Mini Apps, WebAppUser](https://core.telegram.org/bots/webapps)
- Desde Bot API 8.0 `photo_url` está disponible para todas las Mini Apps "si la configuración de privacidad del usuario lo permite". — [Telegram Mini Apps, cambios del 17/11/2024](https://core.telegram.org/bots/webapps)
- **Campos de `WebAppChat`**: `id`, `type` (`group`, `supergroup`, `channel`), `title`, `username` (opcional), `photo_url` (opcional). Solo llega en lanzamientos desde el menú de adjuntos o en solicitudes de ingreso. — [Telegram Mini Apps, WebAppChat](https://core.telegram.org/bots/webapps)
- **Algoritmo oficial con token** (verificado en texto crudo): se compara el `hash` recibido con la representación hexadecimal del HMAC-SHA-256 del data-check-string, usando como clave secreta el HMAC-SHA-256 del token del bot con la constante `WebAppData` como clave. Pseudocódigo oficial: `secret_key = HMAC_SHA256(<bot_token>, "WebAppData")` y luego `if (hex(HMAC_SHA256(data_check_string, secret_key)) == hash)`. — [Telegram Mini Apps, "Validating data received via the Mini App"](https://core.telegram.org/bots/webapps)
- El data-check-string es la cadena de todos los campos recibidos (sin `hash`), ordenados alfabéticamente, en formato `key=<value>` y separados por salto de línea (`\n`, 0x0A). Ejemplo: `auth_date=<auth_date>\nquery_id=<query_id>\nuser=<user>`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Sobre `auth_date` (verificado en texto crudo): "To prevent the use of outdated data, you can additionally check the auth_date field, which contains a Unix timestamp of when it was received by the Mini App." La documentación oficial no fija una ventana de tiempo. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Práctica reportada: rechazar datos más viejos que una ventana fija ("24 horas es un valor por defecto común, menos si hay dinero de por medio") y luego canjear el `initData` validado por un token de sesión propio. — [Adsgram, errores comunes](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Validación para terceros (Ed25519, Bot API 8.0)**: se verifica `signature`, que es la firma Ed25519 del data-check-string codificada en base64url, con la clave pública de Telegram. El data-check-string empieza con `<bot_id>:WebAppData`, un salto de línea, y sigue con los campos ordenados sin `hash` ni `signature`. Ejemplo: `12345678:WebAppData\nauth_date=<auth_date>\nquery_id=<query_id>\nuser=<user>`. — [Telegram Mini Apps, "Validating data for Third-Party Use"](https://core.telegram.org/bots/webapps)
- Claves públicas Ed25519 (hex): producción `e7bf03a2fa4602af4580703d88dda5bb59f32ed8b02a56c187fe7d34caed242d`, entorno de prueba `40055058a4ee38156a06562e52eece92a771bcd8346a8c4615cb7376eddf72ec`. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps), coincide con [docs.telegram-mini-apps.com, Init Data](https://docs.telegram-mini-apps.com/platform/init-data)
- La firma llega en base64url sin relleno y algunos decodificadores estrictos la rechazan. Hay que reponer los `=` antes de decodificar. — [docs.telegram-mini-apps.com, Init Data](https://docs.telegram-mini-apps.com/platform/init-data) y [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- Convención comunitaria para mandar el dato al backend: cabecera `Authorization: tma <initDataRaw>`. — [docs.telegram-mini-apps.com, Init Data](https://docs.telegram-mini-apps.com/platform/init-data)
- Errores típicos: confiar en `initDataUnsafe`, aceptar un `user_id` como parámetro suelto del request, no revisar `auth_date`, y confiar en el parámetro `startapp` sin leerlo del `initData` validado. Se recomienda comparación en tiempo constante y no exponer nunca el token al cliente. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- Para obtener el teléfono hace falta `requestContact()` y para poder escribirle al usuario hace falta `requestWriteAccess()` (o que `allows_write_to_pm` ya sea verdadero). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)

### Inferences
- Traducción directa del pseudocódigo oficial a Python con biblioteca estándar (no la ejecuté contra datos reales):

```python
import hashlib, hmac, json, time
from urllib.parse import parse_qsl

def validar_init_data(init_data: str, bot_token: str, max_edad_seg: int = 86400):
    campos = dict(parse_qsl(init_data, keep_blank_values=True))
    hash_recibido = campos.pop("hash", None)
    if not hash_recibido:
        return None
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(campos.items()))
    secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculado = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculado, hash_recibido):
        return None
    if time.time() - int(campos.get("auth_date", 0)) > max_edad_seg:
        return None
    return json.loads(campos["user"]) if "user" in campos else {}
```

- El error más común es invertir los argumentos del primer HMAC. La clave es la cadena `WebAppData` y el mensaje es el token, no al revés. En la variante HMAC el campo `signature` sí forma parte del data-check-string (solo se excluye `hash`).
- `user.id` es el único identificador estable. `username`, `first_name` y `photo_url` pueden cambiar o faltar, así que la unicidad del voto debe basarse en `id`.
- Los lanzamientos por botón de teclado o modo inline traen `initData` vacío, así que no sirven para identificar al votante de forma verificable.
- Para un solo bot propio alcanza con la validación HMAC. La Ed25519 solo hace falta si un tercero valida sin el token.

### Gaps
- La documentación oficial no recomienda una duración concreta para `auth_date`. Las 24 horas vienen de un blog de un proveedor, no de Telegram.
- La documentación comunitaria no menciona bibliotecas de Python para validar. No busqué paquetes de PyPI porque la integración con Flask la cubre otro investigador.

## 5. Capacidades nuevas de 2024, 2025 y 2026

### Takeaway
El salto grande fue Bot API 8.0 (17/11/2024): pantalla completa, acceso directo en pantalla de inicio, emoji status, compartir mensajes, descargas, geolocalización, sensores de movimiento, suscripciones con Stars y validación para terceros. En 2025 llegaron `DeviceStorage`, `SecureStorage` y `hideKeyboard`. En 2026 lo más relevante para Mini Apps es `requestChat` (9.6), el lanzamiento en solicitudes de ingreso (10.1), el bloqueo de métodos desde otros orígenes (10.2), Telegram Serverless y, como formato aparte, los widgets HTML dentro de mensajes (10.4).

### Cited Findings
- **Última versión**: Bot API 10.4, 9 de noviembre de 2026 (verificado en texto crudo). — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **7.2 (31/03/2024)**: `BiometricManager`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **7.4 (28/05/2024)**: pagos con Telegram Stars (moneda `XTR`). — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **7.6 (01/07/2024)**: cambia el modo de apertura por defecto de las Mini Apps de enlace directo, `MenuButtonWebApp` acepta enlaces t.me, `section_separator_color`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **7.7 (07/07/2024)**: `isVerticalSwipesEnabled`, `enableVerticalSwipes`, `disableVerticalSwipes`, evento `scanQrPopupClosed`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **7.8 (31/07/2024)**: Main Mini App y `shareToStory`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **7.10 (06/09/2024)**: `SecondaryButton`, evento `secondaryButtonClicked`, la clase `MainButton` pasa a llamarse `BottomButton`, `bottomBarColor`, `setBottomBarColor`, `bottom_bar_bg_color`. — [Telegram Mini Apps, "Recent changes"](https://core.telegram.org/bots/webapps)
- **8.0 (17/11/2024)**, la actualización más grande de Mini Apps: pantalla completa en vertical y horizontal (`requestFullscreen`, `exitFullscreen`, `safeAreaInset`, `contentSafeAreaInset`, `isActive`, `isFullscreen`), accesos directos (`addToHomeScreen`, `checkHomeScreenStatus`), emoji status (`setEmojiStatus`, `requestEmojiStatusAccess`, y el método de bot `setUserEmojiStatus`), compartir y descargar (`shareMessage`, `downloadFile`), `LocationManager`, `Accelerometer`, `DeviceOrientation`, `Gyroscope`, `lockOrientation`, `unlockOrientation`, suscripciones pagas y regalos con Stars, pantalla de carga personalizable, información de hardware en el User-Agent de Android, `photo_url` para todas las apps, validación para terceros y depuración completa en iOS. — [Telegram Mini Apps, "Recent changes"](https://core.telegram.org/bots/webapps)
- **9.0 (11/04/2025)**: `DeviceStorage` y `SecureStorage`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **9.1 (03/07/2025)**: `hideKeyboard`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **9.5 (01/03/2026)**: `iconCustomEmojiId` en `BottomButton`. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **9.6 (03/04/2026)**: "Added the method requestChat to the class WebApp" y la clase `PreparedKeyboardButton` con el método `savePreparedKeyboardButton`, que permiten pedir usuarios, chats y bots administrados desde una Mini App. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **10.1 (11/06/2026)**: campo `chat_join_request_query_id` en `WebAppInitData`, métodos `sendChatJoinRequestWebApp` y `answerChatJoinRequestQuery`, campo `guard_bot` en `ChatFullInfo`. Además los resultados de consultas de Web App pueden llevar contenido de "rich messages". — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **10.2 (14/07/2026)**, endurecimiento de seguridad: se prohíbe usar métodos de Mini App "desde orígenes distintos del dominio original de la Mini App". La protección se activó automáticamente para todas las Mini Apps el 20 de julio de 2026. Se puede desactivar desde la Mini App de @BotFather, y en ese caso el bot asume la responsabilidad de que la app no tenga enlaces a sitios no confiables. — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **10.3 (24/08/2026)**: sin cambios de Mini Apps (botones en rich messages, mensajes efímeros, botones inline deshabilitados). — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- **10.4 (09/11/2026)**: widgets HTML. Clase `Widget`, método `sendWidget`, `WidgetQuery`, `answerWidgetQuery`, `editMessageWidgetData`, `sendSharedWidget`. Por ahora, en producción, los widgets solo se pueden enviar a chats privados, quedan con contenido protegido (no se pueden reenviar) y no se pueden enviar como respuesta a consultas inline (verificado en texto crudo). — [Bot API changelog](https://core.telegram.org/bots/api-changelog)
- Los widgets viven dentro de la burbuja del mensaje, a diferencia de las Mini Apps tradicionales que abren páginas web alojadas por el desarrollador. — [Digital Trends](https://digitaltrends.com/phones/telegram-is-turning-chat-messages-into-mini-apps-because-apparently-switching-apps-is-so-last-year)
- **Telegram Serverless** (actualización del 06/10/2026 con hosting de Mini Apps, endpoints, CLI 0.2.0 y `tgcloud.jsonc`) y el objeto `Telegram.WebApp.Serverless`. — [Telegram Serverless](https://core.telegram.org/bots/serverless)
- Otras novedades de 2026 fuera de Mini Apps pero del mismo ecosistema: modo invitado para bots (10.0), mensajes efímeros y Communities (10.2), encuestas con más opciones, varias respuestas correctas y revoto (9.6, 10.0). — [Bot API changelog](https://core.telegram.org/bots/api-changelog)

### Inferences
- Los widgets HTML de 10.4 todavía no sirven para una votación en grupo, porque en producción solo se envían a chats privados. Conviene seguirlos de cerca porque apuntan justo a interfaces interactivas dentro del mensaje.
- El bloqueo por origen de 10.2 rompe los flujos donde la Mini App redirige a otro dominio y desde ahí llama a `Telegram.WebApp`. Todo lo que use el SDK tiene que quedar bajo el dominio registrado (por ejemplo `tupac.pythonanywhere.com`).
- Las mejoras de encuestas nativas de 2026 son una alternativa a evaluar para votaciones simples, aunque no cubren un ranking ordenado tipo Condorcet.

### Gaps
- No leí el detalle completo de cada entrada 10.x (el changelog es largo y parte del texto quedó resumido). Los puntos de Mini Apps de 10.2 y 10.4 sí fueron verificados en el texto crudo.
- No encontré una entrada de blog de telegram.org específica de las novedades de Mini Apps de 2026. Las fuentes fueron el changelog y la documentación.

## 6. Limitaciones y reglas de la plataforma

### Takeaway
Los límites duros son pocos y están documentados (tamaños de `CloudStorage`, `sendData`, popups, botones `web_app` solo en privado, menú de adjuntos restringido, bienes digitales solo con Stars). Los problemas reales vienen del WebView: cada cliente se comporta distinto, `localStorage` y las cookies no son confiables, y los logins de terceros como Google OAuth fallan dentro de la app.

### Cited Findings
- **Pagos**: los bienes y servicios digitales deben cobrarse en Telegram Stars con moneda `XTR`. Telegram indica que, por las políticas de las tiendas de apps, no admite vender bienes digitales en otras monedas. Los bienes físicos usan proveedores de pago tradicionales. — [Bot Features, Payments](https://core.telegram.org/bots/features)
- Para ser destacada en la Mini App Store, la app debe tener Main Mini App, medios de demostración y aceptar pagos en Stars. No hay garantía de ser destacada. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps) y [Bot Features](https://core.telegram.org/bots/features)
- **Límites de tamaño**: `CloudStorage` 1024 claves, clave 1 a 128 caracteres, valor 0 a 4096 caracteres. `DeviceStorage` 5 MB. `SecureStorage` 10 ítems. `sendData` 4096 bytes. `showPopup` título 64, mensaje 256, 3 botones. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Disponibilidad**: `KeyboardButton.web_app` solo en chats privados e `InlineKeyboardButton.web_app` solo en chats privados entre el usuario y el bot. — [Bot API](https://core.telegram.org/bots/api)
- Las Mini Apps de enlace directo y de modo inline "no tienen acceso al chat": no pueden leer mensajes ni enviar en nombre del usuario. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- El menú de adjuntos solo está habilitado para grandes anunciantes, salvo en el entorno de prueba. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Desde el 20/07/2026 los métodos de Mini App no funcionan desde orígenes distintos del dominio original, salvo que se desactive la protección en @BotFather. — [Bot API changelog, 10.2](https://core.telegram.org/bots/api-changelog)
- **Diferencias de WebView**: el WebView de Telegram se comporta distinto en iOS, Android y Desktop, sobre todo en almacenamiento, teclado y gestos. Se recomienda probar en iOS, Android y al menos un cliente de escritorio, porque Telegram Web esconde la mayoría de los errores propios del WebView. — [Adsgram, errores comunes](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **`localStorage`**: puede no persistir en iOS ni en algunas versiones de escritorio para Linux. Se recomienda `CloudStorage` para preferencias que sigan al usuario, `DeviceStorage` o `SecureStorage` para persistencia local, y mantener sesiones y datos importantes en el backend. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Versiones**: los clientes viejos no tienen los métodos nuevos y no hay polyfill. Hay que fijar una versión mínima y proteger las llamadas con `isVersionAtLeast()`. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Viewport**: `100vh` no coincide con el área visible dentro de la hoja deslizable de Telegram. Hay que usar `viewportHeight`, `viewportStableHeight` o las variables CSS, y llamar `expand()` al iniciar. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Gestos**: el deslizamiento vertical puede cerrar la app en medio de un arrastre. Se soluciona con `disableVerticalSwipes()` (7.7+) y `enableClosingConfirmation()` (6.2+). — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Navegación**: usar el `BackButton` nativo y no una flecha propia, para no competir con el botón físico de Android. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **SSR**: las APIs de Telegram necesitan `window`, así que el código que las usa debe correr en el cliente. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)
- **Login de terceros**: desarrolladores reportan el error `403: disallowed_useragent` de Google OAuth dentro de Telegram Web Apps, porque Google bloquea OAuth en WebViews embebidos. — [Reporte de usuario en Base44](https://feedback.base44.com/p/urgent-google-oauth-403-disalloweduseragent-in-telegram-web-app) (fuente secundaria, visto solo como resultado de búsqueda)
- **Telegram Web**: un reporte en el bug tracker de Telegram indica que la versión web muestra la Mini App en un iframe que no puede conservar sesiones por restricciones del navegador. — [bugs.telegram.org/c/37071](https://bugs.telegram.org/c/37071) (visto solo como resultado de búsqueda, sin leer el reporte completo)
- **Diseño**: Telegram pide diseño responsivo y mobile-first, animaciones a 60 fps, y entradas e imágenes etiquetadas. — [Telegram Mini Apps, "Design Guidelines"](https://core.telegram.org/bots/webapps)
- En Android el User-Agent del WebView incluye versión de la app, modelo, versión de Android y SDK, y clase de rendimiento (`LOW`, `AVERAGE`, `HIGH`). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)

### Inferences
- No conviene depender de cookies de sesión de Flask como único mecanismo. En Telegram Web la app corre en un iframe de otro sitio, donde las cookies quedan como de terceros y suelen bloquearse. Lo robusto es mandar `initData` en cada request (cabecera `Authorization`) o canjearlo por un token propio que viaje en cabecera.
- La regla de Stars no afecta a una app de votación gratuita. Solo importaría si se cobrara por algo digital.
- El mecanismo actual del proyecto ("recordar por dispositivo" que ya votó) no debería apoyarse en `localStorage` dentro de Telegram. La identidad validada (`user.id`) lo reemplaza con ventaja.

### Gaps
- No hay una página oficial que describa las diferencias de WebView entre clientes ni el comportamiento de cookies y `localStorage`. Todo lo de ese punto viene de blogs de proveedores y reportes de usuarios, no de Telegram.
- No encontré en la documentación oficial de Mini Apps una regla escrita sobre blockchains (la supuesta exclusividad de TON). No la doy por confirmada.
- No encontré límites oficiales de tamaño de página, tiempo de carga ni duración de `CloudStorage`.

## 7. Puesta en marcha en @BotFather, entorno de prueba y depuración

### Takeaway
El alta mínima es crear el bot con `/newbot`, publicar la página por HTTPS y asociarla al bot, ya sea como botón de menú (`/setmenubutton`), como Main Mini App (Bot Settings > Configure Mini App) o como app de enlace directo (`/newapp` según la documentación comunitaria). Hay un entorno de prueba separado que acepta HTTP sin TLS, y todos los clientes principales permiten inspeccionar el WebView.

### Cited Findings
- **Paso 1, bot**: `/newbot` en @BotFather pide nombre y username (5 a 32 caracteres, terminado en "bot") y entrega el token. `/token` regenera el token. `/mybots` abre la interfaz de edición. — [Bot Features](https://core.telegram.org/bots/features)
- **Paso 2, botón de menú**: `/setmenubutton` o Bot Settings > Menu Button, indicando texto y URL. Para personalizarlo por usuario se usa el método `setChatMenuButton` (verificado en texto crudo). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Paso 3, Main Mini App**: se configura en @BotFather. Agrega el botón "Launch app" al perfil, permite subir capturas y videos de demostración, y habilita el enlace `https://t.me/botusername?startapp`. La ruta documentada para la pantalla de carga es `/mybots > Select Bot > Bot Settings > Configure Mini App > Enable Mini App` (verificado en texto crudo). — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- La pantalla de carga se personaliza con ícono propio y colores para tema claro y oscuro en Bot Settings > Configure Mini App > Configure Splash Screen, con una opción "Open Splash Screen Preview". — [Bot Features](https://core.telegram.org/bots/features)
- **Paso 4, app de enlace directo**: `/newapp` registra una Mini App asociada al bot y genera el enlace `https://t.me/{mybot}/{myapp}`. Con `/myapps` se elige la app y "Edit link" cambia la URL. — [docs.telegram-mini-apps.com, Creating New App](https://docs.telegram-mini-apps.com/platform/creating-new-app)
- **Menú de adjuntos**: `/setattach` o Bot Settings > Configure Attachment Menu, solo desde una cuenta del servidor de prueba para la mayoría de los bots. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Otros comandos**: `/setdomain` vincula un dominio para Web Login (el Login Widget, no es necesario para Mini Apps). `/setinline` activa el modo inline del bot. — [Bot Features](https://core.telegram.org/bots/features)
- @BotFather tiene ahora su propia Mini App (`t.me/botfather?startapp`) y algunas opciones nuevas, como desactivar la protección de origen de 10.2, se manejan desde ahí. — [Bot Features](https://core.telegram.org/bots/features) y [Bot API changelog, 10.2](https://core.telegram.org/bots/api-changelog)
- **Entorno de prueba**: está totalmente separado del principal, así que hace falta una cuenta de usuario nueva y un bot nuevo creado con el @BotFather de ese entorno. — [Telegram Mini Apps, "Testing Mini Apps"](https://core.telegram.org/bots/webapps)
- Cómo entrar al entorno de prueba. iOS: tocar 10 veces el ícono de Settings, luego Accounts > Login to another account > Test. Telegram Desktop: abrir ☰ Settings, mantener Shift + Alt, clic derecho en "Add Account" y elegir "Test Server". macOS: clic 10 veces en el ícono de Settings para abrir el Debug Menu, ⌘ + clic en "Add Account" e iniciar sesión con número de teléfono. — [Telegram Mini Apps, "Using bots in the test environment"](https://core.telegram.org/bots/webapps)
- En el entorno de prueba las llamadas al Bot API usan el formato `https://api.telegram.org/bot<token>/test/METHOD_NAME`, y se permiten enlaces HTTP sin TLS para probar la Mini App. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Los límites de flood no son más altos en el entorno de prueba y pueden ser más estrictos. — [Bot Features](https://core.telegram.org/bots/features)
- La documentación comunitaria aconseja no crear entidades de desarrollo en producción y usar el entorno de prueba, que acepta HTTP y direcciones IP. — [docs.telegram-mini-apps.com, Creating New App](https://docs.telegram-mini-apps.com/platform/creating-new-app)
- **Depuración en Android**: activar la depuración USB en el teléfono. En Telegram Settings, bajar hasta el final y mantener presionado dos veces el número de versión. Elegir "Enable WebView Debug" en Debug Settings. Conectar el teléfono y abrir `chrome://inspect/#devices` en Chrome. — [Telegram Mini Apps, "Debug Mode for Mini Apps"](https://core.telegram.org/bots/webapps)
- **Depuración en Telegram Desktop (Windows y Linux)**: instalar la versión Beta, ir a Settings > Advanced > Experimental settings, activar "Enable webview inspection", y luego clic derecho en el WebView > "Inspect". — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Depuración en iOS**: tocar 10 veces el ícono de Settings y activar "Allow Web View Inspection". Conectar el teléfono por USB a una Mac, abrir Safari > Develop > [nombre del dispositivo] y abrir la Mini App. — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- **Depuración en Telegram macOS**: instalar la versión Beta, clic 5 veces en el ícono de Settings para abrir el menú de depuración, activar "Debug Mini Apps", y clic derecho en la Mini App > "Inspect Element". — [Telegram Mini Apps](https://core.telegram.org/bots/webapps)
- Cuando no hay inspector disponible se puede usar una consola embebida como Eruda. — [Adsgram](https://adsgram.ai/blog/adsgram/telegram-mini-app-tma-development-mistakes-and-how-to-avoid-them)

### Inferences
- Para un desarrollador en Windows el camino más corto es Telegram Desktop Beta con "Enable webview inspection", que da DevTools con clic derecho. Para probar en el celular sirve Android con `chrome://inspect`. La depuración en iOS exige una Mac.
- El camino mínimo para el proyecto es `/newbot`, luego `/setmenubutton` con la URL HTTPS de PythonAnywhere para el chat privado, y Main Mini App o `/newapp` para tener un enlace `t.me/...?startapp=` que se pueda pegar en el grupo.
- Abrir la URL en un navegador común no sirve para probar la identidad, porque fuera de Telegram `initData` llega vacío. Conviene que la página detecte ese caso y muestre un aviso.
- El entorno de prueba pide registrar una cuenta aparte. Para un proyecto chico con HTTPS ya disponible puede ser más simple crear un segundo bot "de desarrollo" en producción, aunque la documentación comunitaria recomiende lo contrario.

### Gaps
- La página oficial de Mini Apps no menciona `/newapp` ni `/myapps` (lo comprobé buscando en el texto completo). Esos comandos solo figuran en la documentación comunitaria. Como @BotFather ahora tiene interfaz de Mini App, los nombres exactos de los menús actuales pueden diferir y conviene verificarlos escribiendo `/` en @BotFather.
- No relevé qué pide `/newapp` paso a paso (título, descripción, imagen, nombre corto). La documentación comunitaria no lo detalla.
- La documentación oficial no describe cómo entrar al entorno de prueba desde Android.
- Es probable que `switchInlineQuery` y `shareMessage` exijan tener activado el modo inline con `/setinline`, pero no lo verifiqué en la documentación.
- No verifiqué si `/setdomain` o algún registro de dominio adicional es obligatorio para Mini Apps tras el cambio de origen de 10.2. La documentación consultada no lo exige.
