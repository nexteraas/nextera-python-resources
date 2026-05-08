from transformers import AutoModel, AutoTokenizer, AutoModelForSequenceClassification

# Path to the folder containing model.safetensors and config.json
model_path = "C:/Nextera/div/ab_roberta/EXPLORER/curated/results"

# Load model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path, use_safetensors=True)

print('w')



from transformers import pipeline

# Assuming 'model' and 'tokenizer' are already loaded in your environment
pipe = pipeline(
    task="text-classification",
    model=model,
    tokenizer=tokenizer
)

# Perform inference
result = pipe("TQSPSSLSASVGDRVTITCQASQDISNYLNWYQQKPGKAPKLLIYDASNLETGVPSRFSGSGSGTDFTFTISSLQPEDIATYYCLQHNSYLPTFGGGTKVEIKQLVQSGAEVKKPGSSVKVSCKASGGTFSSYAISWVRQAPGQGLEWMGGIIPIFGTANYAQKFQGRVTITADESTSTAYMELSSLRSEDTAVYYCARTIGHDLPDAFDIWGQGTMVTVSS")
print(result)