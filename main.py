import re
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_file

# declare file path
file_path = './soal_chart_bokeh.txt'

timestamps = []
bitrate_list = []

# create regex based on data provide in file txt
timestamp_pattern = r"Timestamp:\s([\d-]+\s[\d:]+)"
bitrate_pattern = r"\d+\.\d+-\d+\.\d+\s+sec\s+[\d\.]+\s\w+Bytes\s+([\d\.]+\s\w+/sec)"

# read file
with open(file_path, 'r') as file:
    current_timestamp = None
    for line in file:
        # Extract timestamp
        timestamp_match = re.search(timestamp_pattern, line)
        if timestamp_match:
            current_timestamp = timestamp_match.group(1)
        
        # Extract bitrate
        bitrate_match = re.search(bitrate_pattern, line)
        if bitrate_match and current_timestamp:
            bitrate = bitrate_match.group(1)
            timestamps.append(current_timestamp)
            bitrate_list.append(bitrate)

# convert reading speed to mbps
def convert_to_mbps(bitrate_str):
    value, unit = bitrate_str.split()
    value = float(value)
    if unit == 'Kbits/sec':
        return value / 1000  # Convert to Mbits/sec
    elif unit == 'Mbits/sec':
        return value
    else:
        return None  # Unknown unit

bitrate_mbps = [convert_to_mbps(b) for b in bitrate_list]

data = pd.DataFrame({'Timestamp': pd.to_datetime(timestamps), 'Speed (Mbps)': bitrate_mbps})

# plot data using bokeh
output_file("speed_line_chart.html")

p = figure(title="Speed Bandwidth Over Time",
           x_axis_label="Timestamp",
           y_axis_label="Speed (Mbps)",
           x_axis_type='datetime',
           width=800,   
           height=400) 

p.line(data["Timestamp"], data["Speed (Mbps)"], line_width=2, color='navy', alpha=0.7)

show(p)
