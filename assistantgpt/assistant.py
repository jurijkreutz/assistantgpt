import config
import os
from assistantgpt import gptconnection
from dotenv import load_dotenv

assistant = dict(
    name='',
    description='',
    steps=[]
)


def initialize_assistant():
    load_dotenv()
    get_user_init_data()
    config.configuration['openapi_key'] = os.getenv('OPEN_API_KEY')
    print("🤖: Starting up, please be patient...")
    if gptconnection.test_connection(config.configuration['openapi_key']):
        print(f"🤖: {gptconnection.start_communication_with_gpt(assistant)}")
        communicate_in_loop()


def communicate_in_loop():
    while True:
        user_message = input('Your message: ')
        print(...)
        print(f"🤖: {gptconnection.communicate(assistant, user_message)}")


def get_user_init_data():
    print('How do you want your assistant to be called?')
    print('Example: Research AI')
    assistant['name'] = input('Your Assistants name: ')
    print(f"🤖: Hello! My name is {assistant['name']}")
    print('Example: an AI that researches the internet for you.')
    assistant['description'] = input('Your Assistants description: ')
    print(f"🤖: I will be {assistant['description']}")
    print("🤖: Please tell me what to do, step by step")
    counter = 1
    while True:
        next_step = input(f"🤖: Step number {counter}: ")
        if next_step != '':
            assistant['steps'].append(next_step)
            counter += 1
        else:
            break


