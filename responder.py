from transformers import pipeline

# Use a better instruction-following model
generator = pipeline(
    "text2text-generation",
    model="declare-lab/flan-alpaca-base",
    device=-1  # use CPU; change to device=0 if using GPU
)

def generate_empathetic_reply(user_query: str, context: str, sentiment: str) -> str:
    """
    Generates a helpful and empathetic customer support reply using Hugging Face model.
    The response tone is adjusted based on detected sentiment.
    """

    tone_instruction = ""

    if "negative" in sentiment:
        tone_instruction = "Start with an apology and provide a reassuring and helpful response."
    elif "positive" in sentiment:
        tone_instruction = "Be cheerful and acknowledge their satisfaction while offering help."
    else:
        tone_instruction = "Be polite, concise, and helpful."

    # Build a clear instruction-style prompt
    prompt = f"""
Instruction: {tone_instruction}
Customer Complaint: {user_query}
Help Context: {context}
Response:
""".strip()

    try:
        result = generator(prompt, max_length=256, do_sample=False)
        response = result[0]['generated_text'].strip()

        # Remove placeholder names like [Your Name]
        for placeholder in ["[Your Name]", "[Your name]", "Your Name", "your name"]:
            response = response.replace(placeholder, "Huddle Support Team")

        return response
    except Exception as e:
        return f"(Error generating response: {e})"
