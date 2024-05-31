import pandas as pd
import json
import os

DIR_PATH = "../dataset"
COLS = ['segxmentId','speedLimit', 'frc', 'streetName', 'distance', 'shape']
SEGMENT_TIME_COLS = ['harmonicAverageSpeed', 'medianSpeed', 'averageSpeed', 'standardDeviationSpeed', 'travelTimeStandardDeviation', 'sampleSize', 'averageTravelTime', 'medianTravelTime', 'travelTimeRatio']

if __name__ == "__main__":
    files = [f for f in os.listdir(DIR_PATH)]
    streets_list = []
    for file_name in files:
        with open(DIR_PATH + "/" + file_name, 'r') as file:
            data = json.load(file)

        df = pd.json_normalize(data)

        day = df.loc[0]['timeSets'][0]['dayToTimeRanges'][0]['dayOfWeek']
        hour_interval = df.loc[0]['timeSets'][0]['dayToTimeRanges'][0]['timeRanges'][0]

        # Iterasi setiap hasil/jalan dari suatu file
        for obj in df.loc[0]['network.segmentResults']:
            if obj['segmentTimeResults'][0]['sampleSize'] == 0 or ('streetName' not in obj):
                continue
            street_info = dict()
            street_info['day'] = day 
            street_info['hour_interval'] = hour_interval
            
            for col in COLS:
                street_info[col] = obj[col]

            for col in SEGMENT_TIME_COLS:
                street_info[col] = obj['segmentTimeResults'][0][col]

            streets_list.append(street_info)
    pd.DataFrame(streets_list).to_csv(f"cleaned_jakarta_traffic.csv")

        