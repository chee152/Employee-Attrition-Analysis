import pandas as pd
import os

# Set working directory to the directory containing this script
base_dir = os.path.dirname(os.path.abspath(__file__))

# Define input file paths for check-in and check-out data
file_in_time = os.path.join(base_dir, 'HR Analytics Case Study', 'in_time.csv')
file_out_time = os.path.join(base_dir, 'HR Analytics Case Study', 'out_time.csv')

# Load the datasets into DataFrames
df_in_time = pd.read_csv(file_in_time)
df_out_time = pd.read_csv(file_out_time)

# Reshape the DataFrame from wide to long format
df_in_time_unpivot = pd.melt(df_in_time,id_vars=['EmployeeID'], var_name='Date',value_name='Time_in')
df_out_time_unpivot = pd.melt(df_out_time,id_vars=['EmployeeID'], var_name='Date',value_name='Time_out')

# Merge the two DataFrames on 'EmployeeID' and 'Date'
df_merge_time = pd.merge(df_in_time_unpivot,df_out_time_unpivot,on=['EmployeeID','Date'], how='inner')
df = df_merge_time.dropna()

# Convert the time strings to datetime objects
df['Time_in'] = pd.to_datetime(df['Time_in'])
df['Time_out'] = pd.to_datetime(df['Time_out'])

# Calculate the number of work hours (in hours) per day
df['Work_Hours'] = (df['Time_out'] - df['Time_in']).dt.total_seconds() / 3600

# Compute the average daily working hours per employee across the year 2015
df_work_time = df.groupby('EmployeeID')['Work_Hours'].mean().reset_index()

# Rename the column to 'Avg_Work_Hours'
df_work_time.rename(columns={'Work_Hours': 'Avg_Work_Hours'}, inplace=True)

# Export the result to a CSV file
output_file = os.path.join(base_dir, 'HR Analytics Case Study', 'work_time.csv')
df_work_time.to_csv(output_file, index=False)

print("File work_time.csv đã được tạo thành công!")