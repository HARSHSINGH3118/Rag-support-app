from transformers import pipeline

# Load the FLAN-T5 model
generator = pipeline("text2text-generation", model="google/flan-t5-base", max_new_tokens=150)

def generate_empathetic_reply(query, context, sentiment):
    prompt = (
        f"You are a helpful and empathetic customer support assistant.\n"
        f"Customer message (sentiment: {sentiment}): {query}\n"
        f"Relevant help articles:\n{context}\n\n"
        f"Generate a friendly, understanding, and helpful response:"
    )
    response = generator(prompt)
    return response[0]['generated_text']
