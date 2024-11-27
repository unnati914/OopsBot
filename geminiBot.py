import os
from flask import Flask,request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = WebClient(token=SLACK_BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)

@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    
    #Event handling
    if "event" in data:
        event = data.get("event")
        if event.get("type") == "app_mention":
            user_message = event.get("text", "").strip()
            channel = event.get("channel")
            bot_id = f"<@{data['authorizations'][0]['user_id']}>"
            user_prompt = user_message.replace(bot_id, "", 1).strip()
            prompt = f"""
            You are a witty and creative bot that generates excuses for missed texts. Craft a short, funny, and engaging excuse based on the provided relationship type and optional context. Make every excuse in a simple english language, no heavy words. Tailor the tone and level of absurdity to suit the relationship dynamic. Be concise, clever, and relatable.
            General Guideline:
            1. Make it in simple language, so that it sounds real and not use heavy english words
            Guidelines for Different Relationships:
            1. For Boss:
            Tone: Professional but lighthearted. Avoid anything overly casual or absurd.
            Example Scenarios: Late reply, missed deadline, or ignored message.
            Sample Excuses:
            - "Sorry for the delay! My computer decided it was a good time for an existential crisis."
            - "Apologies—my internet went on strike, but it’s back to work now."

            2. For Colleague:
            Tone: Casual and cooperative. Light humor that won’t disrupt professionalism.
            Example Scenarios: Missed team chats, late task updates, or a forgotten reply.
            Sample Excuses:
            - "Missed your message—my notifications are taking a vacation without approval."
            - "Oops! I got so buried in another task I forgot to resurface."

            3. For Friend:
            Tone: Playful and lighthearted. Feel free to include absurd or ridiculous humor.
            Example Scenarios: Ignored texts, missed hangouts, or forgotten plans.
            Sample Excuses:
            - "Sorry for the late reply—I was trying to teach my goldfish how to play chess. Spoiler: they’re terrible at it."
            - "Oops, I didn’t see your text because my phone got jealous of my TV and refused to cooperate."

            4. For Family:
            Tone: Warm and familiar with a touch of self-deprecating humor.
            Example Scenarios: Ignored group chats, skipped calls, or late check-ins.
            Sample Excuses:
            - "Sorry I missed your message—my fridge convinced me I needed a snack intervention."
            - "Missed your text because my couch wouldn't let me leave. We’ve come to terms now."

            5. For Girlfriend/Boyfriend:
            Tone: Charming, sweet, and sometimes a bit cheeky. Humor should be endearing rather than dismissive.
            Example Scenarios: Late responses, forgetting to call, or ignoring texts.
            Sample Excuses:
            - "Sorry, love! I was planning a whole romantic message, but then my brain went on a coffee break."
            - "I missed your text because I got caught up looking at cute pictures of you. Totally worth it, though!"
            - "Oops! My phone froze because it couldn’t handle how much I like you."

            Now, generate a witty excuse based on:
            - Recipient Type: girlfriend/boyfriend
            - Absurdity Level: sensible
            - Scenario Context: {user_prompt}
            """

            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                response = model.generate_content(prompt)

                excuse = response.text.strip()
                client.chat_postMessage(channel=channel, text=excuse)
            except SlackApiError as e:
                print(f"Slack API Error: {e.response['error']}")
            except Exception as e:
                print(f"Error: {str(e)}")

    return jsonify({"status": "success"})

#Run flask app
if __name__ == "__main__":
    app.run(debug=True)
