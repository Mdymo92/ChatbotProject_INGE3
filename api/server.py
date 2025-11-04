from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from random import randint
import requests

# from chatbot.actions.recommandation import lookup_item, cosine_explore, inventory
from voicebot.t2s import process_bot_answer
from voicebot.s2t import process_voice  

# ENDPOINTS
bot_url = "http://127.0.0.1:5005/webhooks/rest/webhook"
action_server_url = "http://localhost:5055/webhook"

# APP CONTEXT
app = FastAPI()
session_uid = randint(1, 1000)

# DIRECORIES
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# METHODS
def request_to_bot(text, uid="1"):
    print(f"UserID is: {uid}")
    request = {"sender": uid, "message": text}

    bot_answer = requests.post(bot_url, json=request)
    return bot_answer.json()


# ENDPOINTS
@app.get("/")  # Root endpoint
async def get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/wav")  # text to speech endpoint
async def get(request: Request):
    return FileResponse("bot_answer.mp3")


@app.post("/save-record")  # speech to text endpoint
async def get(request: Request):
    process_voice("processed_file.wav")
    return FileResponse("processed_file.wav")


@app.websocket(
    "/ws"
)  # Websocket endpoint to retrieve user messages and send bot anwsers
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_uid = randint(1, 1000)
    while True:
        data = await websocket.receive_text()
        print(f"User message was: {data}")
        print("--" * 20)

        if (
            data == "/restart"
        ):  # just to handle websocket interaction when bot is restarted
            print("Restarting bot...")
            await websocket.send_text(f"Bot: Restarting bot...")
            continue

        print("Sending to bot")
        response = request_to_bot(data, uid=str(session_uid))
        print(f"Bot response: {response}")
        process_bot_answer(
            response[0]["text"] if response else "Sorry, I did not understand that"
        )  # convert bot answer to speech
        print("Sending to client...")
        await websocket.send_text(
            f"Bot: {response[0]['text'] if response else 'Sorry, I did not understand that'}"
        )
        print("Sent to client")
