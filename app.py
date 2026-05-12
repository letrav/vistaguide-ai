from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

GUIDE_KNOWLEDGE = """
You are VistaGuide, a local Rehoboth Beach concierge.

You ONLY recommend places in Rehoboth, Lewes, or Dewey Beach.

Use these known locations first:
- Breakfast: Egg, Sunny Bay Cafe, Cafe Papillon, Goolees Grille
- Brunch: Blue Moon, Cultured Pearl, Victorias Restaurant, Summerhouse
- Breweries: Dogfish Head, Dewey Beer, Crooked Hammock, Big Oyster, Thompson Island, Revelation, Lewes Brewing, First State
- Restaurants: Grotto Pizza, Arenas Deli, Big Fish Grill, Bethany Blues
- Attractions: Funland, Jungle Jims, Midway Speedway, Bandstand concerts
- Shopping: Tanger Outlets, Walmart, Boardwalk shops
- Essentials: CVS, Walgreens, Giant

Rules:

- You are a hyper-local Rehoboth Beach concierge
- Focus on Rehoboth Beach first, then Dewey Beach and Lewes
- Prefer recommendations from this guide when available
- You may answer broader local questions not covered in the guide
- When suggesting places not included in the guide, avoid inventing exact addresses, phone numbers, or hours unless certain
- Never make up fake businesses
- Keep answers short, practical, and conversational
- Sound like a helpful local concierge
- Prioritize useful recommendations over generic AI responses

Example:
User: where to buy whiskey
Answer: Try nearby liquor stores like Atlantic Liquors or Bin 66 on Coastal Highway.
User: best vet
Answer: For veterinary care near Rehoboth Beach, try checking local options like Rehoboth Beach Animal Hospital or nearby Lewes veterinary clinics. Calling ahead is always a good idea for current hours and emergency availability.
User: where can I buy fishing bait
Answer: There are several bait and tackle shops near Rehoboth and Lewes. Lewes is usually your best bet for serious fishing supplies and live bait.
User: where can I get propane
Answer: Most grocery stores, hardware stores, and gas stations around Rehoboth and Lewes offer propane tank exchange services.
"""
HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Ask VistaGuide</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 520px;
      margin: 30px auto;
      padding: 20px;
      background: #f7f7f7;
    }
    .card {
      background: white;
      border-radius: 18px;
      padding: 20px;
      box-shadow: 0 4px 16px rgba(0,0,0,.08);
    }
    input {
  width: 100%;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #ccc;
  box-sizing: border-box;
  font-size: 16px;
}
    button {
  width: 100%;
  padding: 14px;
  margin-top: 10px;
  border: none;
  border-radius: 10px;
  background: #1f6f8b;
  color: white;
  font-size: 16px;
  cursor: pointer;
  box-sizing: border-box;
}
.subtitle {
  color: #666;
  margin-top: -10px;
  margin-bottom: 25px;
}
.helper {
  color: #777;
  font-size: 13px;
  line-height: 1.4;
  margin-top: -10px;
  margin-bottom: 20px;
}
.suggestions {
  margin-top: 15px;
  margin-bottom: 18px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  align-items: center;
}
.suggestion-btn {
  width: auto !important;
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  background: #f4f7f8 !important;
  color: #1f6f8b !important;
  border: 1px solid #d7e3e8 !important;
  padding: 9px 14px !important;
  border-radius: 999px !important;
  cursor: pointer;
  font-size: 13px !important;
  line-height: 1.2;
  margin-top: 0 !important;
  transition: all 0.2s ease;
}
.suggestion-btn:hover {
  background: #163a4a !important;
  color: white !important;
  border-color: #163a4a !important;
}
    #answer {
      margin-top: 15px;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>Ask VistaGuide</h1>
<p class="subtitle">Scan Once. Explore Freely.</p>
    <p class="helper">Ask about food, parking, beach rules, shopping, emergencies, nightlife, and more.</p>
    <input id="question" placeholder="Ask your concierge..." />
    <button onclick="ask()">Ask</button>
    <div class="suggestions">
  <button class="suggestion-btn" onclick="quickAsk('Best breakfast near the beach')">Breakfast</button>

  <button class="suggestion-btn" onclick="quickAsk('Best breweries in Rehoboth Beach')">Breweries</button>

  <button class="suggestion-btn" onclick="quickAsk('Can I bring my dog on the beach?')">Beach Rules</button>

  <button class="suggestion-btn" onclick="quickAsk('Best happy hour nearby')">Happy Hour</button>
</div>
    <div id="answer"></div>
    <div id="followups"></div>
  </div>
<script>
async function ask() {
  const q = document.getElementById("question").value;
  const answer = document.getElementById("answer");
  answer.innerText = "Thinking...";

  const res = await fetch("/ask", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({question: q})
  });

  const data = await res.json();
  answer.innerText = data.answer;
}
async function quickAsk(text) {
  document.getElementById("question").value = text;
  await ask();
}

</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    question = request.json.get("question", "")

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"{GUIDE_KNOWLEDGE}\n\nGuest question: {question}"
        )

        answer = response.output_text

    except Exception as e:
        print("ERROR:", e)
        answer = "Sorry—something went wrong. Please try again."

    return jsonify({
        "answer": answer
    })

if __name__ == "__main__":
    app.run(debug=True)

