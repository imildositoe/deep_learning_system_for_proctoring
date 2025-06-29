"""This file contains functions to prepare the data"""
import os

"""Function to parse the mmss time into seconds in the ground truth txt file
@param mmss is the time in the gt.txt file
"""
def time_to_seconds(mmss):
    mm = int(str(mmss).zfill(4)[:2])
    ss = int(str(mmss).zfill(4)[2:])
    return mm * 60 + ss

"""Function to parse the gt file and return a list of dictionaries
@param gt_path is the path of the gt.txt file
"""
def gt_file_to_dict(gt_path):
    segments = []
    with open(gt_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                start = time_to_seconds(parts[0])
                end = time_to_seconds(parts[1])
                label = int(parts[2])

                segments.append({
                    "start_time_in_sec": start,
                    "end_time_in_sec": end,
                    "cheating_type": label
                })
    return segments

# Print the segments
gt_file_path = os.path.join(r'C:\Users\Dell 88\Desktop\OEP database\subject1', 'gt.txt')
cheating_dict = gt_file_to_dict(gt_file_path)
for item in cheating_dict[:5]:
    print(item)