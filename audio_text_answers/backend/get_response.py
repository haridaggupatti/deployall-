from fastapi import APIRouter, HTTPException
import openai
import asyncio
from models import *
import logging

router = APIRouter(prefix="/api")

# Set your API key
api_key = "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"
openai.api_key = api_key

# Initialize a dictionary to store conversation history per user
user_conversation_history = {}

# Set up logging
logger = logging.getLogger(__name__)

@router.post("/get_answer", tags=["Voice"])
async def generate_humanlike_response(request: prompt_text):
    user_id = request.user_id
    user_prompt = request.prompt_text

    if user_id not in user_conversation_history:
        user_conversation_history[user_id] = []

    # Record the user's prompt in the conversation history
    user_conversation_history[user_id].append({"role": "user", "content": user_prompt})

    # Limit the conversation history to the last 5 interactions to manage context and costs
    limited_history = user_conversation_history[user_id][-5:]

    # Adjusted prompt to simulate a dynamic, interactive job interview
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
    ] + limited_history

    prompt = f"""{request.resume_prompt} {request.resume_context}
    
    I'm the recruiter asking questions to assess your skills and expertise. Respond to any technical or non-technical question in normal Indian slang English in a concise manner, and conversational manner, as if we're speaking face-to-face, showcasing your achievements, skills, and problem-solving abilities based on question. Respond without using any large vocabulary, complicated words, and complicated technologies in the speech, and give the answer short and concise.

    Answer my questions as you are a human: {request.prompt_text}"""

    try:
        response = await asyncio.to_thread(
            openai.ChatCompletion.create,
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Retrieve the generated response and clean it up
        response_content = response['choices'][0]['message']['content'].strip()

        # Log the assistant's response to maintain conversation context
        user_conversation_history[user_id].append({"role": "assistant", "content": response_content})

        return {"response": response_content}

   
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
