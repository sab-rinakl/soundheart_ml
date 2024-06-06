import json
import numpy as np
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer

# Define a function to extract and compute statistics of features from JSON data.
def extract_features(data):
    # Extract temperature and beats per minute data from the input dictionary.
    temp = data['temp']
    bpm = data['bpm']
    
    # Calculate and return a dictionary of statistical features for temperature and BPM.
    features = {
        'temp_max': np.max(temp),
        'temp_min': np.min(temp),
        'temp_avg': np.mean(temp),
        'temp_std': np.std(temp),
        'bpm_max': np.max(bpm),
        'bpm_min': np.min(bpm),
        'bpm_avg': np.mean(bpm),
        'bpm_std': np.std(bpm),
    }
    
    return features

# Lists to hold features and scores from multiple data points.
features_list = []
scores_list = []

# File paths to JSON files containing scores and times data.
scores_file_path = 'training-data/scores.json'
times_file_path = 'training-data/times.json'

# Load scores data from JSON file.
with open(scores_file_path, 'r') as scores_file:
    scores_data = json.load(scores_file)

# Load times data from JSON file.
with open(times_file_path, 'r') as times_file:
    times_data = json.load(times_file)

# Process each subject and activity to extract data and features.
for subject, activities in times_data.items():
    for activity, minute in activities.items():
        filename = f"training-data/{subject}_minute{minute}.json"
        
        # Check if the corresponding JSON file exists.
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            continue  # Skip to the next iteration if file does not exist.

        # Load JSON data from file.
        with open(filename, 'r') as file:
            data = json.load(file)

        # Extract features and store them along with the corresponding score.
        features = extract_features(data)
        features_list.append(features)
        scores_list.append(scores_data[subject][activity])

# Use DictVectorizer to convert feature dictionaries into a feature matrix.
vec = DictVectorizer()
X_train = vec.fit_transform(features_list).toarray()
y_train = np.array(scores_list)

# Prompt for and process input JSON data string to be used for testing.
test_json_str = input()
test_data = json.loads(test_json_str)
test_features = extract_features(test_data)
X_test = vec.transform(test_features).toarray()

# Initialize and train a RandomForestRegressor model.
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict the stress level using the model.
prediction = model.predict(X_test)

# Clip the prediction to the range 0-100.
if prediction[0] > 100:
    prediction[0] = 100
elif prediction[0] < 0:
    prediction[0] = 0

# Output the stress level along with average temperature and BPM from the test data.
print("{stress:", prediction[0], ", avg_temp:", test_features['temp_avg'], ", avg_bpm:", test_features['bpm_avg'], "}")
