# CS 170 Final Project - Fall 2018 - Agrawal, Briggs, Tiwari

In this project, we were presented with an NP-Hard problem learned about what it means to cope with NP-Hardness in practice. The problem statement is included below for reference:

    You are a tired, overworked teacher who has spent the last week organizing
    a field trip for your entire middle school. The night before the trip, you
    realize you forgot to plan the most important part – transportation! Fortunately,
    your school has access to a large fleet of buses. Being the caring teacher
    you are, you’d like to ensure that students can still end up on the same bus
    as their friends. After some investigative work on social media, you’ve managed
    to figure out exactly who is friends with who at your school and begin to
    assign students to buses with the intent of breaking up as few friendships as
    possible. You’ve only just begun when you receive a frantic email from one of
    the chaperones for the trip. The kids this year are particularly rowdy, and the
    chaperones have given you a list of groups of students who get too rowdy when
    they are all together. If any of these groups are seated assigned to the same
    bus, they will all have to be removed from the bus and sent home. Can you
    plan transportation while keeping both the students and the chaperones happy?

    Formally, you’re given an undirected graph G = (V, E), an integer k, and
    an integer s, where each node in the graph denotes a student, and each edge
    (v1, v2) denotes that students v1 and v2 are friends. The integer k denotes the
    number of buses available and the integer s denotes the number of students that
    can fit on a single bus. Furthermore, you’re given a list L, where each element
    Lj is some subset of V which corresponds to a group that should be kept apart.

    You must return a partition of G – a set of sets of vertices Vi such that
    V1 ∪ V2 ∪ V3 ∪ ... ∪ Vk = V and ∀i 6= j, Vi ∩ Vj = ∅. Additionally, ∀i, 0 < |Vi| ≤ s. 
    In other words, every bus must be non-empty, and must not have more students
    on it than its capacity allows.

    Consider a vertex v to be valid if there is no i and j such that v ∈ Lj
    and Lj ⊆ Vi. In other words, a vertex is valid if it is not in a rowdy group
    whose members all end up on the same bus. For example, if one of the rowdy
    groups was ‘Alice’, ‘Bob’, and ‘Carol’, then putting ‘Alice’, ‘Bob’, ‘Carol’, and
    ’Dan’ on the same bus would lead to ‘Alice’, ‘Bob’, and ‘Carol’ being considered
    invalid vertices. However, a bus with just ‘Alice’, ‘Bob’, and ‘Dan’ would have
    no invalid vertices.

    We’d like you to produce a partition that maximizes the percent of edges
    that occur between valid vertices in the same partition in the graph. The score
    for your partition is the percentage of edges (u, v) where u and v are both valid,
    and u, v ∈ Vi for some i. You’d like to produce a valid partition with as high a
    score as possible.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This solution uses a few common additional packages outside of those required for the initial skeleton code. These are listed below:

```
Python
NetworkX
os
time
random
copy
from multiprocessing import Pool
```

### Installing

We assume that you have Python installed. If you do not, please navigate [here](https://www.python.org/about/gettingstarted/) and follow the instructions. Then, you need to install the full [scientific Python stack](https://scipy.org/install.html). Assuming you have the default Python environment already configured on your computer, simply run the following:

```
python -m pip install --user numpy scipy matplotlib ipython jupyter pandas sympy nose
```

Assuming that you have the default Python environment already configured on your computer, here is how to install NetworkX inside of it. First, make sure you have the latest version of pip (the Python package manager) installed. If you do not, refer to the [Pip documentation](https://pip.pypa.io/en/stable/installing/) and install pip first. Then you simply need to run the following:

```
pip install networkx
```

## Running the tests

To construct the graphs and generate the solution set, simply run

```
python solver.py
```

Then, to score the solution set, run

```
python output_scorer.py
```

## Built With

* [Python](https://www.python.org/) - The programming language used.
* [NetworkX 2.2](https://networkx.github.io/) - Used for the generation and manipulation of complex networks and graphs.


## Authors

* **Devan Agrawal** - *Project Team Member* - Bitbucket: [shilorigins](https://bitbucket.org/shilorigins/)
* **Jonathan Briggs** - *Project Team Member* - Bitbucket: [jonathanpbriggs](https://bitbucket.org/jonathanpbriggs/); Github: [JiggleKoala](https://github.com/JiggleKoala)
* **Vedaank Tiwari** - *Project Team Member* - Bitbucket: [vedaank](https://bitbucket.org/vedaank/)

## Acknowledgments

* Hat tip to the passionate instructors and dedicated course staff!
