import pickle
import os
def load_devices():
    devices = {}
    with open("./private_devices/private_mobile_devices.csv") as inpf:
        header = inpf.__next__().replace("\n","").split(",")
        print(header)
        for line in inpf:
            timestamp_device = dict(zip(header,line.replace("\n","").split(",")))
            if devices.get(timestamp_device["id_user"], False):
                devices[timestamp_device["id_user"]]["timestamps"].append(timestamp_device)
            else:
                devices[timestamp_device["id_user"]] = {
                            "id" : timestamp_device["id_user"], 
                            "adjacents_nodes": [],
                            "timestamps": [timestamp_device]
                        }
    return devices

def list_matches(devices):
    matches = {}
    for device1_id in devices.keys():
        for device2_id in devices.keys():
            if (device1_id != device2_id):
               if len(matches) >= 20:
                  break 
               matches = match(devices[device1_id], devices[device2_id], matches) 
    return matches

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
def create_graph(matches):
    graph={}
    for match_id in matches.keys():
        if len(matches[match_id]) >= 1:
            id1, id2 = match_id.split(":")
            if graph.get(id1, False):
                    graph[id1].append(id2)
            else:
                    graph[id1] = [id2]
            if graph.get(id2, False):
                    graph[id2].append(id1)
            else:
                    graph[id2] = [id1]
    return graph

def create_degrees(graph):
    degrees = {}
    for node_id, adjacency_list in graph.items():
        degree = len(adjacency_list)
        if degrees.get(degree,False):
            degrees[degree] +=1
        else:
            degrees[degree] = 1
    return degrees


if os.path.exists("devices.pickle"): 
    devices = pickle.load(open("devices.pickle","rb"))
else:
    devices = load_devices()
    with open("devices.pickle","wb") as devices_file:
        pickle.dump(devices,devices_file)

if os.path.exists("matches.pickle"): 
    devices = pickle.load(open("matches.pickle","rb"))
else:
    matches = list_matches(devices)
    with open("matches.pickle","wb") as matches_file:
        pickle.dump(matches, matches_file)

if os.path.exists("graph.pickle"): 
    graph = pickle.load(open("graph.pickle","rb"))
else:
    graph = create_graph(matches)
    with open("graph.pickle","wb") as graph_file:
        pickle.dump(graph,graph_file)

if os.path.exists("degrees.pickle"): 
    degrees = pickle.load(open("degrees.pickle","rb"))
else:
    degrees = create_degrees(graph)
    with open("degrees.pickle","wb") as degrees_file:
        pickle.dump(degrees,degrees_file)



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
