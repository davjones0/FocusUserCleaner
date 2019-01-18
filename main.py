from progress.bar import Bar
from engine import Engine
from pprint import pprint
from questions import initQuestions, searchQuestions, selectState



def main():
    
    answers = initQuestions()
    
    engine = Engine(answers['list_path'], answers['focus_name'], answers['focus_password'])
    engine.start_browser(False)
    engine.parse_csv()
    
    state = selectState()
    engine.state = state['state']
    
    search_temp = searchQuestions(engine.choices)
    choices = search_temp['search_choice']
    engine._build_search_terms(choices)
    engine.login()
    engine.begin_cleaning(choices)


if __name__ == "__main__":
    main()
