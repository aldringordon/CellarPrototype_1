import json
from Credentials import API_KEY
import openai

openai.api_key = API_KEY
model_id = 'gpt-3.5-turbo'


def chatGpt_conversation(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    api_usage = response['usage']

    # Stop means complete
    print(response['choices'][0].finish_reason)
    print(response['choices'][0].index)

    conversation.append(
        {'role': response['choices'][0].message.role, 'content': response['choices'][0].message.content})

    print('Total tokens used: ', api_usage['total_tokens'])


def answer_question(quiz, profile):
    question = quiz['question']
    answers = quiz['answers']
    print(question)
    for i, answer in enumerate(answers):
        print(f'[{i}] - {answer}')

    choice = int(input('Enter your choice: '))
    print(f"You selected:\n\t{answers[choice]}")

    profile.append(answers[choice])


def get_question_request():
    return """
    Give me 3 fun questions, each with 3 possible answers, to ask somebody to try and guess what type of wine personality they have
    
    Dont include A, B, C in the answers and dont index the answers.

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
    return """Based on these answers determine a fun "Wine Category" personality to associate to the person and 3 wines.

    """ + quiz_answers[0] + "\n" + quiz_answers[1] + "\n" + quiz_answers[2] + "\n" + """

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

    print("loading questions...")

    # Make request for questions
    conversation.append({'role': 'system', 'content': question_request})
    chatGpt_conversation(conversation)

    print("DONE...")
    print()
    print("Starting Quiz...")

    # Load questions
    questions = json.loads(conversation[-1]['content'])
    questions = questions['questions']

    print("---------------------------------------------------")
    answer_question(questions[0], quiz_answers)

    print("---------------------------------------------------")
    answer_question(questions[1], quiz_answers)

    print("---------------------------------------------------")
    answer_question(questions[2], quiz_answers)

    print("---------------------------------------------------")

    category_request = get_category_request(quiz_answers)

    print()
    print("fetching wine personality...")

    # Make request for category
    conversation.append({'role': 'user', 'content': category_request})
    chatGpt_conversation(conversation)

    print("DONE...")
    print()

    # Load category
    category = json.loads(conversation[-1]['content'])

    # Display results
    print("---------------------------------------------------")
    print()
    print(category['category'])
    print()
    print(category['category_description'])
    print()
    print("Wines:\n")

    for wine in category['wines']:
        print(wine['name'])
        print(wine['description'])
        print(wine['region'])
        print()
    print("---------------------------------------------------")


if __name__ == '__main__':
    main()
