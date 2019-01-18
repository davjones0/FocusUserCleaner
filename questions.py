from PyInquirer import prompt, print_json
from pprint import pprint


def initQuestions(answers=None):
    questions = [
        {
            'type': 'input',
            'name': 'list_path',
            'message': 'Enter path to user list:'
        },
        {
            'type': 'input',
            'name': 'focus_name',
            'message': 'Enter your Focus username:'
        },
        {
            'type': 'password',
            'name': 'focus_password',
            'message': 'Enter your Focus password:'
        },
    ]
    
    answers = prompt(questions)
    ready = confirmQuestion()
    if ready["confirmation"]:
        return answers
    else:
        exit()
        #initQuestions(answers)

def searchQuestions(fieldHeaders, answers=None):
    options = []
    for entry in fieldHeaders:
        options.append({'name': entry})

    choice = [
        {
            'type': 'checkbox',
            'name': 'search_choice',
            'message': 'Select search criteria',
            'choices': options,
        }
    ]
    
    answers = prompt(choice)
    if len(answers['search_choice']) != 0:
        return answers
    else:
        print('You must select at least one field')
        return searchQuestions(fieldHeaders, answers)   


def confirmQuestion():
    confirm = [
        {
            'type': 'confirm',
            'message': 'Do you want to continue?',
            'name': 'confirmation',
            'default': False
        }
    ]

    ready = prompt(confirm)
    return ready

def loginFailQuestion():
    login = [
        {
            'type': 'confirm',
            'message': 'Login Failed re-enter your username and password and try again',
            'name': 'login'
        }
    ]

    answer = prompt(login)
    if not answer['login']:
        exit()

def retryLogin():
    questions = [
        {
            'type': 'input',
            'name': 'refocus_name',
            'message': 'Enter your Focus username:'
        },
        {
            'type': 'password',
            'name': 'refocus_password',
            'message': 'Enter your Focus password:'
        },
    ]
    
    answers = prompt(questions)
    return answers

def selectState():
    question = [
        {
            'type': 'rawlist',
            'name': 'state',
            'message': 'Select the state you want to delete from:',
            'choices': [
                'Michigan',
                'Pennsylvania',
                'Texas',
                'New York',
                'New Jersey',
                'California',
                'Wisconsin'
            ]
        }
    ]

    answers = prompt(question)
    return answers