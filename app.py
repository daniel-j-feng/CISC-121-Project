import gradio as gr
import matplotlib.pyplot as plt

stopNames = []
stopCounts = []

def addStop(name, count):
    if name in stopNames:
        raise gr.Error("Stop Already Exists")
        return
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

def sortStopsQuick():


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