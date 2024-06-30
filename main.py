from bson import ObjectId
import re
from pymongo import MongoClient, errors
from getpass import getpass
from crewai import Crew as CrewAI
from agents import Get_Resource_Agent, Show_Career_Agent, Show_path_Agent, Study_Planner_Agent, Recap_Agent, Progress_Tracker_Agent
from tasks import Search_For_Me, What_Next, Career_Path, Study_Plan, Search_History, Track_the_Progress

# Function to connect to MongoDB and store user details
def store_user_details():
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['smart_learning']
        users_collection = db['col_1']
    except errors.ConnectionError as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None, None

    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    password = getpass("Enter your password: ").strip()

    if not name or not email or not password:
        print("All fields are required.")
        return None, None, None

    user_data = users_collection.find_one({'email': email})

    if user_data:
        print("Welcome back!")
        return user_data['_id'], users_collection, user_data

    user_data = {
        'name': name,
        'email': email,
        'password': password,
        'search_history': []
    }

    try:
        user_id = users_collection.insert_one(user_data).inserted_id
        print("User details saved successfully.")
    except errors.PyMongoError as e:
        print(f"Error saving user details: {e}")
        return None, None, None

    return user_id, users_collection, user_data

def main():
    # Store user details
    user_id, users_collection, user_data = store_user_details()
    if not user_data:
        print("User details are required to proceed.")
        return

    # Options dictionary
    options = {
        '1': {
            'agent': Get_Resource_Agent,
            'task': Search_For_Me,
            'description': "Recommend me a Course."
        },
        '2': {
            'agent': Show_Career_Agent,
            'task': What_Next,
            'description': "What should I do next?"
        },
        '3': {
            'agent': Show_path_Agent,
            'task': Career_Path,
            'description': "Show me the path to reach my goal."
        },
        '4': {
            'agent': Study_Planner_Agent,
            'task': Study_Plan,
            'description': "Manage my time to complete my tasks."
        },
        '5': {
            'agent': Recap_Agent,
            'task': Search_History,
            'description': "Show my search history"
        },
        '6': {
            'agent': Progress_Tracker_Agent,
            'task': Track_the_Progress,
            'description': "Show my progress of last study"
        },
        'q': {
            'description': "Quit"
        }
    }

    while True:
        # Prompt the user to choose an option
        print("\nThe things I can provide you....:")
        for key, value in options.items():
            print(f"{key}: {value['description']}")
        choice = input("Choose the number you want (or 'q' to quit): ").strip()

        if choice == 'q':
            print("Exiting.... Happy learning.... Have a great day....!")
            break

        if choice not in options:
            print("Invalid choice. Please try again.")
            continue

        selected_option = options[choice]

        # Collect inputs based on the choice
        inputs = {}
        if choice == '1':
            search_course = input("Enter the course you are searching for: ").strip()
            career_goal = input("Enter your career goal: ").strip()
            learning_preference = input("Enter your learning preference (e.g., blog, Video, etc.): ").strip()

            if not search_course or not career_goal or not learning_preference:
                print("All inputs are required. Please try again.")
                continue

            inputs = {
                'search_course': search_course,
                'career_goal': career_goal,
                'learning_preference': learning_preference
            }

        elif choice == '2':
            search_course = input("Enter the course you are doing now: ").strip()

            if not search_course:
                print("Course you are doing is required. Please try again.")
                continue

            inputs = {
                'search_course': search_course
            }

        elif choice == '3':
            career_goal = input("Enter your career goal: ").strip()

            if not career_goal:
                print("Career goal is required. Please try again.")
                continue

            inputs = {
                'career_goal': career_goal
            }

        elif choice == '4':
            topics = []
            while True:
                topic = input("Enter a topic (or type 'done' to finish): ").strip()
                if topic.lower() == 'done':
                    break
                elif topic:
                    topics.append(topic)

            try:
                max_hours = float(input("Enter the maximum time you can give (in hours): ").strip())

                inputs = {
                    'topics': topics,
                    'max_hours': max_hours
                }

            except ValueError:
                print("Invalid input for maximum hours. Please enter a numerical value.")
                continue

        elif choice == '5':
            if 'search_history' in user_data and user_data['search_history']:
                with open('recommended_material.txt', 'w') as file:
                    file.write("Here is your search history:\n")
                    for idx, entry in enumerate(user_data['search_history'], start=1):
                        file.write(f"\nEntry {idx}:\n")
                        file.write(f"Choice: {entry['choice']}\n")
                        file.write(f"Inputs: {entry['inputs']}\n")
                        if 'output' in entry:
                            file.write(f"Output: {entry['output']}\n")
                        else:
                            file.write("Output: No output stored\n")
            else:
                print("Hello friend....This is the first time you came here.")
                continue

        elif choice=='6':
            latest_study_plan = None
            # Display the progress of the study plan
            print("\nProgress Tracker:")
            if 'search_history' in user_data:
                for entry in reversed(user_data['search_history']):
                    if entry['choice'] == '4':
                        latest_study_plan = entry['output']
                        break
            if not 'search_history':
                print('No study plan found in your history.')
                continue
            if latest_study_plan:
                # Extract the details using regular expression
                study_plan_regex = re.compile(r'\d+\)\s*(.*?)\s*-\s*\[(.*?)\]\s*(.*?)\n')
                matches = study_plan_regex.findall(latest_study_plan)

                if matches:
                    for match in matches:
                        topic = match[0].strip()
                        time_allocated = match[1].strip()
                        status = match[2].strip()
                        print(f'Topic: {topic}, Time Allocated: {time_allocated}, Status: {status}')

                # Prompt the user if they want to update the timing for each topic  
                temp=[]
                updated_study_plan = []
                for match in matches:
                    sr_no=0
                    topic = match[0].strip()
                    time_allocated = match[1].strip()
                    status = match[2].strip()
                    
                    # Ask the user if they want to update the time
                    update_time = input(f'Do you want to update the time for {topic}? (yes/no): ').strip().lower()
                    if update_time == 'yes':
                        new_time = input(f'Enter new time for {topic} (current: {time_allocated}): ').strip()
                        if new_time:
                            time_allocated = new_time
                            temp.append(True)
                            
                    # Ask the user if they want to update the status
                    update_status = input(f'Do you want to update the status for {topic}? (yes/no): ').strip().lower()
                    if update_status == 'yes':
                        new_status = input(f'Enter the status of {topic} (current: {status}): ').strip()
                        if new_time:
                            status= new_status
                            temp.append(True)

                    updated_study_plan.append(f"{sr_no}) {topic} - [{time_allocated}] - {status}\n ")
                    sr_no += 1

                updated_study_plan_str = '\n\n'.join(updated_study_plan)

                # Update the document in MongoDB
                if True in temp:
                    try:
                        result = users_collection.update_one(
                            {'_id': ObjectId(user_id), 'search_history.choice': '4'},
                            {'$set': {'search_history.$.output': updated_study_plan_str}}
                        )
                        if result.modified_count > 0:
                            print("Update successful")
                        else:
                            print("No matching document found or update not needed")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    
            else:
                print('No study plan details found.')
                continue

        # Execute the task
        try:
            crew_task = CrewAI(
                agents=[selected_option['agent']],
                tasks=[selected_option['task']],
                verbose=2,
                memory=False,
                cache=True
            )

            result = crew_task.kickoff(inputs=inputs)
            if not choice=='6':
                search_entry = {'choice': choice, 'inputs': inputs, 'output': result}  # Store the output

            # Update the user's search history with the choice, inputs, and output
            users_collection.update_one(
                {'_id': user_id},
                {'$push': {'search_history': search_entry}}
            )

            if choice == '4':
                print("\nGenerated Study Plan:")
                print(result)

        except Exception as e:
            # print(f"An error occurred during the {selected_option['description'].lower()} task: {e}")
            continue

if __name__ == "__main__":
    main()
