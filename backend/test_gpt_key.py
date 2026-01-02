import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("Checking available models...")
    models = client.models.list()
    

    gpt_models = [m.id for m in models.data if "gpt" in m.id]
    
    print(f"Total available models: {len(models.data)}")
    print("\n--- Available GPT models ---")
    for model_id in sorted(gpt_models):
        print(model_id)

except Exception as e:
    print(f"\nError checking: {e}")