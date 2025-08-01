from escalation import check_escalation

# Simulate message + sentiment history (you can tweak this)
message_history = [
    "I’m really angry with your service.",
    "You haven’t refunded me yet!",
    "This is the worst experience ever"
]

sentiment_history = [
    "neutral",
    "very negative",
    "very negative"
]

# Run the check
check_escalation(message_history, sentiment_history)
