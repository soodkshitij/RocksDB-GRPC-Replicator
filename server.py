import time
import grpc
import replicator_pb2_grpc
import replicator_pb2
import rocksdb
from queue import Queue
from functools import wraps

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
encoding = "UTF-8"

class ReplicationHandler(replicator_pb2_grpc.ReplicatorServicer):
    '''
    '''
    _client_data_queue_map = {} 
    def __init__(self):
        self.db = rocksdb.DB("master.db", rocksdb.Options(create_if_missing=True))
        
    def register_client(self,client_id):
        if (ReplicationHandler._client_data_queue_map.get(client_id) is None):
            ReplicationHandler._client_data_queue_map[client_id] = Queue()

            
    def _replicator(func):
        @wraps(func)
        def addToQueue(*args):
            if ReplicationHandler._client_data_queue_map:
                for v in ReplicationHandler._client_data_queue_map.values():
                    v.put(args[1])  #Adding grpc request object to client specific queue
            return func(*args)
        return addToQueue

    
    @_replicator
    def performOperation(self, request, context):
        print(request.op)
        if (request.op == 0):
            self.put(request.key, request.value)
        if (request.op == 1):
            self.delete(request.key)
        
        return replicator_pb2.Response(result=True)
    
    def put(self,key,value):
        self.db.put(bytes(key,encoding) ,bytes(value, encoding))
    
    def delete(self,key):
        print(key)
        self.db.delete(bytes(key, encoding))
        
        
    def replicateOperation(self, request, context):
        c_id = request.id
        self.register_client(c_id)
        print("client connected Client Id - %d"%(c_id))
        while True:
            q = ReplicationHandler._client_data_queue_map.get(c_id)
            while not q.empty():
                d = q.get()
                yield (d)

def run(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    replicator_pb2_grpc.add_ReplicatorServicer_to_server(ReplicationHandler(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
