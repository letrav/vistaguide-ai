from openai import OpenAI
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

print("VistaGuide Concierge is ready!")

while True:
    user_input = input("\nAsk a question: ")

    if user_input.lower() in ["exit", "quit"]:
        break

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
You are VistaGuide, a local Rehoboth Beach concierge.

Use this knowledge:
- Best breweries: Dogfish Head, Dewey Beer, Crooked Hammock
- Breakfast: Egg, Sunny Bay Café
- Happy hour: Henlopen Oyster House, Purple Parrot
- Beach rules: no dogs in summer, no smoking, no tents

Be helpful, short, and sound like a local.

User: {user_input}
"""
    )

    print("\nAnswer:", response.output[0].content[0].text)