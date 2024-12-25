import pandas as pd
from sqlalchemy import create_engine
from pandasai import PandasAI
from pandasai.llm.huggingface import HuggingFace

# Initialize a local Hugging Face model for PandasAI
llm = HuggingFace(model="gpt2")  # Use a lightweight model like GPT-2
pandas_ai = PandasAI(llm)

# Database connection
DB_USERNAME = "your_username"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"  # Or your database host
DB_NAME = "sentidb"

# Create a connection to the MySQL database
engine = create_engine(f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Load data into Pandas DataFrames
companies = pd.read_sql('SELECT * FROM companies', engine)
users = pd.read_sql('SELECT * FROM users', engine)
products = pd.read_sql('SELECT * FROM products', engine)
feedback = pd.read_sql('SELECT * FROM feedback', engine)

# Combine tables for comprehensive analysis
merged_df = feedback.merge(users, on='uid').merge(products, on='pid').merge(companies, on='cid')

# Define a function to query data using Pandas AI
def ask_question(query):
    try:
        print(f"Question: {query}")
        result = pandas_ai.run(merged_df, query)
        print(f"Result:\n{result}")
    except Exception as e:
        print(f"Error: {e}")

# Interactive CLI for asking questions
def interactive_session():
    print("\nWelcome to the User Feedback Analyzer System!")
    print("Ask your questions in plain English (type 'exit' to quit):\n")
    
    while True:
        query = input("Your question: ")
        if query.lower() in ['exit', 'quit']:
            print("Goodbye!")
            break
        ask_question(query)

# Run the interactive session
if __name__ == "__main__":
    interactive_session()
