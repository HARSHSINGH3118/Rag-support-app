from transformers import pipeline

# ✅ Load sentiment analysis pipeline (once at startup)
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(message: str) -> str:
    result = sentiment_analyzer(message)[0]
    label = result['label']
    score = result['score']

    # Normalize sentiment categories
    if label == "NEGATIVE" and score > 0.75:
        return "very negative"
    elif label == "NEGATIVE":
        return "negative"
    elif label == "POSITIVE" and score > 0.75:
        return "very positive"
    elif label == "POSITIVE":
        return "positive"
    else:
        return "neutral"
