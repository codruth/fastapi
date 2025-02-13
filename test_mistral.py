import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load the model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")  # Or 'Mistral-7B-Instruct-v0.3'
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3",
    device_map="auto",
    torch_dtype="auto"
)

# Check if CUDA (GPU) is available
print("CUDA available1:", torch.cuda.is_available())
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Send a test prompt
prompt = "which is the france capital"
inputs = tokenizer(prompt, return_tensors="pt").to(device)
outputs = model.generate(inputs.input_ids, max_length=50)

# Print the generated response
print("Generated Text:")
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
