import os
from aiohttp import web

# Telegram Webhook logikasi (joriy holat saqlab qolinadi)
async def telegram_webhook(request):
    # Bu yerda sizning webhook logikangiz turadi
    return web.Response(text="OK")

# J.A.R.V.I.S. Telegram Mini App (TMA) interfeysi
async def miniapp_handler(request):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>J.A.R.V.I.S. Console</title>
        <script src="https://telegram.org/js/telegram-web-app.js"></script>
        <style>
            body {
                background-color: #050505;
                color: #00e5ff;
                font-family: 'Courier New', Courier, monospace;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                margin: 0;
            }
            .arc-reactor {
                width: 150px;
                height: 150px;
                border-radius: 50%;
                border: 4px solid #00e5ff;
                box-shadow: 0 0 20px #00e5ff, inset 0 0 20px #00e5ff;
                display: flex;
                align-items: center;
                justify-content: center;
                animation: pulse 2s infinite alternate;
                margin-bottom: 30px;
            }
            @keyframes pulse {
                0% { box-shadow: 0 0 20px #00e5ff, inset 0 0 20px #00e5ff; }
                100% { box-shadow: 0 0 40px #00e5ff, inset 0 0 40px #00e5ff; }
            }
            h1 { font-size: 24px; text-transform: uppercase; letter-spacing: 2px; }
            p { font-size: 14px; opacity: 0.8; }
        </style>
    </head>
    <body>
        <div class="arc-reactor">
            <h1>SYS</h1>
        </div>
        <h1 id="greeting">Awaiting Connection...</h1>
        <p>J.A.R.V.I.S. Online</p>
        
        <script>
            let tg = window.Telegram.WebApp;
            tg.expand();
            tg.ready();
            
            // Foydalanuvchi ismini olish
            let user = tg.initDataUnsafe?.user?.first_name || "Sir";
            document.getElementById("greeting").innerText = `Welcome back, ${user}.`;
            
            // Haptic feedback
            tg.HapticFeedback.impactOccurred('heavy');
        </script>
    </body>
    </html>
    """
    return web.Response(text=html_content, content_type='text/html')

app = web.Application()
app.router.add_get('/', miniapp_handler)
app.router.add_post('/webhook/telegram', telegram_webhook)

if __name__ == '__main__':
    # PORT 8081 GA O'ZGARTIRILDI
    port = int(os.getenv("PORT", 8081))
    web.run_app(app, host='127.0.0.1', port=port)
