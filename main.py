import argparse
import json
import multiprocessing
from time import sleep
from concurrent import futures
from termcolor import colored

import grpc

import branch_pb2_grpc
from Branch import Branch
from Customer import Customer


# Start branch gRPC server process
def serveBranch(branch):
    branch.createStubs()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    branch_pb2_grpc.add_BranchServicer_to_server(branch, server)
    port = str(50000 + branch.id)
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


# Start customer gRPC client processes
def serveCustomer(customer):
    customer.createStub()
    customer.executeEvents()

    output = customer.output()
    output_file = open("output.txt", "a")
    output_file.write(str(output) + "\n")
    output_file.close()
    # print(str(output))


# Parse JSON & create objects/processes
def createProcesses(processes):
    # List of Customer objects
    customers = []
    # List of Customer processes
    customerProcesses = []
    # List of Branch objects
    branches = []
    # List of Branch IDs
    branchIds = []
    # List of Branch processes
    branchProcesses = []

    # Instantiate Branch objects
    for process in processes:
        if process["type"] == "branch":
            branch = Branch(process["id"], process["balance"], branchIds)
            branches.append(branch)
            branchIds.append(branch.id)

    # Spawn Branch processes
    for branch in branches:
        branch_process = multiprocessing.Process(target=serveBranch, args=(branch,))
        branchProcesses.append(branch_process)
        branch_process.start()

    # Allow branch processes to start
    sleep(0.25)

    # Instantiate Customer objects
    for process in processes:
        if process["type"] == "customer":
            customer = Customer(process["id"], process["events"])
            customers.append(customer)

    # Spawn Customer processes
    for customer in customers:
        customer_process = multiprocessing.Process(target=serveCustomer, args=(customer,))
        customerProcesses.append(customer_process)
        customer_process.start()

    # Wait for Customer processes to complete
    for customerProcess in customerProcesses:
        customerProcess.join()

    # Terminate Branch processes
    for branchProcess in branchProcesses:
        branchProcess.terminate()


if __name__ == "__main__":
    # Setup command line argument for 'input_file'
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    try:
        # Load JSON file from 'input_file' arg
        input = json.load(open(args.input_file))

        # Initialize output file
        open("output.txt", "w").close()

        # Create objects/processes from input file
        createProcesses(input)
    except FileNotFoundError:
        print(colored("Could not find input file '" + args.input_file + "'", "red"))
    except json.decoder.JSONDecodeError:
        print(colored("Error decoding JSON file", "red"))
