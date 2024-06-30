>>>> Introduction : 

    Personalized Learning app for students to provide them learning paths, recommend resources , giving course suggestions based on their interests and making a study plan to help them and to track their progress to implement it.

    Connected to the MongoDB database to store the information about the user after logged in and to store the search history of the user to show him when he logged in again with the same credentials.


>>>> Key Components:

    main.py: 
        Main class 
    agents.py: 
        Class defining the CrewAI Agents.
    tasks.py: 
        Class defining the CrewAI Tasks.
    tools.py: 
        Class implementing the GmailDraft Tool.
    recommended_material.txt: 
        File to show the output at the moment

>>>> Running the Code

    This code uses GPT-3.5.

    Configure Environment: 
        Smart_Learning folder in vs code
        Run conda create --name smart_learning python=3.11

    Install Dependencies: 
        Run pip install crewai
        Run pip install crewai_tools
        Run pip install pymongo

    Execute the Script: 
        Run python main.py


>>>> Execution: 

    Running the Script: Execute python main.py


>>>> About Project : 

    The project was made using CrewAI with following Agents, Tasks, Tools, Inputs, Outputs...

    Tasks : 
    1.
    Name : Search_For_Me
    Description : Search the courses and resources for students to provide them 
    Agent : Get_Resource_Agent
    Input : Search_Course,
            Career_Goal, 
            Learning_Preference
    Output : Resources list or links that are recommended for user search
    Async : true
    Tools : web_search


    2.
    Name : What_Next
    Description : Ask the user to give few details to predict and show them them what can be their next step in choosing future tasks as results
    Agent : Show_Career_Agent
    Input : search_course
    Output : Resources list or links that are recommended after for user search
    Async : true
    Tools : web_Search


    3.
    Name : Career_Path
    Description : Ask the user to give few details of his career , and suggest the path to reach it
    Agent :  Show_path_Agent
    Input : Career_Goal
    Output : Steps to follow for the user to reach his career goal
    Async : true
    Tools : web_search


    4.
    Name : Study_Plan
    Description : Ask the user to give few details of his subjects,goal,no. of hours he can spend and suggest a suitable study plan to reach it
    Agent :  Study_Planner_Agent
    Input : Subjects, no. of hours,date of completion, Career_Goal
    Output : A study plan for user to follow by splitting the times in an optimal way
    Async : true
    Tools : web_search


    5.
    Name : Search_History
    Description : Shows the search history of the user if he wants to see , if the user is new to the application, it will just gives a welcome message
    Agent : Recap_Agent 
    Input : No input
    Output : shows the options/choice selected by the user before and the outputs of them
    Async : true


    6.
    Name : Track_the_Progress
    Description : Shows the previous study plan with the status, and allows users to update the time and status
    Agent : Progress_Tracker_Agent 
    Input : new time update, new status update
    Output : shows the updated study plan
    Async : true


