# Binary Decision Trees - implementation of ID3 Alghoritm

## Description

This Python project implements a binary decision tree algorithm to suggest a movie based on user preferences. The tree is built by analyzing conditional entropy (information gain) and visualized using the Graphviz library. The dataset is read from an Excel file and contains information on user preferences (e.g., age, company, mood) and the recommended movie. The algorithm recursively splits the data into branches, selecting attributes that maximize the gain in decision certainty, until unambiguous conclusions can be made.

## Alghoritm

- Calculates the entropy of the current dataset.
- For each attribute, computes the information gain when the dataset is split on that attribute.
- Selects the attribute that offers the highest gain (or falls back to the first valid attribute).
- Recursively splits the dataset until each leaf leads to a unique conclusion.
- Visualizes each step using Graphviz edges and nodes.

## Requirements

- Python 3
- pandas
- graphviz
- math
- os
