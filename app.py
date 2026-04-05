import gradio as gr
import matplotlib.pyplot as plt

stop_names = []
stop_counts = []

def add_stop(name, count):
    stop_names.append(name)
    stop_counts.append(count)
    return plot_stops()

def remove_stop(name):
    if name in stop_names:
        idx = stop_names.index(name)
        stop_names.pop(idx)
        stop_counts.pop(idx)
    return plot_stops()

def plot_stops():
    fig, ax = plt.subplots()
    ax.bar(stop_names, stop_counts, color="steelblue")
    ax.set_xlabel("Stop"); ax.set_ylabel("Crowd Count")
    return fig

with gr.Blocks() as app:
    with gr.Row():
        name_in = gr.Textbox(label="Stop Name")
        count_in = gr.Number(label="Crowd Count")
    add_btn = gr.Button("Add Stop")
    remove_in = gr.Textbox(label="Remove Stop by Name")
    remove_btn = gr.Button("Remove Stop")
    chart = gr.Plot()

    add_btn.click(add_stop, [name_in, count_in], chart)
    remove_btn.click(remove_stop, remove_in, chart)

app.launch()