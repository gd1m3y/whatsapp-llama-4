import os
import base64
import asyncio
import requests
import httpx
from PIL import Image
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MEDIA_URL = "https://graph.facebook.com/v20.0/{media_id}"
BASE_URL = os.getenv("BASE_URL")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def send_message(to: str, text: str):
    if not text:
        print("Error: Message text is empty.")
        return

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    headers = {
        "Authorization": f"Bearer {META_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        print("Message sent")
    else:
        print(f"Send failed: {response.text}")



async def send_message_async(user_phone: str, message: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, send_message, user_phone, message)


# async def fetch_media(media_id: str) -> str:
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(
#                 MEDIA_URL.format(media_id=media_id),
#                 headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
#             )
#             if response.status_code == 200:
#                 return response.json().get("url")
#             else:
#                 print(f"Failed to fetch media: {response.text}")
#         except Exception as e:
#             print(f"Exception during media fetch: {e}")
#     return None


# async def handle_image_message(media_id: str, user_phone: str, caption: str):
#     media_url = await fetch_media(media_id)
#     if not media_url:
#         loop = asyncio.get_running_loop()
#         await loop.run_in_executor(None, send_message, user_phone, "Failed to fetch media.")
#         return

#     async with httpx.AsyncClient() as client:
#         headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
#         response = await client.get(media_url, headers=headers)
#         response.raise_for_status()

#         # Convert image to base64
#         image = Image.open(BytesIO(response.content))
#         buffered = BytesIO()
#         image.save(buffered, format="JPEG")  # Save as JPEG
#         image.save("./test.jpeg", format="JPEG")  # Optional save
#         base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

#     await call_llm_api(base64_image, caption, user_phone)


# async def call_llm_api(image_base64: str, caption: str, user_phone: str):
#     try:
#         url = "https://api.together.ai/v1/chat/completions"

#         payload = {
#             "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
#             "messages": [{
#                 "role": "user",
#                 "content": [
#                     {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}},
#                     {"type": "text", "text": caption}
#                 ]
#             }]
#         }

#         headers = {
#             "Authorization": f"Bearer {TOGETHER_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         async with httpx.AsyncClient() as client:
#             response = await client.post(url, json=payload, headers=headers)
#             response_data = response.json()

#             if response.status_code == 200 and "choices" in response_data:
#                 message_content = response_data["choices"][0]["message"]["content"]
#                 if message_content:
#                     loop = asyncio.get_running_loop()
#                     await loop.run_in_executor(None, send_message, user_phone, message_content)
#                 else:
#                     print("Error: Empty message content from LLM API")
#                     await send_message_async(user_phone, "Received empty response from LLM API.")
#             else:
#                 print("Error: Invalid LLM API response", response_data)
#                 await send_message_async(user_phone, "Failed to process image due to an internal server error.")

#     except Exception as e:
#         print("LLM error:", e)
#         await send_message_async(user_phone, "Sorry, something went wrong while processing the image.")


# def llm_reply_to_text(user_input: str, user_phone: str):
#     try:
#         headers = {
#             "Authorization": f"Bearer {TOGETHER_API_KEY}",
#             "Content-Type": "application/json"
#         }

#         json_data = {
#             "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": [{"type": "text", "text": user_input}]
#                 }
#             ]
#         }

#         response = requests.post(
#             "https://api.together.ai/v1/chat/completions",
#             headers=headers,
#             json=json_data
#         )
#         response_data = response.json()

#         if response.status_code == 200 and "choices" in response_data:
#             message_content = response_data["choices"][0]["message"]["content"]
#             if message_content:
#                 send_message(user_phone, message_content)
#             else:
#                 print("Error: Empty message content from LLM API")
#                 send_message(user_phone, "Received empty response from LLM API.")
#         else:
#             print("Error: Invalid LLM API response", response_data)
#             send_message(user_phone, "Sorry, I couldn't understand your request.")

#     except Exception as e:
#         print("LLM error:", e)
#         send_message(user_phone, "Sorry, something went wrong while generating a response.")
################### attempting audio to audio experience free ##########################


# def get_llm_response(user_input: str) -> str:
#     headers = {
#         "Authorization": f"Bearer {TOGETHER_API_KEY}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "model": "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": [{"type": "text", "text": user_input}]
#             }
#         ]
#     }

#     response = requests.post("https://api.together.ai/v1/chat/completions", headers=headers, json=payload)

#     if response.status_code == 200 and "choices" in response.json():
#         return response.json()["choices"][0]["message"]["content"]
#     else:
#         print("LLM error:", response.text)
#         return None

# def text_to_speech(text: str, output_path: str = "reply.mp3") -> str:
#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": "Bearer " + os.getenv("GROQ_API_KEY", ""),
#     }

#     json_data = {
#         "model": "playai-tts",
#         "voice": "Aaliyah-PlayAI",
#         "input": text,
#         "response_format": "mp3"
#     }

#     response = requests.post(
#         "https://api.groq.com/openai/v1/audio/speech",
#         headers=headers,
#         json=json_data
#     )

#     if response.status_code == 200:
#         with open(output_path, "wb") as f:
#             f.write(response.content)
#         return output_path
#     else:
#         print("TTS failed:", response.text)
#         return None

        
async def send_audio_message(to: str, file_path: str):
    url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/media"
    with open(file_path, "rb") as f:
        files = { "file": ("reply.mp3", open(file_path, "rb"), "audio/mpeg")}
        params = {
            "messaging_product": "whatsapp",
            "type": "audio",
            "access_token": ACCESS_TOKEN
        }
        response = requests.post(url, params=params, files=files)

    if response.status_code == 200:
        media_id = response.json().get("id")
        payload = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "audio",
            "audio": {"id": media_id}
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    else:
        print("Audio upload failed:", response.text)






async def llm_reply_to_text_v2(user_input: str, user_phone: str, media_id: str = None,kind: str = None):
    try:
        # print("inside this function")
        headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

        json_data = {
            'user_input': user_input,
            'media_id': media_id,
            'kind': kind
        }
        
        async with httpx.AsyncClient() as client:
          response = await client.post("https://df00-171-60-176-142.ngrok-free.app/llm-response", json=json_data, headers=headers,timeout=60)
          response_data = response.json()
          # print(response_data)
          if response.status_code == 200 and response_data['error'] == None:
              message_content = response_data['response']
              if message_content:
                  loop = asyncio.get_running_loop()
                  await loop.run_in_executor(None, send_message, user_phone, message_content)
              else:
                  print("Error: Empty message content from LLM API")
                  await send_message_async(user_phone, "Received empty response from LLM API.")
          else:
              print("Error: Invalid LLM API response", response_data)
              await send_message_async(user_phone, "Failed to process image due to an internal server error.")

    except Exception as e:
        print("LLM error:", e)
        await send_message_async(user_phone, "Sorry, something went wrong while generating a response.")