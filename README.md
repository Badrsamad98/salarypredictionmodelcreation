The goal of this project was to identify the different aspects that influence the salary of a data scientist in the USA.

First step: scrapping data from the web with Selinium.

scrapper.py: the script goes through job offers and scrapes the following data from the job listing:
Job title, Salary estimate, Job description, Rating, Company, Location, Size of the company, Founded date, Type of ownership, Industry, Sector and revenue.

Second step: cleaning the data

cleaning.py: the data needs be cleaned in order to be understandable and usable by our model.
In order to do so, I made the following changes: 
- Extract numeric data out of salary and create three columns: minimum salary, maximum salary and average salary. 
- Remove rows without salary.
- Create columns for employer provided salary and hourly wages.
- Extract rating out of company text.
- Make a new column for company state.
- Add a column if the job is in the company’s headquarters.
- Indicate the age of the company from the year of foundation
- Add a column with the listed skills in the job description (Python, R_studio, Excel, AWS, Spark)

Third step: EDA (Exploratory data analysis)

eda_cleaning.ipyb: I added two steps of data cleaning :
- Column for simplified job title and seniority 
- Column for description length 
Then I plotted the data to understand it better. I explored the data by varying different characteristics such as the age of the company, its size, the location, the skills required…

Last step: model building

model.py: import cleaned data and create a prediction model by evaluating different algorithms (linear regression, lasso regression, random forest). Choosing the best prediction model and saving it using Pickle.
