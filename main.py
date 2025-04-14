from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils import send_message,llm_reply_to_text
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
AGENT_URL = os.getenv("AGENT_URL")

class WhatsAppMessage(BaseModel):
    object: str
    entry: list


# @app.get("/webhook")
# async def verify_webhook(request: Request):
#     mode = request.query_params.get("hub.mode")
#     token = request.query_params.get("hub.verify_token")
#     challenge = request.query_params.get("hub.challenge")
#     print(mode)
#     print(token)
#     print(challenge)

#     # if mode and token and mode == "subscribe" and token == "1234":
#     #     return {"hub_verfiy_mode":mode,"hub_verify_token":token, "hub_verify_challange":challenge }
#     # return token

#     return int(challenge)
#     # return {"error": "Invalid verification token"}


@app.post("/webhook")
async def webhook_handler(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    message_data = WhatsAppMessage(**data)

    try:
        change = message_data.entry[0]["changes"][0]["value"]
        message = change["messages"][-1]
        user_phone = message["from"]

        if "text" in message:
            user_message = message["text"]["body"].lower()

            
            background_tasks.add_task(send_message, user_phone,llm_reply_to_text(user_message,user_phone))
            # elif user_message.startswith("order:"):
            #     query = user_message[6:]
            #     background_tasks.add_task(call_order_api, user_phone, query)

        # elif "image" in message:
        #     media_id = message["image"]["id"]
        #     media_url = await fetch_media(media_id)
        #     base64_image = await process_image_to_base64(media_url)
        #     background_tasks.add_task(call_llm_api, base64_image, user_phone)

        # elif "audio" in message:
        #     media_id = message["audio"]["id"]
        #     media_url = await fetch_media(media_id)
        #     await send_message(user_phone, f"Audio received. Download URL: {media_url}")

    except Exception as e:
        print("Error processing message:", e)

    return JSONResponse(content={"status": "ok"})

# Endpoint to verify webhook with WhatsApp
