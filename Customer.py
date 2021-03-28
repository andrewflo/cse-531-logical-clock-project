import grpc
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
        port = 50000 + self.id
        channel = grpc.insecure_channel("localhost:50001")
        self.stub = branch_pb2_grpc.BranchStub(channel)
        print(
            "Connecting customer #"
            + str(self.id)
            + " to branch at localhost:"
            + str(port)
        )

    def executeEvents(self):
        self.createStub()

        response = self.stub.MsgDelivery(
            branch_pb2.MsgRequest(id=1, interface="query", money=49)
        )
        print(response)

        # for event in self.events:
        #     print(event)
        #     response = self.stub.MsgDelivery(
        #         branch_pb2.MsgRequest(
        #             id=event["id"], interface=event["interface"], money=event["money"]
        #         )
        #     )
        #     print(response)

    def print(self):
        print(self.id, self.events)
