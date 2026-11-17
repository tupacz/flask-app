# Flujos de grupo e ideas de producto para una Mini App de votación por ranking en Telegram

Estado de referencia: Bot API 10.4 (9 de noviembre de 2026), la última versión publicada al 17 de noviembre de 2026. Las citas textuales de la documentación oficial se verificaron sobre copias descargadas ese día de `core.telegram.org/bots/api`, `core.telegram.org/bots/webapps` y `core.telegram.org/bots/api-changelog`.

Abreviaturas de fuentes usadas abajo: WEBAPPS = https://core.telegram.org/bots/webapps , API = https://core.telegram.org/bots/api , CHANGELOG = https://core.telegram.org/bots/api-changelog , LINKS = https://core.telegram.org/api/links , FEATURES = https://core.telegram.org/bots/features , FAQ = https://core.telegram.org/bots/faq .

## 1. ¿Cómo se abre una Mini App desde un chat de grupo?

### Takeaway
En un grupo, la única vía práctica y abierta a cualquier bot es el enlace directo (`https://t.me/<bot>/<app>?startapp=<param>` o `https://t.me/<bot>?startapp=<param>`), que se puede pegar como texto o poner en un botón inline de tipo `url`. Los botones `web_app` (inline y de teclado) y el botón de menú siguen limitados al chat privado con el bot, y el menú de adjuntos sigue restringido a grandes anunciantes.

### Cited Findings

Tabla comparativa (cada fila está respaldada por las citas que siguen):

| Vía de apertura | ¿Funciona en grupos? | Qué recibe la Mini App | Límite principal |
|---|---|---|---|
| Enlace directo `t.me/<bot>/<app>?startapp=` | Sí, "in any chat" | `user`, `start_param`, `chat_type`, `chat_instance` | Sin `query_id` ni objeto `chat`, no puede enviar mensajes en nombre del usuario |
| Enlace a la Main Mini App `t.me/<bot>?startapp=` (Bot API 7.8) | Sí, se abre "in the current chat" | Igual que el enlace directo | Requiere configurar la Main Mini App en @BotFather |
| Botón inline `url` con un enlace `t.me` | Sí (el campo `url` no tiene restricción de tipo de chat) | Lo mismo que el enlace que contiene | Es solo un envoltorio del enlace directo |
| Botón inline `web_app` | No, solo chat privado con el bot | `user`, `query_id` | En grupos la API lo rechaza |
| Botón de teclado `web_app` (`KeyboardButton`) | No, solo chats privados | initData vacío, usa `sendData` | Solo privado |
| Botón de menú (`setChatMenuButton`) | No, solo chat privado con el bot | Igual que el botón inline `web_app` | Solo privado |
| Modo inline (`InlineQueryResultsButton.web_app`) | Sí, se invoca escribiendo `@bot` en cualquier chat | initData vacío | No conoce al usuario por initData ni el chat |
| Menú de adjuntos | Sí, y es el único que entrega el objeto `chat` | `user`, `chat`, `receiver`, `query_id`, `start_param` | Solo grandes anunciantes de Telegram Ads (todos los bots en el entorno de test) |

