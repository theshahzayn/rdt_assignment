
import time
import random

class Packet:
    def __init__(self, seq, data):
        self.seq = seq
        self.data = data

class Sender:
    def __init__(self, timeout=2):
        self.seq = 0
        self.timeout = timeout

    def send(self, data, network, receiver):
        pkt = Packet(self.seq, data)
        print(f"Sender: Sending packet {self.seq}")
        network.send_packet(pkt, receiver, self, self.timeout)
        self.seq = 1 - self.seq

    def handle_ack(self, ack):
        print(f"Sender: ACK {ack} received")

class Receiver:
    def __init__(self):
        self.expected_seq = 0

    def receive(self, pkt, network, sender):
        if pkt == "CORRUPTED":
            print("Receiver: Received corrupted packet")
            return
        if pkt.seq == self.expected_seq:
            print(f"Receiver: Packet {pkt.seq} received correctly")
            self.expected_seq = 1 - self.expected_seq
            network.send_ack(pkt.seq, sender)
        else:
            print(f"Receiver: Duplicate or out-of-order packet {pkt.seq}")

class NetworkSimulator:
    def __init__(self, loss_prob=0.2, corrupt_prob=0.1, delay_prob=0.1):
        self.loss_prob = loss_prob
        self.corrupt_prob = corrupt_prob
        self.delay_prob = delay_prob

    def send_packet(self, pkt, receiver, sender, timeout):
        if random.random() < self.loss_prob:
            print("Network: Packet lost")
            return
        if random.random() < self.corrupt_prob:
            pkt = "CORRUPTED"
        if random.random() < self.delay_prob:
            print("Network: Packet delayed")
            time.sleep(random.uniform(0.5, 1.5))
        receiver.receive(pkt, self, sender)

    def send_ack(self, ack, sender):
        print(f"Network: Sending ACK {ack}")
        sender.handle_ack(ack)
