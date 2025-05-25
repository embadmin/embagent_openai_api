from fastapi import APIRouter, Request
from openai import OpenAI

router = APIRouter()
client = OpenAI()

@router.post("/chat")
async def chat_with_agent(request: Request):
    data = await request.json()

    message = data.get("message", "")
    name = data.get("name", "Agent")
    icon = data.get("icon", "default.png")
    mission = data.get("mission", "")
    expertise = data.get("expertise", "")
    etiquette = data.get("etiquette", "")
    links = data.get("links", "")
    knowledge = data.get("knowledge", "")

    # Construct prompt with persistent context
    prompt = f"""
You are a helpful AI assistant named {name} with the following configuration:

• 🎯 Mission: {mission}
• 📘 Expertise: {expertise}
• 💬 Tone / Etiquette: {etiquette}
• 🔗 Reference Links: {links}

Use the internal knowledge below to guide your answers:
{knowledge}

User asked: {message}

Only use the above knowledge when crafting your reply. If the information is not available in the provided context, politely let the user know.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        initial_context = f'''
You are a helpful AI assistant with the following background:

Use Case: {usecase}
Expertise: {expertise}
Tone: {etiquette}
Reference Links: {links}

Only answer questions using this internal knowledge:
{knowledge}

Begin with a friendly tone and always refer to the above context.
''',

        messages = [
            {"role": "system", "content": initial_context},
            {"role": "user", "content": message}
        ],
        temperature=0.7
    )

    return {
        "response": response.choices[0].message.content.strip()
    }