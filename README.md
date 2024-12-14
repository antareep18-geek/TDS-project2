# TDS-PROJECT 2 : AUTOLYSIS PROJECT

## Overview

The **AutoLysis Project** is an automated data analysis tool designed to simplify data exploration and generate meaningful insights from CSV datasets. This project leverages AI (through an AI Proxy) to perform various data analyses, including outlier detection, correlation analysis, regression analysis, and more, without the need for manual intervention.

## Features

- **Automated Data Analysis**: Performs outlier detection, correlation analysis, regression analysis, time series analysis, cluster analysis, and more.
- **Visualization Generation**: Automatically generates and saves visualizations (charts, graphs) in PNG format.
- **Dynamic Python Code Generation**: Uses an AI Proxy to generate Python code for different analyses based on the dataset structure.
- **Report Generation**: Produces a narrative report of the analysis and insights, saved as a `README.md` file.

## Prerequisites

Before running the project, ensure the following prerequisites are met:

- **Python 3.6+**
- Required Python libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `requests`
  - `statsmodels`

These libraries can be installed using the following command:

```bash
pip install numpy pandas matplotlib seaborn requests statsmodels
