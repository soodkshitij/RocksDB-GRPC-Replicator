# RocksDB-GRPC-Replicator

![alt text][logo]

[logo]: https://github.com/soodkshitij/RocksDB-GRPC-Replicator/blob/master/out.gif ""


### Run Server
```bash
python3 server.py
```

### Run slaves 
#   Arguments master host & unique client-id
```bash
python3 slave.py 0.0.0.0 1
python3 slave.py 0.0.0.0 2
python3 slave.py 0.0.0.0 3
```

### server console output
```bash
client connected Client Id - 1
client connected Client Id - 2
client connected Client Id - 3
```

### dummy client for op
```
python3 dummyclient.py 0.0.0.0
Enter the operation you want to perform.PUT or DELETE
pu

Illegal operation

Enter the operation you want to perform.PUT or DELETE
put

Enter the key you want to store.
kshitij

Enter the value you want to store.
sood
Enter the operation you want to perform.PUT or DELETE
delete

Enter the key you want to delete.
kshitij

```

### slave replication console
```
Client ID- 1 Stream from server
Performing put for key kshitij and value sood 
Client ID- 2 Stream from server
Performing put for key kshitij and value sood 
Client ID- 3 Stream from server
Performing put for key kshitij and value sood 

Client ID- 1 Stream from server
Performing delete for key kshitij 
Client ID- 2 Stream from server
Performing delete for key kshitij 
Client ID- 3 Stream from server
Performing put for key kshitij and value sood 
Client ID- 3 Stream from server
Performing delete for key kshitij 

```
###
