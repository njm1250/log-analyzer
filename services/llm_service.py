import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
  ]
)

response = chat_session.send_message("Hi There")
print(response.text)

async def call_gemini_api(error_log: dict) -> str:
    try:
        prompt = f"Provide a suggested solution for this error: {error_log['message']}"
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"LLM API Error: {str(e)}"
