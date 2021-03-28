<h1>CSE 531: gRPC Project</h1>

Andrew Flores, Spring 2021 B

CSE 531: Distributed and Multiprocessor Operating Systems



## Quick Start

1. `git clone` the repo and `cd` into the repo directory
2. `python3 -m venv env` to initialize the virtual environment
3. `source env/bin/activate` to activate the virtual environment
4. `pip install -r requirements.txt` to install project dependencies
5. `python main.py input.json` to start the program
6. The result will be written to `output.txt`

## Overview

### Important Files

The following important files are included in this project:

* `main.py`: Main program to be executed from the command line with: `python main.py input.json`

* `input.json`: Input file containing a list of branch processes and customer processes with transaction events.

* `output.txt`: The output file containing each Customer's `recvMsg` output. This file will be overwritten each time the program is ran.

* `branch.proto`: Protocol buffer file defining RPC messages & services. This file has already been compiled to produce the `branch_pb2.py` & `branch_pb2_grpc.py` files.

* `Branch.py`: Branch class served as a gRPC server to process customer transactions and propagate them to other branches.

* `Customer.py`: Customer class with gRPC client branch stub to send transaction requests to its corresponding bank branch.

### Input File

The input file should be in `.json` format and is passed to the program via a command line argument.

The following `input.json` file is included from the CSE 531 gRPC Project instructions:

```json
[
  {
    "id": 1,
    "type": "customer",
    "events": [
      { "id": 1, "interface": "query", "money": 400 }
    ]
  },
  {
    "id": 2,
    "type": "customer",
    "events": [
      { "id": 2, "interface": "deposit", "money": 170 },
      { "id": 3, "interface": "query", "money": 400 }
    ]
  },
  {
    "id": 3,
    "type": "customer",
    "events": [
      { "id": 4, "interface": "withdraw", "money": 70 },
      { "id": 5, "interface": "query", "money": 400 }
    ]
  },
  {
    "id": 1,
    "type": "branch",
    "balance": 400
  },
  {
    "id": 2,
    "type": "branch",
    "balance": 400
  },
  {
    "id": 3,
    "type": "branch",
    "balance": 400
  }
]

```

### Python Environment

Python 3 is required for this project. `venv` is used to sandbox the Python project and dependencies in a virtual environment.

In order to use the included Python version and project dependency files, the virtual environment must be initialized and activated before the program is ran.

From the project root:

```sh
# Initialize the Python virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install project dependencies in the virtual environment
pip install -r requirements.txt
```

For more information, please refer to the [12. Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) page of the official Python documentation.