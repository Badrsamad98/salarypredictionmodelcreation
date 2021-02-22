import pandas as pd

data = pd.read_csv("glassdoor_jobs.csv", index_col=0)

# salary parsing
data['hourly'] = data['Salary Estimate'].apply(
    lambda x: 1 if 'per hour' in x.lower() else 0)
data['employer_provided'] = data['Salary Estimate'].apply(
    lambda x: 1 if 'employer provided salary' in x.lower() else 0)

data = data[data['Salary Estimate'] != '-1']
salary = data['Salary Estimate'].apply(lambda x: x.split('(')[0])

remove_K_Dollar = salary.apply(lambda x: x.replace('K', '').replace('$', ''))

remove_hour_provided = remove_K_Dollar.apply(lambda x: x.lower().replace(
    'per hour', '').replace('employer provided salary:', ''))

data['minimum_salary'] = remove_hour_provided.apply(
    lambda x: int(x.split('-')[0]))
data['maximum_salary'] = remove_hour_provided.apply(
    lambda x: int(x.split('-')[1]))
data['average_salary'] = (data.minimum_salary+data.maximum_salary)/2

# Company Name
data['company_name_txt'] = data.apply(
    lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)  # rows

# State of the job

data['job_state'] = data['Location'].apply(lambda x: x.split(',')[1])
data.job_state.value_counts()

data['same_state'] = data.apply(
    lambda x: 1 if x.Location == x.Headquarters else 0, axis=1)  # rows
# Age of the company

data['Age of the company'] = data.Founded.apply(
    lambda x: x if x <= 0 else 2021 - x)


# Data Science tools in the job description

# python
data["Python"] = data['Job Description'].apply(
    lambda x: 1 if 'python' in x.lower() else 0)
print(data.Python.value_counts())
# R studio
data['R_studio'] = data['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower(
) or 'r-studio' in x.lower() or 'r_studio' in x.lower() else 0)
print(data.R_studio.value_counts())

# spark
data['spark'] = data['Job Description'].apply(
    lambda x: 1 if 'spark' in x.lower() else 0)
print(data.spark.value_counts())

# aws
data['aws'] = data['Job Description'].apply(
    lambda x: 1 if 'aws' in x.lower() else 0)
print(data.aws.value_counts())

# excel
data['excel'] = data['Job Description'].apply(
    lambda x: 1 if 'excel' in x.lower() else 0)
print(data.excel.value_counts())

data.to_csv('data_cleaned.csv', index=False)
