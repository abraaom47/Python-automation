# Python-automation
Python scripts that automatically make changes to users' registration data. 


This is a test tool to change employees' registration data in three different platforms whenever they leave the company or get transferred to another team.

The scripts open Chrome, log in to the two different websites the company uses, search for the employees' data and make the necessary changes - one script disables the employee's credentials when they leave the company, the other one changes the data of the employee's supervisor when they change teams.

Once the changes in those two websites are done, the scripts connect to the company's internal database and make the changes there as well. 
