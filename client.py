import grpc
import replicator_pb2
import replicator_pb2_grpc
import rocksdb

class ReplicationClient():
    '''
    '''

    def __init__(self, host='0.0.0.0', port=3000):
        '''
        '''
        # TODO
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2_grpc.ReplicatorStub(self.channel)

    def put(self, data):
        '''
        '''
        # TODO
        
        request = replicator_pb2.Request(key="hello",value="1000",op =replicator_pb2._REQUEST_OPERATION.values_by_number[0].name )
        self.stub.performOperation(request)
        #repRequest = replicator_pb2.ReplicationRequest(id=17)
        #res = self.stub.replicateOperation(repRequest)
        #for z in res:
        #    print(z.key+" "+z.value)
        
        
    def get(self, id):
        '''
        '''
        # TODO
        return None # self.stub.get(req)


print("Client is running...")
client = ReplicationClient()
client.put("hello")

x= {'a':1,'b':2}

