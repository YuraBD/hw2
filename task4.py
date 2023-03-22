import hazelcast
import threading

client = hazelcast.HazelcastClient()
my_map = client.get_map("my-distributed-map").blocking()

def no_lock_example():
    value = my_map.get("some-key")
    my_map.put("some-key", value + 1)

def pessimistic_lock_example():
    my_map.lock("some-key")
    try:
        value = my_map.get("some-key")
        my_map.put("some-key", value + 1)
    finally:
        my_map.unlock("some-key")

def optimistic_lock_example():
    while True:
        value = my_map.get("some-key")
        updated = my_map.replace_if_same("some-key", value, value + 1)
        if updated:
            break

my_map.put("some-key", 0)
print("Starting value of 'some-key' for no_lock_example:", my_map.get("some-key"))

threads = [threading.Thread(target=no_lock_example) for _ in range(3)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print("Final value of 'some-key' for no_lock_example:", my_map.get("some-key"))


my_map.put("some-key", 0)
print("Starting value of 'some-key' for pessimistic_lock_example:", my_map.get("some-key"))

threads = [threading.Thread(target=pessimistic_lock_example) for _ in range(3)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
    
print("Final value of 'some-key' for pessimistic_lock_example:", my_map.get("some-key"))


my_map.put("some-key", 0)
print("Starting value of 'some-key' for optimistic_lock_example:", my_map.get("some-key"))

threads = [threading.Thread(target=optimistic_lock_example) for _ in range(3)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
    
print("Final value of 'some-key' for optimistic_lock_example:", my_map.get("some-key"))

client.shutdown()