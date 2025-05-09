# Install dependencies first if you haven't:
# pip install openai instructor pydantic

from openai import OpenAI
import instructor
from pydantic import BaseModel, Field
from typing import List

# Step 1: Define your Pydantic model
class Character(BaseModel):
    name: str
    age: int
    facts: List[str] = Field(..., description="List of interesting facts about the character")

# Step 2: Create OpenAI client for Ollama
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",  # Ollama exposes OpenAI compatible API here
        api_key="ollama"  # dummy value, Ollama ignores this
    ),
    mode=instructor.Mode.JSON  # Force JSON structured outputs
)

# Step 3: Call the LLM
response = client.chat.completions.create(
    model="mistral",
    messages=[
        {"role": "user", "content": "Tell me about Harry Potter"}
    ],
    response_model=Character
)

# Step 4: Print the structured response
print(response.model_dump_json(indent=2))
