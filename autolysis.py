# Import necessary libraries
import numpy as np  # For numerical operations like arrays and math functions
import matplotlib.pyplot as plt  # For data visualization using plots
import seaborn as sns  # For enhanced data visualization (works with Matplotlib)
import pandas as pd  # For data manipulation and analysis (especially with DataFrames)
import requests  # For sending HTTP requests (needed to query the AI API)
import json  # For parsing and handling JSON data
import os  # For interacting with the operating system (especially environment variables)
import chardet #For different types of encodings

# Setting up the environment variable to securely store your API token
# This makes sure that the token is retrieved from the environment, rather than hardcoded in the code.
AIPROXY_TOKEN = os.environ["AIPROXY_TOKEN"]  # Retrieves the API token securely from environment variables

# Importing requests and os again, though already imported earlier. This seems redundant and might be an oversight.
import os
import requests

# Define the function that queries the LLM (Language Learning Model)
def query_llm(prompt):
    """
    Function to send a request to the AI API with a given prompt and retrieve the response.
    
    Arguments:
    prompt: The input text to send to the AI model.
    
    Returns:
    The AI's response to the prompt, or an error message if the request fails.
    """
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"  # API endpoint URL
    headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",  # Authentication header with API token
        "Content-Type": "application/json"  # Setting the content type as JSON for the API
    }
    
    # The data to be sent with the request: it contains the model details and the messages (conversation)
    data = {
        "model": "gpt-4o-mini",  # Model identifier (chat-based model)
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},  # System message setting context
            {"role": "user", "content": prompt}  # User's prompt to the model
        ]
    }

    # Sending the POST request to the API
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.reason}\nDetails: {response.text}"

    # Try to extract the AI's response from the returned JSON, handling any issues if they arise
    try:
        return response.json()['choices'][0]['message']['content']  # Extract the AI's content from the response
    except (KeyError, IndexError):
        return f"Unexpected response format: {response.json()}"  # Return error if the response structure is unexpected

# Reading the dataset (CSV file) into a Pandas DataFrame
with open('dataset.csv', 'rb') as file:
    raw_data = file.read(10000)  # Read a sample of the file
    detected_encoding = chardet.detect(raw_data)['encoding'] #chardet was used to decide the encoding of the dataset

# Read the CSV file using the detected encoding
df = pd.read_csv('dataset.csv', encoding=detected_encoding)
df.head()  # Display the first few rows of the dataset (default 5 rows)

# Displaying summary statistics for all columns (numerical and non-numerical)
df.describe(include='all')  # Describes the dataset, including object columns

# Checking for missing values (NaNs) in each column
df.isnull().sum()  # Counts the number of missing values in each column

# Checking the data types of all columns in the dataset
df.dtypes  # Displays the datatype of each column in the dataset

# Dropping rows with missing values (NaNs)
df = df.dropna()  # Removes rows that contain any missing values

# Selecting only the numeric columns for correlation analysis
numeric_df = df.select_dtypes(include=['number'])  # Selects only columns with numeric data types

# Creating a correlation matrix to see the relationships between numeric columns
correlation_matrix = numeric_df.corr()  # Computes the correlation matrix of numeric columns

# Plotting the correlation matrix as a heatmap
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')  # Visualizing the correlation matrix
plt.show()  # Display the heatmap

# Calculating the percentage of missing values for each column
missing_values = df.isnull().mean() * 100  # Calculates the percentage of missing values
print("Percentage of missing values:\n", missing_values)  # Prints the result

# Displaying example values from each column (up to 5 unique non-null values per column)
example_values = {col: df[col].dropna().unique()[:5] for col in df.columns}  # Extracts example values
print("Example values from columns:", example_values)  # Prints the example values

# Loop to create boxplots for outlier detection in numeric columns
for col in df.select_dtypes(include=['float', 'int']):  # Loops over numeric columns only
    sns.boxplot(x=df[col])  # Creates a boxplot for the column
    plt.title(f"Outliers in {col}")  # Adds a title with the column name
    plt.show()  # Displays the plot

