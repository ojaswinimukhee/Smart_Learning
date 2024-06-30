from crewai import Task
from agents import Get_Resource_Agent , Show_Career_Agent , Show_path_Agent , Study_Planner_Agent , Recap_Agent ,Progress_Tracker_Agent


#Task-01....................#############################################################################################################################

Search_For_Me = Task(
    description="Conduct thorough research to identify high-quality study resources for the topic '{search_course}."
                "Focus on providing resources that only  belongs to '{search_course}', that align with the user's career goal of '{career_goal}' and their preferred learning style of '{learning_preference}."
                "The resources should include a mix of blogs, articles, and video links that are reputable and highly rated."
                "If the user is not satisfied with the provided resources, and say sent a feedback, get some new resources according to the user",
    expected_output=''' A curated list of study materials tailored to the user's learning preference of '{learning_preference}'.
                Each entry should include the title, a link to the resource, and a brief description of why it was chosen.

                Example Output:

                ## Recommended Study Materials in {learning_preference} Format

                1) Title of Resource 1 - [link]
                  _Description_: A brief description of why this resource is recommended and how it helps in achieving the career goal '{career_goal}'.

                2) Title of Resource 2 - [link]
                  _Description_: A brief description of why this resource is recommended and how it helps in achieving the career goal '{career_goal}'.

                3) Title of Resource 3 - [link]
                  _Description_: A brief description of why this resource is recommended and how it helps in achieving the career goal '{career_goal}'.

                Ensure the resources are relevant, engaging, and provide valuable information to help the user progress in their learning journey.
                ''',
    agent= Get_Resource_Agent,
    output_file= 'recommended_material.txt'
)


#Task-02....................########################################################################################################################################

What_Next = Task(
    description="Conduct thorough research to identify the immediate next steps can taken after the course '{search_course}'."
                "Focus on providing resources that outline the next academic or professional steps required, such as entrance exams, certifications, or preparatory courses."
                "The resources should include a mix of blogs, articles, and video links that are reputable and highly rated."
                "If the user is not satisfied with the provided resources, and say sent a feedback, get some new resources according to the user",
    expected_output='''A curated list of the immediate next steps the user should take after '{search_course}'.
                Each entry should include the title and a brief description of why it was chosen.
                Example Output:

                ## Next Steps ....

                1) Title of Resource 1 - [link]
                  _Description_: A brief description of why this resource is recommended and what can be achieved through it.

                2) Title of Resource 2 - [link]
                  _Description_: A brief description of why this resource is recommended and what can be achieved through it.

                3) Title of Resource 3 - [link]
                  _Description_: A brief description of why this resource is recommended and  what can be achieved through it.

                Ensure the resources are relevant, engaging, and provide valuable information to help the user progress in their learning journey.
                ''',
    agent=Show_Career_Agent,
    output_file= 'recommended_material.txt'
)



#Task-03....................#########################################################################################################################################################################################


Career_Path = Task(
    description="Conduct thorough research to identify best path, so that the user can reach his career goal of '{career_goal}'."
                "Focus on providing the step by step process of reaching the user's career goal of '{career_goal}'."
                "If the user is not satisfied with the provided resources, and say sent a feedback, get some new resources according to the user",
    expected_output='''A curated list of exams that need to clear to reach '{career_goal}'  .
                Each entry should include the title and a brief description of why it was chosen..
                Example Output:

                ## Recommended steps for reach your goal

                1) Title of exam/course/step 1 - [link]
                  _Description_: A brief description of why this exam/course/step is recommended and how it helps in achieving the career goal '{career_goal}'.

                2) Title of exam/course/step 2 - [link]
                  _Description_: A brief description of why this exam/course/step is recommended and how it helps in achieving the career goal '{career_goal}'.

                3) Title of exam/course/step 3 - [link]
                  _Description_: A brief description of why this exam/course/step is recommended and how it helps in achieving the career goal '{career_goal}'.

                Ensure the exams or steps are relevant, engaging, and provide valuable information to help the user progress in their achieving journey.
                ''',
    agent= Show_path_Agent,
    output_file= 'recommended_material.txt'
)


#Task-04....................#####################################################################################################################################################################################################


Study_Plan = Task(
    description="Conduct thorough research on the each topic '{topics}' to identify the subtopics to a lot the time for the user, so that the user can possibly complete all the topics in tine '{max_hours}."
                "Focus on splitting the time '{max_hours}' in minutes/hours, so that the user can complete and get a quality time for each topic and must complete in time '{max_hours}'."
                "Keep the value os status as not done for every topic so that the user can get access to change the time and status of the topic in agent and task 6",
    expected_output='''A curated list of topics that the user given to complete in time '{max_hours}" .
                Each entry should include the topic name , time given for it and a brief description of why the user have to spend that much of time on it..
                Example Output:

                ## On analyzing the list of topics you have to complete, I suggest you the following plan

                1) name of the topic 1 - [number of hours/minutes/seconds] - not done
                  _Description_: A brief description of why this topic from topics {topics} is recommended for the user to give this much of time'.

                2) name of the topic 2 - [number of hours/minutes/seconds] - not done
                  _Description_: A brief description of why this topic from topics {topics} is recommended for the user to give this much of time'.
                
                3) name of the topic 3 - [number of hours/minutes/seconds] - not done
                  _Description_: A brief description of why this topic from topics {topics} is recommended for the user to give this much of time'.
                 
                
                ## Start working...... Happy learning
                ''',
    agent=Study_Planner_Agent,
    output_file= 'recommended_material.txt'
) 


#Task-05....................##################################################################################################################################################################

Search_History = Task(
    description="Remember the user's previous tasks and outputs to show them again if they need.",
    expected_output='''Gather the information and output of user previous tasks minimum upto five tasks
                Example Output:
                
                if the user have no search history :
                ## Hello friend, you are new here....
                
                else : 

                ## Your Search History >>>>>

                1) {Task_1} : {output_file}
                
                2) {Task_2} : {output_file}
                
                3) {Task_3} : {output_file}
                
                4) {Task_4} : {output_file}
                
                5) {Task_5} : {output_file}

                ''',
    agent=Recap_Agent
)

#Task-06....................##################################################################################################################################################################

Track_the_Progress = Task(
    description="Track the user's study progress based on their previous study plan all the topics '{topic}'. Display the study plan with the current status of each topic (done/not done/in progress) and allow the user to update the status. Save the updated progress.",
    expected_output='''Retrieve the user's previous study plan and display it along with the progress for each topic.

                Example Output:

                If the user has no previous study plan:
                ## Make a study plan... Track your progress...

                Otherwise:

                ## Your Progress >>>>>
                
                study plan 1 :
                
                1) {Topic_1} - {number of hours/minutes/seconds} - {done/not done/in progress}
                
                2) {Topic_2} - {number of hours/minutes/seconds} - {done/not done/in progress}
                
                3) {Topic_3} - {number of hours/minutes/seconds} - {done/not done/in progress}
                
                4) {Topic_4} - {number of hours/minutes/seconds} - {done/not done/in progress}
                
                5) {Topic_5} - {number of hours/minutes/seconds} - {done/not done/in progress}
                
                Allow the user to update the status for each topic. Save the final output.

                If all topics are marked as done, print a message:

                ## Great consistency... Good luck...
                ''',
    agent=Progress_Tracker_Agent,
    output_file='Recommended_material.txt'
)
