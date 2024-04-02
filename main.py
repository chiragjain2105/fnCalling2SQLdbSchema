import db
import openai
import json

functions = [
    {
        "name": "ask_database",
        "description": "Use this function to answer user questions about Sales Person. Output should be a fully formed sql query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": f"""
                                SQL query extracting info to answer user's question.
                                SQL should be written using database schema:
                                {db.database_schema_string}
                                The query should be returned in plain text, not in JSON.
                                Do not use new lines characters in the query. 
                                """
                }
            },
            "required": ["query"]
        }
    }
]


def execute_function_call(message):
    if message.function_call.name == 'ask_database':
        query = eval(message.function_call.arguments)["query"]
        # print("query-> " + query)
        results = db.ask_database(query)
    else:
        results = f"Error: function {message.function_call.name} does not exist"

    return query,results


def openai_functions_chain(query):
    messages = []
    messages.append(
        {"role": "system", "content": "Answer user questions by generating SQL queries against Sales_Person database"})
    messages.append({"role": "user", "content": query})

    response = openai.chat.completions.create(
        temperature=0,
        model='gpt-3.5-turbo',
        messages=messages,
        functions=functions,
        function_call='auto'
    )

    response_message = response.choices[0].message

    if response_message.__getattribute__("function_call"):
        print("Executing Function: ", response_message.function_call)
        query,results = execute_function_call(response_message)
        messages.append(response_message)
        messages.append(
            {
                "role": "function",
                "name": "ask_database",
                "content": str(results)
            }
        )
        second_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return query,second_response.choices[0].message.content
    else:
        return None,response_message.content


if __name__ == '__main__':
    print("1")
    print(openai_functions_chain("Write a solution to find the names of all the salespersons who did not have any orders related to the company with the name \"RED\""))
