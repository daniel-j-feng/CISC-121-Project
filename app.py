import gradio as gr
import matplotlib.pyplot as plt
import time
from matplotlib.patches import Patch

#setting up variables and storage spaces that are required across the entire code
stopNames = []
stopCounts = []
defaultStopNames = ["Guthrie at Joyce", "242 Guthrie Dr.", "Guthrie at Karlee", "118 Virginia St.", "80 Virginia St.", "Virginia at Sutherland", "Sutherland at Guthrie", "Sutherland at Conacher", "Conacher at Morenz", "Conacher at Wilson", "235 Conacher Dr.", "Conacher at Nicholas", "Benson at Division", "Division at First Canada", "John Counter at Rigney", "Bus Terminal", "Elliott at Douglas", "Elliott at Rockford", "Elliott at Division", "Division at Kirkpatrick", "Division at Barbara", "Division at Railway", "Division at Fraser", "Division at Guy", "Division at Adelaide", "Division at Pine", "Division at York", "Division at Colborne", "Princess at Barrie", "270 Princess St.", "Downtown", "Bagot at Johnson", "Bagot at Earl", "Bagot at West", "Stuart at Arch", "Queen's at Kingston General Hospital", "Grant Hall", "Union at Alfred", "Union at Albert", "Union at Victoria", "Union at Willingdon", "Union at Pembroke", "Queen's West Campus", "Union at Yonge", "King at Mowat", "King at McDonald", "King at Portsmouth", "Portsmouth at Baiden", "Portsmouth at Calderwood", "St. Lawrence College", "Southeast Public Health", "Portsmouth at Johnson", "Portsmouth at Miles", "Portsmouth at Van Order", "Portsmouth at Elmwood", "Portsmouth at Phillips", "Portsmouth at Fairview", "Portsmouth at Valleyview", "Portsmouth at Howard", "Portsmouth at Hampstead", "Portsmouth at Glengarry", "Portsmouth at Old Quarry", "VIA Rail Station"]
defaultStopCounts = [8, 5, 4, 4, 3, 4, 3, 4, 3, 3, 3, 4, 5, 6, 5, 35, 8, 6, 7, 8, 6, 6, 7, 6, 8, 7, 9, 10, 18, 14, 30, 10, 9, 8, 12, 28, 22, 12, 10, 9, 7, 7, 20, 8, 7, 6, 7, 6, 5, 40, 8, 5, 4, 4, 4, 5, 4, 4, 4, 4, 4, 5, 22]
frames = []
current_frame = [0]
global optimalStop
optimalStop = "None" 

#Function to clear all data, and then set all data to the default data for testing and demonstration purposes
def revertToDefault():
    stopNames.clear()
    stopCounts.clear()
    stopNames.extend(defaultStopNames)
    stopCounts.extend(defaultStopCounts)
    return plotStops()

#Function to clear all stop data, and make sure that both arrays are emptied 
def emptyStops():
    stopNames.clear()
    stopCounts.clear()
    return plotStops()

#Function to add a stop based on user input to the database
def addStop(name, count):
    #If the name does not exist, or if the name is empty, raise error
    if not name or name.strip() == "":
        raise gr.Error("Please enter a stop name")
    #If a stop count is not specified, raise an error
    if count is None:
        raise gr.Error("Please enter a crowd count")
    #If the count is not an integer (whole number) or if it is not greater than zero, raise error
    if count != int(count) or count < 0:
        raise gr.Error("Whole numbers only!")
    #For loop to go through the entire stop names array
    for i in range(len(stopNames)):
        #Check if the name is already in the array, if it is, raise error
        if name == stopNames[i]:
            raise gr.Error("Stop Already Exists")
    #If everything else passes, add the new stop name and count to the arrays, and plot on graph
    stopNames.append(name)
    stopCounts.append(int(count))
    return plotStops()

#Function to remove a stop by it's name
def removeStop(name):
    #Loop through each stop name to check if the name exists, if it does, remove
    for i in range(len(stopNames)):
        if name == stopNames[i]:
            idx = stopNames.index(name)
            stopNames.pop(idx)
            stopCounts.pop(idx)
            return plotStops()
    #If stop name does not exist, raise error
    raise gr.Error("Stop Does Not Exist")

