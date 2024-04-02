## Complex Exam Scheduling with Answer Set Programming (ASP)
This exam scheduling tool is developed as a part of a research project under the guidance of **Dr. Sarah Alice Gaggl** at **TU Dresden**.

This project focuses on scheduling complex examinations using the ASP (Answer Set Programming) solver Clingo. It utilizes Clorm to integrate Clingo encodings into Python object models, providing a seamless solution for exam scheduling.

## Installation

### Prerequisites

- Python 3.10.11
- pip 22.0.4

### Steps

1. Clone the repository
    ```bash
    git clone https://github.com/kansakarpratistha/ASP_Exam_Scheduling.git

2. Navigate to the project directory and install dependencies using 'requirements.txt':
    ```bash
    pip install -r requirements.txt

## Usage

- To run the tool in command line, execute the following command:
    ```bash
    py main.py

- To run the tool with UI in localhost, execute the following command:
    ```bash
    streamlit run scheduler.py

## Dependencies

The project depends on the following Python packages:
- `clorm==1.4.2`
- `pandas==2.0.3`
- `streamlit==1.32.0`
- `streamlit-multipage==0.0.18`

*Currently only command line version is available. User interface is under development using Streamlit library.*
