import gradio as gr
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Patch

stopNames = []
stopCounts = []
defaultStopNames = ["Guthrie at Joyce", "242 Guthrie Dr.", "Guthrie at Karlee", "118 Virginia St.", "80 Virginia St.", "Virginia at Sutherland", "Sutherland at Guthrie", "Sutherland at Conacher", "Conacher at Morenz", "Conacher at Wilson", "235 Conacher Dr.", "Conacher at Nicholas", "Benson at Division", "Division at First Canada", "John Counter at Rigney", "Bus Terminal", "Elliott at Douglas", "Elliott at Rockford", "Elliott at Division", "Division at Kirkpatrick", "Division at Barbara", "Division at Railway", "Division at Fraser", "Division at Guy", "Division at Adelaide", "Division at Pine", "Division at York", "Division at Colborne", "Princess at Barrie", "270 Princess St.", "Downtown", "Bagot at Johnson", "Bagot at Earl", "Bagot at West", "Stuart at Arch", "Queen's at Kingston General Hospital", "Grant Hall", "Union at Alfred", "Union at Albert", "Union at Victoria", "Union at Willingdon", "Union at Pembroke", "Queen's West Campus", "Union at Yonge", "King at Mowat", "King at McDonald", "King at Portsmouth", "Portsmouth at Baiden", "Portsmouth at Calderwood", "St. Lawrence College", "Southeast Public Health", "Portsmouth at Johnson", "Portsmouth at Miles", "Portsmouth at Van Order", "Portsmouth at Elmwood", "Portsmouth at Phillips", "Portsmouth at Fairview", "Portsmouth at Valleyview", "Portsmouth at Howard", "Portsmouth at Hampstead", "Portsmouth at Glengarry", "Portsmouth at Old Quarry", "VIA Rail Station"]
defaultStopCounts = [8, 5, 4, 4, 3, 4, 3, 4, 3, 3, 3, 4, 5, 6, 5, 35, 8, 6, 7, 8, 6, 6, 7, 6, 8, 7, 9, 10, 18, 14, 30, 10, 9, 8, 12, 28, 22, 12, 10, 9, 7, 7, 20, 8, 7, 6, 7, 6, 5, 40, 8, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5, 22]
frames = []
current_frame = [0]
global optimalStop
optimalStop = "None" 

def revertToDefault():
    stopNames.clear()
    stopCounts.clear()
    stopNames.extend(defaultStopNames)
    stopCounts.extend(defaultStopCounts)
    return plotStops()

def emptyStops():
    stopNames.clear()
    stopCounts.clear()
    return plotStops()

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
        time.sleep(0.6)

with gr.Blocks() as app:
    title = gr.HTML("<h1>Find Optimal Stop to Send Shuttle<h1>")
    with gr.Row():
        name_in = gr.Textbox(label="Stop Name")
        count_in = gr.Number(label="Crowd Count")
    revert_btn = gr.Button("Set Stops to Kingston Transit #2 Demo")
    add_btn = gr.Button("Add Stop")
    remove_in = gr.Textbox(label="Remove Stop by Name")
    remove_btn = gr.Button("Remove Stop")
    clear_btn = gr.Button("Clear Stops")
    recommendation = gr.HTML(f"<h1>Optimal stop to send shuttle: {optimalStop}<h1>")
    sort_btn = gr.Button("Sort Stops")
    chart = gr.Plot()

    revert_btn.click(revertToDefault, None, chart)
    add_btn.click(addStop, [name_in, count_in], chart)
    remove_btn.click(removeStop, remove_in, chart)
    clear_btn.click(emptyStops, None, chart)
    sort_btn.click(startSort, None, [chart, recommendation])
    
app.launch()