import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running db_bot.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE
sqliteDbPath = getPath("aidb.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath)

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # setup tables and keys
sqliteCursor.executescript(setupSQlDataScript) # setup tables and keys

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

# OPENAI
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(api_key = config["openaiKey"])
openAiClient.models.list() # check if the key is valid (update in config.json)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result


# strategies
commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not expalin it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript +
                   " Which users haven't logged any progress metrics? " +
                   "\nSELECT u.user_id, u.username\nFROM users u\nLEFT JOIN progress_metric pm ON u.user_id = pm.user_id\nWHERE pm.progress_id IS NULL;\n" +
                   commonSqlOnlyRequest),
    "chain_of_thought": (setupSqlScript +
                    " Let's think step by step. First, we want to find out how many workouts each user has done. Next, we need to count the number of workouts for each user. Then, we should order the results by the count in descending order to see which users have done the most. Finally, select the user IDs and usernames along with the count of workouts.\n"
                    " SELECT u.user_id, u.username, COUNT(w.workout_id) AS workout_count "
                    " FROM users u JOIN workout w ON u.user_id = w.user_id "
                    " GROUP BY u.user_id, u.username "
                    " ORDER BY workout_count DESC;\n"
                    + commonSqlOnlyRequest),
    "self asking": (setupSqlScript + " First, how do I get all users? Second, how do I know which ones have no progress metrics?" +
                    " \n Third, how do I get the users who have no progress metrics? Fourth, how do I write a query that answers the question? " +
                    " \nSELECT u.user_id, u.username FROM users u LEFT JOIN progress_metric pm ON u.user_id = pm.user_id WHERE pm.progress_id IS NULL;\n" +
                    commonSqlOnlyRequest),
    "few_shot": (setupSqlScript +
                    " Example 1: Which users have logged progress?\nSELECT DISTINCT u.user_id, u.username FROM users u JOIN progress_metric pm ON u.user_id = pm.user_id;\n" +
                    " Now answer: Which users haven't logged any progress metrics?\n" +
                    " SELECT u.user_id, u.username FROM users u LEFT JOIN progress_metric pm ON u.user_id = pm.user_id WHERE pm.progress_id IS NULL;\n" +
                    commonSqlOnlyRequest),
    "no_context": (
                    " Which users haven't logged any progress metrics?"
                    " \nSELECT u.user_id, u.username FROM users u LEFT JOIN progress_metric pm ON u.user_id = pm.user_id WHERE pm.progress_id IS NULL;\n" +
                    commonSqlOnlyRequest)
}

questions = [
    "Which users have done the most workouts?", 
    # "Which workouts are associated with multiple programs?", 
    # "Which users are enrolled in multiple programs?", 
    "What are the top 3 most-used gym locations?", 
    "Which users have multiple progress metric entries?", 
    "Which users haven't logged any progress metrics?",  
    "Are there any users with progress data who haven't worked out recently?"  
    # "Can you provide insert SQL with realistic user and workout data?"  
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    print("########################################################################")
    print(f"Running strategy: {strategy}")
    for question in questions:

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Question:")
        print(question)
        error = "None"
        try:
            getSqlFromQuestionEngineeredPrompt = strategies[strategy] + " " + question
            sqlSyntaxResponse = getChatGptResponse(getSqlFromQuestionEngineeredPrompt)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print("SQL Syntax Response:")
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print("Query Raw Response:")
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question +"\" and the response was \""+queryRawResponse+"\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            # betterFriendlyResultsPrompt = "I asked a question: \"" + question +"\" and I queried this database " + setupSqlScript + " with this query " + sqlSyntaxResponse + ". The query returned the results data: \""+queryRawResponse+"\". Could you concisely answer my question using the results data?"
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print("Friendly Response:")
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)


sqliteCursor.close()
sqliteCon.close()
print("Done!")
