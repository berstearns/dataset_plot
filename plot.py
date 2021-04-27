def match(device1, device2, matches):
    for t1 in device1['timestamps']:
        for t2 in device2['timestamps']:
            same_time = t1["timestamp_stop"] == t2["timestamp_stop"]
            same_x = float(t1["x"]) - float(t2["x"]) < 0.001
            same_y = float(t1["y"]) - float(t2["y"]) < 0.001
            if(same_y and same_x and same_time):
                match_id = f'{t1["id_user"]}:{t2["id_user"]}'
                if matches.get(match_id,False):
                    latest_match = matches[match_id][-1]
                    time_delta = int(t1["timestamp_stop"])-int(latest_match)
                    if(time_delta > 6*60*60 ):
                        matches[match_id].append(t1["timestamp_stop"])
                else:
                    matches[match_id] =  [t1["timestamp_stop"]]
                    print(len(matches))
    return matches

devices = {}
timestamps = []
matches = {}
degrees = {}
graph = {}

with open("./private_devices/private_mobile_devices.csv") as inpf:
    header = inpf.__next__().replace("\n","").split(",")
    print(header)
    for line in inpf:
        timestamp_device = dict(zip(header,line.replace("\n","").split(",")))
        timestamps.append(timestamp_device["timestamp_start"])
        timestamps.append(timestamp_device["timestamp_stop"])
        if devices.get(timestamp_device["id_user"], False):
            devices[timestamp_device["id_user"]]["timestamps"].append(timestamp_device)
        else:
            devices[timestamp_device["id_user"]] = {
                        "id" : timestamp_device["id_user"], 
                        "adjacents_nodes": [],
                        "timestamps": [timestamp_device]
                    }
    timestamps = set(timestamps)

for device1_id in devices.keys():
    for device2_id in devices.keys():
        if (device1_id != device2_id):
           if len(matches) >= 2000:
              break 
           matches = match(devices[device1_id], devices[device2_id], matches) 

for match_id in matches.keys():
    if len(matches[match_id]) >= 2:
        id1,id2 = match_id.split(":")
        if graph.get(id1, False):
                graph[id1].append(id2)
        else:
                graph[id1] = [id2]

        if graph.get(id2, False):
                graph[id2].append(id1)
        else:
                graph[id2] = [id1]

for node_id, adjacency_list in graph.items():
    degree = len(adjacency_list)
    if degrees.get(degree,False):
        degrees[degree] +=1
    else:
        degrees[degree] = 1

import seaborn
from matplotlib.pyplot import show
import matplotlib
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
x = [x for (x,_) in degrees.items()]
y = [y for (_,y) in degrees.items()]
ax.scatter(x=x,y=y)

ax.set_xlabel(r'degrees', fontsize=15)
ax.set_ylabel(r'frequency', fontsize=15)
ax.set_title('degrees x frequency')

ax.grid(True)
fig.tight_layout()

show()
