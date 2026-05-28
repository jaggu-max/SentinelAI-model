
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# FASTAPI APP
app = FastAPI()

# CORS SETTINGS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LM STUDIO CONNECTION
client = OpenAI(
    base_url="http://127.0.0.1:1234/v1",
    api_key="lm-studio"
)

# REQUEST MODEL
class ChatRequest(BaseModel):
    message: str

# HOME ROUTE
@app.get("/")
def home():
    return {
        "message": "AI Backend Running"
    }

# CHAT ROUTE
@app.post("/chat")
def chat(request: ChatRequest):

    try:

        # AI RESPONSE
        response = client.chat.completions.create(

            # YOUR QWEN MODEL
            model="qwen2.5-7b-instruct-1m",

            messages=[

                {
                    "role": "system",
                    "content": """
                    You are a smart AI assistant like ChatGPT.

                    Rules:
                    - Give short, clear, human-like answers.
                    - Avoid long textbook explanations.
                    - Answer naturally and directly.
                    - Keep responses concise unless user asks for detail.
                    - Never show thinking process.
                    - Never show analysis.
                    - Behave like modern ChatGPT.
                    """
                },

                {
                    "role": "user",
                    "content": request.message
                }
            ],

            temperature=0.5,

            max_tokens=120
        )

        # FINAL REPLY
        reply = response.choices[0].message.content

        # SAFETY FALLBACK
        if not reply or reply.strip() == "":
            reply = "Sorry, I couldn't generate a response."

        return {
            "reply": reply
        }

    except Exception as e:

        return {
            "reply": f"Backend Error: {str(e)}"
        }

