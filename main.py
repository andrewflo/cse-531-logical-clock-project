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
    print(colored("Serving branch #" + str(branch.id) + " on :" + port, "green"))
    server.add_insecure_port("[::]:" + port)
    server.start()

    sleep(0.5 * branch.id)
    output_array = json.load(open("output.json"))
    output_array.append({"pid": branch.id, "data": branch.output()})
    output = json.dumps(output_array, indent=4)
    output_file = open("output.json", "w")
    output_file.write(output)
    output_file.close()

    server.wait_for_termination()


# Start customer gRPC client processes
def serveCustomer(customer):
    customer.createStub()
    customer.executeEvents()


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

    # Allow branches to complete output before terminating
    sleep(1)

    # Terminate Branch processes
    for branchProcess in branchProcesses:
        branchProcess.terminate()


# Write events to output.json
def outputEvents():
    output = json.load(open("output.json"))
    events_dict = {}

    for pid in output:
        for event in pid["data"]:
            if event["id"] in events_dict.keys():
                events_dict[event["id"]].append(event)
            else:
                events_dict[event["id"]] = [event]

    # print(str(json.dumps(events_dict, indent=4)))

    for event in events_dict:
        data = sorted(events_dict[event], key=lambda event: event["clock"])
        output.append({"eventid": event, "data": data})

    output_file = open("output.json", "w")
    output_file.write(json.dumps(output, indent=4))
    output_file.close()


if __name__ == "__main__":
    # Setup command line argument for 'input_file'
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    try:
        # Load JSON file from 'input_file' arg
        input = json.load(open(args.input_file))

        # Initialize output file
        output_file = open("output.json", "w")
        output_file.write("[]")
        output_file.close()

        # Create objects/processes from input file
        createProcesses(input)

        # Write events to output file
        sleep(1.5)
        outputEvents()
    except FileNotFoundError:
        print(colored("Could not find input file '" + args.input_file + "'", "red"))
    except json.decoder.JSONDecodeError:
        print(colored("Error decoding JSON file", "red"))
