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


def serveBranch(branch):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    branch_pb2_grpc.add_BranchServicer_to_server(branch, server)
    port = str(50000 + branch.id)
    print(colored("Serving branch #" + str(branch.id) + " on :" + port, "green"))
    server.add_insecure_port("[::]:" + port)
    server.start()
    server.wait_for_termination()


def serveCustomer(customer):
    customer.createStub()
    customer.executeEvents()


def createProcesses(processes):
    customers = []
    customerProcesses = []
    branches = []
    branchProcesses = []

    # Branch processes need to be spawned before Customer processes
    for process in processes:
        if process["type"] == "branch":
            branch = Branch(process["id"], process["balance"], branches)
            branches.append(branch)

    for branch in branches:
        branch_process = multiprocessing.Process(target=serveBranch, args=(branch,))
        branchProcesses.append(branch_process)
        branch_process.start()

    for process in processes:
        if process["type"] == "customer":
            customer = Customer(process["id"], process["events"])
            customers.append(customer)

    # Allow branch processes to fully start
    sleep(0.25)

    for customer in customers:
        customer_process = multiprocessing.Process(target=serveCustomer, args=(customer,))
        customerProcesses.append(customer_process)
        customer_process.start()

    for customerProcess in customerProcesses:
        customerProcess.join()

    for branchProcess in branchProcesses:
        branchProcess.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    try:
        input = json.load(open(args.input_file))
        createProcesses(input)
    except FileNotFoundError:
        print("Could not find input file '" + args.input_file + "'")
    except json.decoder.JSONDecodeError:
        print("Error decoding JSON file")

    # branch_process = multiprocessing.Process(
    #     target=serveBranch, args=(Branch(1, 100, []),)
    # )
    # branch_process.start()

    # customer_process = multiprocessing.Process(
    #     target=serveCustomer, args=(Customer(1, []),)
    # )
    # customer_process.start()
