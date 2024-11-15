import torch
from model_loader import models, tokenizers, device

# Define a function to get predictions from each model
def get_model_predictions(text):
    print("Device:", device)
    print("Available models:", models.keys())  # Check if models are present

    results = {}

    for model_name, model in models.items():
        tokenizer = tokenizers[model_name]
        
        # Tokenize input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to("cpu")  # Use CPU for testing
        print(f"Tokenized inputs for {model_name}: {inputs}")  # Debug: Tokenized input check
        
        # Get model output
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits  # Raw output before softmax
            print(f"{model_name} raw logits: {logits}")  # Debug: Log raw logits
            
            probabilities = torch.softmax(logits, dim=1)
            print(f"{model_name} probabilities: {probabilities}")  # Debug: Log probabilities
            
            predicted_class = torch.argmax(probabilities, dim=1).item()
            confidence = probabilities[0][predicted_class].item()
        
        # Store the prediction and confidence for each model
        results[model_name] = {"label": predicted_class, "confidence": confidence}
        print(f"{model_name} predicted class: {predicted_class}, confidence: {confidence:.2f}")  # Debug: Prediction result

    return results


def aggregate_predictions(predictions, threshold=0.3):  # Lower threshold to 0.3
    hate_votes = 0
    non_hate_votes = 0
    
    for model_name, result in predictions.items():
        label = result["label"]
        confidence = result["confidence"]
        
        # Apply confidence threshold
        if confidence >= threshold:
            if label == 1:
                hate_votes += 1
            else:
                non_hate_votes += 1
        
        # Log each model’s contribution to the vote
        print(f"{model_name} voted {'Hate' if label == 1 else 'Safe'} with confidence {confidence:.2f}")

    # Decision based on majority voting
    final_label = 1 if hate_votes >= non_hate_votes else 0
    
    # Log the final decision
    print(f"Final Decision - Hate Votes: {hate_votes}, Non-Hate Votes: {non_hate_votes}, Label: {'Hate' if final_label == 1 else 'Safe'}")
    
    return final_label, {"hate_votes": hate_votes, "non_hate_votes": non_hate_votes}


if __name__ == "__main__":
    test_text = "This is a test message with potential hate speech."
    predictions = get_model_predictions(test_text)
    print("Predictions:", predictions)

