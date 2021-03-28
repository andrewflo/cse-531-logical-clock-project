<h1>CSE 531: gRPC Project</h1>

Author: **Andrew Flores**

CSE 531: Distributed and Multiprocessor Operating Systems (Spring 2021 - B)

## Quick Start

From the project root directory:

1. Activate the virtual environment with: `source bin/activate`
2. Start the program with: `python main.py input.json`
3. The result will be written to the output file: `output.txt`

The input file should be in `.json` format and is passed to the program via a command line argument.

## Overview

### File Descriptions

The following important files are included in this project:

* `main.py`: Main program to be executed from the command line with: `python main.py input.json`

* `input.json`: Input file containing a list of branch processes and customer processes with transaction events.

* `output.txt`: The output file containing each Customer's `recvMsg` output. This file will be overwritten each time the program is ran.

* `branch.proto`: Protocol buffer file defining RPC messages & services. This file has already been compiled to produce the `branch_pb2.py` & `branch_pb2_grpc.py` files.

* `Branch.py`: Branch class served as a gRPC server to process customer transactions and propagate them to other branches.

* `Customer.py`: Customer class with gRPC client branch stub to send transaction requests to its corresponding bank branch.

### Python Environment

Python 3 is required for this project. `venv` is used to sandbox the Python project and dependencies in a virtual environment.

In order to use the included Python version and project dependency files, the virtual environment must be activated before the program is ran:

```sh
# From project root
source bin/activate
```

For more information, please refer to the [12. Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html) page of the official Python documentation.