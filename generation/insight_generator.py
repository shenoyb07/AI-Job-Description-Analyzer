from transformers import pipeline
import torch

class InsightGenerator:
    def __init__(self, model_name="gpt2"):
        # Detect device
        self.device = 0 if torch.cuda.is_available() else -1
        try:
            # Initialize the pipeline
            self.generator = pipeline("text-generation", model=model_name, device=self.device)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.generator = None

    def generate_insight(self, job_description, skills, experience_level):
        """
        Generates a concise professional summary using GPT-2.
        """
        if not self.generator:
            return "AI Insight Generation is currently unavailable. Please review skills manually."

        tech_skills = ", ".join(skills.get("technical_skills", []))
        soft_skills = ", ".join(skills.get("soft_skills", []))
        
        # Construct the prompt
        prompt = (
            f"You are an AI assistant specialized in analyzing job descriptions. "
            f"Analyze the following {experience_level} role requiring skills: {tech_skills} and {soft_skills}. "
            f"Job description: {job_description[:500]}... "
            f"\n\nProfessional Summary:"
        )

        try:
            # Generate response
            response = self.generator(
                prompt, 
                max_length=150, 
                num_return_sequences=1, 
                temperature=0.7,
                truncation=True,
                pad_token_id=50256 # GPT-2 specific pad token
            )
            
            # Extract only the generated text (remove the prompt)
            generated_text = response[0]['generated_text']
            insight = generated_text[len(prompt):].strip()
            
            # Fallback if generation is too short or empty
            if len(insight) < 10:
                insight = (
                    f"This is a {experience_level} position focused on {tech_skills}. "
                    f"Ideal candidates should have strong {soft_skills} and relevant industry experience."
                )
            
            return insight
        except Exception as e:
            return f"Error generating insight: {str(e)}"

# Singleton-like instance to be used in st.cache_resource
_generator_instance = None

def get_generator():
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = InsightGenerator()
    return _generator_instance
