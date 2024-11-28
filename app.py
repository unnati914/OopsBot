import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key is None:
    st.error("API key not found. Please set the GEMINI_API_KEY environment variable.")
else:
    genai.configure(api_key=api_key)
    st.title("OOPS Bot 🤖")
    st.subheader("Generate witty and tailored excuses for missed texts!")

    recipient_type = st.selectbox(
        "Who is the excuse for?",
        ["Boss", "Colleague", "Friend", "Family", "Girlfriend/Boyfriend"]
    )

    absurdity_level = st.radio(
        "Choose the level of absurdity:",
        ["Believable", "Ridiculous"]
    )

    scenario_context = st.text_input(
        "Optional: Describe the situation briefly (e.g., late reply, missed deadline)",
        ""
    )

    if st.button("Generate Excuse"):
        prompt = f"""
        You are a witty and creative bot that generates excuses for missed texts. Craft a short, funny, and engaging excuse based on the provided relationship type and optional context. Make every excuse in a simple english language, no heavy words. Tailor the tone and level of absurdity to suit the relationship dynamic. Be concise, clever, and relatable.
        The excuses can be in Hinglish, try not to use heavy english words, and excuses should be realistic. 
        Understand the user sentiment, and understand each situation
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
        - Recipient Type: {recipient_type}
        - Absurdity Level: {absurdity_level}
        - Scenario Context: {scenario_context or "None provided"}
        """

        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            excuse = response.text.strip()
            st.success("Here's your excuse:")
            st.write(f"💡 *{excuse}*")
        except Exception as e:
            st.error("An error occurred while generating the excuse.")
            st.write(e)

    st.markdown("---")
    st.markdown("🤔 Need a quick excuse for any situation? Let **Excuse Maker Bot** lighten the load!")
