import json
import random
import string
import subprocess
from datetime import datetime, timedelta

filepath = './data.json'

def run_git_command(command):
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        # print(f'Erro ao executar comando: {" ".join(command)} - {e}')
        print(e)
        return None

def generate_dates(start, finish):
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(finish, '%Y-%m-%d')
    
    formatted_dates = []
    current_date = start_date
    
    while current_date <= end_date:
        formatted_date = current_date.strftime(f'%Y-%m-%d 10:00:00')
        formatted_dates.append(formatted_date)
        current_date += timedelta(days=1)
    
    return formatted_dates

def generate_random_key(length):
    # Gera uma sequência aleatória de letras (maiúsculas e minúsculas)
    letters = string.ascii_letters  # Contém 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = ''.join(random.choice(letters) for _ in range(length))
    return key

def update_json(data, filepath):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file)
    except IOError as e:
        print(e)

def commit_file(message, date, filepath):    
    contributions_per_day = random.randint(1, 10)
    
    last_hour = 10
    last_minute = 0
    last_second = 0
    
    for i in range(contributions_per_day):
        hour = random.randint(last_hour, 23)
        
        if hour == last_hour:
            minute = random.randint(last_minute, 59)
            if minute == last_minute:
                second = last_second + 1
            else:
                second = random.randint(0, 59)
        else:
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
        last_hour = hour
        last_minute = minute
        last_second = second
        
        date = date.split(' ')[0] + f' {hour}:{minute:02d}:{second:02d}'
        
        data = {'date': generate_random_key(random.randint(10, 30))}
        update_json(data, filepath)
        
        run_git_command(['git', 'add', filepath])    
        run_git_command(['git', 'commit', '--date', date, '-m', message])
        run_git_command(['git', 'push', 'origin', 'main'])
    
    print(f'Commited {contributions_per_day} changes on {date}')

def main():
    start = input("Digite a data de início (YYYY-MM-DD): ")
    finish = input("Digite a data de término (YYYY-MM-DD): ")

    dates = generate_dates(start, finish)
    
    for date in dates:
        print(f'Preparing to commit on {date}...')
        commit_file(f'Commited on {date}', date, filepath)

if __name__ == '__main__':
    main()