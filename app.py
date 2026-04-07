import gradio as gr
import matplotlib.pyplot as plt

stop_names = []
stop_counts = []

def addStop(name, count):
    stop_names.append(name)
    stop_counts.append(count)
    return plotStops()

def removeStop(name):
    if name in stop_names:
        idx = stop_names.index(name)
        stop_names.pop(idx)
        stop_counts.pop(idx)
    return plotStops()

def plotStops():
    fig, ax = plt.subplots()
    ax.bar(stop_names, stop_counts, color="steelblue")
    ax.set_xlabel("Stop"); ax.set_ylabel("Crowd Count")
    return fig

def sortStops():


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