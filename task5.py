import hazelcast
from threading import Thread
import time

client = hazelcast.HazelcastClient()
bounded_queue = client.get_queue("bounded-queue").blocking()

def producer(queue):
    for i in range(20):
        if (queue.offer(i)):
            print(f"Producer: Added {i} to the queue")
        else:
            print(f"Producer: Queue is full. Could not add {i}")
    queue.offer(-1)

def consumer(queue, consumer_id):
    while True:
        value = queue.take()
        if value == -1:
            queue.offer(-1)
            print("Consumer stop")
            break
        print(f"Consumer {consumer_id}: Read {value} from the queue")

producer_thread = Thread(target=producer, args=(bounded_queue,))
consumer_threads = [Thread(target=consumer, args=(bounded_queue, i)) for i in range(1, 3)]

producer_thread.start()
for consumer_thread in consumer_threads:
    consumer_thread.start()

producer_thread.join()
for consumer_thread in consumer_threads:
    consumer_thread.join()

value = bounded_queue.take()

client.shutdown()