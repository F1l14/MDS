# Tasks:  <br>

Check if the code can be simpler


# How it works: <br>
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

Tree so far:

{
    point: (5.0, 94, 2019, 1),
    left: [...],
    right: [...]
}

<br>
<br>
At depth 1 (split by y):
<br>
Left Subtree:
Points: [(4.5, 95, 2020, 1), (4.8, 97, 2020, 3)].
Median Point: (4.8, 97, 2020, 3).
<br>
Right Subtree:
Points: [(6.0, 96, 2021, 2), (7.0, 98, 2021, 1)].
Median Point: (6.0, 96, 2021, 2).

<br>
Tree structure:
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

This process continues until all points are placed into leaf nodes.

---------------------------------------------------------------------------------------------------------------------------------------------------


Step 2: Query Execution


Initialization:
Start at the root node (5.0, 94, 2019, 1).
Query range is x ∈ [4.0,6.0], y ∈ [94,96], z ∈ [2019,2021], w ∈ [1,2].


At depth 0 (split by x):

Current node: (5.0, 94, 2019, 1).

Check if point is within the range:

5.0 ∈ [4.0,6.0]:    True
94 ∈ [94,96]:       True
2019 ∈ [2019,2021]: True
1 ∈ [1,2]:          True
Point is in range, add it to results: [(5.0, 94, 2019, 1)].

Traverse left because 4.0 ≤ 5.0.
Traverse right as well because 6.0 ≥ 5.0.



At depth 1 (split by y):

Left Subtree:
Current node: (4.8, 97, 2020, 3).
Check if point is within the range:
4.8∈[4.0,6.0]: True
97∈[94,96]:    False
Point is out of range, do not add to results.

Traverse left and right subtrees of (4.8, 97, 2020, 3) --> but both are None.


Right Subtree:
Current node: (6.0, 96, 2021, 2).
Check if point is within the range:
6.0∈[4.0,6.0]:    True
96 ∈ [94,96]:     True
2021∈[2019,2021]: True
2 ∈ [1,2]:        True
Point is in range, add to results: [(5.0, 94, 2019, 1), (6.0, 96, 2021, 2)].


Final Results
After exploring all relevant subtrees, the points within the range are:
[(5.0, 94, 2019, 1), (6.0, 96, 2021, 2)]       These are printed as the final output.
