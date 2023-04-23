import openai
import config
import json


previous_conversation = []
standard_definition = "You are a chatbot used in an autonomous \
                 environment. You get messages from the program (system) and from the \
                 user. The user can decide, which role you have. Behave, like the user wants \
                 you to and never leave the role. Always answer in JSON. \
                 Always share your inner thoughts and the answer to the user. \
                 The JSON should have 3 properties: inner_thoughts, message_to_user, plan. \
                 Example JSON: {{\" message_to_user\"=Your message to user, \"inner_thoughts\"=Your inner thoughts, \"plan\"=Your plan as list/array}} \
                 Always answer with this exact JSON format and exact keys. If not, the program will crash."


def test_connection(api_key):
    openai.api_key = api_key
    try:
        modelName = openai.Model.retrieve('gpt-3.5-turbo')["id"]
        print(f"🤖: I will be using {modelName} as my brain.")
        return True
    except (openai.error.AuthenticationError):
        print('Connection failed.')
        return False


def start_communication_with_gpt(assistant):
    assistant_definition = f"{standard_definition} Your name, decided by the user: {assistant['name']}. \
                Your description, decided by the user: {assistant['description']}. \
                The user is allowed to create a step by step list, of what they want you to do. \
                Generate a plan based on that list. This plan will be saved and you will be reminded of it \
                because your token limit is really small and we don't want you to forget about the plan. \
                Your steps, decided by the user: {assistant['steps']}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": assistant_definition},
                {"role": "user", "content": "Hello!"},
            ]
    )
    if (config.configuration['debug']):
        print(response)
    result = ''
    for choice in response.choices:
        result += choice.message.content
    previous_conversation.append(dict(user_input='Hello!', ai_answer=result))
    json_result = json.loads(result)
    return json_result['message_to_user']


def communicate(assistant, user_message):
    assistant_definition = f"{standard_definition} Your name, decided by the user: {assistant['name']}. \
                Your description, decided by the user: {assistant['description']}. \
                The user is allowed to create a step by step list, of what they want you to do. \
                Generate a plan based on that list. This plan will be saved and you will be reminded of it \
                because your token limit is really small and we don't want you to forget about the plan. \
                Your steps, decided by the user: {assistant['steps']}. \
                Since you have a small memory, here is a reminder of our chat history: {previous_conversation}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": assistant_definition},
                {"role": "user", "content": user_message},
            ]
    )
    if (config.configuration['debug']):
        print("\n DEBUG \n")
        print(response)
        print("\n DEBUG END \n")
    result = ''
    for choice in response.choices:
        result += choice.message.content
    previous_conversation.append(dict(user_input=user_message, ai_answer=result))
    if (config.configuration['debug']):
        print("\n DEBUG \n")
        print(f"Previous conv: {previous_conversation}")
        print("\n DEBUG END \n")
    json_result = json.loads(result)
    return json_result['message_to_user']