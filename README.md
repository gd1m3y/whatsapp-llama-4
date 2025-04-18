# WhatsApp AI Webhook Service

This project provides a FastAPI-based backend for handling WhatsApp messages, integrating with LLMs (Large Language Models) and text-to-speech (TTS) services. It can process text, image, and audio messages, generate AI responses, and reply with text or audio.

## Features
- **WhatsApp Webhook Handler**: Receives and processes WhatsApp messages (text, image, audio).
- **LLM Integration**: Uses LLMs to generate intelligent responses based on user input.
- **Image & Audio Handling**: Supports image captioning and audio transcription.
- **Text-to-Speech**: Converts AI-generated text responses to audio (mp3) and returns them to users.
- **API Endpoints**: Exposes endpoints for LLM response and TTS conversion.

## API Endpoints

### `/llm-response` (POST)
Handles user input and returns an LLM-generated response. If the input is audio, it returns an audio file (mp3).

**Request Body:**
```
{
  "user_input": "<text>",
  "media_id": "<optional media id>",
  "kind": "audio" | "image",
  "to": "<optional recipient>"
}
```

**Response:**
- For text/image: `{ "response": "<llm reply>", "error": null }`
- For audio: Returns an mp3 file with `audio/mpeg` content type.

### `/text-to-speech` (POST) *(Commented in code)*
Converts text to speech and returns the mp3 file path.

**Request Body:**
```
{
  "text": "<text>",
  "output_path": "<optional output path>"
}
```

**Response:**
- `{ "file_path": "reply.mp3", "error": null }`

## Key Files
- `aiservices.py`: FastAPI endpoints and data models.
- `service.py`: Core logic for LLM, TTS, image/audio handling, and WhatsApp integration.
- `main.py`: (Optional) May contain webhook handlers and app entrypoint.
- `requirements.txt`: Python dependencies.

## Setup & Running
1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables** in `.env` (see below).
4. **Run the FastAPI server**:
   ```bash
   uvicorn aiservices:app --reload
   ```
5. **(Optional)**: For WhatsApp webhook, run `main.py` if needed:
   ```bash
   uvicorn main:app --reload
   ```

## Environment Variables (`.env`)
Set the following variables in your `.env` file:
- `TOGETHER_API_KEY`  
- `GROQ_API_KEY`  
- `META_ACCESS_TOKEN`  
- `PHONE_NUMBER_ID`  
- `WHATSAPP_API_URL`  
- `ACCESS_TOKEN`  
- `AGENT_URL`  

## Dependencies
See `requirements.txt` for all dependencies. Key packages:
- fastapi
- uvicorn
- pydantic
- pillow
- requests
- httpx
- python-dotenv
- together, groq (for LLM/TTS)

## Notes
- Audio responses are returned as mp3 files and are playable/downloadable in Swagger UI.
- Make sure your API keys and WhatsApp credentials are valid.
- The codebase is modular: core logic is in `service.py`, API in `aiservices.py`.

---

Feel free to extend the API or integrate with your own WhatsApp/LLM provider as needed.
