# GPT Gym Workout Tracker

This project demonstrates an AI-powered natural language interface to a gym workout and progress tracking database.

## Project Structure

- **setup.sql**  
  Sets up the SQLite database schema for users, workouts, exercises, programs, and gym locations.

- **setupData.sql**  
  Seeds the database with sample data for users, locations, workouts, programs, exercises, and progress metrics.

- **db_bot.py**  
  Initializes the database, connects to OpenAI, and handles generating prompts, querying the database, and returning friendly natural language responses.

- **strategies**  
  The code experiments with several prompting strategies ("zero-shot", "few-shot", "chain-of-thought", etc.), inspired by ideas from [this research paper](https://arxiv.org/abs/2305.11853).

- **response_\<strategy>_\<time>.json**  
  These files record all prompts, generated SQL queries, and friendly responses for each strategy and question.

- **[sample_post.md](sample_post.md)**  
  A report showing sample questions, SQL queries, results, and project findings.

- **[schema.png](schema.png)**  
  A schema diagram of the database.  
  _Tip: Can you spot where the foreign keys are defined?_  
  Created from the SQLite database using [schemacrawler](https://www.google.com/search?q=install+schemacrawler):
