
import random
import time

class Packet:
    def __init__(self, seq, data):
        self.seq = seq
        self.data = data

class Sender:
    def __init__(self, window_size):
        self.window_size = window_size
        self.base = 0
        self.next_seq = 0
        self.sent_packets = {}

    def send(self, data, network, receiver):
        if self.next_seq < self.base + self.window_size:
            pkt = Packet(self.next_seq, data)
            self.sent_packets[self.next_seq] = pkt
            print(f"Sender: Sending packet {self.next_seq}")
            network.send_packet(pkt, receiver, self)
            self.next_seq += 1
        else:
            print("Sender: Window full")

    def handle_ack(self, ack):
        print(f"Sender: ACK {ack} received")
        if ack in self.sent_packets:
            del self.sent_packets[ack]
        while self.base not in self.sent_packets and self.base < self.next_seq:
            self.base += 1

class Receiver:
    def __init__(self, window_size):
        self.window_size = window_size
        self.expected_seq = 0
        self.buffer = {}

    def receive(self, pkt, network, sender):
        if pkt == "CORRUPTED":
            print("Receiver: Corrupted packet")
            return
        print(f"Receiver: Packet {pkt.seq} received")
        if pkt.seq >= self.expected_seq and pkt.seq < self.expected_seq + self.window_size:
            self.buffer[pkt.seq] = pkt
            network.send_ack(pkt.seq, sender)
            while self.expected_seq in self.buffer:
                print(f"Receiver: Delivering packet {self.expected_seq}")
                del self.buffer[self.expected_seq]
                self.expected_seq += 1

class NetworkSimulator:
    def __init__(self, loss_prob=0.2, corrupt_prob=0.1, delay_prob=0.1):
        self.loss_prob = loss_prob
        self.corrupt_prob = corrupt_prob
        self.delay_prob = delay_prob

    def send_packet(self, pkt, receiver, sender):
        if random.random() < self.loss_prob:
            print("Network: Packet lost")
            return
        if random.random() < self.corrupt_prob:
            pkt = "CORRUPTED"
        if random.random() < self.delay_prob:
            print("Network: Delaying packet")
            time.sleep(random.uniform(0.5, 1.5))
        receiver.receive(pkt, self, sender)

    def send_ack(self, ack, sender):
        print(f"Network: Sending ACK {ack}")
        sender.handle_ack(ack)
