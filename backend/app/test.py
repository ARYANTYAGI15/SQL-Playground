from app.utils import get_llm

llm = get_llm()
response = llm("Write a SQL query to select top 5 customers by revenue.")
print(response)