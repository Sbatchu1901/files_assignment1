import json
import os
import pandas as pd

def load_json_data():
    #print("Current directory:", os.getcwd())
    folder_name = input("Enter the folder name where the JSON file is located at: ")
    file_name = 'sbatchu_adoptions.json'
    file_path = os.path.join(folder_name, file_name)
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: The specified file was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception :
        print("An unexpected error occurred")

def csv_files(data, filename):
    df = pd.DataFrame(data)
    path_to_directory = "C:\\Users\\sruja\\OneDrive\\Desktop\\files_assignment1"
    total_path = os.path.join(path_to_directory, filename)
    df.to_csv(total_path, index=False)

def contacts_file(data):
    contacts = []
    for item in data:
        if 'contacts' in item:
            for contact in item['contacts']:
                #contact['record_id'] = item['id']
                contacts.append(contact)
    csv_files(contacts, 'contacts.csv')

def universities_file(data):
    universities = []
    for item in data :
        universities.append(item['university'])
    csv_files(universities, 'universities.csv')

def adoptions_file(data):
    adoptions = []
    books = []
    for item in data:
        if 'adoptions' in item:
            for adoption in item['adoptions']:
                adoption_record = {
                    'adoption_id': adoption['id'],
                    'record_id' : item['id'],
                    'date': adoption['date'],
                    'quantity': adoption['quantity'],
                    'book_id': adoption['book']['id']
                }
                adoptions.append(adoption_record)
                book_record = {
                    'book_id': adoption['book']['id'],
                    'isbn10': adoption['book'].get('isbn10', ''),
                    'isbn13': adoption['book'].get('isbn13', ''),
                    'title': adoption['book']['title'],
                    'category': adoption['book']['category']
                }
                books.append(book_record)
    csv_files(adoptions, 'adoptions.csv')
    csv_files(books, 'books.csv') 

def messages_file(data):
    messages = []
    for item in data:
        if 'messages' in item:
            for message in item['messages']:
                message['record_id'] = item['id']
                messages.append(message)
    csv_files(messages, 'messages.csv')

    
def universities_in_state(state_name, csv_filename='universities.csv'):
    try:
        state_df = pd.read_csv(csv_filename)
        filtered_state_df = state_df[state_df['state'].str.lower() == state_name.lower()]
        if not filtered_state_df.empty:
            print("Universities in {}: ".format(state_name))
            for university in filtered_state_df['name']:
                print(university)
        else:
            print("No universities found in {}.".format(state_name))
    except FileNotFoundError:
        print("Error: The file {} was not found.".format(csv_filename))
    except Exception :
        print("An unexpected error occurred")
        
def books_by_category(category_name, csv_filename='books.csv'):
    try:
        df = pd.read_csv(csv_filename)
        filtered_books_df = df[df['category'].str.lower() == category_name.lower()]
        if not filtered_books_df.empty:
            filename = f"{category_name.replace(' ', '_')}_booktitles.txt"
            with open(filename, 'w', encoding='utf-8') as file:
                for title in filtered_books_df['title']:
                    file.write(title + '\n')
            print("Book titles in the category {} have been saved to {}.".format(category_name,filename))
        else:
            print("No books found in the category {}.".format(category_name))
    except FileNotFoundError:
        print("Error: The file {} was not found.".format(csv_filename))
    except Exception :
        print("An unexpected error occurred")
    
    
if __name__ == "__main__":
    data = load_json_data()
    if data:
        contacts_file(data)
        universities_file(data)
        adoptions_file(data)
        messages_file(data)
        print("Data is saved into csv files.")
        user_state_input = input("Would you like to search for universities by state? (yes/no): ").strip().lower()
        if user_state_input == 'yes':
            state_name = input("Enter the state name to search for universities: ")
            universities_in_state(state_name)
        else:
            print("University search skipped.")
        user_category_input = input("Would you like to search for books by category? (yes/no): ").strip().lower()
        if user_category_input == 'yes':
            category_name = input("Enter the book category name to search: ")
            books_by_category(category_name)