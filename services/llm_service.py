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


def safe_invoke(llm, prompt):

    try:

        response = llm.invoke(prompt)

        return response.content

    except Exception as e:

        error_message = str(e).lower()

        if "quota" in error_message or "resource_exhausted" in error_message:

            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please wait for the quota to reset and try again."
            )

        if "api key" in error_message or "authentication" in error_message:

            raise RuntimeError(
                "Gemini API key is invalid or missing. "
                "Please check your .env file."
            )

        if "429" in error_message:

            raise RuntimeError(
                "Gemini API request limit reached. "
                "Please wait and try again."
            )

        if "timeout" in error_message:

            raise RuntimeError(
                "Gemini API request timed out. "
                "Please try again."
            )

        raise RuntimeError(
            f"Gemini API error: {str(e)}"
        )


if __name__ == "__main__":

    llm = get_llm()

    response = safe_invoke(
        llm,
        "Say hello to CareerPilot AI in one short sentence."
    )

    print(response)