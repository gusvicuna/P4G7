# P4G7

Para correr el bot debe abrir una consola en la carpeta P4G7 y ejectuar bot.py
Luego en otra consola en la misma carpeta debe ejecutar 'ngrok http 8080', apareceran varias lineas, de estas una con la forma
    'Forwarding                    https://1e1d-181-43-38-66.ngrok.io -> http://localhost:8080'
es la importante, de aqui hay que guardar la parte equivalente a 'https://1e1d-181-43-38-66.ngrok.io'
Finalmente hay que configurar el webhook del bot para que redireccione los mensajes a esa pagina, para esto en un navegador hay que ingresar a la direccion
    'https://api.telegram.org/bot2105695159:AAGP21o80wOJeBFXHDGTX7n7aJxAAEm3jwg/setWebHook?url=URL_IMPORANTE'
remplazando URL_IMPORTANTE por la url que nos dio ngrok, para este ejemplo seria
    'https://api.telegram.org/bot2105695159:AAGP21o80wOJeBFXHDGTX7n7aJxAAEm3jwg/setWebHook?url=https://1e1d-181-43-38-66.ngrok.io'
Si todo esta bien vera este mensaje
    '{"ok":true,"result":true,"description":"Webhook was set"}'