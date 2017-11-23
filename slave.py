import grpc
import replicator_pb2
import argparse
import replicator_pb2_grpc
import rocksdb

PORT=3000
HOST = None
CLIENT_ID = None
encoding = "UTF-8"


class Slave():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2_grpc.ReplicatorStub(self.channel)
        self.db = rocksdb.DB("client-{}.db".format(CLIENT_ID), rocksdb.Options(create_if_missing=True))

    def start_replication(self):
        r = replicator_pb2.ReplicationRequest(id=CLIENT_ID)
        rep_response = self.stub.replicateOperation(r)
        for stream in rep_response:
            print("Client ID- {} Stream from server".format(CLIENT_ID))
            if (stream.op == 0):
                self.put(stream.key, stream.value)
            if (stream.op == 1):
                self.delete(stream.key)
    
    def put(self,key,value):
        print("Performing put for key {} and value {} ".format(key,value))
        self.db.put(bytes(key,encoding) ,bytes(value, encoding))
    
    def delete(self,key):
        print("Performing delete for key {} ".format(key))
        self.db.delete(bytes(key, encoding))


def main():
    global HOST
    global CLIENT_ID
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="host where grpc server is running")
    parser.add_argument("client_id", help="unique client_id of slave")
    args = parser.parse_args()
    HOST = args.host
    CLIENT_ID = int(args.client_id)
    s = Slave()
    s.start_replication()
    


if __name__ == "__main__":
    main()
