
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

