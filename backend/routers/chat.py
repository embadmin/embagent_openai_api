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

    # Construct prompt for GPT
    initial_context = f"""
You are a helpful AI assistant named {name} with the following configuration:

• 🎯 Mission: {mission}
• 📘 Expertise: {expertise}
• 💬 Tone / Etiquette: {etiquette}
• 🔗 Reference Links: {links}

Only use this internal knowledge to answer:
{knowledge}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": initial_context},
            {"role": "user", "content": message}
        ],
        temperature=0.7
    )

    return {
        "response": response.choices[0].message.content.strip()
    }