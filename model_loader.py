from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Define model paths
MODEL_NAMES = {
    # "roberta": "./local-models/roberta",
    # "berttweet": "./local-models/berttweet",
    "hatexplain": "./local-models/hatexplain", 
    "BERTicelli": "./local-models/BERTicelli"
    # "toxic-comment": "./local-models/toxic-comment"
    # "hateBERT": "./local-models/hateBERT"
    # "xlm_roberta": "./local-models/xlm_roberta"
}

models = {}
tokenizers = {}

# Use CPU
device = torch.device("cpu")

def load_models():
    for name, model_path in MODEL_NAMES.items():
        print(f"Attempting to load model and tokenizer for {name} from path: {model_path}")
        try:
            # Load model and tokenizer
            model = AutoModelForSequenceClassification.from_pretrained(model_path)
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            
            # Move model to device
            model.to(device)
            
            # Store model and tokenizer
            models[name] = model
            tokenizers[name] = tokenizer
            print(f"Successfully loaded {name}")
        
        except Exception as e:
            print(f"Error loading model {name} from {model_path}: {e}")

    # Final loaded models check
    print("Loaded models:", models.keys())
    print("Loaded tokenizers:", tokenizers.keys())
    return models, tokenizers, device


load_models()