import socket
import struct

# Set your coin's name here
coin = ""

# Seed nodes that will be returned to peers
# Can be IP address as well
SEED_NODES = [
    'node1.example.com',
    'node2.example.com',
    'node3.example.com',
]

# Define the port to listen on
PORT = 52202

# Create a UDP socket to listen for queries
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

print(f"{coin} seeder initialized.")

# Respond to DNS queries
while True:
    data, addr = sock.recvfrom(1024)
    print('Received query from', addr)

    # Extract the DNS query ID from the message
    query_id = struct.unpack('!H', data[:2])[0]

    # Construct the DNS response with the seed nodes
    response = b''
    response += struct.pack('!H', query_id) # copy the query ID
    response += b'\x81\x80' # flags
    response += b'\x00\x01' # questions
    response += b'\x00\x03' # answer RRs
    response += b'\x00\x00' # authority RRs
    response += b'\x00\x00' # additional RRs

    # Add the seed nodes to the response
    for node in SEED_NODES:
        # Create a DNS answer record with the node's IP address
        ip_bytes = socket.inet_aton(socket.gethostbyname(node))
        response += b'\xc0\x0c' # pointer to the domain name
        response += b'\x00\x01' # type: A (IPv4 address)
        response += b'\x00\x01' # class: IN (Internet)
        response += b'\x00\x00\x01\x00' # TTL: 1 second
        response += struct.pack('!H', len(ip_bytes)) # data length
        response += ip_bytes

    # Send the DNS response
    sock.sendto(response, addr)
    print('Sent response to', addr)
