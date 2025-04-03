import google.generativeai as genai
from typing import Optional


class GeminiTextGenerator:
    def __init__(self, api_key: str, system_instructions: Optional[str] = None):
        """Initialize Gemini API connection
        
        Args:
            api_key (str): Google API key for Gemini
        """
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite',system_instruction=system_instructions)  
    
    def generate_text(self, prompt: str, max_tokens: Optional[int] = None) -> str:
        """Generate text using Gemini API
        
        Args:
            prompt (str): Input prompt for text generation
            max_tokens (Optional[int]): Maximum number of tokens to generate
            
        Returns:
            str: Generated text response
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    'max_output_tokens': max_tokens
                } if max_tokens else None
            )
            return response.text
        except Exception as e:
            raise Exception(f"Error generating text: {str(e)}")
    
    def set_api_key(self, new_api_key: str) -> None:
        """Update the API key
        
        Args:
            new_api_key (str): New Google API key
        """
        self.api_key = new_api_key
        genai.configure(api_key=self.api_key)
