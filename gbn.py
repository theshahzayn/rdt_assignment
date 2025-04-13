
class Packet:
    def __init__(self, seq, data):
        self.seq = seq
        self.data = data

class Sender:
    def __init__(self, window_size, timeout=3):
        self.window_size = window_size
        self.base = 0
        self.next_seq = 0
        self.timeout = timeout
        self.buffer = {}

    def send(self, data, network, receiver):
        if self.next_seq < self.base + self.window_size:
            pkt = Packet(self.next_seq, data)
            self.buffer[self.next_seq] = pkt
            print(f"Sender: Sending packet {self.next_seq}")
            network.send_packet(pkt, receiver, self)
            self.next_seq += 1
        else:
            print("Sender: Window full, cannot send")

    def handle_ack(self, ack):
        print(f"Sender: ACK {ack} received")
        self.base = ack + 1

class Receiver:
    def __init__(self):
        self.expected_seq = 0

    def receive(self, pkt, network, sender):
        if pkt == "CORRUPTED":
            print("Receiver: Corrupted packet")
            return
        if pkt.seq == self.expected_seq:
            print(f"Receiver: Packet {pkt.seq} received")
            network.send_ack(pkt.seq, sender)
            self.expected_seq += 1
        else:
            print("Receiver: Out-of-order packet discarded")
