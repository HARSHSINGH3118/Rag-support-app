def check_escalation(message_history: list[str], sentiment_history: list[str]) -> bool:
    """
    Returns True if the user appears frustrated or angry based on recent sentiment or keywords.
    """
    negative_count = sum(1 for s in sentiment_history[-3:] if "negative" in s)

    # Check for repeated negativity
    if negative_count >= 2:
        return True

    # Trigger escalation based on keywords
    escalation_keywords = ["angry", "cancel", "complain", "worst", "useless", "frustrated", "refund"]
    last_message = message_history[-1].lower()

    if any(word in last_message for word in escalation_keywords):
        return True

    return False
