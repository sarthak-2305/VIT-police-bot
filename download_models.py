from transformers import AutoModelForSequenceClassification, AutoTokenizer

# List of models to download and save locally
MODEL_NAMES = {
    "roberta": "cardiffnlp/twitter-roberta-base-hate",
    "berttweet": "cardiffnlp/twitter-roberta-base-sentiment",
    "hatexplain": "Hate-speech-CNERG/dehatebert-mono-english",
    "xlm_roberta": "j-hartmann/emotion-english-distilroberta-base", 
    "hateBERT": "GroNLP/hateBERT", 
    "BERTicelli": "patrickquick/BERTicelli", 
    "toxic-comment": "dougtrajano/toxic-comment-classification"
}

# Download each model and tokenizer to a specific subdirectory
for model_key, model_name in MODEL_NAMES.items():
    print(f"Downloading and caching {model_name} into ./local-models/{model_key}")
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    model.save_pretrained(f"./local-models/{model_key}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(f"./local-models/{model_key}")

print("All models downloaded and saved to subdirectories in local-models.")
