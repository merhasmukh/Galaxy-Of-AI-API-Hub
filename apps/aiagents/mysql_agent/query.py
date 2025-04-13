from langchain_openai import ChatOpenAI
from langchain.chains import SQLDatabaseChain
from langchain.sql_database import SQLDatabase
import os

# 1. Set your OpenAI API Key
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# 2. Set up MySQL Connection via SQLAlchemy + pymysql
mysql_uri = "mysql+pymysql://username:password@host:port/databasename"

# 3. Connect to your MySQL database
db = SQLDatabase.from_uri(mysql_uri)

# 4. Initialize the OpenAI LLM (GPT model)
llm = ChatOpenAI(temperature=0, model_name="gpt-4")  # You can use "gpt-3.5-turbo" too

# 5. Create the SQL Database Chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# 6. Run a natural language query
query = "How many orders were placed in the last 30 days?"
response = db_chain.run(query)

# 7. Print the result
print("Answer:", response)
