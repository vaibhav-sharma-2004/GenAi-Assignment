import os
import pandas as pd
from google import genai
import json
from dotenv import load_dotenv

load_dotenv()
# ---------------------------------------------------
# STEP 1: Configure Gemini API
# ---------------------------------------------------

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------------------------------
# STEP 2: Read CSV File
# ---------------------------------------------------

df = pd.read_csv("customers.csv")

sample_data = df.head(5).to_dict(orient="records")

# ---------------------------------------------------
# STEP 3: Prompt
# ---------------------------------------------------

prompt = f"""
You are a synthetic data generator.

Below is sample customer data in JSON format:

{json.dumps(sample_data, indent=2)}

Generate 10 more similar realistic customer records.

Rules:
- Maintain same schema
- Keep data realistic
- Do not duplicate existing records
- Return ONLY valid JSON array
"""

# ---------------------------------------------------
# STEP 4: Generate Synthetic Data
# ---------------------------------------------------

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

generated_text = response.text.strip()

# Remove markdown if present
generated_text = generated_text.replace("```json", "").replace("```", "")

synthetic_data = json.loads(generated_text)

# ---------------------------------------------------
# STEP 5: Convert to DataFrame
# ---------------------------------------------------

synthetic_df = pd.DataFrame(synthetic_data)

print("\nGenerated Synthetic Data:")
print(synthetic_df)

# ---------------------------------------------------
# STEP 6: Combine Data
# ---------------------------------------------------

augmented_df = pd.concat([df, synthetic_df], ignore_index=True)

# ---------------------------------------------------
# STEP 7: Save Output
# ---------------------------------------------------

augmented_df.to_csv("augmented_customers.csv", index=False)

print("\nAugmented dataset saved successfully.")