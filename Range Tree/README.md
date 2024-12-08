# Tasks:  <br>

Check if the code can be simpler


# How the rangeTree.py works: <br>
----------------------------------------------------------------------------------------------------------------------------
Step 1: Build the Tree  <br>
The range tree is built by recursively splitting the points along the dimensions 
x, y, z, and w, cycling through the dimensions as depth increases.
<br>
<br>

At depth 0 (split by x):
<br>
Sort by x:

[(4.5, 95, 2020, 1),
(4.8, 97, 2020, 3),
(5.0, 94, 2019, 1),
(6.0, 96, 2021, 2),
(7.0, 98, 2021, 1)]

<br>
Median Point: (5.0, 94, 2019, 1).
<br>
<br>
Tree so far:
{
    point: (5.0, 94, 2019, 1),
    left: [...],
    right: [...]
}

<br>
<br>
<br>
<br>
At depth 1 (split by y): <br>
<br>
Left Subtree: <br>
Points: [(4.5, 95, 2020, 1), (4.8, 97, 2020, 3)].   <br>
Median Point: (4.8, 97, 2020, 3).                   <br>
<br>
Right Subtree: <br>
Points: [(6.0, 96, 2021, 2), (7.0, 98, 2021, 1)].   <br>
Median Point: (6.0, 96, 2021, 2).                   <br>
  
<br>
Tree structure:
<pre>
{
	point: (5.0, 94, 2019, 1),
	left: {
		point: (4.8, 97, 2020, 3),
		left: ...,
		right: ...
	},
	right: {
		point: (6.0, 96, 2021, 2),
		left: ...,
		right: ...
	}
}
</pre>



This process continues until all points are placed into leaf nodes.

---------------------------------------------------------------------------------------------------------------------------------------------------


Step 2: Query Execution <br>
<br>
<br>

Initialization: <br>
Start at the root node (5.0, 94, 2019, 1). <br>
Query range is x ∈ [4.0,6.0], y ∈ [94,96], z ∈ [2019,2021], w ∈ [1,2].   <br>

<br><br> <br>
At depth 0 (split by x):
<br>
Current node: (5.0, 94, 2019, 1).
<br>
Check if point is within the range:
<br>
5.0 ∈ [4.0,6.0]:    True      <br>
94 ∈ [94,96]:       True      <br>
2019 ∈ [2019,2021]: True      <br>
1 ∈ [1,2]:          True      <br>
Point is in range, add it to results: [(5.0, 94, 2019, 1)].    <br>
 <br> <br>
Traverse left because 4.0 ≤ 5.0.    <br>
Traverse right as well because 6.0 ≥ 5.0.

 <br> <br> <br>

At depth 1 (split by y):
 <br>
Left Subtree: <br>
Current node: (4.8, 97, 2020, 3). <br>
Check if point is within the range: <br>
4.8 ∈ [4.0,6.0]: True    <br>
97 ∈ [94,96]:    False    <br>
Point is out of range, do not add to results.  <br>
 <br>
Traverse left and right subtrees of (4.8, 97, 2020, 3) --> but both are None.
 <br> <br>

Right Subtree: <br>
Current node: (6.0, 96, 2021, 2).     <br>
Check if point is within the range:    <br>
6.0 ∈ [4.0,6.0]:    True       <br>
96 ∈ [94,96]:     True       <br>
2021 ∈ [2019,2021]: True       <br>
2 ∈ [1,2]:        True       <br>
Point is in range, add to results: [(5.0, 94, 2019, 1), (6.0, 96, 2021, 2)].     <br>
 <br> <br> <br>

Final Results
After exploring all relevant subtrees, the points within the range are:
[(5.0, 94, 2019, 1), (6.0, 96, 2021, 2)]       These are printed as the final output.
