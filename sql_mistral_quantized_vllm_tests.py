from vllm import LLM

# For generative models (task=generate) only
llm = LLM(model="google/gemma-2b")  # Name or path of your model
output = llm.generate("Hello, my name is")
print(output)
