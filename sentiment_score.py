from google.cloud import language_v1

# Initialize the Natural Language API client
client = language_v1.LanguageServiceClient()

def triage_support_ticket(ticket_text):
    # Classify the ticket content
    category, confidence = classify_ticket_content(ticket_text)
    # Analyze the sentiment of the ticket
    sentiment_score, sentiment_magnitude = analyze_ticket_sentiment(ticket_text)
    
    # Determine the priority based on sentiment
    if sentiment_score < -0.5:
        priority = "High"
    elif sentiment_score < 0:
        priority = "Medium"
    else:
        priority = "Low"
		
	return {
        "Ticket Text": ticket_text,
        "Category": category,
        "Confidence": confidence,
        "Sentiment Score": sentiment_score,
        "Sentiment Magnitude": sentiment_magnitude,
        "Priority": priority
    }
		
