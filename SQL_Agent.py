from openai import OpenAI
from dotenv import load_dotenv

import os 
import sqlite3

load_dotenv()


class SQLAgent:
   
    def __init__(self):
       
        self.conn = sqlite3.connect("company.db")
        self.cursor = self.conn.cursor()
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL")
        )
        self.model = os.getenv("LLM_MODEL_NAME")
        
        
        
    def get_schema(self):
        
        schema = ""
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        tables = self.cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            if table_name == "sqlite_sequence": 
                continue
            schema += f"\nTable: {table_name}\n"
            self.cursor.execute(
                f"PRAGMA table_info({table_name})"
            )
            columns = self.cursor.fetchall()
            for col in columns:
                schema += (
                    f"- {col[1]} ({col[2]})\n"
                           
                           )
        
        return schema



    def generate_sql(self, question):
        schema = self.get_schema()

        prompt = f"""
تو یک متخصص SQL هستی.

کاربر ممکن است فارسی یا انگلیسی سؤال بپرسد.

فقط یک Query معتبر SQLite تولید کن.

قوانین:

- فقط SELECT تولید کن.
- هیچ توضیحی ننویس.
- فقط SQL برگردان.
- از Markdown استفاده نکن.
- از ```sql استفاده نکن.
- هیچ متن اضافه‌ای قبل یا بعد از Query ننویس.
- اگر پاسخ از روی Schema قابل تولید نیست فقط بنویس:

I don't know

Schema:

{schema}

Question:

{question}
"""

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content":
                    "You are an SQL generator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        sql = response.choices[0].message.content

        if sql is None:
            sql = ""
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()
        

        return sql.strip()
    
    
    def execute_sql(self, sql):

        sql_upper = sql.upper()

        forbidden = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "ALTER",
            "CREATE",
            "PRAGMA"
        ]

        if not sql_upper.startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed.")

        for word in forbidden:

            if word in sql_upper:
                raise ValueError(
                    f"{word} is not allowed."
                )

        self.cursor.execute(sql)

        rows = self.cursor.fetchall()

        columns = [
            column[0]
            for column in self.cursor.description
        ]

        return columns, rows
    
    
    def generate_answer(
        self,
        question,
        sql,
        columns,
        rows
    ):

        prompt = f"""
کاربر سؤال زیر را پرسیده است:

{question}

SQL اجرا شده:

{sql}

ستون‌ها:

{columns}

نتیجه:

{rows}

بر اساس نتیجه بالا، پاسخ کوتاه و روان تولید کن.

اگر سؤال فارسی است فارسی جواب بده.

اگر سؤال انگلیسی است انگلیسی جواب بده.
"""

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role":"system",
                    "content":"You are a helpful assistant."
                },
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        answer = response.choices[0].message.content

        if answer is None:
            answer = ""

        return answer.strip()
    
    
    
    def ask(self, question):

        sql = self.generate_sql(question)

        if sql == "I don't know":
            return "اطلاعات کافی برای پاسخ وجود ندارد."

        print("\nGenerated SQL:\n")
        print(sql)

        if not sql:
            return "مدل هیچ Query معتبری تولید نکرد."
        
        columns, rows = self.execute_sql(sql)
        
        print("\nColumns:")
        print(columns)

        print("\nRows:")
        print(rows)
        
        answer = self.generate_answer(
            question,
            sql,
            columns,
            rows
        )

        return answer


    def close(self):

        self.conn.close()
        
    
    
def main():

    agent = SQLAgent()

    print("SQL Agent")
    print("type exit to quit.\n")

    while True:

        question = input("Question: ")

        if question.lower() == "exit":
            break

        try:

            answer = agent.ask(question)

            print("\nAnswer:\n")
            print(answer)
            print("-" * 50)

        except Exception as e:

            print(e)

    agent.close()    


if __name__ == "__main__":

    main()