- La documentación oficial enumera siete formas de lanzar una Mini App: "the main Mini App from a profile button, from a keyboard button, from an inline button, from the bot menu button, via inline mode, from a direct link – and even from the attachment menu". — [WEBAPPS](https://core.telegram.org/bots/webapps#implementing-mini-apps)
- Enlaces directos: "Mini App Bots can be launched from a direct link in any chat. They support a startapp parameter and are aware of the current chat context." Si `startapp` no está vacío, "it will be passed to the Mini App in the start_param field and in the GET parameter tgWebAppStartParam". — [WEBAPPS](https://core.telegram.org/bots/webapps#direct-link-mini-apps)
- En ese modo "Mini Apps can use the chat_type and chat_instance parameters to keep track of the current chat context. This introduces support for concurrent and shared usage by multiple chat members – to create live whiteboards, group orders, multiplayer games and similar apps." — [WEBAPPS](https://core.telegram.org/bots/webapps#direct-link-mini-apps)
- Límite de los enlaces directos: "Mini Apps opened from a direct link have no access to the chat – they can't read messages or send new ones on behalf of the user. To send messages, the user must be redirected to inline mode and actively pick a result." — [WEBAPPS](https://core.telegram.org/bots/webapps#direct-link-mini-apps)
- Desde Bot API 7.6 las Mini Apps de enlace directo se abren a altura completa por defecto, y `mode=compact` las abre a media altura. Ejemplos oficiales: `https://t.me/botusername/appname?startapp=command&mode=compact`. — [WEBAPPS](https://core.telegram.org/bots/webapps#direct-link-mini-apps)
- La Main Mini App (Bot API 7.8, 31 de julio de 2024) "can also be opened in the current chat by direct link in the format https://t.me/botusername?startapp" y recibe los mismos `start_param`, `chat_type` y `chat_instance`. — [WEBAPPS](https://core.telegram.org/bots/webapps#launching-the-main-mini-app); versión en [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Sintaxis completa de los enlaces a nivel cliente: `t.me/<bot_username>/<short_name>?startapp=<start_parameter>&mode=<mode>` (directo) y `t.me/<bot_username>?startapp=<start_parameter>&mode=<mode>` (Main Mini App). `mode` admite `compact` y `fullscreen`. Un mismo bot puede tener varias Mini Apps con distinto `short_name`. — [LINKS](https://core.telegram.org/api/links)
- Botón inline `web_app`: "Available only in private chats between a user and the bot. Not supported for messages sent on behalf of a business account and ephemeral messages." — [API, InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- Desarrolladores reportan que enviar a un grupo o canal un mensaje con botón inline `web_app` falla con `BUTTON_TYPE_INVALID`, mientras que el mismo mensaje funciona en el chat privado. — [Habr Q&A](https://qna.habr.com/q/1330672)
- Botón de teclado `web_app` (`KeyboardButton.web_app`): "Available in private chats only." — [API, KeyboardButton](https://core.telegram.org/bots/api#keyboardbutton)
- Botón de menú: `setChatMenuButton` sirve para "change the bot's menu button in a private chat, or the default menu button", y su `chat_id` es "Unique identifier for the target private chat". — [API, setChatMenuButton](https://core.telegram.org/bots/api#setchatmenubutton)
- Botón inline `url`: "HTTP or tg:// URL to be opened when the button is pressed", sin restricción de tipo de chat en su descripción. — [API, InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- Modo inline: `InlineQueryResultsButton.web_app` muestra un botón sobre los resultados inline, y la Mini App "will be able to switch back to the inline mode using the method switchInlineQuery". El objeto `WebAppInitData` "is empty if the Mini App was launched from a keyboard button or from inline mode". — [API, InlineQueryResultsButton](https://core.telegram.org/bots/api#inlinequeryresultsbutton); [WEBAPPS, WebAppInitData](https://core.telegram.org/bots/webapps#webappinitdata)
- Hay reportes de `BUTTON_TYPE_INVALID` al intentar poner un botón `web_app` dentro del `reply_markup` de un resultado de `answerInlineQuery` (el mensaje que termina en el chat). — [telegraf issue 1936](https://github.com/telegraf/telegraf/issues/1936)
- Menú de adjuntos: "Attachment menu integration is currently only available for major advertisers on the Telegram Ad Platform. However, all bots can use it in the test server environment." — [WEBAPPS](https://core.telegram.org/bots/webapps#launching-mini-apps-from-the-attachment-menu)
- Límites de `startapp` según la documentación comunitaria: "Only the following characters are allowed: A-Z, a-z, 0-9, _ (underscore) and the - (minus)", "The parameter can be up to 512 characters long", regex `/^[\w-]{0,512}$/`, y se recomienda base64url para contenido binario. — [docs.telegram-mini-apps.com](https://docs.telegram-mini-apps.com/platform/start-parameter)
- La documentación oficial de enlaces no especifica caracteres ni longitud máxima para `startapp` o `startattach`. Para `start` y `startgroup` sí fija "up to 64 base64url characters". — [LINKS](https://core.telegram.org/api/links)
- Deep links clásicos del bot: caracteres permitidos "A-Z, a-z, 0-9, _ and -" y hasta 64 caracteres. `?startgroup=` pide al usuario elegir un grupo donde agregar el bot, y el update resultante llega como `/start@your_bot <param>`. — [FEATURES](https://core.telegram.org/bots/features#deep-linking)
- El enlace `t.me/<bot_username>?startgroup=<parameter>&admin=<permissions>` permite pedir permisos de administrador al agregar el bot (por ejemplo `pin_messages`). — [LINKS](https://core.telegram.org/api/links)
- Endurecimiento de seguridad (Bot API 10.2, 14 de julio de 2026): se deshabilita el uso de métodos de Mini App desde orígenes distintos al dominio original de la Mini App. La protección se activó automáticamente para todas las Mini Apps el 20 de julio de 2026, con opt-out desde @BotFather. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)

### Inferences
- El patrón estándar para un grupo es: el bot (miembro del grupo) publica un mensaje con un botón inline `url` cuyo valor es `https://t.me/<bot>/<app>?startapp=<id_de_eleccion>`. Es el reemplazo funcional del botón `web_app`, que en grupos no existe.
- Conviene mantener `startapp` corto (un id de elección de 8 a 16 caracteres en base64url). El límite de 512 solo aparece en documentación comunitaria, y quedarse dentro de 64 caracteres y del alfabeto `A-Za-z0-9_-` es compatible con ambas fuentes.
- El modo inline no sirve como puerta de entrada al voto porque la Mini App abierta así no recibe initData (sin identidad verificable).
- El endurecimiento de julio de 2026 implica que todas las páginas que llamen a `Telegram.WebApp.*` deben servirse desde el mismo dominio registrado como URL de la Mini App. Si la app hace redirecciones a otro dominio, los métodos dejarán de funcionar.

### Gaps
- No encontré en documentación oficial el límite exacto de longitud de `startapp`. El valor 512 proviene solo de docs.telegram-mini-apps.com.
- La definición del campo `start_param` en la tabla oficial de `WebAppInitData` solo menciona `startattach`, mientras que las secciones de enlaces directos y Main Mini App dicen que `startapp` también lo completa. Es una inconsistencia interna de la documentación oficial. El parámetro GET `tgWebAppStartParam` es la vía más segura para leerlo.
- No pude recuperar la tabla comparativa del README de telegraf-docs (`github.com/feathers-studio/telegraf-docs`, error 503), que resume qué campos entrega cada vía.

## 2. ¿Puede la Mini App saber desde qué grupo se abrió?

### Takeaway
No directamente: con enlace directo solo recibe `chat_type` y `chat_instance` (un identificador opaco, no el `chat_id`), y el objeto `chat` con id y título solo llega por el menú de adjuntos o por solicitudes de ingreso. La forma fiable de atar un voto a un grupo es que el bot cree la elección dentro del grupo (ahí sí ve `chat.id`) y codifique el id de la elección en `startapp`.

### Cited Findings
- `chat_type`: "Type of the chat from which the Mini App was opened. Can be either "sender" for a private chat with the user opening the link, "private", "group", "supergroup", or "channel". Returned only for Mini Apps launched from direct links." — [WEBAPPS, WebAppInitData](https://core.telegram.org/bots/webapps#webappinitdata)
- `chat_instance`: "Global identifier, uniquely corresponding to the chat from which the Mini App was opened. Returned only for Mini Apps launched from a direct link." — [WEBAPPS, WebAppInitData](https://core.telegram.org/bots/webapps#webappinitdata)
- `chat` (`WebAppChat`): "An object containing data about the chat where the bot was launched via the attachment menu or the chat to which the join request query was sent. Returned for supergroups, channels and group chats – only for Mini Apps launched via the attachment menu and chat join requests." — [WEBAPPS, WebAppInitData](https://core.telegram.org/bots/webapps#webappinitdata)
- `query_id`: "A unique identifier for the Mini App session, required for sending messages via the answerWebAppQuery method." La sección de botón inline lo describe como propio de ese modo de lanzamiento. — [WEBAPPS](https://core.telegram.org/bots/webapps#inline-button-mini-apps)
- El mismo concepto `chat_instance` existe en `CallbackQuery`: "Global identifier, uniquely corresponding to the chat to which the message with the callback button was sent. Useful for high scores in games." — [API, CallbackQuery](https://core.telegram.org/bots/api#callbackquery)
- La integridad de initData se verifica en el servidor comparando `hash` con el HMAC-SHA-256 del data-check-string, cuya clave secreta es el HMAC-SHA-256 del token del bot con la constante `WebAppData`. — [WEBAPPS](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)
- Un grupo básico puede migrar a supergrupo y cambiar de identificador: `migrate_to_chat_id` indica "The group has been migrated to a supergroup with the specified identifier". — [API, Message](https://core.telegram.org/bots/api#message)
- Bot API 9.6 (3 de abril de 2026) agregó `Telegram.WebApp.requestChat(req_id)`, que abre un diálogo para que el usuario elija un chat existente o cree uno, a partir de un `PreparedKeyboardButton` guardado con `savePreparedKeyboardButton` (tipos `request_users`, `request_chat` o `request_managed_bot`). — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps); [API, savePreparedKeyboardButton](https://core.telegram.org/bots/api#savepreparedkeyboardbutton)

### Inferences
- Flujo recomendado de mapeo voto-grupo: (1) un miembro escribe `/votacion@bot` en el grupo, (2) el bot lee `message.chat.id` y crea una elección `{id, chat_id, creador}` en su almacenamiento, (3) publica la tarjeta con un botón `url` a `t.me/<bot>/<app>?startapp=<id>`, (4) la Mini App envía initData más el id al backend, que valida `hash` y resuelve el grupo a partir del id. Así el `chat_id` nunca depende de lo que diga el cliente.
- `chat_instance` sirve como señal secundaria: el backend puede guardar el primer `chat_instance` visto para una elección y avisar (o rechazar) si llega un voto con otro valor, lo que indica que el enlace fue reenviado a otro chat. No debe ser la única barrera, porque un enlace pegado fuera de Telegram o en el chat privado llega con `chat_type` distinto o sin `chat_instance`.
- `start_param` no prueba pertenencia al grupo: cualquiera que reciba el enlace puede abrirlo. La pertenencia se comprueba con `getChatMember` (ver sección 7).
- Si el grupo migra a supergrupo, las elecciones guardadas con el `chat_id` viejo quedan huérfanas. Para un grupo de amigos alcanza con escuchar el mensaje de servicio de migración y actualizar el id, o crear el grupo ya como supergrupo.
- `requestChat` (9.6) abre una alternativa sin comando: desde la Mini App en privado, el organizador elige el grupo destino. Es más complejo que el comando y no hace falta en los niveles simples.

### Gaps
- No encontré confirmación oficial de que el `chat_instance` de initData coincida con el `chat_instance` de `CallbackQuery` para el mismo chat y bot. Hay que probarlo antes de usarlo para cruzar datos.
- No encontré ninguna forma documentada de convertir `chat_instance` en `chat_id`. Las búsquedas en Stack Overflow y Habr no devolvieron un método.

## 3. ¿Cómo publicar en el grupo la tarjeta de "votá ahora" o los resultados?

### Takeaway
Lo más simple y robusto es que el bot, como miembro del grupo, envíe y edite sus propios mensajes (`sendMessage`, `editMessageText`) con un botón `url`. Las vías iniciadas desde la Mini App (`shareMessage`, `switchInlineQuery`, `t.me/share/url`) sirven cuando el bot no está en el grupo, pero dependen de que el usuario elija el chat y confirme.

### Cited Findings
- `answerWebAppQuery` envía un mensaje "on behalf of the user to the chat from which the query originated" y necesita `web_app_query_id`, que solo existe cuando la Mini App se abrió con botón inline `web_app` o botón de menú (ambos solo en chat privado). — [API, answerWebAppQuery](https://core.telegram.org/bots/api#answerwebappquery); [WEBAPPS](https://core.telegram.org/bots/webapps#inline-button-mini-apps)
- `savePreparedInlineMessage` (Bot API 8.0, 17 de noviembre de 2024) "Stores a message that can be sent by a user of a Mini App". Parámetros: `user_id`, `result` (`InlineQueryResult`), y los filtros `allow_user_chats`, `allow_bot_chats`, `allow_group_chats`, `allow_channel_chats`. Devuelve `PreparedInlineMessage` con `id` y `expiration_date` ("Expired prepared messages can no longer be used"). — [API, savePreparedInlineMessage](https://core.telegram.org/bots/api#savepreparedinlinemessage)
- `Telegram.WebApp.shareMessage(msg_id[, callback])` (Bot API 8.0+) "opens a dialog allowing the user to share a message provided by the bot", y el callback recibe un booleano que indica si se envió. El `msg_id` debe pertenecer a un `PreparedInlineMessage`. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `Telegram.WebApp.switchInlineQuery(query[, choose_chat_types])` (Bot API 6.7+) inserta el username del bot y la consulta en el campo de texto del chat actual, o pide elegir un chat de los tipos `users`, `bots`, `groups`, `channels`. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- El modo inline debe habilitarse en @BotFather. Si no, "your bot will not receive inline Updates". — [FEATURES](https://core.telegram.org/bots/features#inline-requests)
- `Telegram.WebApp.shareToStory(media_url[, params])` (Bot API 7.8+) abre el editor nativo de historias con un medio en URL HTTPS. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `Telegram.WebApp.openTelegramLink(url)` abre un enlace de Telegram dentro de la app, y desde Bot API 7.0 la Mini App ya no se cierra al llamarlo. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- Enlaces para compartir: `t.me/share/url?url=<url>&text=<text>`, con `url` obligatorio (urlencoded) y `text` opcional. — [LINKS](https://core.telegram.org/api/links)
- Rich Messages (Bot API 10.1, 11 de junio de 2026): `sendRichMessage` permite enviar texto altamente estructurado, con bloques como `RichBlockTable` (tablas, con `is_compact` desde 10.3), `RichBlockDetails`, `RichBlockList` y `RichBlockDivider`. `editMessageText` acepta el parámetro `rich_message`. Desde 10.3 hay botones dentro del mensaje (`RichMessageButton`, `RichBlockButtons`). — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Widgets (Bot API 10.4, 9 de noviembre de 2026): `sendWidget` envía mensajes con widgets HTML, pero "Currently, in the production environment, widgets can be sent only to private chats", y tampoco se pueden enviar como respuesta a consultas inline en producción. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Guest Mode (Bot API 10.0, 8 de mayo de 2026): permite a los bots "receive certain messages and issue replies within chats they are not a member of", con `guest_message` en `Update`, `guest_query_id` en `Message` y el método `answerGuestQuery`. — [CHANGELOG](https://core.telegram.org/bots/api-changelog); [API, answerGuestQuery](https://core.telegram.org/bots/api#answerguestquery)
- Estilo de botones (Bot API 9.4, 9 de febrero de 2026): `InlineKeyboardButton.style` admite "danger" (rojo), "success" (verde) o "primary" (azul). Desde 10.3 existe `DisabledButton` y el campo `disabled`. — [API, InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton); [CHANGELOG](https://core.telegram.org/bots/api-changelog)

Requisitos de cada vía:

| Vía | Requiere bot en el grupo | Requiere acción del usuario | Quién figura como autor | Editable por el bot después |
|---|---|---|---|---|
| `sendMessage` / `sendRichMessage` del bot | Sí | No | El bot | Sí (`editMessageText`) |
| `answerWebAppQuery` | No aplica (solo chat privado) | Abrir desde botón `web_app` | El usuario, vía bot | Solo si lleva teclado inline (`inline_message_id`) |
| `savePreparedInlineMessage` + `shareMessage` | No | Elegir chat y confirmar | El usuario, vía bot | Ver Gaps |
| `switchInlineQuery` | No | Elegir chat y tocar un resultado | El usuario, vía bot | Solo con teclado inline |
| `openTelegramLink` + `t.me/share/url` | No | Elegir chat y enviar | El usuario (texto plano con enlace) | No |
| `shareToStory` | No | Publicar historia | El usuario | No |

- Sobre la columna "editable": `SentWebAppMessage.inline_message_id` está "Available only if there is an inline keyboard attached to the message". — [API, SentWebAppMessage](https://core.telegram.org/bots/api#sentwebappmessage)

### Inferences
- Para un club de lectura que ya tiene su grupo, agregar el bot al grupo es un paso único y habilita todo lo demás (tarjeta, conteo en vivo, anuncio, fijado). Las vías sin bot en el grupo quedan como plan B.
- La matriz de enfrentamientos por pares se puede publicar de forma nativa en el chat con `sendRichMessage` y un `RichBlockTable` compacto, sin generar una imagen. Como alternativa conservadora, una tabla monoespaciada en `<pre>` o una imagen generada por el servidor.
- `shareMessage` es útil para "compartir mi invitación a votar" o "compartir el resultado" en otro chat, con un botón `url` de vuelta a la Mini App dentro del mensaje preparado.
- `shareToStory` no aporta a un grupo privado de amigos.
- Los widgets HTML (10.4) serían ideales para mostrar resultados interactivos dentro del mensaje, pero hoy no llegan a grupos en producción. Conviene vigilar el changelog.
- Guest Mode podría permitir invocar el bot sin agregarlo al grupo, pero falta detalle sobre qué mensajes dispara. No es base segura para el diseño.

### Gaps
- No verifiqué si `savePreparedInlineMessage` exige tener habilitado el modo inline del bot ni cuánto dura un `PreparedInlineMessage` antes de expirar. La documentación solo expone `expiration_date`.
- No encontré información sobre qué clientes de Telegram (Android, iOS, Desktop, Web) renderizan correctamente Rich Messages con tablas a noviembre de 2026. Hay que probarlo en los dispositivos del grupo.
- No obtuve la descripción detallada de Guest Mode (cómo se "invoca" al bot invitado) más allá del changelog y de los campos de la API.

## 4. Notificaciones y recordatorios

### Takeaway
El bot puede escribir libremente en el grupo, pero al privado de cada persona solo si esa persona inició el bot o le concedió permiso (`requestWriteAccess`, reflejado en `allows_write_to_pm`). El bot no puede listar los miembros del grupo, así que "quién falta votar" se arma con un padrón propio. Desde julio de 2026 los mensajes efímeros permiten avisos en el grupo visibles para una sola persona.

### Cited Findings
- `Telegram.WebApp.requestWriteAccess([callback])` (Bot API 6.9+) "shows a native popup requesting permission for the bot to send messages to the user". El callback recibe un booleano con la decisión. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `WebAppUser.allows_write_to_pm`: "True, if this user allowed the bot to message them." — [WEBAPPS, WebAppUser](https://core.telegram.org/bots/webapps#webappuser)
- En chats privados, el update `my_chat_member` "is received only when the bot is blocked or unblocked by the user". — [API, Update](https://core.telegram.org/bots/api#update)
- La API de bots ofrece para miembros solo `getChatAdministrators` (lista de administradores), `getChatMemberCount` (número de miembros) y `getChatMember` (un usuario puntual por `user_id`). No hay ningún método que devuelva la lista completa de miembros. — [API, métodos disponibles](https://core.telegram.org/bots/api#getchatadministrators)
- `getChatMember`: "The method is only guaranteed to work for other users if the bot is an administrator in the chat." — [API, getChatMember](https://core.telegram.org/bots/api#getchatmember)
- Updates `chat_member` (altas y bajas de miembros): "The bot must be an administrator in the chat and must explicitly specify "chat_member" in the list of allowed_updates to receive these updates." — [API, Update](https://core.telegram.org/bots/api#update)
- `pinChatMessage`: "the bot must be an administrator with the 'can_pin_messages' right ... to pin messages in groups". El parámetro `disable_notification` evita notificar a todos sobre el mensaje fijado. — [API, pinChatMessage](https://core.telegram.org/bots/api#pinchatmessage)
- Edición: los métodos de "Updating messages" permiten cambiar un mensaje existente en lugar de enviar uno nuevo, y "it is currently only possible to edit messages without reply_markup or with inline keyboards". — [API, Updating messages](https://core.telegram.org/bots/api#updating-messages)
- Límites de envío: en un mismo chat conviene no superar un mensaje por segundo, y en grupos "bots are not be able to send more than 20 messages per minute". — [FAQ](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this)
- Menciones sin username: los enlaces `tg://user?id=<user_id>` "can be used to mention a user by their identifier without using a username, if this is allowed by their privacy settings". — [API, InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- Mensajes efímeros (Bot API 10.2, 14 de julio de 2026): permiten al bot "send group messages and receive commands that are visible only to a specific user and the bot". — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Reglas de los efímeros: cualquier bot puede enviar uno a un usuario dentro de los 15 segundos de una acción elegible (un `callback_query_id` o la respuesta a un comando efímero). "If the bot is a chat administrator, it can send an ephemeral message to any non-bot member of the chat at any time". En todos los casos "It is not guaranteed that the ephemeral message will be received, especially if the user is offline", y pueden desaparecer solos o al reiniciar la app. — [API, Ephemeral Messages and Commands](https://core.telegram.org/bots/api#sendmessage)
- Comandos efímeros: `BotCommand.is_ephemeral` declara un comando cuyo envío "remains invisible to all members of the chat, including both users and other bots". — [API, BotCommand](https://core.telegram.org/bots/api#botcommand)
- Desde Bot API 10.4 se puede responder de forma efímera a un `callback_query` en cualquier chat (salvo mensajes directos de canal) indicando `callback_query_id` sin `receiver_user_id`. `replace_callback_query_message` (10.3) muestra el efímero en lugar del mensaje original. — [CHANGELOG](https://core.telegram.org/bots/api-changelog); [API, EphemeralMessageParameters](https://core.telegram.org/bots/api#ephemeralmessageparameters)
- Los botones `web_app` y `login_url` no están soportados en mensajes efímeros. — [API, InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- Entidad `date_time` (Bot API 9.5, 1 de marzo de 2026): permite a los bots "show a formatted date and time to the user". — [CHANGELOG](https://core.telegram.org/bots/api-changelog)

### Inferences
- Padrón de votantes: como no se pueden enumerar miembros, el bot debe construirlo con lo que ve. Fuentes posibles: quienes abrieron la Mini App (initData validado), quienes votaron en elecciones anteriores, quienes tocaron un botón de callback o enviaron un comando, y las altas y bajas vía `chat_member` si el bot es admin. En un grupo de 5 a 30 personas el padrón se completa solo después de la primera votación.
- "X de N votaron": `N` puede salir de `getChatMemberCount` (hay que restar los bots, al menos el propio) o del tamaño del padrón. Mostrar "votaron 7 (de unos 12 miembros)" evita prometer precisión que la API no da.
- "Faltan votar": solo se puede nombrar a quienes están en el padrón. Un recordatorio grupal puede mencionar a los faltantes conocidos con menciones por id, y cerrar con "y cualquiera que todavía no haya entrado".
- Conteo en vivo: editar el mensaje de la tarjeta con `editMessageText` en cada voto es viable. Con 30 personas no se roza el límite de 20 mensajes por minuto, pero conviene agrupar ediciones (por ejemplo una cada 5 a 10 segundos como máximo) y no editar si el texto no cambió.
- Recordatorios privados: pedir `requestWriteAccess` justo después de enviar el voto ("¿Querés que te avise el resultado por privado?") es el momento natural. Guardar `allows_write_to_pm` por usuario y degradar al aviso en el grupo si no hay permiso.
- Recordatorio efímero: si el bot es administrador, puede mandar a cada faltante conocido un mensaje efímero en el grupo ("te falta votar") sin ensuciar el chat ni requerir permiso de privado. No hay garantía de entrega, así que complementa y no reemplaza el recordatorio público.
- Botón de callback "¿Ya voté?" en la tarjeta: el bot responde con un efímero solo para quien lo tocó, mostrando su boleta actual y un botón `url` para cambiarla. Es una mejora barata gracias a 10.4.
- El plazo de cierre se puede mostrar con la entidad `date_time` para que cada cliente lo vea formateado en su configuración local.
- Fijar la tarjeta (`pinChatMessage`) exige que el bot sea admin con `can_pin_messages`. Para un grupo de amigos es aceptable, y si no se concede, el organizador puede fijarla a mano.
- Los recordatorios y el cierre por fecha necesitan un proceso programado en el servidor (no solo responder a requests). Es el principal requisito de infraestructura nuevo, y el investigador de integración con Flask y PythonAnywhere debería confirmar cómo resolverlo.

### Gaps
- No recuperé en esta sesión la cita textual oficial de que "los bots no pueden iniciar conversaciones con usuarios". La regla se desprende de `requestWriteAccess` y `allows_write_to_pm`, y es conocimiento extendido, pero falta la cita directa.
- No hay fuente que indique si `getChatMemberCount` incluye bots. Lo asumo por ser "number of members in a chat".
- No está documentado si las ediciones con `editMessageText` cuentan igual que los envíos para el límite de 20 por minuto en grupos.
- No encontré datos sobre la tasa real de entrega de los mensajes efímeros ni cuánto tiempo permanecen visibles.

## 5. Modo privacidad, permisos de grupo, comandos y temas de foro

### Takeaway
Con el modo privacidad activado (el valor por defecto) el bot ya recibe lo que este caso necesita: comandos dirigidos a él, respuestas a sus mensajes y mensajes de servicio. No hace falta desactivarlo ni leer el chat. Solo se requiere ser administrador para fijar mensajes, para garantizar `getChatMember` y para recibir altas y bajas.

### Cited Findings
- "By default, all bots added to groups run in Privacy Mode and only see relevant messages and commands." — [FEATURES](https://core.telegram.org/bots/features#privacy-mode)
- Con modo privacidad activado, el bot recibe: "Commands explicitly meant for them (e.g., /command@this_bot)", comandos generales como `/start` solo si fue el último bot en escribir en el grupo, mensajes inline enviados vía el bot y respuestas a sus mensajes. — [FAQ](https://core.telegram.org/bots/faq#what-messages-will-my-bot-get)
- Todos los bots reciben siempre los mensajes de servicio, los de chats privados y los de canales donde son miembros. — [FAQ](https://core.telegram.org/bots/faq#what-messages-will-my-bot-get)
- "Bot admins and bots with privacy mode disabled will receive all messages except messages sent by other bots." — [FAQ](https://core.telegram.org/bots/faq#what-messages-will-my-bot-get)
- Si se cambia el modo privacidad, el bot debe ser quitado y vuelto a agregar al grupo para que el cambio surta efecto. Los usuarios pueden ver el estado de privacidad del bot en la lista de miembros. — [FEATURES](https://core.telegram.org/bots/features#privacy-mode)
- Los comandos empiezan con `/`, tienen hasta 32 caracteres y pueden dirigirse a un bot concreto con la forma `/command@botname`. — [FEATURES](https://core.telegram.org/bots/features#commands)
- `setMyCommands` admite ámbitos como `BotCommandScopeAllGroupChats`, `BotCommandScopeAllChatAdministrators`, `BotCommandScopeChat`, `BotCommandScopeChatAdministrators` y `BotCommandScopeChatMember`, lo que permite mostrar comandos distintos a administradores y miembros. — [API, BotCommandScope](https://core.telegram.org/bots/api#botcommandscope)
- Bot API 10.0 agregó "the ability to see certain messages sent by other bots in groups". — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Derechos: `can_pin_messages` ("True, if the user is allowed to pin messages; for groups and supergroups only") y `can_manage_topics` forman parte de `ChatMemberAdministrator` y `ChatAdministratorRights`. — [API, ChatMemberAdministrator](https://core.telegram.org/bots/api#chatmemberadministrator)
- Temas de foro: `Chat.is_forum` indica "True, if the supergroup chat is a forum (has topics enabled)". Los métodos de envío aceptan `message_thread_id`, "Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only", y los mensajes entrantes traen `is_topic_message`. — [API, sendMessage](https://core.telegram.org/bots/api#sendmessage)
- Desde Bot API 9.3 (31 de diciembre de 2025) existe además un modo de temas en el chat privado con el bot, y desde 10.4 hay enlaces `https://t.me/<bot_username>/<message_thread_id>` a esos temas. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)

### Inferences
- Configuración mínima recomendada: bot con modo privacidad activado, comandos registrados para grupos (`/votacion`, `/resultado`, `/recordar`), y pedir en el enlace de alta solo el permiso `pin_messages` (`?startgroup&admin=pin_messages`). Hacerlo admin da de paso la garantía de `getChatMember`, los updates `chat_member` y los efímeros a cualquier miembro.
- Efecto secundario a tener presente: un bot administrador recibe todos los mensajes del grupo. El código debe ignorar todo lo que no sea comando propio, y conviene decírselo al grupo por transparencia.
- En un grupo con temas, el bot debe responder en el mismo `message_thread_id` del comando para que la tarjeta quede en el tema donde se pidió (por ejemplo "Próximo libro").
- Si en el grupo hay un solo bot, `/votacion` a secas suele llegar igual, pero la forma `/votacion@bot` es la única garantizada. El menú de comandos del cliente agrega el sufijo automáticamente.
- Los administradores anónimos del grupo no envían comandos con su identidad de usuario, así que el bot no puede atribuirles la creación de una elección. La Mini App sí recibe su usuario real en initData.

### Gaps
- La página de features no cubre el comportamiento de bots en temas de foro de grupos (solo temas en privado). El detalle del tema "General" y de permisos por tema no quedó verificado.
- No verifiqué el texto exacto de `is_topic_message` ni el comportamiento cuando el bot omite `message_thread_id` en un foro.

## 6. Encuestas nativas de Telegram en 2026

### Takeaway
Las encuestas nativas mejoraron mucho en 2026 (cambiar el voto, agregar opciones, ocultar resultados hasta el cierre, medios en opciones, hasta 12 opciones), pero el tipo sigue siendo solo "regular" o "quiz". No existe ordenamiento por preferencia, así que un voto Condorcet sigue necesitando una Mini App.

### Cited Findings
- `Poll.type`: "Poll type, currently can be "regular" or "quiz"". `sendPoll` acepta `type` con los valores "quiz" o "regular". — [API, Poll](https://core.telegram.org/bots/api#poll); [API, sendPoll](https://core.telegram.org/bots/api#sendpoll)
- Opciones: "A JSON-serialized list of 1-12 answer options". El máximo subió a 12 en Bot API 9.1 (3 de julio de 2025) y el mínimo bajó de 2 a 1 en Bot API 10.0. — [API, sendPoll](https://core.telegram.org/bots/api#sendpoll); [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Bot API 9.6 (3 de abril de 2026) agregó: `allows_revoting` (por defecto True en encuestas regulares), `shuffle_options` ("options must be shown in random order"), `allow_adding_options` ("answer options can be added to the poll after creation; not supported for anonymous polls and quizzes"), `hide_results_until_closes`, `description` de hasta 1024 caracteres, quizzes con varias respuestas correctas (`correct_option_ids` reemplaza a `correct_option_id`) y cierre automático de hasta 2628000 segundos. — [CHANGELOG](https://core.telegram.org/bots/api-changelog); [API, sendPoll](https://core.telegram.org/bots/api#sendpoll)
- También en 9.6: ids persistentes de opción (`PollOption.persistent_id`, `PollAnswer.option_persistent_ids`), quién agregó cada opción (`added_by_user`, `added_by_chat`, `addition_date`) y mensajes de servicio `poll_option_added` y `poll_option_deleted`. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Bot API 10.0 (8 de mayo de 2026) agregó medios en la encuesta, en la explicación del quiz y en cada opción (`InputPollMedia`, `InputPollOptionMedia`), y los parámetros `members_only` y `country_codes`. Bot API 10.1 agregó enlaces como medio de opción (`InputMediaLink`). — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- `members_only` y `country_codes` en `sendPoll` son "for channel chats only". — [API, sendPoll](https://core.telegram.org/bots/api#sendpoll)
- `is_anonymous` vale True por defecto. El update `poll_answer` solo llega para encuestas no anónimas, y "Bots receive new votes only in polls that were sent by the bot itself". — [API, sendPoll](https://core.telegram.org/bots/api#sendpoll); [API, Update](https://core.telegram.org/bots/api#update)
- `sendChecklist` solo funciona "on behalf of a connected business account" (requiere `business_connection_id`). — [API, sendChecklist](https://core.telegram.org/bots/api#sendchecklist)
- En todo el changelog de 2024 a noviembre de 2026 no aparece ningún cambio de encuestas relacionado con ranking u orden de preferencias. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)

### Inferences
- Una encuesta nativa solo captura "elegí una" o "elegí varias" (equivalente a voto por aprobación). No registra el orden entre opciones, que es el dato que alimenta la matriz de pares de Condorcet. Tampoco soporta más de 12 candidatos ni arrastrar para ordenar.
- Las encuestas nativas sí sirven como complemento barato alrededor de la Mini App:
  - Fase de nominaciones: una encuesta no anónima con `allow_adding_options` donde cada miembro agrega su libro propuesto. El bot ve quién agregó cada opción y puede volcar las opciones a la lista de candidatos (máximo 12).
  - Preselección: una encuesta de respuesta múltiple ("¿cuáles leerías?") para recortar una lista larga antes del ranking.
  - Desempate o confirmación rápida ("¿arrancamos con el ganador el 1 de diciembre?").
- `hide_results_until_closes` y `shuffle_options` muestran que Telegram reconoce los mismos problemas que la app ya resuelve (sesgo de orden y efecto arrastre). La Mini App debería conservar ambos comportamientos: lista mezclada y resultados ocultos hasta el cierre.

### Gaps
- No revisé el blog de telegram.org para ver si los clientes anunciaron algún tipo de encuesta "ranking" del lado usuario que la Bot API no exponga. En la Bot API no existe.

## 7. Identidad y confianza para votar

### Takeaway
El `user.id` de initData validado en el servidor reemplaza al nombre tipeado y da "una persona, un voto" real. La pertenencia al grupo se comprueba con `getChatMember` y el rol de organizador se deriva de `getChatAdministrators`, lo que elimina la contraseña fija del panel actual.

### Cited Findings
- `WebAppUser.id`: identificador único con hasta 52 bits significativos, seguro en un entero de 64 bits. `WebAppUser` incluye además `first_name`, `last_name`, `username`, `language_code` e `is_premium`. — [WEBAPPS, WebAppUser](https://core.telegram.org/bots/webapps#webappuser)
- `photo_url`: URL de la foto de perfil (.jpeg o .svg). Desde Bot API 8.0 está disponible para todas las Mini Apps, sujeta a la configuración de privacidad del usuario. — [WEBAPPS, WebAppUser](https://core.telegram.org/bots/webapps#webappuser); [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Los datos de initData solo son confiables tras validar `hash` (HMAC-SHA-256 con clave derivada del token del bot y la constante `WebAppData`). Bot API 8.0 agregó `signature` para validación por terceros. `auth_date` es el "Unix time when the form was opened". — [WEBAPPS](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)
- `getChatMember(chat_id, user_id)` devuelve un `ChatMember` cuyo `status` es uno de "creator", "administrator", "member", "restricted", "left" o "kicked". Solo está garantizado para otros usuarios si el bot es administrador. — [API, getChatMember](https://core.telegram.org/bots/api#getchatmember); [API, ChatMember](https://core.telegram.org/bots/api#chatmember)
- `getChatAdministrators` devuelve la lista de administradores. Por defecto omite a los bots distintos del actual, y desde Bot API 10.0 `return_bots=True` los incluye. — [API, getChatAdministrators](https://core.telegram.org/bots/api#getchatadministrators)
- Bot API 9.5 (1 de marzo de 2026) agregó etiquetas de miembro (`tag` en `ChatMemberMember`, `setChatMemberTag`, `sender_tag` en `Message`). — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Las encuestas nativas ya ofrecen el precedente de UX para dos decisiones de diseño: voto anónimo por defecto (`is_anonymous`) y posibilidad de cambiar el voto (`allows_revoting`). — [API, sendPoll](https://core.telegram.org/bots/api#sendpoll)

### Inferences
- Una persona, un voto: la clave de la boleta pasa a ser `(eleccion_id, user.id)`. Reenviar una boleta la reemplaza (upsert) en lugar de rechazarla, lo que da "cambiar el voto hasta el cierre" sin lógica extra. Esto corrige de raíz el control actual por coincidencia de texto del nombre.
- Nombre visible: usar `first_name` más `last_name` de initData como nombre por defecto, guardando el `user.id` como identidad. Conviene rechazar initData con `auth_date` viejo (por ejemplo más de 24 horas) para limitar la reutilización de un initData capturado.
- Restringir a miembros: al recibir la boleta, llamar a `getChatMember(chat_id_de_la_eleccion, user.id)` y aceptar solo "creator", "administrator", "member" (y "restricted" si sigue siendo miembro). Requiere que el bot sea admin para que la consulta sea confiable.
- Rol de organizador: quien creó la elección con el comando, más cualquier usuario cuyo `status` sea "creator" o "administrator" en ese grupo, puede cerrar la votación, ver la matriz completa y editar candidatos. El resultado se cachea unos minutos para no llamar a la API en cada request.
- Boleta pública o secreta es una decisión de producto, no una limitación técnica: el servidor siempre conoce quién votó qué. Opciones razonables para amigos: (a) pública la lista de quienes votaron con avatar (`photo_url`) y secreto el contenido hasta el cierre, (b) todo público tras el cierre, (c) solo agregados. La opción (a) coincide con el comportamiento actual de la app (el público ve quién ya votó, el admin ve el detalle).
- `photo_url` puede venir vacío por privacidad. Hay que tener un avatar de respaldo con iniciales.
- Para un grupo de amigos no hace falta más protección contra fraude. Los riesgos realistas son un enlace reenviado a alguien de afuera (cubierto por `getChatMember`) y un voto doble desde dos cuentas de la misma persona (no evitable ni relevante a esta escala).

### Gaps
- No verifiqué cuánto tiempo sigue siendo válida la URL de `photo_url` ni si se puede guardar de forma persistente. Conviene tratarla como efímera y refrescarla en cada apertura.
- No hay fuente oficial que recomiende una ventana concreta de validez para `auth_date`. El valor sugerido es criterio propio.

## 8. Capacidades opcionales de la Mini App útiles para este caso

### Takeaway
Hay un conjunto pequeño de APIs del cliente que mejoran mucho la experiencia de ordenar por arrastre con muy poco código: `disableVerticalSwipes` (imprescindible para el drag), `HapticFeedback`, el botón inferior con progreso, `CloudStorage` para el borrador y `enableClosingConfirmation`.

### Cited Findings
- `disableVerticalSwipes()` (Bot API 7.7+): "disables vertical swipes to close or minimize the Mini App. This method is useful if your Mini App uses swipe gestures that may conflict with the gestures for minimizing and closing the app." — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `enableClosingConfirmation()` (Bot API 6.2+): activa un diálogo de confirmación cuando el usuario intenta cerrar la Mini App. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `HapticFeedback` (Bot API 6.1+): `impactOccurred` (light, medium, heavy, rigid, soft), `notificationOccurred` (error, success, warning) y `selectionChanged()`, que "tells that the user has changed a selection". — [WEBAPPS, HapticFeedback](https://core.telegram.org/bots/webapps#hapticfeedback)
- `CloudStorage` (Bot API 6.9+): "Each bot can store up to 1024 items per user in the cloud storage". Claves de 1 a 128 caracteres (A-Z, a-z, 0-9, _ y -) y valores de 0 a 4096 caracteres. — [WEBAPPS, CloudStorage](https://core.telegram.org/bots/webapps#cloudstorage)
- `DeviceStorage` y `SecureStorage` se agregaron en Bot API 9.0 (11 de abril de 2025). — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- El botón principal pasó a ser `BottomButton` en Bot API 7.10 (6 de septiembre de 2024), que también agregó el botón secundario y el color de la barra inferior. `showProgress(leaveActive)` muestra un indicador de carga en el botón. Bot API 9.5 agregó `iconCustomEmojiId`. — [WEBAPPS, BottomButton](https://core.telegram.org/bots/webapps#bottombutton); [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Bot API 8.0 (17 de noviembre de 2024) agregó pantalla completa (`requestFullscreen`), acceso directo en la pantalla de inicio (`addToHomeScreen`, `checkHomeScreenStatus`), estado de emoji (`setEmojiStatus`, `requestEmojiStatusAccess`), compartir medios, descarga de archivos (`downloadFile`), geolocalización y `photo_url`. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- `setEmojiStatus(custom_emoji_id[, params, callback])` abre un diálogo nativo y no puede cambiar el estado sin interacción manual del usuario. `params` admite una duración. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `addToHomeScreen()` pide al usuario agregar la Mini App a la pantalla de inicio. El evento `homeScreenAdded` puede no llegar en algunos dispositivos. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- `hideKeyboard` se agregó en Bot API 9.1 (3 de julio de 2025). — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Opciones de encuesta con medios y enlaces (10.0 y 10.1) muestran que Telegram ya contempla tapas o enlaces por opción en votaciones nativas. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)

### Inferences
- Prioridad alta para una lista ordenable con SortableJS dentro de Telegram: llamar a `disableVerticalSwipes()` al iniciar. Sin eso, arrastrar un libro hacia abajo puede minimizar o cerrar la Mini App. Es el riesgo de UX más concreto del port.
- Háptica: `selectionChanged()` cada vez que un ítem cambia de posición durante el arrastre, `impactOccurred('light')` al soltar y `notificationOccurred('success')` al confirmar el voto.
- Botón inferior: texto "Enviar mi orden", `showProgress()` mientras el POST está en curso, y luego cambiar a "Actualizar mi voto" si ya votó.
- Borrador: guardar el orden actual en `CloudStorage` bajo una clave como `borrador_<eleccion_id>`. Una lista de 10 a 20 ids de libros entra holgada en 4096 caracteres, y se sincroniza entre dispositivos del mismo usuario. Combinar con `enableClosingConfirmation()` mientras haya cambios sin enviar.
- Enlace profundo a una elección concreta: `startapp=<eleccion_id>` abre directo la boleta, y `startapp=r_<eleccion_id>` (u otro prefijo) puede abrir directo la pantalla de resultados.
- Tapas de libros: son imágenes comunes en el HTML de la Mini App. En la tarjeta del grupo, el bot puede enviar un álbum o una foto con la tapa del ganador.
- Toques lúdicos de bajo costo: ofrecer con `setEmojiStatus` un emoji de libro como estado a quien propuso el libro ganador, o usar etiquetas de miembro (`setChatMemberTag`, 9.5) para marcar "eligió el libro del mes". Son opcionales y dependen de permisos.
- `addToHomeScreen` y pantalla completa aportan poco en una app que se usa una vez por mes desde el grupo. El modo `compact` en el enlace puede ser mejor para la vista rápida de resultados.

### Gaps
- No verifiqué en qué versión se agregó `showProgress` ni los requisitos exactos de `setEmojiStatus` (por ejemplo si exige Telegram Premium o un emoji personalizado propio).
- No verifiqué los permisos necesarios para que un bot use `setChatMemberTag`.
- No probé la interacción real entre SortableJS y los gestos del WebView de Telegram en iOS y Android. La recomendación de `disableVerticalSwipes` se basa en la descripción oficial del método.

## 9. Proyectos abiertos y casos publicados que sirvan de modelo

### Takeaway
Encontré poco material verificable específico de votación o encuestas en grupo. La referencia más sólida es la propia documentación oficial, que describe el patrón de uso compartido con `chat_instance` y `startapp`, más un proyecto abierto de quiz multijugador. Este punto queda mayormente como vacío, y otro investigador cubre apps de ejemplo.

### Cited Findings
- La documentación oficial presenta como casos de uso del modo de enlace directo "live whiteboards, group orders, multiplayer games and similar apps" y, para la Main Mini App, "Cooperative, multiplayer or teamwork-oriented services within a chat context". — [WEBAPPS](https://core.telegram.org/bots/webapps#direct-link-mini-apps)
- InstaQuiz es una Mini App de código abierto de quiz multijugador en tiempo real dentro de Telegram, donde los jugadores crean salas e invitan amigos. Stack: TypeScript, Express.js, PostgreSQL y Vue.js. Repositorio: `github.com/yasdpt/insta-quiz`. — [Documentación de InstaQuiz](https://yasdpt.gitbook.io); [GitHub](https://github.com/yasdpt/insta-quiz)
- El Mini App Contest de Telegram (2023) exigía "build any useful Mini App for Telegram and publish its client and server code on Github", por lo que las entradas premiadas tienen código público enlazado desde cada página de entrada. — [contest.com/mini-apps](https://contest.com/mini-apps)

### Inferences
- El patrón "sala con id + invitación por enlace" de los quiz multijugador es estructuralmente igual a "elección con id + tarjeta en el grupo": un recurso compartido identificado por un id corto que viaja en `startapp`, identidad por initData, y estado en el servidor.
- Las páginas de entradas del concurso de 2023 son una cantera de repositorios para revisar, pero hay que abrir cada entrada para ver su descripción y su enlace a GitHub.

### Gaps
- No verifiqué cómo InstaQuiz comparte la sala (enlace `startapp`, modo inline o `switchInlineQuery`). La página de documentación consultada no lo detalla y no revisé el código.
- Un resultado de búsqueda mencionó una entrada del concurso de 2023 que gestionaba un calendario de llamadas dentro de chats ("Slim Elk"), pero no pude confirmar la descripción ni el repositorio en la página del concurso, que solo lista nombres y premios.
- No encontré proyectos abiertos ni artículos verificables de Mini Apps de votación por ranking, encuestas de grupo, agenda de reuniones o división de gastos que documenten su manejo de `chat_instance`. Las búsquedas devolvieron solo recursos genéricos.

## 10. Tres niveles de ideas de producto y sus riesgos

### Takeaway
Hay un camino incremental claro: primero identidad automática con un enlace en el grupo (casi sin bot), después un bot que publica la tarjeta, actualiza el conteo y anuncia el ganador, y por último un ciclo completo con nominaciones, recordatorios e historial. Cada nivel reutiliza el anterior y el cálculo Condorcet existente no cambia.

### Cited Findings
Los hechos que sostienen cada nivel ya están citados arriba. Los puntos de apoyo principales son:
- Enlaces directos abribles "in any chat" con `start_param`, `chat_type` y `chat_instance`. — [WEBAPPS](https://core.telegram.org/bots/webapps#direct-link-mini-apps)
- Botón inline `web_app` solo en chat privado, por lo que la tarjeta del grupo usa un botón `url`. — [API, InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton)
- Validación de initData por HMAC. — [WEBAPPS](https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app)
- `getChatMember` garantizado solo si el bot es admin, y `pinChatMessage` con `can_pin_messages`. — [API, getChatMember](https://core.telegram.org/bots/api#getchatmember); [API, pinChatMessage](https://core.telegram.org/bots/api#pinchatmessage)
- Sin método para listar miembros. — [API](https://core.telegram.org/bots/api#getchatmembercount)
- `requestWriteAccess` y `allows_write_to_pm` para mensajes privados. — [WEBAPPS](https://core.telegram.org/bots/webapps#initializing-mini-apps)
- Mensajes efímeros en grupos (10.2 a 10.4), sin garantía de entrega. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Encuestas con `allow_adding_options` y hasta 12 opciones (9.6). — [API, sendPoll](https://core.telegram.org/bots/api#sendpoll)
- Rich Messages con tablas (10.1). — [CHANGELOG](https://core.telegram.org/bots/api-changelog)
- Límite de 20 mensajes por minuto del bot en un grupo. — [FAQ](https://core.telegram.org/bots/faq#my-bot-is-hitting-limits-how-do-i-avoid-this)
- Restricción de métodos de Mini App al dominio original desde julio de 2026. — [CHANGELOG](https://core.telegram.org/bots/api-changelog)

### Inferences

**Nivel 1, mínimo: "el mismo link, pero sabe quién sos"**
- Qué es: registrar un bot y una Mini App en @BotFather apuntando a la página actual. El organizador pega `https://t.me/<bot>/<app>` en el grupo (el bot ni siquiera necesita estar en el grupo). La página carga `telegram-web-app.js`, toma initData, el servidor valida `hash` y usa `user.id` y el nombre de Telegram en lugar del campo de nombre.
- Qué gana el grupo: nadie tipea su nombre, un voto por cuenta, se puede cambiar el voto reenviando, se muestran avatares de quienes ya votaron, y `disableVerticalSwipes` más háptica mejoran el arrastre.
- Qué no tiene: tarjeta automática, conteo en el chat, anuncio del ganador, control de pertenencia al grupo.
- Riesgos técnicos:
  - Validación de initData mal hecha o ausente (es la única barrera de identidad).
  - Mantener el acceso por navegador común como alternativa: fuera de Telegram no hay initData, hay que decidir si se conserva el flujo viejo con nombre manual o se bloquea.
  - Formato de `data.txt`: agregar el `user.id` sin romper los parsers duplicados que dependen del formato de línea actual.
  - Gestos del WebView contra el arrastre de SortableJS.
  - Todo debe servirse por HTTPS desde el mismo dominio registrado (restricción de 10.2).
  - Cualquiera con el enlace puede votar, porque no hay chequeo de grupo.

**Nivel 2, medio: "el bot lleva la votación en el grupo"**
- Qué es: el bot se agrega al grupo (idealmente como admin con permiso de fijar). `/votacion@bot` crea la elección ligada a `chat.id` y publica una tarjeta con botón `url` a `t.me/<bot>/<app>?startapp=<id>`. Con cada voto el bot edita la tarjeta ("Votaron 7: Ana, Beto, ..."). Al cerrar (`/cerrar` del organizador o de un admin del grupo), el bot anuncia el ganador Condorcet con la tapa y, opcionalmente, la tabla de pares.
- Extras baratos: fijar la tarjeta, botón de callback "¿Ya voté?" con respuesta efímera, chequeo `getChatMember` al votar, rol de organizador por `getChatAdministrators` en lugar de contraseña fija, botón "Ver resultados" que abre la Mini App en la vista de resultados.
- Riesgos técnicos:
  - Hace falta recibir updates del bot (webhook HTTPS o polling), que es infraestructura nueva respecto de la app actual.
  - Persistencia: con varias elecciones y ediciones concurrentes, los archivos planos empiezan a quedar cortos. Como mínimo hay que guardar `chat_id`, `message_id` de la tarjeta y estado de la elección.
  - "X de N" no es exacto porque el bot no puede listar miembros.
  - Migración de grupo a supergrupo cambia el `chat_id`.
  - Si el bot no es admin: no puede fijar, `getChatMember` no está garantizado y no hay efímeros a demanda.
  - Si el bot es admin: recibe todos los mensajes del grupo, y hay que ignorarlos explícitamente.
  - Empates y ausencia de ganador Condorcet estricto deben explicarse bien en el anuncio (la app ya tiene un criterio de respaldo, pero el mensaje del bot debe decir cuál se usó).
  - El caso de cero boletas debe manejarse antes de anunciar.

**Nivel 3, ambicioso: "el club de lectura completo"**
- Qué es: ciclo mensual con fases. (1) Nominaciones: cada miembro propone libros desde la Mini App (título, autor, tapa, enlace) o mediante una encuesta nativa con `allow_adding_options`. (2) Preselección opcional por aprobación si hay demasiados candidatos. (3) Ranking por arrastre con fecha de cierre. (4) Recordatorios automáticos a quienes faltan: mención en el grupo, mensaje efímero o privado si dieron `requestWriteAccess`. (5) Cierre automático y anuncio con tabla de resultados (`sendRichMessage` o imagen). (6) Historial de ganadores, quién propuso cada uno y estadísticas simples. Varias elecciones y varios grupos con el mismo bot.
- Toques opcionales: compartir el resultado con `shareMessage`, emoji de estado para quien propuso el ganador, visualización de la matriz de pares y del "camino" del ganador dentro de la Mini App, exportar el historial.
- Riesgos técnicos:
  - Necesita tareas programadas (recordatorios y cierre por fecha), no solo responder a requests.
  - Necesita una base de datos real (elecciones, candidatos, boletas, padrón, permisos de privado).
  - El padrón de "quién falta" es siempre aproximado y los efímeros no garantizan entrega.
  - Riesgo de exceso de notificaciones en un grupo de amigos: limitar a uno o dos recordatorios por elección y permitir silenciarlos.
  - Dependencia de funciones muy nuevas (Rich Messages de 10.1, efímeros de 10.2 a 10.4) cuyo soporte en todos los clientes no está confirmado. Hay que tener alternativa en texto plano.
  - Los widgets HTML (10.4) aún no funcionan en grupos, así que no deben entrar en el diseño.
  - El alcance crece rápido para un proyecto de hobby. Conviene que cada fase sea opcional y que el nivel 2 siga funcionando sin ellas.

Orden sugerido de construcción: nivel 1 completo, luego del nivel 2 primero la tarjeta y el anuncio (lo de mayor valor percibido), después el conteo en vivo y el chequeo de pertenencia, y del nivel 3 empezar por el historial (solo lectura, sin infraestructura nueva) antes que por nominaciones y recordatorios.

### Gaps
- No evalué el esfuerzo en horas de cada nivel ni las restricciones concretas del hosting actual para webhooks y tareas programadas. Eso corresponde al investigador de integración con Flask y PythonAnywhere.
- No hay evidencia publicada, que yo haya encontrado, de una Mini App de voto Condorcet en grupos de Telegram. Las ideas de los tres niveles son derivaciones propias a partir de las capacidades documentadas, no réplicas de un producto existente.