#Function to plot stops on the graph
def plotStops():
    fig, ax = plt.subplots()
    #Setting labels, names, colours and bars
    ax.bar(stopNames, stopCounts, color="steelblue")
    ax.set_xlabel("Stop"); ax.set_ylabel("Crowd Count")
    return fig

#Quicksort function to sort each stop based on the number of people waiting at each
def sortStopsQuick(low, high):
    #Base case: if the low index pointer is greater or equal to the high pointer, there is nothing left to sort, thus we return and plot the stops
    if low >= high:
        return plotStops()
    #Setting the pivot index to the middle of the array
    pivot = (low + high)//2
    #First step in quicksort, moving the pivot element out of the way by shifting it all the way to the right
    stopCounts[pivot], stopCounts[high] = stopCounts[high], stopCounts[pivot]
    stopNames[pivot], stopNames[high] = stopNames[high], stopNames[pivot]
    #Setting the new low and high indicies 
    pivotLocation = high
    newPivotLocation = low
    #Loop through all stop counts, from low to high indicies
    for i in range(low,high):
        #Check if stop counts at the current index is smaller than the pivot element, if it is, export the data to the display, and swap the elements
        if stopCounts[i] < stopCounts[pivotLocation]:
            frames.append((stopCounts.copy(), stopNames.copy(), i, i, newPivotLocation, pivotLocation, -1))
            stopCounts[i], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[i]
            stopNames[i], stopNames[newPivotLocation] = stopNames[newPivotLocation], stopNames[i]
            #Move onto the next location to check for a swap
            newPivotLocation += 1
        #Otherwise, send data to display frames, and do nothing
        else:
            frames.append((stopCounts.copy(), stopNames.copy(), i, i, newPivotLocation, pivotLocation, -1))
    #After everything is done, swap the pivot element into position, otherwise known as the place that the code stopped during the for loop, which represents a point at which everything to the right is larger than the pivot, and everything on the left is smaller than the pivot
    stopCounts[pivotLocation], stopCounts[newPivotLocation] = stopCounts[newPivotLocation], stopCounts[pivotLocation]
    stopNames[pivotLocation], stopNames[newPivotLocation] = stopNames[newPivotLocation], stopNames[pivotLocation]
    #Send data to the display frames 
    frames.append((stopCounts.copy(), stopNames.copy(), -1, -1, -1, newPivotLocation, newPivotLocation))
    #Recursive call for the left side (smaller than pivot) and the right side (larger than pivot) subarrays to continue the sorting process
    sortStopsQuick(newPivotLocation + 1, high)
    sortStopsQuick(low, newPivotLocation - 1)

#Function to stat the sort display process
def startSort():
    #Clear the frames, sort the stop, display the optimal stop
    frames.clear()
    current_frame[0] = 0
    sortStopsQuick(0, len(stopCounts) - 1)
    optimalStop = stopNames[-1]

    #if no data collected yet, set to default shuttle stop
    if not frames: 
        yield plotStops(), f"<h1>Optimal stop to send shuttle: {optimalStop}</h1>"
        return

    #Based on data provided by the quicksort function, recolour bars into specific colours to show sorting process
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
        #Setting individual bars, labels, and creating the legend
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
        #Slow down actions to display the sort in real time, and ensure that the sorting process completes before something else happens
        yield fig, f"<h1>Optimal stop to send shuttle: {optimalStop}</h1>"
        time.sleep(0.6)

with gr.Blocks() as app:
    #Creating elements that are ultimately displayed in the Gradio UI
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

    #Create button functionalities, and link inputs to the correct functions
    revert_btn.click(revertToDefault, None, chart)
    add_btn.click(addStop, [name_in, count_in], chart)
    remove_btn.click(removeStop, remove_in, chart)
    clear_btn.click(emptyStops, None, chart)
    sort_btn.click(startSort, None, [chart, recommendation])
    
app.launch()