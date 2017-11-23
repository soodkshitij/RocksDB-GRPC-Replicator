import grpc
import replicator_pb2
import argparse
import sys
import replicator_pb2_grpc

PORT=3000
HOST = None

check_input = lambda op : op in ['put','delete']

class DummyClient():
    
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2_grpc.ReplicatorStub(self.channel)
        
    def put(self, k , v):
        request = replicator_pb2.Request(key=k,value=v,op =replicator_pb2._REQUEST_OPERATION.values_by_number[0].name )
        self.stub.performOperation(request)

    def remove(self, k):
        request = replicator_pb2.Request(key=k,value="0",op =replicator_pb2._REQUEST_OPERATION.values_by_number[1].name )
        self.stub.performOperation(request)
    
def fetch_inputs():
    client = DummyClient(host=HOST)
    while True:
        try:
            method = input("Enter the operation you want to perform.PUT or DELETE\n").lower()
            if not check_input(method):
                print("\nIllegal operation\n")
                continue
            if method == "put":
                key = input("\nEnter the key you want to store.\n").strip()
                val = input("\nEnter the value you want to store.\n").strip()
                if not val or not val:
                    print("\nIllegal key or value\n")
                    continue
                client.put(key,val)
                
                
            else:
                key = input("\nEnter the key you want to delete.\n").strip()
                if not key:
                    print("\nIllegal key\n")
                    continue
                client.remove(key)
                
                
        except KeyboardInterrupt:
            print("Terminating program......")
            sys.exit(1)

def main():
    global HOST
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="host where grpc server is running")
    args = parser.parse_args()
    HOST =args.host
    fetch_inputs()
    


if __name__ == "__main__":
    main()
