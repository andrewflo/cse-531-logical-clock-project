import grpc
from termcolor import colored

import branch_pb2
import branch_pb2_grpc


class Customer:
    def __init__(self, id, events):
        # unique ID of the Customer
        self.id = id
        # events from the input
        self.events = events
        # a list of received messages used for debugging purpose
        self.recvMsg = list()
        # pointer for the stub
        self.stub = None

    def createStub(self):
        port = str(50000 + self.id)
        channel = grpc.insecure_channel("localhost:" + port)
        self.stub = branch_pb2_grpc.BranchStub(channel)
        print(
            colored("Customer #" + str(self.id) + " on branch at [::]:" + port, "blue")
        )

    def executeEvents(self):
        for event in self.events:
            print(event)
            response = self.stub.MsgDelivery(
                branch_pb2.MsgRequest(
                    id=event["id"], interface=event["interface"], money=event["money"]
                )
            )
            print(response)
