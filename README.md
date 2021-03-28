<h1>CSE 531: gRPC Project</h1>

Author: **Andrew Flores**

CSE 531: Distributed and Multiprocessor Operating Systems (Spring 2021 - B)

## Quick Start

From the project root directory:

1. Activate the virtual environment with: `source bin/activate`
2. Start the program with: `python main.py input.json`
3. The result will be written to the output file: `output.txt`

The input file should be in `.json` format and is passed to the program via a command line argument.

`venv` is used to sandbox the Python project and dependencies in a virtual environment.

## Overview

The following key files are included in this project:

#### `main.py`:

Main program to be executed from the command line with: `python main.py input.json`

#### `branch.proto`:

Protocol buffer file defining RPC messages & services. This file has already been compiled to produce the `branch_pb2.py` & `branch_pb2_grpc.py` files.

#### `Branch.py`:

Branch class served as a gRPC server to processes customer transactions and propagate them to other branches.

#### `Customer.py`:

Customer class with gRPC client stubs to send transaction events to the bank branch.

#### `input.json`:

Input file containing a list of branch processes and customer processes with transaction events.