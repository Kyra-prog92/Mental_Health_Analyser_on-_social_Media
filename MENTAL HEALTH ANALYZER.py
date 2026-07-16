import re

# Define negative and positive word lists
negative_word_list = ["sad", "depressed", "anxious", "stressed"]
positive_word_list = ["happy", "joyful", "relaxed", "calm"]

def analyze_mental_health(post_data):
    # Calculate post metrics
    post_length = len(re.findall(r'\b\w+\b', post_data["text"]))  # number of words
    engagement_rate = (post_data["likes"] + post_data["comments"]) / post_data["views"] if post_data["views"] > 0 else 0

    # Determine sentiment analysis
    if post_data["sentiment"] == "Positive":
        sentiment = "Low Risk"
    elif post_data["sentiment"] == "Negative":
        sentiment = "High Risk"
    else:
        sentiment = "Moderate Risk"

    # Analyze language patterns
    negative_word_count = 0
    positive_word_count = 0
    words = re.findall(r'\b\w+\b', post_data["text"].lower())
    for word in words:
        if word in negative_word_list:
            negative_word_count += 1
        elif word in positive_word_list:
            positive_word_count += 1

    # Avoid division by zero if post_length is 0
    word_ratio = (negative_word_count / post_length) if post_length > 0 else 0

    # Score weights
    sentiment_weight = {"High Risk": 1, "Moderate Risk": 0.5, "Low Risk": 0}

    # Calculate mental health risk score
    risk_score = (word_ratio * 0.5) + (engagement_rate * 0.3) + (sentiment_weight[sentiment] * 0.2)

    # Determine mental health risk level
    if risk_score > 0.7:
        risk_level = "High Risk"
    elif risk_score > 0.4:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    return {
        "sentiment": sentiment,
        "risk_level": risk_level,
        "risk_score": round(risk_score, 2)
    }

def determine_sentiment(text):
    negative_word_count = 0
    positive_word_count = 0
    words = re.findall(r'\b\w+\b', text.lower())
    for word in words:
        if word in negative_word_list:
            negative_word_count += 1
        elif word in positive_word_list:
            positive_word_count += 1
    if negative_word_count > positive_word_count:
        return "Negative"
    elif positive_word_count > negative_word_count:
        return "Positive"
    else:
        return "Neutral"

def main():
    post_text = input("Enter post text: ")
    likes = int(input("Enter likes: "))
    comments = int(input("Enter comments: "))
    views = int(input("Enter views: "))
    sentiment = determine_sentiment(post_text)
    post_data = {
        "text": post_text,
        "likes": likes,
        "comments": comments,
        "views": views,
        "sentiment": sentiment
    }
    mental_health_insights = analyze_mental_health(post_data)
    print("\nMental Health Insights:")
    print(f"Sentiment : {mental_health_insights['sentiment']}")
    print(f"Risk Level : {mental_health_insights['risk_level']}")
    print(f"Risk Score : {mental_health_insights['risk_score']}")

if __name__ == "__main__":
    main()
