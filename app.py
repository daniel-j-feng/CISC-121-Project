import gradio as gr
import matplotlib.pyplot as plt

stopNames = []
stopCounts = []

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
        return;
    pivot = (low + high)//2
    stopCounts[pivot], stopCounts[high] = stopCounts[high], stopCounts[pivot]
    pivotLocation = high
    newPivotLocation = low
    for i in range(low,high):
        if stopCounts[i] < stopCount[pivotLocation]:
            stopCounts[i], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[i]
            newPivotLocation += 1
    stopCounts[pivotLocation], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[pivotLocation]
    sortStopsQuick(newPivotLocation + 1, high)
    sortStopsQuick(low, newPivotLocation - 1)
    



with gr.Blocks() as app:
    with gr.Row():
        name_in = gr.Textbox(label="Stop Name")
        count_in = gr.Number(label="Crowd Count")
    add_btn = gr.Button("Add Stop")
    remove_in = gr.Textbox(label="Remove Stop by Name")
    remove_btn = gr.Button("Remove Stop")
    chart = gr.Plot()

    add_btn.click(addStop, [name_in, count_in], chart)
    remove_btn.click(removeStop, remove_in, chart)

app.launch()