from concurrent import futures

import grpc
from termcolor import colored

import branch_pb2_grpc
from branch_pb2 import MsgRequest, MsgResponse


class Branch(branch_pb2_grpc.BranchServicer):
    def __init__(self, id, balance, branches):
        self.id = id
        self.balance = balance
        self.branches = branches
        self.stubList = list()
        self.events = list()
        self.clock = 1

    # Setup gRPC channel & client stub for each branch
    def createStubs(self):
        for branchId in self.branches:
            if branchId != self.id:
                port = str(50000 + branchId)
                channel = grpc.insecure_channel("localhost:" + port)
                self.stubList.append(branch_pb2_grpc.BranchStub(channel))

    # Incoming MsgRequest from Customer transaction
    def MsgDelivery(self, request, context):
        if request.interface != "query":
            self.Event_Request(request)
        return self.ProcessMsg(request, False)

    # Incoming MsgRequest from Branch propagation
    def MsgPropagation(self, request, context):
        if request.interface != "query":
            self.Propagate_Request(request)
        return self.ProcessMsg(request, True)

    # Handle received Msg, generate and return a MsgResponse
    def ProcessMsg(self, request, isPropagation):
        if request.interface != "query":
            if not isPropagation:
                self.Event_Execute(request)
            else:
                self.Propagate_Execute(request)

        result = "success"

        if request.money < 0:
            result = "fail"
        elif request.interface == "query":
            pass
        elif request.interface == "deposit":
            self.balance += request.money
        elif request.interface == "withdraw":
            if self.balance >= request.money:
                self.balance -= request.money
            else:
                result = "fail"
        else:
            result = "fail"

        response = MsgResponse(
            id=request.id, interface=request.interface, result=result, money=self.balance, clock=self.clock
        )

        if not isPropagation and request.interface != "query":
            self.Event_Response(response)
            self.Propagate_Transaction(request)

        return response

    # Propagate Customer event to other Branches
    def Propagate_Transaction(self, request):
        for stub in self.stubList:
            response = stub.MsgPropagation(
                MsgRequest(id=request.id, interface=request.interface, money=request.money, clock=self.clock)
            )
            self.Propagate_Response(response)

    # Generate output msg
    def output(self):
        return self.events

    # Receive event from Customer (max + 1)
    def Event_Request(self, request):
        self.clock = max(self.clock, request.clock) + 1
        self.events.append({"id": request.id, "name": request.interface + "_request", "clock": self.clock})

    # Execute event from Customer (+ 1)
    def Event_Execute(self, request):
        self.clock += 1
        self.events.append({"id": request.id, "name": request.interface + "_execute", "clock": self.clock})

    # Receive propagated event from Branch (max + 1)
    def Propagate_Request(self, request):
        self.clock = max(self.clock, request.clock) + 1
        self.events.append({"id": request.id, "name": request.interface + "_propagate_request", "clock": self.clock})

    # Execute propagated event from Branch (+ 1)
    def Propagate_Execute(self, request):
        self.clock += 1
        self.events.append({"id": request.id, "name": request.interface + "_propagate_execute", "clock": self.clock})

    # Receive returned propagation response from Branch (max + 1)
    def Propagate_Response(self, response):
        self.clock = max(self.clock, response.clock) + 1
        self.events.append({"id": response.id, "name": response.interface + "_propagate_response", "clock": self.clock})

    # Return response to Customer (+ 1)
    def Event_Response(self, response):
        self.clock += 1
        self.events.append({"id": response.id, "name": response.interface + "_response", "clock": self.clock})