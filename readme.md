# SQL Agent (LLM + SQLite)

A lightweight SQL Agent that converts natural language questions (Persian & English) into SQLite queries using an OpenAI-compatible LLM, executes the generated SQL safely, and returns a natural language answer.

---

## Features

- Natural language → SQL
- Persian & English support
- Automatic database schema extraction
- SQLite backend
- Read-only SQL execution (SELECT only)
- SQL safety validation
- Natural language response generation

---

## Project Structure

```
.
├── SQL_Agent.py
├── company.db
├── .env.example
├── requirements.txt
└── README.md
```

---

## Workflow

```text
User Question
      │
      ▼
LLM
      │
      ▼
Generate SQL
      │
      ▼
SQLite Database
      │
      ▼
Query Result
      │
      ▼
LLM
      │
      ▼
Natural Language Answer
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
LLM_API_KEY=YOUR_API_KEY
LLM_BASE_URL=https://api.gapgpt.app/v1
LLM_MODEL_NAME=gpt-4o
```

---

## Run

```bash
python SQL_Agent.py
```

---

## Example

### Input

```
Question:
چند کارمند داریم؟
```

### Generated SQL

```sql
SELECT COUNT(*) AS employee_count
FROM Employees;
```

### Query Result

```
[(50,)]
```

### Final Answer

```
50 کارمند داریم.
```

---

## Technologies

- Python
- SQLite
- OpenAI Compatible API
- python-dotenv

---

## Future Improvements

- Support for JOIN-heavy queries
- Conversation memory
- SQL query optimization
- Streaming responses
- Web interface (Streamlit / FastAPI)
- Multi-database support (PostgreSQL, MySQL)

---

## License

MIT