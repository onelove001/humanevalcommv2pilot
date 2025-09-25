import os
import openai


OPENAI_API_KEY = ""
model = "gpt-4o-mini"
openai.api_key = os.getenv(OPENAI_API_KEY)

client = openai.OpenAI()

def call_llm(prompt, model=model):
    """
    Call LLM with a given prompt and Returns raw string response.
    """
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
            # returns the error as a string so pipeline doesn't break
            return f"LLM_ERROR: {str(e)}"
    


