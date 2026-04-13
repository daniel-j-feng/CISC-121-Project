import gradio as gr
import matplotlib.pyplot as plt
import time

stopNames = []
stopCounts = []
frames = []
current_frame = [0]

def addStop(name, count):
    if name in stopNames:
        raise gr.Error("Stop Already Exists")
        return plotStops()
    else:
        stopNames.append(name)
        stopCounts.append(count)
        return plotStops()

def removeStop(name):
    if name in stopNames:
        idx = stopNames.index(name)
        stopNames.pop(idx)
        stopCounts.pop(idx)
    return plotStops()

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
    
    for frame in frames:
        data, names, looking, swap1, swap2, pivot, justSwapped = frame
        colors = []
        for i in range(len(data)):
            if i == pivot:
                colors.append('orange')
            elif i == justSwapped:
                colors.append('pink')
            elif i == swap1 or i == swap2:
                colors.append('purple')
            elif i == looking:
                colors.append('yellow')
            else:
                colors.append('steelblue')
        fig, ax = plt.subplots()
        ax.bar(names, data, color=colors)
        ax.set_xlabel("Stops")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        yield fig
        time.sleep(0.5)

with gr.Blocks() as app:
    with gr.Row():
        name_in = gr.Textbox(label="Stop Name")
        count_in = gr.Number(label="Crowd Count")
    add_btn = gr.Button("Add Stop")
    remove_in = gr.Textbox(label="Remove Stop by Name")
    remove_btn = gr.Button("Remove Stop")
    sort_in = gr.Textbox(label = "Sort Stops by Crowd")
    sort_btn = gr.Button("Sort Stops")
    chart = gr.Plot()

    add_btn.click(addStop, [name_in, count_in], chart)
    remove_btn.click(removeStop, remove_in, chart)
    sort_btn.click(startSort, None, chart)
    
app.launch()