import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api_key,
    model="openai/gpt-oss-20b",
    temperature=0.7,
    max_tokens=1000
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         """You are a certified diet specialist.
Always respond in this structured format:

1. Summary
2. Key Recommendations (bullet points)
3. Sample Meal Plan (if relevant)
4. Warnings or Medical Disclaimer (if necessary)

After completing the response, always end with:
"Would you like this plan customized based on your age, weight, or medical history?"

Keep answers practical and evidence-based.
         """
        ),
        ("placeholder", "{history}"),
        ("user", "{question}")
    ]
)

chain = prompt | llm
