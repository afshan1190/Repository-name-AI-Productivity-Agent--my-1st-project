from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv("../.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv("../.env")

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_summary(tasks):

    task_text = "\n".join(tasks)

    prompt = f"""
You are an expert productivity coach.

Tasks:
{task_text}

Generate:
1. Summary of today's work
2. Productivity score out of 10
3. Suggestions for tomorrow

Keep response concise.
"""

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def generate_tomorrow_plan(tasks):

    task_text = "\n".join(tasks)

    prompt = f"""
You are a productivity coach.

Current Tasks:
{task_text}

Create a prioritized plan for tomorrow.

Include:
1. Top 3 priorities
2. Suggested schedule
3. Productivity tips

Keep response concise.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content