import json
import random
import string
import subprocess
from datetime import datetime, timedelta

FILEPATH = './data.json'

def run_git_command(command):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f'Error executing command: {" ".join(command)} - {e}')
        return None

def generate_dates(start, finish):
    """Generate a list of dates between start and finish."""
    start_date = datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.strptime(finish, '%Y-%m-%d')
    
    formatted_dates = []
    current_date = start_date
    
    while current_date <= end_date:
        formatted_date = current_date.strftime('%Y-%m-%d 10:00:00')
        formatted_dates.append(formatted_date)
        current_date += timedelta(days=1)
    
    return formatted_dates

def generate_random_key(length):
    """Generate a random string of letters of specified length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def update_json(data, filepath):
    """Update the JSON file with the given data."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file)
    except IOError as e:
        print(f'Error writing to file: {e}')

def commit_file(message, date, filepath):    
    """Commit changes to the git repository with a specific message and date."""
    contributions_per_day = random.randint(1, 10)
    
    last_hour = 10
    last_minute = 0
    last_second = 0
    
    for _ in range(contributions_per_day):
        hour = random.randint(last_hour, 23)
        
        if hour == last_hour:
            minute = random.randint(last_minute, 59)
            second = last_second + 1 if minute == last_minute else random.randint(0, 59)
        else:
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
        
        last_hour, last_minute, last_second = hour, minute, second
        
        date_time_str = f"{date.split(' ')[0]} {hour}:{minute:02d}:{second:02d}"
        
        data = {'date': generate_random_key(random.randint(10, 30))}
        update_json(data, filepath)
        
        run_git_command(['git', 'add', filepath])    
        run_git_command(['git', 'commit', '--date', date_time_str, '-m', message])
        run_git_command(['git', 'push', 'origin', 'main'])
    
    print(f'Committed {contributions_per_day} changes on {date_time_str}')

def main():
    """Main function to execute the script."""
    start = input("Enter the start date (YYYY-MM-DD): ")
    finish = input("Enter the end date (YYYY-MM-DD): ")

    dates = generate_dates(start, finish)
    
    for date in dates:
        print(f'Preparing to commit on {date}...')
        commit_file(f'Committed on {date}', date, FILEPATH)

if __name__ == '__main__':
    main()