# Constructing the prompt for the AI model, summarizing the dataset structure and asking for relevant analysis
prompt = f"""
Here is the dataset's structure:
- Column names and types: {df.dtypes.to_dict()}  # Converts data types to a dictionary and adds to the prompt
- Example values: {example_values}  # Adds the example values to the prompt
- Summary statistics: {df.describe().to_dict()}  # Adds summary statistics to the prompt

The dataframe is already generated name df. Use that. No need to load the dataset again
Give me python code to do the following if it is relevant on this dataset. I have given you the summary of the data. Do those analysis from the following that you find are relevant for this particular data set :
1. Outlier and Anomaly Detection: You might find errors, fraud, or high-impact opportunities.
2. Correlation Analysis, Regression Analysis, and Feature Importance Analysis: You might find what to improve to impact an outcome.
3. Time Series Analysis: You might find patterns that help predict the future.
4. Cluster Analysis: You might find natural groupings for targeted marketing or resource allocation.
5. Geographic Analysis: You might find where the biggest problems or opportunities are.
6. Network Analysis: You might find what to cross-sell or collaborate with.
Just give me the code in such a way that I can execute it using function calls directly, without copying the code into cell
Please note that you need to identify the datatypes and perform accordingly.
VERY IMPORTANT:
1. Outlier and anomaly analysis only for numeric data columns, exclude non-numeric columns to avoid errors.
2. Correlation regression, feature importance analysis only for numeric data columns, exclude non-numeric columns to avoid errors.
3. Cluster analysis can be done only for numeric data columns, exclude non-numeric columns to avoid errors.
4. Ensure the 'date' column is properly parsed as a datetime object for time series analysis, and exclude it from numeric analyses.
5. DO NOT ATTEMPT TO PERFORM SUCH OPERATIONS ON COLUMNS THAT HAVE NON NUMERIC DATATYPES
Keep a check for that
So accordingly identify all the data types and perform relevant analysis on them
Also call the function in the code itself no need to comment it out
Also Include code to:
- Save all generated charts as PNG files in the current directory.
- Use a fixed size of 512x512 pixels for each chart.
Do not add any extra text like "Here's a python code..." as this will make it difficult to auto execute the code using function call. Or if u want to add any such text such add it with # so that it gets commented out
Also do not add the ```python at the beginning and ``` at the end as that also hinders the execution
"""
# Sending the above prompt to the AI model and retrieving the response
llm_response = query_llm(prompt)  # Sends the query to the AI API and stores the response
print(llm_response)  # Prints the AI's response (Python code) for review

# Executing the code returned by the AI model
llm_code = llm_response  # The code received from the AI model is stored here
exec(llm_code)  # Executes the AI-generated code

# Constructing a summary prompt for the storytelling part of the analysis
summary_prompt = f"""
Based on the following data:
- Summary statistics: {df.describe().to_dict()}  # Adds summary statistics for storytelling
- Correlation analysis: {correlation_matrix.to_dict()}  # Adds correlation analysis data
- Missing values: {missing_values.to_dict()}  # Adds missing value percentages

You performed :
Outlier and Anomaly Detection
Correlation Analysis, Regression Analysis, and Feature Importance Analysis
Time Series Analysis
Cluster Analysis

Now do a story telling on :
The data you received, briefly
The analysis you carried out
The insights you discovered
The implications of your findings (i.e. what to do with the insights)

"""
# Sending the summary prompt to the AI model for narrative generation
narrative = query_llm(summary_prompt)  # Gets the narrative summary from the AI model

# Print the narrative for verification (optional)
print("Analysis Story:\n", narrative)  # Prints the AI-generated narrative to the console

# Save the narrative as a README.md file
with open('README.md', 'w') as file:  # Opens the README.md file in write mode
    file.write(narrative)  # Writes the narrative into the README.md file

print("Story saved to README.md.")  # Notifies the user that the story has been saved successfully
