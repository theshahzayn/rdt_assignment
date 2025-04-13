
from network_simulator import NetworkSimulator
from config import *

import rdt3
import gbn
import sr

def run_rdt3():
    print("Running rdt3.0 (Stop and Wait Protocol)")
    sender = rdt3.Sender(TIMEOUT)
    receiver = rdt3.Receiver()
    network = NetworkSimulator(LOSS_PROBABILITY, CORRUPT_PROBABILITY, DELAY_PROBABILITY)
    for i in range(TOTAL_PACKETS):
        sender.send(f"Data {i}", network, receiver)

def run_gbn():
    print("Running Go-Back-N Protocol")
    sender = gbn.Sender(WINDOW_SIZE, TIMEOUT)
    receiver = gbn.Receiver()
    network = NetworkSimulator(LOSS_PROBABILITY, CORRUPT_PROBABILITY, DELAY_PROBABILITY)
    for i in range(TOTAL_PACKETS):
        sender.send(f"Data {i}", network, receiver)

def run_sr():
    print("Running Selective Repeat Protocol")
    sender = sr.Sender(WINDOW_SIZE)
    receiver = sr.Receiver(WINDOW_SIZE)
    network = NetworkSimulator(LOSS_PROBABILITY, CORRUPT_PROBABILITY, DELAY_PROBABILITY)
    for i in range(TOTAL_PACKETS):
        sender.send(f"Data {i}", network, receiver)

def main():
    print("Select Protocol:")
    print("1. rdt3.0 (Stop-and-Wait)")
    print("2. Go-Back-N")
    print("3. Selective Repeat")

    choice = int(input("Enter choice (1/2/3): "))

    if choice == 1:
        run_rdt3()
    elif choice == 2:
        run_gbn()
    elif choice == 3:
        run_sr()
    else:
        print("Invalid Choice")

if __name__ == "__main__":
    main()
