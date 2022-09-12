import pandas as pd

if __name__ == '__main__':
    path_train = 'JEOPARDY_QUESTIONS1.json'

    df = pd.read_json(path_train)
    # Index(['category', 'air_date', 'question', 'value', 'answer', 'round',
    #    'show_number'],
    print(df['question'])
    print(df['answer'])
    print(df['round'])