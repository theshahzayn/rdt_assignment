
import random
import time

class NetworkSimulator:
    def __init__(self, loss_prob=0.1, corrupt_prob=0.1, delay_prob=0.1):
        self.loss_prob = loss_prob      # Probability of packet loss
        self.corrupt_prob = corrupt_prob  # Probability of packet corruption
        self.delay_prob = delay_prob      # Probability of packet delay

    def send_packet(self, pkt, receiver, sender=None, timeout=None):
        if random.random() < self.loss_prob:
            print("Network: Packet lost")
            return  # Packet lost, do nothing

        if random.random() < self.corrupt_prob:
            pkt = "CORRUPTED"  # Mark packet as corrupted
            print("Network: Packet corrupted")

        if random.random() < self.delay_prob:
            delay = random.uniform(0.5, 1.5)  # Random delay between 0.5 to 1.5 seconds
            print(f"Network: Packet delayed for {delay:.2f} seconds")
            time.sleep(delay)

        receiver.receive(pkt, self, sender)  # Deliver packet to receiver

    def send_ack(self, ack, sender):
        print(f"Network: Sending ACK {ack}")
        sender.handle_ack(ack)  # Deliver ACK to sender
