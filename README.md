# CISC-121-Project
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

Pattern Recognition:

Abstraction

Algorithmic Design

Flowchart:

Testing:

Test Run Videos:

