import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError(
            "GOOGLE_API_KEY is not configured in the .env file."
        )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    return llm


if __name__ == "__main__":

    llm = get_llm()

    response = llm.invoke(
        "Say hello to CareerPilot AI in one short sentence."
    )

    print(response.content)