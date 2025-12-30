import os
from dotenv import load_dotenv
import openai

load_dotenv(dotenv_path='/home/pontes/LeishAI/backend/.env')

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
model="gpt-4o",
messages=[
{"role": "system", "content": "Você é um especialista em Python, React, Docker e PostgreSQL. Analise, explique e sugira melhorias em códigos dessas tecnologias."},
{"role": "user", "content": "Melhore o seguinte código Python para performance e boas práticas:\ndef exemplo():\n  x = 1\n  y = 2\n  return x + y"}
]
)

print(response.choices[0].message.content)