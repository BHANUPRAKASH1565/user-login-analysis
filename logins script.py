import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta

# Generate sample data
np.random.seed(0)  # For reproducibility

# Define sample size
num_records = 100

# Create random device IDs, user IDs, and timestamps
device_ids = [f'device_{i}' for i in range(1, 6)]
user_ids = [f'user_{i}' for i in range(1, 11)]

data = {
    'deviceId': np.random.choice(device_ids, num_records),
    'userId': np.random.choice(user_ids, num_records),
    'logged_in': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 180)) for _ in range(num_records)],
    'logged_out': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(180, 360)) for _ in range(num_records)],
    'lastOpenedAt': [datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 360)) for _ in range(num_records)]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert columns to datetime
df['logged_in'] = pd.to_datetime(df['logged_in'])
df['logged_out'] = pd.to_datetime(df['logged_out'])
df['lastOpenedAt'] = pd.to_datetime(df['lastOpenedAt'])

# Calculate login duration
df['login_duration'] = df['logged_out'] - df['logged_in']

# Find the last accessed device for each user
latest_device = df.groupby('userId').apply(lambda x: x.loc[x['lastOpenedAt'].idxmax()])

# Check for overlapping login sessions
def check_overlap(group):
    overlaps = []
    for i, row1 in group.iterrows():
        for j, row2 in group.loc[i+1:].iterrows():
            if row1['logged_out'] > row2['logged_in']:
                overlaps.append((row1['deviceId'], row2['deviceId'], row1['userId']))
    return overlaps

overlaps = df.groupby('userId').apply(check_overlap).tolist()

# Aggregate data for summary
user_summary = df.groupby('userId').agg(
    total_login_time=pd.NamedAgg(column='login_duration', aggfunc='sum'),
    avg_session_duration=pd.NamedAgg(column='login_duration', aggfunc='mean')
).reset_index()

# Print the summary
print("User Summary:")
print(user_summary)

# Example: Plot distribution of login durations
plt.figure(figsize=(10, 6))
sns.histplot(df['login_duration'].dt.days, bins=30, kde=True)
plt.xlabel('Login Duration (days)')
plt.ylabel('Frequency')
plt.title('Distribution of Login Duration')
plt.show()

# Print the last accessed device information
print("Last Accessed Device for Each User:")
print(latest_device)

# Print overlaps
print("Detected Overlapping Sessions:")
for overlap in overlaps:
    print(f"User ID: {overlap[2]} had overlapping sessions between Device {overlap[0]} and Device {overlap[1]}")
