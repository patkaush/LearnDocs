import os

import google.generativeai as genai
import instructor
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

os.environ["GOOGLE_API_KEY"] = "AIzaSyAOAKfxrHtG2aloFnVCZUwZohG2XJrGEM8"


# Step 1: Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.4)
embedder_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")



# Setup API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Create Instructor-wrapped model
client = instructor.from_gemini(
    client=genai.GenerativeModel(model_name="models/gemini-2.0-flash"),
    mode=instructor.Mode.GEMINI_JSON,
)
