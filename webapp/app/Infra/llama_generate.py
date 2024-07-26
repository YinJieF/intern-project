from app.Infra.prompt_gcs import get_prompt
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import time

def process_text(input_text):
    try:
        chat = ChatGroq(
            temperature=0.5, 
            model_name="llama3-8b-8192", 
            groq_api_key="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"
        )
        system = "You are a helpful detective."
        prompt = ChatPromptTemplate.from_messages([
            ("system", system), 
            ("human", "{text}")
        ])
        prompt_text = get_prompt()
        chain = prompt | chat
        input_text = f"{system}\n {prompt_text}: {input_text}"
        result = chain.invoke({"text": input_text})
        print(result.content)
        return result.content
    
    except Exception as e:
        print(f"API failure: {e}")
        return "No data found"