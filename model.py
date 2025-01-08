from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from conversation_chain import CustomConversationChain
from huggingface_hub import login

# Authentication with Hugging Face Hub
# Put your Hugging Face token
login(token='hf_xxxxxxxxxxxxxxxxxxxxxxxx')

# Model and tokenizer configuration
model_id = "Yassinj/Llama-3.1-8B_medical"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token

# Configure quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True
)

# Load the model with quantization
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="auto"
)

# Initialize the custom conversation chain
conversation_chain = CustomConversationChain(model, tokenizer)
