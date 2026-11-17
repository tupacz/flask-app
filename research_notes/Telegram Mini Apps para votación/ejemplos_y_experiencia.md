# Ejemplos reales de Telegram Mini Apps y cómo se sienten para el usuario (noviembre de 2026)

Nota de método, válida para todo el documento: la investigación se hizo solo con búsqueda web y lectura de páginas (documentación oficial, blog de Telegram, repositorios de GitHub, catálogos). **No se pudo abrir Telegram ni probar ningún bot**, así que "sigue activo" significa "la fuente lo presenta como vigente", no "lo abrí y funcionó". Cada sección marca qué quedó sin verificar. Conviene que el lector abra cada bot en su Telegram antes de darlo por vivo.

## 1. ¿Qué Mini Apps conocidas existen y siguen funcionando a fines de 2026?

### Takeaway
La demo oficial sigue siendo @DurgerKingBot (la documentación oficial, actualizada a Bot API 10.1 de junio de 2026, todavía la recomienda), @wallet es la Mini App más usada, y los juegos tap-to-earn (Hamster Kombat, Notcoin) existen pero colapsaron en usuarios. Para alguien que quiere ver apps chicas y útiles, lo mejor son las apps de ejemplo de código abierto del concurso de Mini Apps de 2023 (agenda de fechas, notas, OTP, flashcards, wishlist), varias con bot público.

### Cited Findings

