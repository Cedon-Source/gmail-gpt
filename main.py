import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },                                        
                "customer": {
                    "type": "string",
                    "description": "Try to identify the company is a law firm or bank, or note that is it unclear"
                },
                "summary":{
                    "type": "string",
                    "description": "Try to summarize the email"
                },
                "interest": {
                    "type": "string",
                    "description": "Try to categorise this email into an a level of interest for the product: 1. Very Interested; 2. Somewhat Interested; 3. Not Interested; 4. Unclear; etc."
                },
                "nextStep":{
                    "type": "string",
                    "description": "What is the suggested next step to move this forward?"
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email based on how quickly it should be responded to, from 0 to 5; 5 most important"
                },
            },
            "required": ["companyName", "customer", "summary", "priority", "interest", "nextStep"]
        }
    }
]


# email = """
# Dear Jason 
# I hope this message finds you well. I'm Shirley from Gucci;

# I'm looking to purchase some company T-shirt for my team, we are a team of 100k people, and we want to get 2 t-shirt per personl

# Please let me know the price and timeline you can work with;

# Looking forward

# Shirley Lou
# """

# prompt = f"Please extract key information from this email: {email} "
# message = [{"role": "user", "content": prompt}]

# response = openai.ChatCompletion.create(
#    model="gpt-3.5-turbo-0613",
#    messages=message,
#    functions = function_descriptions,
#    function_call="auto"
# )

# print(response)


class Email(BaseModel):
     from_email: str
     content: str

@app.get("/")
def read_root():
     return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
     content = email.content
     query = f"Please extract key information from this email: {content} "

     messages = [{"role": "user", "content": query}]

     response = openai.ChatCompletion.create(
         model="gpt-3.5-turbo-0613",
         messages=messages,
         functions = function_descriptions,
         function_call="auto"
     )

     arguments = response.choices[0]["message"]["function_call"]["arguments"]
     companyName = eval(arguments).get("companyName")
     customer = eval(arguments).get("customer")
     summary = eval(arguments).get("summary")
     interest = eval(arguments).get("interest")
     priority = eval(arguments).get("priority")
     nextStep = eval(arguments).get("nextStep")

     return {
         "companyName": companyName,
         "customer": customer,
         "summary": summary,
         "priority": priority,
         "interest": interest,
         "nextStep": nextStep
     }

