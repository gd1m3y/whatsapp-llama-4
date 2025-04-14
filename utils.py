import requests
import httpx
from PIL import Image
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
from together import Together
load_dotenv()


client = Together()  # Uses TOGETHER_API_KEY from .env
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
AGENT_URL = os.getenv("AGENT_URL")
MEDIA_URL = "https://graph.facebook.com/v20.0/{media_id}"

def send_message(to: str, text: str):
    print(AGENT_URL,MEDIA_URL,WHATSAPP_API_URL,ACCESS_TOKEN)
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    print("Message sent" if response.status_code == 200 else f"Send failed: {response.text}")

async def fetch_media(media_id: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            MEDIA_URL.format(media_id=media_id),
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        if response.status_code == 200:
            return response.json().get("url")
        return None

async def process_image_to_base64(media_url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(media_url, headers={"Authorization": f"Bearer {ACCESS_TOKEN}"})
        image = Image.open(BytesIO(response.content))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

# async def call_llm_api(base64_image: str, user_phone: str):
#     url = f"{AGENT_URL}/generate_info_from_image"
#     payload = {"image_message": base64_image, "language": "Hindi"}
#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
#     # response = requests.post(url, json=payload, headers=headers)
#     # res
#     if response.status_code == 200:
#         # await send_message(user_phone, response.json()["response"])
#         await send_message(user_phone,"hello")
#     else:
#         await send_message(user_phone, "Failed to process image.")

# async def call_order_api(user_phone: str, query: str):
#     url = f"{AGENT_URL}/order_based_on_name"
#     payload = {"query": query}
#     headers = {"Authorization": f"Bearer {ACCESS_TOKEN}", "Content-Type": "application/json"}
#     response = requests.post(url, json=payload, headers=headers)
#     if response.status_code == 200:
#         await send_message(user_phone, response.json()["response"]["content"])
#     else:
#         await send_message(user_phone, "Could not fetch order information.")


def llm_reply_to_text(user_input: str,user_phone):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
            messages=[{"role": "user", "content": user_input}]
        )
        return send_message(user_phone, response.choices[0].message.content)
    except Exception as e:
        print("❌ LLM error:", e)
        return "Sorry, something went wrong while generating a response."
