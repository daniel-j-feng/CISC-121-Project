# CISC-121-Project
Problem: Looking for optimal stop to send additional shuttle bus.

Why Quicksort?:
Quicksort was selected due to it's implace sorting functionalities, and ease of visualisation. 
Quicksort has a lower space complexity, which means that there are less things stored, and less copies that are created
that have to be compiled and computed by the cache and computer. Hence it uses in place swaps to achieve this, which 
works a lot better with space and memory. When comparing against mergesort, it uses less space at a O(logN) space complexity
when compared to mergesort at O(n) space complexity. This means that temporary arrays are avoided. 
For the problem specifically, I wanted to use matplots to plot out a graph to show where things swap, and how they swap.
Functionally, quicksort worked a lot better for this due to it's in place swaps, and it was a lot easier to visualise in place
swaps on a graph as opposed to the dividing and remerging of subarrays. I could just show what two bars will be swapped, where
the pivot is, and where the pointers are looking at any given moment. Since this was my first time using Gradio, it made sense
to use frames to capture states, and then use coloured bars as focal points to show where things were swapping around without having
to add things to the array to show the array splitting apart before the sort. Additionally, I could simply attach the 
data associated with various shifts and changes to the actual quicksort algorithm, without needing to do extra with gradio to 
figure out how to make the visuals look nice, especially since i was aiming for functionality, and an end to end product that 
demonstrated my understanding for the quicksort algorithm, and to create something that I could show precisely how it worked.

Enforcement & User Visuals:
There are five inputs, in which three will always run properly no matter what. There are also two inputs that have enforcement measures
put into place, to make sure that all inputs made by the user meet the proper criteria. The two inputs that have these enforcement measures
are the stop inputs, and the stop removal input. For the stop input, there's a check to make sure that the stop does not already exist, and checks
to make sure that the data being entered follows the correct format, where something must be typed into the cells, and that the stop count
must be positive. For the stop removal, it was about making sure that the stop existed in the array for removal. As for user visuals, there are
two main visuals, one of which being a header showing which stop would be the best to send a shuttle bus to, based on the stop with the most people
waiting. The second visual is the graph, which dynamically shows where the data is in relativity to other data points, on each input and output
This graph also displays the simulation through colored bars. A legend is available, however to iterate again, when the sort button is pressed,
the array will begin it's quicksort. In this situation, the yellow bar represents the pivot value, a pink bar represents the current best pivot 
position identified by the code, and the purple bar represents where the pointer is currently located. Additionally, any swaps can be identifiable
by the presence of both a pink and purple highlight, by which after the pink highlight dissapears, signifies the completion of the swap. 

Problem Decomposition:
In this project, I identified four key segments that I had to address, being user inputs, the sorting function, outputs, and gradio setup/display.
In the user inputs section, I divided that problem into three smaller segments, being the interface elements for user interaction, 
functionality of the interface elements, and the storage of data that the user enters. In the sorting function, I divided the problem into three main
steps, which is the base case, the process that executes, and the recursive calls. Within the process, it was further broken down into identifying
the pivot, identifying situations where there is a swap, and then the swapping of datapoints based on the principles of a quicksort. Outputs were
divided into two main segments that i wanted to figure out, being visual outputs, and data outputs from each function. Finally, the gradio setup/display
was divided into two main problems I wanted to address, being how to set up the display such that the gradio would function if it were present, and 
how to organise all the buttons such that it looked visually appealing, and would be easily figured out by users. 

Pattern Recognition:
Within the quicksort algorithm, there are five main patterns that are addressed. The pivot is repeatedly chosen as the middle of the array, or 
subarray within the subsequent recursive calls. The partitioning is done using two pointers, one of which points to the next best pivot
location, and the other pointer goes through each element, and decides whether or not it needs to be swapped to a position behind the first
pointer. The two arrays are both synchronised in parallel, to make sure that stop names and stop counts line up together. The entire process I 
outlined is repeated in each subsequent recursive call, in which both sides of the array after the pivot is put back in place is sorted again. 
Finally, the last thing that repeats constantly is the framesnapshots which send data back to Gradio for use in the display functions. 

Abstraction:
The things that should be shown to the user should simply be the inputs and the outputs. They should only be able to see what they inputted, 
the current data as is, the best locaiton to send a shuttle, and the sorting process. They should not be able to see the gradio display update process,
nor the process of plotting the data. Additionally, they should not be able to see how exactly data is being cleared, added to, or removed from the 
dataset, where they should not be abel to see what could trigger error messages etc. 

Algorithmic Design:
The inputs required are the stops with the stop count, stop removal, clearing stops, resetting the stops to the default demo values, and the 
button that allows one to sort the stops. Each would have it's own functions, in which the processes would run, and output the graph's animations
playing out, and the newest optimal stop to send a shuttle bus to. With regard to the GUI, it should be organised such that the option to add 
stops comes first, with the stop name and stop crowd count inputs being in a row next to one another, and a button below it to input it into the database.
There should be the option to just set it to the default demo values, which is a button below that. And even below that, there should be an input
textbox that allows users to type in a stop they want to remove by name, and then the button to execute that function. Finally, at the very bottom, there
should be an option to clear the entire array, and a button to sort. Before the clear button, there should be a display showing where the optimal stop is. And
finally, at the very bottom, there should be a visual display of how the quicksort is playing out, and where the data is. 

Testing:
Test One: Inputting a negative number into the array.
Expected: Error thrown
Actual: Negative number got into the array, and upon the pressing of the sort button, the function broke, and threw a default gradio error.

Test Two: Interrupting the sort by pressing the sort button and then pressing another button such as clear array before the sort display has finished up with it's activities
Expected: Sorting display clears, and new display comes in
Actual: Sorting display disappears for a moment, and then comes right back in

Test Three: Trying to add a stop that does not have a name.
Expected: Error thrown, 'Please enter a stop name'
Actual: Error thrown, 'Please enter a stop name'

Test Four: Trying to add a stop with the same name as another stop that already exists
Expected: Error thrown, 'Stop already exists'
Actual: Error thrown, 'Stop already exists'

Test Run Videos:
Test two run video (view the code files on GITHUB):
<video controls src="20260416-0349-36.9741334.mp4" title="Title"></video>

## Steps to Run
Install gradio, matplot, and time through the terminal
Run python3 app.py on terminal (from codespace)

## Hugging Face Link

## Author & AI Acknowledgment
