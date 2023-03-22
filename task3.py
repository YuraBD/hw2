import hazelcast

client = hazelcast.HazelcastClient()

my_map = client.get_map("my-distributed-map").blocking()
put_futures = []
for i in range(1000):
    my_map.put(i, f"value-{i}")

print("Data is stored in the distributed map.")

client.shutdown()