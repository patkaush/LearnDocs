

def generate_clean_data_prompt(raw_text):
    prompt = f"""
    You have a block of text. Your job is to:

    1. Organize it into topics.
    2. For each topic, produce an object with exactly two keys:
       • \"topic\": the topic title (string)  
       • \"content\": the related content (string; 2–3 paragraphs concatenated)

    **Return strictly valid JSON**—nothing else. No markdown fences, no comments, no trailing commas, no extra fields.

    **Example output**:
    [
      {{
        "topic": "Overview",
        "content": "Paragraph one text. Paragraph two text."
      }},
      {{
        "topic": "Details",
        "content": "Paragraph one text. Paragraph two text."
      }}
    ]

    Now process this text:

    \"\"\"{raw_text}\"\"\"
    """
    return prompt
def generate_flashcard_prompt(context,query):
    flashcard_prompt = f"""
    You are a Teaching Assistant.

    Generate as many flashcards as make sense based on the following context and question. Do NOT exceed 20 flashcards.


    Return it strictly in this JSON format:
    {{
        "flashcards": [
            {{"Q": "...", "A": "..."}},
            {{"Q": "...", "A": "..."}},
            {{"Q": "...", "A": "..."}}
        ]
    }}

    Context:
    {context}

    Question:
    {query}
    """
    return flashcard_prompt
def generate_mcq_prompt(context,query):
    mcq_prompt = f"""
    You are a helpful Teaching Assistant.

    Based on the following context and user query, generate multiple-choice questions (MCQs).

    Rules:
    - Each MCQ must have 1 correct answer and 3 distractor options.
    - Maximum 20 MCQs.
    - Strict JSON output:
    {{
        "mcqs": [
            {{
                "question": "....",
                "options": [
                    {{"option": "A", "text": "..."}},
                    {{"option": "B", "text": "..."}},
                    {{"option": "C", "text": "..."}},
                    {{"option": "D", "text": "..."}}
                ],
                "correct_option": "A"
            }},
            ...
        ]
    }}

    Context:
    {context}

    Question:
    {query}
    """
    return mcq_prompt
def generate_fib_prompt(context,query):
    fib_prompt = f"""
    You are a helpful Teaching Assistant.

    Based on the following context and user query, generate Fill in the Blanks (FIB) exercises.

    Rules:
    - Maximum 20 sentences.
    - Replace important keywords with blanks (_____) but make sentences readable.
    - Return strictly in JSON format:
    {{
        "fibs": [
            {{
                "sentence_with_blank": "The transformer uses _____.",
                "answer": "self-attention"
            }},
            ...
        ]
    }}

    Context:
    {context}

    Question/Topic:
    {query}
    """
    return fib_prompt
def generate_qa_prompt(context: str, query: str) -> str:
    return f"""
    You are a helpful Teaching Assistant.

    Based on the following context and user query, generate Question and Answer (Q&A) pairs.

    Rules:
    - Maximum 20 Q&A pairs
    - Clear, concise answers
    - Output strictly in JSON format:
    {{
        "qas": [
            {{"question": "...", "answer": "..."}},
            ...
        ]
    }}

    Context:
    {context}

    Topic/Question:
    {query}
    """
