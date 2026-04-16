import gradio as gr
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Patch

stopNames = []
stopCounts = []
frames = []
current_frame = [0]
global optimalStop
optimalStop = "None" 

def addStop(name, count):
    if not name or name.strip() == "":
        raise gr.Error("Please enter a stop name")
    if count is None:
        raise gr.Error("Please enter a crowd count")
    if count != int(count) or count < 0:
        raise gr.Error("Whole numbers only!")
    for i in range(len(stopNames)):
        if name == stopNames[i]:
            raise gr.Error("Stop Already Exists")
    stopNames.append(name)
    stopCounts.append(int(count))
    return plotStops()

def removeStop(name):
    for i in range(len(stopNames)):
        if name == stopNames[i]:
            idx = stopNames.index(name)
            stopNames.pop(idx)
            stopCounts.pop(idx)
            return plotStops()
    raise gr.Error("Stop Does Not Exist")

def plotStops():
    fig, ax = plt.subplots()
    ax.bar(stopNames, stopCounts, color="steelblue")
    ax.set_xlabel("Stop"); ax.set_ylabel("Crowd Count")
    return fig

def sortStopsQuick(low, high):
    if low >= high:
        return plotStops()
    pivot = (low + high)//2
    stopCounts[pivot], stopCounts[high] = stopCounts[high], stopCounts[pivot]
    stopNames[pivot], stopNames[high] = stopNames[high], stopNames[pivot]
    pivotLocation = high
    newPivotLocation = low
    for i in range(low,high):
        if stopCounts[i] < stopCounts[pivotLocation]:
            frames.append((stopCounts.copy(), stopNames.copy(), i, i, newPivotLocation, pivotLocation, -1))
            stopCounts[i], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[i]
            stopNames[i], stopNames[newPivotLocation] = stopNames[newPivotLocation], stopNames[i]
            newPivotLocation += 1
        else:
            frames.append((stopCounts.copy(), stopNames.copy(), i, i, newPivotLocation, pivotLocation, -1))
    stopCounts[pivotLocation], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[pivotLocation]
    stopNames[pivotLocation], stopNames[newPivotLocation] = stopNames[newPivotLocation], stopNames[pivotLocation]
    frames.append((stopCounts.copy(), stopNames.copy(), -1, -1, -1, newPivotLocation, newPivotLocation))
    sortStopsQuick(newPivotLocation + 1, high)
    sortStopsQuick(low, newPivotLocation - 1)

def startSort():
    frames.clear()
    current_frame[0] = 0
    sortStopsQuick(0, len(stopCounts) - 1)
    optimalStop = stopNames[-1]

    if not frames: 
        yield plotStops(), f"<h1>Optimal stop to send shuttle: {optimalStop}</h1>"
        return

    for frame in frames:
        data, names, looking, swap1, swap2, pivot, justSwapped = frame
        colors = []
        for i in range(len(data)):
            if i == pivot:
                colors.append('orange')
            elif i == swap1:
                colors.append('purple')
            elif i == swap2:
                colors.append('pink')
            else:
                colors.append('steelblue')
        fig, ax = plt.subplots()
        ax.bar(names, data, color=colors)
        ax.set_xlabel("Stops")
        ax.set_ylabel("Count")
        legend_elements = [
            Patch(facecolor='orange', label='Pivot'),
            Patch(facecolor='purple', label='Current Pointer'),
            Patch(facecolor='pink', label='Tentative New Pivot Location'),
        ]
        ax.legend(handles=legend_elements, loc='upper left')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        yield fig, f"<h1>Optimal stop to send shuttle: {optimalStop}</h1>"
        time.sleep(1)

with gr.Blocks() as app:
    title = gr.HTML("<h1>Find Optimal Stop to Send Shuttle<h1>")
    with gr.Row():
        name_in = gr.Textbox(label="Stop Name")
        count_in = gr.Number(label="Crowd Count")
    add_btn = gr.Button("Add Stop")
    remove_in = gr.Textbox(label="Remove Stop by Name")
    remove_btn = gr.Button("Remove Stop")
    recommendation = gr.HTML(f"<h1>Optimal stop to send shuttle: {optimalStop}<h1>")
    sort_btn = gr.Button("Sort Stops")
    chart = gr.Plot()


    add_btn.click(addStop, [name_in, count_in], chart)
    remove_btn.click(removeStop, remove_in, chart)
    sort_btn.click(startSort, None, [chart, recommendation])
    
app.launch()