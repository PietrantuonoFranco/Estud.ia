def format_generated_text(text: str) -> str:
    """
    Helper function to clean markdown code blocks from LLM generation.
    """
    generation_text = text.strip()
    
    if generation_text.startswith("```json"):
        generation_text = generation_text[7:]  # Remove ```json
    
    if generation_text.startswith("```"):
        generation_text = generation_text[3:]  # Remove ```
    
    if generation_text.endswith("```"):
        generation_text = generation_text[:-3]  # Remove ```
    
    generation_text = generation_text.strip()
    
    return generation_text