import time
import json
from Credentials import API_KEY
import openai

openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo'

NUM_QUESTIONS = 3
NUM_ANSWERS = 4


def chatGpt_conversation(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    api_usage = response['usage']

    # Stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)

    conversation.append(
        {'role': response['choices'][0].message.role, 'content': response['choices'][0].message.content})

    # print('Total tokens used: ', api_usage['total_tokens'])


def answer_question(quiz, profile):
    question = quiz['question']
    answers = quiz['answers']
    print(question)
    for i, answer in enumerate(answers):
        print(f'[{i}] - {answer}')

    choice = int(input('Enter your choice: '))
    print()
    print(f"You selected:\n\t{answers[choice]}")

    profile.append(answers[choice])


def get_question_request():
    return """
    Give me """ + str(NUM_QUESTIONS) + """ fun random non-wine questions, each with answers up to """ + str(NUM_ANSWERS) + """ possible answers, to ask somebody to try and guess what type of wine personality they have
    
    Dont include A, a, B, b, C, c, 1, 2, 3 in the answers.

    Randomise the number of answers each time.

    Give your answer in the following JSON:
    {
        "questions": [
            {
                "question"; "",
                "answers": [
                    "", "", ""
                ]
            }
        ]
    }
    """


def get_category_request(quiz_answers):

    answer_str = ""
    for answer in quiz_answers:
        answer_str += answer + "\n"

    return """Based on these answers determine a fun "Wine Category" personality to associate to the person and 3 common popular Australian or New Zealand wines.

""" + answer_str + """

    Give your answer in the following JSON:
    {
        "category": "",
        "category_description": "",
        "wines": [
            {
                "name": "",
                "description": "",
                "region": ""
            }
        ],
    }
    """


def main():
    quiz_answers = []
    conversation = []

    question_request = get_question_request()

    # print(question_request)

    print("fetching personalised questions...")

    tic = time.perf_counter()

    # Make request for questions
    conversation.append({'role': 'system', 'content': question_request})
    chatGpt_conversation(conversation)

    toc = time.perf_counter()
    print()
    print(f"Retrieved Questions in {toc - tic:0.4f} seconds")
    print()

    print("DONE...")
    print()
    print("Starting Quiz...")

    # Load questions
    questions = json.loads(conversation[-1]['content'])
    questions = questions['questions']

    for i in range(NUM_QUESTIONS):
        print("---------------------------------------------------")
        answer_question(questions[i], quiz_answers)

    category_request = get_category_request(quiz_answers)

    # print(category_request)

    print()
    print("fetching wine personality...")

    tic = time.perf_counter()

    # Make request for category
    conversation.append({'role': 'user', 'content': category_request})
    chatGpt_conversation(conversation)

    toc = time.perf_counter()
    print()
    print(f"Calculated Category in {toc - tic:0.4f} seconds")
    print()

    print("DONE...")
    print()

    # Load category
    category = json.loads(conversation[-1]['content'])

    # Display results
    print("##################################################")
    print()
    print(f"\t{category['category']}")
    print()
    categories = category['category_description'].split('.')
    for cat in categories:
        print(f"- {cat}.")
    print()

    print()
    print("\tWines for you:")
    print()
    for wine in category['wines']:
        print(f"{wine['name']} - ({wine['region']}) ")
        print(wine['description'])
        print()
    print("##################################################")


if __name__ == '__main__':
    main()