**Demo oficial**
- La documentación oficial dice textualmente que para ver una Mini App en acción hay que probar el bot de muestra @DurgerKingBot (https://t.me/DurgerKingBot). Lo usa como ejemplo de lanzamiento por botón inline, por botón de menú y por menú de adjuntos. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Esa misma página no nombra ningún otro bot de demostración (solo @BotFather como herramienta de configuración). La última versión que registra es Bot API 10.1 del 11 de junio de 2026. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- No se encontró código fuente oficial de @DurgerKingBot. Lo que hay en GitHub son clones comunitarios (por ejemplo uno en Next.js con menú, pedido y pagos). — [awesome.ecosyste.ms, ermanoj-sharma/durgerkingbot](https://awesome.ecosyste.ms/projects/github.com%2Fermanoj-sharma%2Fdurgerkingbot)

**Billetera**
- Un catálogo de 2026 del ecosistema TON describe a @wallet (https://t.me/wallet) como la Mini App más usada, una billetera custodial que corre entera dentro de Telegram. La fuente es un blog con interés en TON, tomarlo como orientativo. — [DEV Community, "30 best Mini Apps on TON in 2026"](https://dev.to/ton-adoption/30-best-mini-apps-on-ton-in-2026-catalog-by-category-1jc7)

**Juegos y plataformas de juegos (categoría mencionada brevemente)**
- El post de Telegram del 17 de noviembre de 2024 ("la actualización más grande en la historia de las mini apps") cita como primeras implementaciones de pantalla completa y nuevas funciones a @playdeckbot, @tverse y @major. — [Telegram Blog, Full-screen Mini Apps and more](https://telegram.org/blog/fullscreen-miniapps-and-more)
- PlayDeck (https://playdeckbot.t.me) figura como "catálogo definitivo de juegos de Telegram" en la lista awesome. — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Hamster Kombat llegó a unos 300 millones de usuarios en 2024 y después del airdrop perdió la mayoría. Las cifras varían según la fuente: caída del 85% de jugadores mensuales desde el máximo (Protos vía DailyCoin), de 300 millones en agosto a 41 millones en noviembre de 2024 (Coin360). — [DailyCoin](https://dailycoin.com/is-hamster-kombat-hype-over-token-sinks-as-users-abandon-game/); [Coin360](https://coin360.com/news/telegram-games-q4-drop)
- Un informe de Caladan citado por BeInCrypto califica al 93% de los proyectos de juegos Web3 como "efectivamente muertos", incluido Hamster Kombat. — [BeInCrypto](https://beincrypto.com/web3-gaming-projects-dead-caladan-report/)
- Un blog del ecosistema TON afirma que para 2026 Hamster Kombat "colapsó casi por completo" y que Notcoin (unos 40 millones de usuarios en su pico de 2024) pasó a una etapa estable de nicho. Es una sola fuente y con interés en el tema. — [DEV Community, "Hamster Kombat: what remains after the hype in 2026"](https://dev.to/ton-adoption/hamster-kombat-what-remains-after-the-hype-in-2026-4c1n); [DEV Community, "Tap-to-earn after Hamster Kombat"](https://dev.to/ton-adoption/tap-to-earn-after-hamster-kombat-what-survived-in-2026-531c)

**Utilidades y productividad (las más parecidas al proyecto del lector)**
- Dayfinder, @dayfinderbot (https://t.me/dayfinderbot): encuesta de fechas tipo Doodle. Mini App con tres páginas (`/create`, `/vote`, `/results`). Backend en Python (python-telegram-bot + Quart), licencia MIT, etiquetado `telegram-miniapp-contest-2023`. — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)
- ConveneBot, @ConveneBot (https://t.me/ConveneBot): los miembros de un grupo votan los días y horarios que les quedan cómodos para un evento. Node.js + Express + SQLite, MIT, presentado al concurso de Mini Apps de 2023 como ejemplo para clonar. — [GitHub hip-hyena/ConveneBot](https://github.com/hip-hyena/ConveneBot)
- Forms, @formston_bot: formularios y encuestas dentro de Telegram (crear, compartir, recibir respuestas en tiempo real y descargar los datos). Categoría "Business and Work" en FindMini. — [FindMini.app, Forms](https://www.findmini.app/formston_bot)
- Notepher: notas que se guardan en la nube de Telegram. Aparece en las menciones honoríficas de una lista de 2026 y su código está publicado. — [merge.rocks, best Telegram Mini Apps list 2026](https://merge.rocks/blog/are-telegram-mini-apps-safe-to-use-best-telegram-mini-apps-list-2026); [GitHub deptyped/notepher-bot](https://github.com/deptyped/notepher-bot)
- Otras utilidades chicas con código abierto listadas en la lista awesome: TeleOTP (generador de códigos de un solo uso), MemoCard (flashcards con repetición espaciada), Wishlist (lista de deseos), @PaintBot (dibujos colaborativos), ChessNowBot (ajedrez en vivo entre usuarios), StickerWiz y fStik (stickers), Calculator. — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- TON Names (@toname): seguimiento de transacciones TON para reportes impositivos, por suscripción. — [DEV Community, "30 best Mini Apps on TON in 2026"](https://dev.to/ton-adoption/30-best-mini-apps-on-ton-in-2026-catalog-by-category-1jc7)

**Tiendas y reservas (conceptos de ejemplo)**
- MiniWoo (Mini App para tiendas WooCommerce), Telebook (reserva de hotel), TRide (pedido de viajes), MedSync (turnos médicos) son apps concepto con código abierto. — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)

**Paso a paso de Dayfinder (el mejor modelo de flujo para una app de votación)**
- Crear: se manda `/start` al bot (o "Create new poll" en modo inline), se toca el botón adjunto que abre la Mini App, se carga título, descripción opcional y fechas candidatas, se elige si es anónima y si avisa en cada voto, y se toca "Create poll". — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)
- Compartir: el bot le manda al creador un enlace de votación. Se reenvía directo o se escribe `@dayfinderbot` en cualquier chat (modo inline) y se elige mandar el enlace de voto o los resultados a ese chat. — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)
- Votar: se abre el enlace, se marca cada fecha con Sí, No o Quizás, y se toca "Confirm vote". Reabrir el enlace permite cambiar el voto (pisa el anterior). — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)
- Resultados: desde el enlace se elige "View results". Hay un botón "Share with chat". En encuestas no anónimas, tocar los conteos muestra quién votó, con fecha y hora. El creador lista sus encuestas con `/polls` y puede borrarlas. — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)

### Inferences
- Dayfinder es el ejemplo vivo más cercano al proyecto del lector: backend Python, tres pantallas (crear, votar, resultados), voto editable, resultados compartibles al chat. El mapeo es casi directo: `/create` equivale a `/books-manager`, `/vote` al índice con la lista arrastrable, `/results` a `/winner`.
- La categoría tap-to-earn se puede resumir en una línea para el lector: existió, fue enorme en 2024 y a 2026 es residual. No sirve como referencia de diseño para una app de votación.
- Que la documentación oficial de junio de 2026 siga apuntando a @DurgerKingBot es el mejor indicio disponible de que la demo sigue en línea.

### Gaps
- No se verificó en vivo que ninguno de estos bots responda hoy (no hay acceso a Telegram desde esta investigación). Los bots de concurso de 2023 (@dayfinderbot, @ConveneBot) dependen de servidores de aficionados y pueden estar caídos. Las reglas del concurso solo exigían mantenerlos en línea hasta 10 días después de los resultados.
- @asmico_attach_bot: no apareció en ninguna fuente consultada. No se pudo confirmar que exista o siga activo. La documentación oficial actual solo nombra a @DurgerKingBot.
- Experiencia paso a paso de @DurgerKingBot: no se encontró una descripción citada. Recuerdo no verificado del investigador: el bot responde con un botón que abre una grilla de comidas con emoji, se suman ítems con botones +/-, el botón principal inferior dice algo como "VIEW ORDER" y luego "PAY", y termina en una factura de prueba que no cobra. Tomarlo como orientación, no como dato.
- No se obtuvieron cifras de usuarios de 2026 para @wallet ni para ninguna utilidad.
- No se confirmaron los @usernames de Notepher, TeleOTP, MemoCard, Wishlist ni ChessNowBot (solo los repositorios). Hay que mirar cada README.
- Se encontró pero no se leyó un artículo ruso de junio de 2026 con un top 12 de Mini Apps (https://kod.ru/top12-telegram-mini-apps). Puede servir para ampliar la lista.

## 2. ¿Existen Mini Apps o bots para encuestas, voto por ranking, quizzes, agenda o decisiones de grupo? ¿Las encuestas nativas soportan ranking?

### Takeaway
Las encuestas nativas de Telegram sumaron mucho en 2026 (medios, descripción, opciones sugeridas, límite de tiempo, resultados ocultos, mezcla de opciones, sin revoto, estadísticas) pero **no tienen ranking ni orden de preferencia**. Existen dos bots de voto por ranking, ambos con conteo Instant Runoff y ninguno con Condorcet o Schulze: @RankedPollBot y @ranked_choice_voting_bot. No se encontró ninguna Mini App con lista arrastrable y conteo Condorcet, que es justo lo que ofrece la app del lector.

### Cited Findings

**Encuestas nativas en 2026**
- La actualización del 31 de marzo de 2026 ("Mighty Polls") agregó: medios o ubicación en preguntas y opciones, descripción de la encuesta, que los usuarios sugieran opciones nuevas en encuestas activas, ver quién votó cada opción en encuestas de voto visible, desactivar el revoto, mezclar las opciones por usuario, límite de tiempo, resultados ocultos hasta que termine, que el creador vea resultados sin votar, quizzes con varias respuestas correctas, aviso al creador por cada respuesta en grupos, y una pestaña de encuestas en el perfil de grupos y canales. — [Telegram Blog, AI Editor, Mighty Polls...](https://telegram.org/blog/ai-editor-mighty-polls-and-more)
- Ese post no menciona ranking, voto preferencial ni ordenar opciones. Lo único relacionado con el orden es la mezcla aleatoria por usuario. — [Telegram Blog, AI Editor, Mighty Polls...](https://telegram.org/blog/ai-editor-mighty-polls-and-more)
- Una actualización posterior (reportada como de mayo de 2026) agregó estadísticas para administradores (gráfico de votos por opción en el tiempo, disponible a partir de 100 votos) y restricción de votantes en canales a suscriptores o a países específicos. Tampoco menciona ranking. — [The Tech Outlook](https://www.thetechoutlook.com/news/apps/10-new-features-and-various-bug-improvements-released-with-telegrams-latest-update/); [Postium](https://postium.ru/telegram-dobavil-statistiku-dlya-oprosov/)
- Límites según un rastreador no oficial: pregunta de 1 a 255 caracteres, de 1 a 12 opciones, opciones de hasta 100 caracteres, descripción de hasta 4.096 caracteres, duración de hasta 30 días. — [Telegram Limits, tginfo](https://limits.tginfo.me)
- Los tipos base siguen siendo encuesta común (una o varias respuestas, anónima o visible) y quiz, desde Polls 2.0. — [Telegram Blog, Polls 2.0](https://telegram.org/blog/polls-2-0-vmq)

**Bots de voto por ranking**
- @RankedPollBot (https://t.me/RankedPollBot): "encuestas donde podés rankear cada opción en vez de elegir una sola". Conteo Instant Runoff. Python 3 con aiogram y Redis, licencia Apache 2.0, 30 commits. El README no describe la interfaz de voto y dice solo "hablale en Telegram". Instala `svg-sankey`. — [GitHub ASzc/telegram-rcv-bot](https://github.com/ASzc/telegram-rcv-bot)
- @ranked_choice_voting_bot (https://t.me/ranked_choice_voting_bot), lanzado en Product Hunt el 28 de diciembre de 2024 como "RCV Tele Bot": crear y votar encuestas de ranking en Telegram. — [Product Hunt](https://www.producthunt.com/products/ranked-choice-voting-telegram-bot/launches)
- El repositorio de ese bot se describe como "bot de voto por ranking + webapp React de Telegram". Flujo: `/create_poll` con lista de `@usernames`, título y opciones en líneas separadas, o `/create_group_poll` para que los miembros del chat se registren solos. Se vota con `/vote {poll_id}: opción_1 > opción_2` o desde la webapp. El último lugar admite `withhold` (voto de no confianza) y `abstain`. Los resultados solo se ven cuando el creador cierra con `/close_poll`. Solo votan los usuarios registrados para esa encuesta. — [GitHub milselarch/RCV-tele-bot](https://github.com/milselarch/RCV-tele-bot)
- Stack de ese bot: Python 3.12 con python-telegram-bot y peewee, MySQL/MariaDB y Redis, conteo en una librería Rust (`trie_rcv`) vía pyo3, webapp en React + TypeScript desplegada en Firebase. 385 commits, 5 estrellas. Faltantes declarados: no hay webapp para crear o administrar encuestas, las encuestas se referencian solo por ID numérico, no soporta encuestas simples de sí/no. — [GitHub milselarch/RCV-tele-bot](https://github.com/milselarch/RCV-tele-bot)
- La búsqueda específica de bots de Telegram con Condorcet o Schulze no devolvió ninguno. Lo que aparece son librerías de conteo (por ejemplo `votes` en JavaScript) y servicios web ajenos a Telegram como CIVS. — [GitHub lzear/votes](https://www.github.com/lzear/votes); [CIVS, Condorcet Internet Voting Service](https://civs.cs.columbia.edu/rp.html)

**Agenda y decisiones de grupo**
- Dayfinder (@dayfinderbot) y ConveneBot (@ConveneBot), descritos en la sección 1, resuelven "qué día nos juntamos" con Mini App. En ConveneBot la elección final de la fecha por parte del organizador todavía no está en la interfaz y se hace fuera de la app. — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder); [GitHub hip-hyena/ConveneBot](https://github.com/hip-hyena/ConveneBot)

**Encuestas, formularios y quizzes**
- Forms (@formston_bot) es una Mini App de formularios y encuestas con descarga de datos. — [FindMini.app, Forms](https://www.findmini.app/formston_bot)
- @QuizBot es el bot oficial de quizzes. En el bug tracker de Telegram hay reportes (sin año visible) de que los quizzes enviados por @QuizBot fallaban al enviarse en Android, con estado "Fix coming". — [Telegram Bugs and Suggestions](https://bugs.telegram.org/c/62346)
- InstaQuiz es una Mini App de código abierto de quiz multijugador en tiempo real (hallada en resultados de búsqueda, no leída en detalle). — [awesome.ecosyste.ms](https://awesome.ecosyste.ms/projects/1386294)
- Ultimate Poll Bot (Nukesor), un bot de encuestas avanzado en Python con licencia GPL-3.0, figura como archivado y no es una Mini App. — [GitHub topics: pollbot](https://www.github.com/topics/pollbot)
- python-telegram-bot trae un ejemplo oficial `pollbot.py` que muestra cómo un bot crea encuestas nativas y recibe las respuestas. — [python-telegram-bot, pollbot.py](https://docs.python-telegram-bot.org/en/latest/examples.pollbot.html)

### Inferences
- Hay un hueco real: los dos bots de ranking usan Instant Runoff, uno vota por comandos de texto (`a > b > c`) y el otro no documenta su interfaz. Ninguna fuente muestra una Mini App con lista arrastrable más matriz de enfrentamientos Condorcet. La app del lector (SortableJS + Condorcet + tabla de duelos) no duplicaría algo existente.
- Lo que les falta a los bots existentes, visto desde un club de lectura: creación de la encuesta sin comandos, lista de candidatos administrable desde la app, resultados explicados (quién le gana a quién) y no solo un ganador.
- Las mejoras nativas de 2026 (resultados ocultos hasta el cierre, sin revoto, límite de tiempo, opciones mezcladas por usuario, opciones sugeridas) marcan lo que los usuarios de Telegram ya esperan de una votación. La app del lector ya mezcla la lista. Son buenas referencias de paridad.
- Para una primera ronda de filtrado (por ejemplo armar la lista de libros candidatos) alcanza una encuesta nativa con "sugerir opciones". El ranking final es lo que justifica la Mini App.

### Gaps
- @vote, @PollBot, @groupagreebot y "Easy Poll": las búsquedas no devolvieron ninguna fuente sobre su estado actual. No se pudo confirmar si siguen funcionando. Recuerdo no verificado del investigador: @vote y @PollBot son bots antiguos de la era previa a las encuestas nativas (2018) y son bots de chat con botones inline, no Mini Apps.
- No se pudo abrir ni @RankedPollBot ni @ranked_choice_voting_bot para describir la interfaz real de ranking ni confirmar que respondan. Los READMEs no muestran fecha del último commit.
- Los resultados de búsqueda mencionan actualizaciones de Telegram del 11 de junio y del 14 de julio de 2026 con cambios en encuestas ("límites", "encuestas más inteligentes") que no se pudieron abrir. Es poco probable que agreguen ranking, pero no está descartado con fuente primaria. Verificar en https://telegram.org/blog antes de afirmarlo de forma tajante.
- No se encontró ninguna Mini App ni bot orientado a clubes de lectura.

## 3. ¿Qué ve el usuario al abrir una Mini App (móvil y escritorio)?

### Takeaway
Una Mini App es una página web dentro de un WebView que Telegram presenta como un panel propio: aparece una pantalla de carga con el ícono del bot, luego la página con los colores del tema del usuario, un encabezado de Telegram arriba (con botón de volver o cerrar y un menú), y opcionalmente uno o dos botones grandes pegados abajo. Se abre a altura completa o a media altura, se puede expandir, minimizar a una barra inferior, pasar a pantalla completa o cerrar deslizando hacia abajo.

### Cited Findings

**Cómo se lanza (lo que toca el usuario)**
- Telegram soporta siete formas de lanzamiento: Main Mini App (botón "Launch app" en el perfil del bot y enlace `?startapp`), botón de teclado, botón inline debajo de un mensaje, botón de menú del chat, modo inline ("Switch to Mini App"), enlace directo `t.me/botusername/appname`, y menú de adjuntos (este último limitado a grandes anunciantes fuera del entorno de prueba). — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Los bots con Main Mini App pueden subir a su perfil videos y capturas de demostración (traducibles por idioma), y aparecen en la pestaña Apps de la búsqueda para los usuarios que ya los lanzaron. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)

**Apertura y tamaño**
- La Main Mini App y los enlaces directos se abren a altura completa por defecto (desde Bot API 7.6) o a media altura con `mode=compact`. La app puede llamar a `expand()` para ocupar toda la altura y el usuario también puede tirar del panel hacia arriba. `isExpanded` indica si está al máximo. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Pantalla de carga: el bot puede configurar en @BotFather su propio ícono y colores separados para modo claro y oscuro. El placeholder desaparece cuando la app llama a `ready()` o cuando la página termina de cargar. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps); [Telegram Blog, Full-screen Mini Apps](https://telegram.org/blog/fullscreen-miniapps-and-more)
- Pantalla completa: desde noviembre de 2024 las Mini Apps pueden ocupar toda la pantalla en vertical u horizontal (`requestFullscreen` / `exitFullscreen`) y bloquear la orientación. En ese modo desaparecen las barras superior e inferior de Telegram. — [Telegram Blog, Full-screen Mini Apps](https://telegram.org/blog/fullscreen-miniapps-and-more); [Mini App Features, grom-dev](https://grom-dev.github.io/mini-apps/features/overview)

**Elementos de interfaz que pone Telegram**
- Botón inferior (`BottomButton`, antes `MainButton`, renombrado en Bot API 7.10): un botón al pie de la pantalla con texto, colores, visibilidad, estado habilitado e indicador de carga configurables. Hay un `SecondaryButton` que se ubica a la izquierda, derecha, arriba o abajo del principal. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- `BackButton`: control de volver en el encabezado, que la app muestra con `show()` y maneja con `onClick`. `SettingsButton`: un ítem "Settings" en el menú contextual de la app. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Color del encabezado: `setHeaderColor` acepta cualquier `#RRGGBB` o palabras clave del tema. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Tema: `colorScheme` vale "light" o "dark", `themeParams` entrega los colores del tema del usuario en tiempo real, también como variables CSS (`--tg-theme-bg-color` y similares), y el evento `themeChanged` se dispara al pasar de día a noche o cambiar de tema. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)

**Cerrar, minimizar y gestos**
- Por defecto el usuario puede ocultar la app deslizándola hacia abajo. Los gestos verticales propios de la app pueden chocar con ese gesto y minimizarla por accidente. La app puede desactivar los deslizamientos verticales (`disableVerticalSwipes`), y aun así se puede minimizar o cerrar deslizando el encabezado. — [docs.telegram-mini-apps.com, Swipe behavior](https://docs.telegram-mini-apps.com/platform/swipe-behavior); [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- `enableClosingConfirmation` hace que aparezca un diálogo de confirmación cuando el usuario intenta cerrar. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- La documentación comunitaria advierte que antes de bloquear el cierre por deslizamiento hay que asegurarse de que la app no pueda colgarse, porque deslizar hacia abajo es la salida de emergencia del usuario. — [docs.telegram-mini-apps.com, Sticky app](https://docs.telegram-mini-apps.com/platform/sticky-app)
- Problema conocido: si el contenido no es scrolleable o está en la posición cero, deslizar hacia abajo colapsa el panel en vez de scrollear. Hay quejas de usuarios en el bug tracker por cierres accidentales. — [DEV Community, scrolling collapse issue](https://dev.to/nimaxin/how-to-fix-the-telegram-mini-app-scrolling-collapse-issue-a-handy-trick-1abe); [Telegram Bugs and Suggestions](https://bugs.telegram.org/c/36664)
- Las páginas y Mini Apps se pueden colapsar a una barra inferior y reabrir desde ahí sin perder el progreso, para alternar entre mensajes, sitios y apps. En macOS el navegador integrado tiene pestañas que incluyen Mini Apps. — [Telegram Blog, julio de 2024](https://telegram.org/blog/w3-browser-mini-app-store)
- El usuario puede agregar un acceso directo de una Mini App a la pantalla de inicio del teléfono (`addToHomeScreen`). — [Telegram Blog, Full-screen Mini Apps](https://telegram.org/blog/fullscreen-miniapps-and-more); [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)

**Devolver algo al chat**
- `sendData` (solo apps de botón de teclado) manda un mensaje de servicio al bot y cierra la app. `answerWebAppQuery` (botón inline, de menú o adjuntos) publica un mensaje en nombre del usuario y cierra la app. `shareMessage` abre un diálogo para compartir un mensaje preparado a cualquier chat. `switchInlineQuery` deja escrito el usuario del bot y una consulta en el campo de texto del chat. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)

**Plataformas**
- Los clientes se identifican como `android`, `ios`, `macos`, `tdesktop` (Telegram Desktop), `weba` (Web A) y `web` (Web K). Las Mini Apps son aplicaciones web comunes mostradas en un WebView, y como cada cliente se desarrolla por separado puede haber variaciones en cómo implementan la plataforma. — [docs.telegram-mini-apps.com, About platform](https://docs.telegram-mini-apps.com/platform/about)

### Inferences
- Imagen mental en el celular, armada con lo anterior: el usuario toca un botón debajo de un mensaje del bot (o un enlace `t.me/bot/app` pegado en el grupo). Sube un panel desde abajo con el ícono del bot mientras carga. Aparece la página con el mismo fondo y los mismos colores que su Telegram (claro u oscuro). Arriba queda una franja de Telegram con el nombre de la app y un control para cerrar o volver. Abajo, pegado al borde, un botón ancho del color de acento del tema, por ejemplo "Enviar voto". Al tocarlo, el botón muestra un spinner, la app se cierra y en el chat aparece un mensaje del bot. Si se arrepiente, desliza el panel hacia abajo y vuelve al chat.
- Para una lista arrastrable (SortableJS) el conflicto de gestos es el riesgo de experiencia número uno: arrastrar un libro hacia abajo puede minimizar la app. La combinación razonable es `expand()` al abrir más `disableVerticalSwipes()`, dejando el encabezado como vía de cierre.
- El flujo "ordenar y confirmar" calza con el patrón nativo: el botón "Enviar" debería ser el `BottomButton` de Telegram y no un botón HTML dentro de la página, y `enableClosingConfirmation` evita perder un orden a medio armar.

### Gaps
- Confirmación del primer lanzamiento: ni la documentación oficial ni las otras fuentes consultadas describen el aviso que aparece la primera vez. Recuerdo no verificado del investigador: en el primer lanzamiento de una app por enlace directo o Main Mini App, Telegram muestra un diálogo de confirmación que menciona los términos de servicio de Mini Apps, y para ciertos tipos de lanzamiento pregunta si se permite al bot enviar mensajes. Confirmar probando en vivo.
- Escritorio y Web: la documentación oficial no describe cómo se ve en Telegram Desktop ni en la versión web. Recuerdo no verificado del investigador: en Telegram Desktop la Mini App se abre en una ventana flotante angosta con proporción de teléfono, con barra de título propia y los botones inferiores al pie de esa ventana, y en la web se abre como un modal centrado. No hay gesto de deslizar y se cierra con la X. Probar con el cliente real antes de documentarlo como hecho.
- No se encontró texto oficial sobre la altura por defecto de las apps lanzadas por botón de teclado, inline o de menú (la página consultada no lo detalla en la parte leída). Quedaron sin leer los últimos 15.000 caracteres de la página oficial.
- No se consiguieron capturas de pantalla citables. Los perfiles de bots con Main Mini App muestran capturas y videos, que es la forma más rápida de ver cómo luce una app antes de abrirla.

## 4. ¿Qué dicen las pautas de diseño oficiales? ¿Hay kits de UI?

### Takeaway
Las pautas oficiales son breves y concretas: diseño responsivo mobile-first, controles que imiten a los de Telegram, animaciones fluidas a 60 fps, inputs e imágenes con etiquetas, usar los colores dinámicos del tema, respetar las áreas seguras y bajar efectos en Android de gama baja. El kit de referencia es TelegramUI (`@telegram-apps/telegram-ui`), que es solo para React. Para HTML y JS planos alcanza con las variables CSS `--tg-theme-*`.

### Cited Findings
- Diseño responsivo: todos los elementos deben ser responsivos y diseñarse con enfoque mobile-first. — [Telegram Mini Apps, Design Guidelines](https://core.telegram.org/bots/webapps)
- Interfaz familiar: los elementos interactivos deben copiar el estilo, el comportamiento y la intención de los controles existentes de Telegram. — [Telegram Mini Apps, Design Guidelines](https://core.telegram.org/bots/webapps)
- Animación: las animaciones deben ser fluidas, idealmente a 60 fps. — [Telegram Mini Apps, Design Guidelines](https://core.telegram.org/bots/webapps)
- Accesibilidad: los inputs y las imágenes deben tener etiquetas. — [Telegram Mini Apps, Design Guidelines](https://core.telegram.org/bots/webapps)
- Colores: la app debe seguir los colores dinámicos del tema que entrega la API. — [Telegram Mini Apps, Design Guidelines](https://core.telegram.org/bots/webapps)
- Áreas seguras: la interfaz no debe superponerse con otros controles, sobre todo en pantalla completa. `safeAreaInset` da los márgenes del sistema (notch, barra de navegación) y `contentSafeAreaInset` el área libre de la interfaz de Telegram. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Rendimiento en Android: usar los datos del User-Agent para detectar la clase de rendimiento del dispositivo y reducir animaciones y efectos en equipos de gama baja. — [Telegram Mini Apps, Design Guidelines](https://core.telegram.org/bots/webapps)
- Posicionamiento: `viewportHeight` cambia en vivo y no sirve para fijar elementos al borde inferior. Para eso se usa `viewportStableHeight`. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- TelegramUI es una librería de componentes React para Mini Apps inspirada en la interfaz de Telegram. Paquete `@telegram-apps/telegram-ui`, licencia MIT, 873 estrellas. Trae soporte para las Human Interface Guidelines de iOS y Material Design de Android (se ve nativo en ambas), soporta los esquemas de color de Telegram, layouts responsivos y renderizado del lado del servidor. — [GitHub Telegram-Mini-Apps/TelegramUI](https://github.com/Telegram-Mini-Apps/TelegramUI)
- TelegramUI tiene kit de Figma (https://figma.com/community/file/1348989725141777736/) y un Storybook con playground (https://tgui.xelene.me/). — [GitHub Telegram-Mini-Apps/TelegramUI](https://github.com/Telegram-Mini-Apps/TelegramUI)
- Otros recursos de la lista awesome: `@twa-dev/Mark42` (kit liviano), `@tonconnect/ui` (solo para conectar billeteras TON) y "Telegram Graphics" en Figma como inspiración visual (https://www.figma.com/community/file/1248595286803212338/telegram-graphics). — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Consejos de una guía de 2026 para comunidades: reducir pasos, mantener al usuario dentro de Telegram, diseñar mobile-first con conciencia del tema, pantalla completa y áreas seguras, mapear cada paso antes de construir, dejar que el usuario corrija errores y definir qué pasa cuando un paso falla. — [Metricgram, Telegram Mini Apps Guide](https://metricgram.com/blog/telegram-mini-apps-guide)

### Inferences
- Para la app del lector (plantillas Jinja + JS plano + SortableJS) TelegramUI no aplica de forma directa porque exige React. El camino corto es reescribir el CSS usando `var(--tg-theme-bg-color)`, `var(--tg-theme-text-color)`, `var(--tg-theme-button-color)` y afines, y usar el Storybook de TelegramUI y el Figma solo como referencia visual de cómo se ven una lista, una celda y una sección al estilo Telegram.
- "Sentirse nativo" se reduce en la práctica a cinco cosas: colores del tema, botón de acción principal provisto por Telegram, botón de volver de Telegram en vez de enlaces propios, nada de encabezados web propios (logo, navbar), y filas de lista con el aspecto de las listas de ajustes de Telegram.
- La regla de etiquetas en inputs afecta al campo de nombre actual. Dentro de Telegram ese campo incluso podría desaparecer porque la app recibe la identidad del usuario (tema que cubren otros investigadores).

### Gaps
- La página del repositorio de TelegramUI no lista los componentes ni muestra versión o fecha del último release. Recuerdo no verificado del investigador: incluye componentes como List, Section, Cell, Button, Input, Checkbox, Modal, Tabbar, Avatar, Badge y Placeholder. Verificar en el Storybook.
- No se encontró un kit de componentes oficial para HTML/CSS plano sin framework.
- La sección de pautas de diseño oficial es corta. No se encontró un documento oficial más extenso con medidas, tipografías o espaciados.

## 5. ¿Dónde se pueden explorar Mini Apps y cómo se logra aparecer ahí?

### Takeaway
Hay tres lugares: dentro de Telegram (pestaña Apps de la búsqueda, perfiles de bots con botón "Launch app" y capturas), el Telegram Apps Center de la TON Foundation (tapps.center) y catálogos independientes como FindMini.app. En los dos catálogos externos cualquiera puede enviar su app. Para una app privada de un club de lectura ninguno es necesario.

### Cited Findings
- Los bots con Main Mini App configurada muestran un botón "Launch app" en su perfil, pueden subir capturas y videos de demostración, y pueden aparecer en la pestaña Apps de la búsqueda de Telegram para los usuarios que ya los lanzaron. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- El post de Telegram del 31 de julio de 2024 lleva "Mini App Store" en su imagen de título, pero el texto no explica la tienda. Describe el navegador integrado, la barra inferior para minimizar páginas y apps, y las pestañas en macOS. — [Telegram Blog, julio de 2024](https://telegram.org/blog/w3-browser-mini-app-store)
- Telegram Apps Center (tApps Center) fue creado por la TON Foundation como directorio central de bots y Mini Apps, con interfaz parecida a una tienda de apps. La antigua página de publicación de docs.ton.org ahora redirige a la documentación oficial de Telegram. — [docs.ton.org, Publishing Mini Apps](https://docs.ton.org/develop/dapps/telegram-apps/publishing)
- Según un blog de una red publicitaria, enviar una app a Telegram Apps Center es gratis para los desarrolladores. — [AdsGram blog](https://adsgram.ai/blog/adsgram/telegram-apps-center-your-gateway-to-mini-apps-bots)
- La página de marketing de TON indica que solo las Mini Apps ya listadas en tApps Center pueden ser destacadas, que la solicitud de listado se hace por un formulario enlazado ahí, y que los pedidos de destaque se mandan con al menos 7 días hábiles de anticipación. — [TON, Telegram Apps Center Featuring](https://ton-org.notion.site/Telegram-Apps-Center-Featuring-b7a50b252b5144108deeb5a13176943a)
- FindMini.app es un catálogo independiente. Un listado lo describe con más de 6.200 apps. Cada ficha muestra categoría, usuarios mensuales y un gráfico de popularidad. — [WebCatalog, FindMini.app](https://webcatalog.io/apps/findmini-app); [FindMini.app, Forms](https://www.findmini.app/formston_bot)
- En FindMini se envía una app con el botón "+ Add your app" (sirve para Mini Apps, bots y apps TON). También vende promoción: 200 dólares en TON o USDT por una semana en el bloque Promo. Cada ficha tiene "Report this app". — [FindMini.app, Forms](https://www.findmini.app/formston_bot)
- Categorías en tendencia en FindMini al momento de la consulta: Marketplaces, Stars, Homework Help, NFT and Collectibles, Video Generation, Text Generation, Travel and Tickets, Image Generation, Fitness and Sports, AI Assistants and Chatbots. — [FindMini.app, Forms](https://www.findmini.app/formston_bot)
- Otros puntos de descubrimiento: el canal Trending Apps (https://t.me/trendingapps) y PlayDeck para juegos (https://playdeckbot.t.me). — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Advertencia de un catálogo de 2026: la mayoría de las Mini Apps listadas son clones de baja calidad o spam. Telegram nunca pide el código de inicio de sesión por un bot o Mini App, y cualquier pedido así es una estafa. — [merge.rocks, best Telegram Mini Apps list 2026](https://merge.rocks/blog/are-telegram-mini-apps-safe-to-use-best-telegram-mini-apps-list-2026)

### Inferences
- Para buscar ejemplos de encuestas y votaciones, el camino práctico es abrir FindMini.app y buscar "poll", "vote", "survey" o "quiz", o mirar la categoría "Business and Work > Organizers and Productivity" donde está Forms.
- Una app de club de lectura no necesita ningún catálogo. Se distribuye pegando el enlace `t.me/<bot>/<app>` en el grupo o con un botón en un mensaje fijado. Listarse solo tiene sentido si se quiere ofrecer la app a otros clubes.
- Las categorías en tendencia de FindMini (IA, marketplaces, Stars) muestran que el ecosistema se movió del tap-to-earn hacia utilidades e IA, y que una herramienta de votación entra en un nicho poco poblado.

### Gaps
- No se pudo leer el formulario ni los requisitos exactos de envío a tapps.center (la búsqueda sugiere un bot @tapps_bot pero sin fuente que lo confirme). Tampoco se confirmó si el catálogo sigue activo a fines de 2026.
- No se encontró una descripción oficial detallada de la "Mini App Store" dentro de Telegram ni de los criterios para aparecer en la pestaña Apps para usuarios que nunca lanzaron la app.
- No se consultó tgstat ni otros directorios de bots.

## 6. ¿Hay Mini Apps de ejemplo con código abierto y fácil de leer?

### Takeaway
Sí, y varias son chicas. Para el caso del lector (Python + HTML plano) los mejores puntos de partida son Dayfinder (Python, encuesta de fechas, MIT), el boilerplate `twa-dev/vanilla-js-boilerplate` (HTML y JS sin framework), los ejemplos de backend Python de la lista awesome y ConveneBot (Node + SQLite, muy pocos archivos). El concurso de Mini Apps de 2023 obligó a publicar todo el código bajo licencia libre, así que es la mejor cantera.

### Cited Findings
- El concurso de Mini Apps de Telegram de 2023 exigía publicar el código completo de cliente y servidor bajo una licencia libre (BSD, MIT o similar) y mantener la app en línea hasta 10 días después de los resultados, anunciados el 31 de octubre de 2023. — [Telegram Contests](https://t.me/s/contest)
- Entre los ganadores mencionados en el canal del concurso están una app de cafetería (Laurel Cafe), una "Mini App Store" hecha como Mini App, una app de propinas y un Pictionary. Las entradas se pueden ver en contest.com. — [Telegram Contests](https://t.me/s/contest); [contest.com, entrada de ejemplo](https://contest.com/mini-apps/entry4515)
- MemoCard (flashcards con repetición espaciada) fue una de las ganadoras y su autor publicó un relato del desarrollo en abril de 2024. Código: https://github.com/kubk/memo-card. — [Teletype, MemoCard contest win](https://teletype.in/@alteregor/memocard-telegram-contest-win); [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Dayfinder: Python 3.11+, python-telegram-bot y Quart sirviendo la Mini App, MIT, 26 commits, se puede alojar una instancia propia. — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)
- ConveneBot: `server.js`, `package.json` y una carpeta `static/`, con Express y SQLite, MIT, 3 commits, pensado como ejemplo para clonar y modificar. — [GitHub hip-hyena/ConveneBot](https://github.com/hip-hyena/ConveneBot)
- Plantilla sin framework: `@twa-dev/vanilla-js-boilerplate` (https://github.com/twa-dev/vanilla-js-boilerplate). También hay plantillas con Vite y Webpack de la misma organización. — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Ejemplos con backend Python: "Python Backend Example" (https://github.com/poshl000/telegram-webapp-bot), ejemplo con aiogram y aiohttp (https://github.com/abdullaev388/Telegram-Web-App), Mini Events, un framework Python para Mini Apps de eventos (https://github.com/mbasaglia/mini_apps), y `telegram-webapp-auth` para validar `initData` en Python (https://github.com/swimmwatch/telegram-webapp-auth). — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Otras apps de ejemplo con código: Notepher (https://github.com/deptyped/notepher-bot), TeleOTP (https://github.com/UselessStudio/TeleOTP), Wishlist (https://github.com/grulex/telegram-wishlist-miniapp), ChessNowBot (https://github.com/Quatern1on/ChessNowBot), @PaintBot (https://github.com/hip-hyena/PaintBot), Datetime Picker (https://github.com/Expented/tgdtp), Telebook (https://github.com/neSpecc/telebook). — [awesome-telegram-mini-apps](https://github.com/telegram-mini-apps-dev/awesome-telegram-mini-apps)
- Voto por ranking con código: RCV-tele-bot (Python + Rust + React, complejo de desplegar porque requiere toolchain de Rust, MySQL y Redis) y telegram-rcv-bot (Python + aiogram + Redis). — [GitHub milselarch/RCV-tele-bot](https://github.com/milselarch/RCV-tele-bot); [GitHub ASzc/telegram-rcv-bot](https://github.com/ASzc/telegram-rcv-bot)
- La organización `Telegram-Mini-Apps` en GitHub aloja TelegramUI y la documentación comunitaria de la plataforma (docs.telegram-mini-apps.com). — [GitHub Telegram-Mini-Apps/TelegramUI](https://github.com/Telegram-Mini-Apps/TelegramUI); [docs.telegram-mini-apps.com](https://docs.telegram-mini-apps.com/platform/about)

### Inferences
- Orden de lectura sugerido para el lector: primero Dayfinder (mismo dominio, mismo lenguaje, mismo tamaño de proyecto), después el boilerplate vanilla para ver el mínimo de HTML que hace falta, y por último ConveneBot para el patrón "enlace en el grupo que abre la app".
- RCV-tele-bot sirve más como referencia de reglas de negocio (registro de votantes, abstención, cierre de la encuesta antes de mostrar resultados) que como base de código, por su complejidad de despliegue.
- No apareció ningún ejemplo con Flask. Quart (el de Dayfinder) tiene una API casi idéntica a Flask, así que su código se lee de forma directa.

### Gaps
- No se encontró una lista única y oficial de repositorios de los ganadores del concurso. Hay que buscarlos uno por uno en GitHub (etiqueta `telegram-miniapp-contest-2023`) o en el canal @contest.
- No se abrió el código de ninguno de estos repositorios para evaluar su legibilidad real, ni se verificó qué usa Dayfinder en el frontend (el README no lo dice).
- No se verificó la fecha del último commit de la mayoría. Varios son de 2023 y pueden usar versiones antiguas de la API (por ejemplo `MainButton` en vez de `BottomButton`).

## 7. ¿Cómo se usan las Mini Apps en grupos y comunidades chicas?

### Takeaway
El patrón dominante es: alguien publica en el grupo un mensaje con un enlace o botón que abre la Mini App, cada miembro la abre por su cuenta, hace su parte y el bot (o el propio usuario con "compartir") devuelve un resumen al chat. Dayfinder y ConveneBot muestran las dos variantes. Una guía de 2026 advierte que para necesidades simples alcanza con una encuesta nativa o un mensaje fijado.

### Cited Findings
- ConveneBot: un miembro escribe `@ConveneBot <NOMBRE DEL EVENTO>` en el campo de mensaje del grupo, toca la opción de crear evento y eso publica en el chat un enlace al evento. Cada miembro abre el enlace, que lanza la Mini App, se suma y marca sus horarios. — [GitHub hip-hyena/ConveneBot](https://github.com/hip-hyena/ConveneBot)
- Dayfinder: la encuesta se crea en privado con el bot, se comparte al grupo por modo inline (`@dayfinderbot` más el nombre) y los resultados tienen un botón "Share with chat". — [GitHub falko17/dayfinder](https://github.com/falko17/dayfinder)
- RCV-tele-bot: `/create_group_poll` crea una encuesta en la que los miembros del chat se registran solos, y existe `/whitelist_chat_registration` para habilitar el registro desde un chat. Los resultados quedan ocultos hasta `/close_poll`. — [GitHub milselarch/RCV-tele-bot](https://github.com/milselarch/RCV-tele-bot)
- Un enlace directo `t.me/botusername/appname` abre la Mini App en el chat actual con contexto del chat pero sin acceso al chat, es decir que la app no puede leer ni escribir mensajes por sí sola. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- `shareMessage` abre un diálogo para que el usuario comparta un mensaje preparado a cualquier chat, y `answerWebAppQuery` publica un mensaje en nombre del usuario cuando la app se abrió desde un botón inline o de menú. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Desde noviembre de 2024 los usuarios pueden compartir medios generados por una Mini App a cualquier chat o a sus historias. — [Telegram Blog, Full-screen Mini Apps](https://telegram.org/blog/fullscreen-miniapps-and-more)
- Desde Bot API 10.1 (junio de 2026) hay un lanzamiento específico para solicitudes de ingreso a un chat, donde un bot guardián muestra una Mini App antes de aprobar el ingreso. — [Telegram Mini Apps, core.telegram.org](https://core.telegram.org/bots/webapps)
- Usos típicos en comunidades según una guía de julio de 2026 (actualizada en octubre): inscripción a eventos y turnos, onboarding de varios pasos, perfiles y preferencias de miembros, contenido restringido para miembros pagos, formularios de soporte. — [Metricgram, Telegram Mini Apps Guide](https://metricgram.com/blog/telegram-mini-apps-guide)
- La misma guía dice que una Mini App es excesiva cuando el problema es de reglas o de organización, y que para lo simple conviene un mensaje fijado, una respuesta del bot, una encuesta nativa, botones del bot o temas de foro: "una interfaz a medida no arregla un modelo operativo débil". — [Metricgram, Telegram Mini Apps Guide](https://metricgram.com/blog/telegram-mini-apps-guide)
- En grupos con encuestas nativas de voto visible, el creador recibe un aviso por cada respuesta, y los grupos tienen una pestaña con encuestas activas y pasadas. — [Telegram Blog, AI Editor, Mighty Polls...](https://telegram.org/blog/ai-editor-mighty-polls-and-more)

### Inferences
- Flujo natural para el club de lectura, calcado de Dayfinder y ConveneBot: el organizador abre la votación, el bot publica en el grupo un mensaje con el botón o enlace "Votar", cada miembro abre la Mini App, ordena los libros y confirma, el bot va actualizando en el grupo quiénes ya votaron (algo que la app actual ya muestra al público) y al cerrar publica el ganador con un enlace a la tabla de enfrentamientos.
- El ranking por arrastre es justamente un caso en que la Mini App no es excesiva, porque la encuesta nativa no puede expresarlo. La elección previa de candidatos sí se puede resolver con una encuesta nativa.
- Como el enlace directo no da acceso al chat, publicar resultados en el grupo requiere que el bot sea miembro del grupo y mande el mensaje él, o que el usuario lo comparta con `shareMessage`. Es una decisión de diseño que el redactor del informe debería cruzar con las notas técnicas de los otros investigadores.

### Gaps
- No se encontraron relatos de uso real (reseñas, posts de comunidades) de Mini Apps de votación en grupos chicos. Lo documentado viene de READMEs y de una guía de un proveedor.
- La guía de Metricgram no nombra ninguna app concreta y pertenece a una empresa que vende herramientas de gestión de grupos, así que su postura de "primero ordená la operación" tiene sesgo comercial.
- No se confirmó cómo se ve el mensaje con botón de Mini App dentro de un grupo (por ejemplo si los botones `web_app` inline funcionan en grupos o solo en chats privados, donde históricamente estaban limitados). Es un punto técnico a verificar por quien cubra los fundamentos de la plataforma.
