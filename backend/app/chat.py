# backend/app/chat.py

from openai import OpenAI
import sqlalchemy
from sqlalchemy import text
from database import SessionLocal
import os

BASE_PROMPT = """
You are an assistant that converts natural language questions into safe SQL queries (only SELECT statements).
The database contains a table called `products` with the following columns:
id, name, description, price, stock, is_fragile, created_at.

Convert the following question into a **pure SQL** statement, without explanations, markdown formatting, or comments.
Only return the SQL statement, avoiding ambiguous aliases or unnecessary functions.

Avoid using EXISTS. Always return an explicit SELECT query over the products table.
If the question is about "how many products" or "how many units", use SUM(stock).
If the question is about whether something exists, use SELECT * WHERE ... LIMIT 1.

Question: {question}
"""


def generate_sql_from_question(question: str) -> str:

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    prompt = BASE_PROMPT.format(question=question)
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    sql = completion.choices[0].message.content.strip()

    if not sql.lower().startswith("select"):
        raise ValueError("The query isn't a valid SQL query.")
    return sql

def execute_query(sql_query: str):
    db = SessionLocal()
    try:
        result = db.execute(text(sql_query))
        return [dict(row._mapping) for row in result]
    except sqlalchemy.exc.SQLAlchemyError as e:
        return {"error": str(e)}
    finally:
        db.close()


def clean_sql(sql_raw: str) -> str:
    return sql_raw.replace("```sql", "").replace("```", "").strip()

def summarize_results(results, question):
    from openai import OpenAI
    import os
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are an assistant that answers questions about a product catalog. Given the following user question and the JSON results of a SQL query, reply with a short and clear sentence in the language of the question that summarizes the findings.

Question: {question}

Results:
{results}

Answer:
"""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return completion.choices[0].message.content.strip()
