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
        self.recvMsg = list()

    # Setup gRPC channel & client stub for each branch
    def createStubs(self):
        for branchId in self.branches:
            if branchId != self.id:
                port = str(50000 + branchId)
                channel = grpc.insecure_channel("localhost:" + port)
                self.stubList.append(branch_pb2_grpc.BranchStub(channel))

    # Incoming MsgRequest from Customer transaction
    def MsgDelivery(self, request, context):
        return self.ProcessMsg(request, True)

    # Incoming MsgRequest from Branch propagation
    def MsgPropagation(self, request, context):
        return self.ProcessMsg(request, False)

    # Handle received Msg, generate and return a MsgResponse
    def ProcessMsg(self, request, propagate):
        result = "success"

        if request.money < 0:
            result = "fail"
        elif request.interface == "query":
            pass
        elif request.interface == "deposit":
            self.balance += request.money
            if propagate == True:
                self.Propagate_Deposit(request)
        elif request.interface == "withdraw":
            if self.balance >= request.money:
                self.balance -= request.money
                if propagate == True:
                    self.Propagate_Withdraw(request)
            else:
                result = "fail"
        else:
            result = "fail"

        # Create msg to be appended to self.recvMsg list
        msg = {"interface": request.interface, "result": result}

        # Add 'money' entry for 'query' events
        if request.interface == "query":
            msg["money"] = request.money

        self.recvMsg.append(msg)

        return MsgResponse(interface=request.interface, result=result, money=self.balance)

    # Propagate Customer withdraw to other Branches
    def Propagate_Withdraw(self, request):
        for stub in self.stubList:
            stub.MsgPropagation(MsgRequest(id=request.id, interface="withdraw", money=request.money))

    # Propagate Customer deposit to other Branches
    def Propagate_Deposit(self, request):
        for stub in self.stubList:
            stub.MsgPropagation(MsgRequest(id=request.id, interface="deposit", money=request.money))
