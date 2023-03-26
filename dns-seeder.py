# Copyright (c) 2023, Karac V. Thweatt
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
# may be used to endorse or promote products derived from this software without
# specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import socket
import struct

# Set your coin's name here
coin = ""

# Seed nodes that will be returned to peers
# Can be IP address as well
NODES = [
    'node1.example.com',
    '255.255.255.0',
    'node3.example.com',
]

# Define the port to listen on
PORT = 0000

# Create a UDP socket to listen for queries
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

print(f"DNS Seeder  Copyright (C) 2023 Karac V. Thweatt\nThis software comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to\nredistribute it under certain conditions.\n\n{coin} seeder initialized.")

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
    for node in NODES:
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
