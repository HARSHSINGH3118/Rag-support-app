from retriever import build_vector_db, retrieve_context
from sentiment import analyze_sentiment
from responder import generate_empathetic_reply

# Step 1: Load data into ChromaDB
build_vector_db()

# Step 2: Ask Loop
while True:
    query = input("Ask something: ")
    results = retrieve_context(query)

    print("\nTop Relevant Chunks:\n")
    for i, doc in enumerate(results):
        print(f"{i+1}. {doc}\n")

    # Step 3: Analyze sentiment
    sentiment = analyze_sentiment(query)
    print(f"Detected Sentiment: {sentiment}")

    # Step 4: Generate AI response
    ai_reply = generate_empathetic_reply(query, "\n".join(results), sentiment)
    print(f"\n🤖 AI Response: {ai_reply}\n")
