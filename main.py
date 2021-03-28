import argparse
import json
import multiprocessing
from time import sleep
from concurrent import futures

import grpc

import branch_pb2_grpc
from Branch import Branch
from Customer import Customer


def serveBranch(branch):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    branch_pb2_grpc.add_BranchServicer_to_server(branch, server)
    port = 50000 + branch.id
    print("Serving branch #" + str(branch.id) + " at localhost:" + str(port))
    server.add_insecure_port("[::]:50001")
    server.start()
    server.wait_for_termination()


def serveCustomer(customer):
    customer.executeEvents()


def createProcesses(processes):
    customers = []
    branches = []

    for process in processes:
        if process["type"] == "customer":
            customer = Customer(process["id"], process["events"])
            customers.append(customer)
        elif process["type"] == "branch":
            branch = Branch(process["id"], process["balance"], branches)
            branches.append(branch)

    for branch in branches:
        branch_process = multiprocessing.Process(target=serveBranch, args=(branch,))
        branch_process.start()

    for customer in customers:
        customer_process = multiprocessing.Process(target=customer.executeEvents)
        customer_process.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    args = parser.parse_args()

    # try:
    #     input = json.load(open(args.input_file))
    #     createProcesses(input)
    # except FileNotFoundError:
    #     print("Could not find input file '" + args.input_file + "'")
    # except json.decoder.JSONDecodeError:
    #     print("Error decoding JSON file")

    branch_process = multiprocessing.Process(
        target=serveBranch, args=(Branch(1, 100, []),)
    )
    branch_process.start()

    customer_process = multiprocessing.Process(
        target=serveCustomer, args=(Customer(1, []),)
    )
    customer_process.start()
