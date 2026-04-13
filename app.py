import gradio as gr
import matplotlib.pyplot as plt

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
            frames.append((stopCounts.copy(), i, i, newPivotLocation))
            stopCounts[i], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[i]
            stopNames[i], stopNames[newPivotLocation] = stopNames[newPivotLocation], stopNames[i]
            newPivotLocation += 1
        else:
            frames.append((stopCounts.copy(), i, -1, -1))
    stopCounts[pivotLocation], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[pivotLocation]
    stopNames[pivotLocation], stopNames[newPivotLocation] = stopNames[newPivotLocation], stopNames[pivotLocation]
    sortStopsQuick(newPivotLocation + 1, high)
    sortStopsQuick(low, newPivotLocation - 1)

def sortAndDisplay():
    sortStopsQuick(0, len(stopCounts) - 1)
    fig, ax = plt.subplots()
    ax.bar(stopNames, stopCounts)
    ax.set_xlabel("Stops")
    ax.set_ylabel("Count")
    ax.set_title("Sorted Stop Counts")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def startSort():
    frames.clear()
    current_frame[0] = 0
    tempCounts = stopCounts.copy()
    tempNames = stopNames.copy()
    sortStopsQuick(0, len(stopCounts) - 1)
    stopCounts[:] = tempCounts
    stopNames[:] = tempNames
    return plotStops()

def nextStep():
    if current_frame[0] >= len(frames):
        return plotStops()
    data, looking, swap1, swap2 = frames[current_frame[0]]
    current_frame[0] += 1
    colors = []
    for i in range(len(data)):
        if i == looking:
            colors.append('yellow')
        elif i == swap1 or i == swap2:
            colors.append('red')
        else:
            colors.append('steelblue')
    fig, ax = plt.subplots()
    ax.bar(stopNames, data, color=colors)
    ax.set_xlabel("Stops")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

with gr.Blocks() as app:
    with gr.Row():
        name_in = gr.Textbox(label="Stop Name")
        count_in = gr.Number(label="Crowd Count")
    add_btn = gr.Button("Add Stop")
    remove_in = gr.Textbox(label="Remove Stop by Name")
    remove_btn = gr.Button("Remove Stop")
    sort_in = gr.Textbox(label = "Sort Stops by Crowd")
    sort_btn = gr.Button("Prepare Sorting")
    next_btn = gr.Button("Next Sort Step")
    chart = gr.Plot()

    add_btn.click(addStop, [name_in, count_in], chart)
    remove_btn.click(removeStop, remove_in, chart)
    sort_btn.click(startSort, None, chart)
    next_btn.click(nextStep, None, chart)
    
app.launch()