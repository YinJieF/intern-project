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
        system = "You are a helpful assistant."
        prompt = ChatPromptTemplate.from_messages([
            ("system", system), 
            ("human", "{text}")
        ])

        chain = prompt | chat
        input_text = f"{system}\n Here are the court: {input_text}"
        result = chain.invoke({"text": input_text})
        time.sleep(2)
        print(result.content)
        return result.content
    except Exception as e:
        print(f"API調用失敗: {e}")
        return ""
#   print('yes')
process_text("i meant your model temperature, not the actual temperature of the room.")