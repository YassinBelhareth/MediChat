from transformers import GenerationConfig

def generate_response(user_input, model, tokenizer):
    """
    Generates a response using a model and tokenizer.
    """
    # Create the prompt
    prompt = formatted_prompt(user_input)

    # Prepare inputs for the model
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda')

    # Generation configuration
    generation_config = GenerationConfig(
        penalty_alpha=0.6,
        do_sample=True,
        top_k=5,
        temperature=0.5,
        repetition_penalty=1.2,
        max_new_tokens=60,
        pad_token_id=tokenizer.eos_token_id
    )

    # Generate the response
    outputs = model.generate(**inputs, generation_config=generation_config)

    # Decode the response and extract only the relevant content
    theresponse = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return extract_answer(theresponse)

def formatted_prompt(question) -> str:
    return f"<|im_start|>user\n{question}<|im_end|>\n<|im_start|>answer:"

def extract_answer(model_output: str) -> str:
    """
    Extracts only the relevant answer from the model's output.
    """
    start_marker = "<|im_start|>answer:"
    if start_marker in model_output:
        answer_start = model_output.find(start_marker) + len(start_marker)
        raw_answer = model_output[answer_start:].strip()
        end_marker = "<|im_end|>"
        if end_marker in raw_answer:
            raw_answer = raw_answer.split(end_marker)[0].strip()
        return raw_answer
    else:
        return "Error: Unexpected output format or response not found."
