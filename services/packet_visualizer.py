class PacketVisualizer:
    """TCP/IP packet flow visualizer"""
    
    def __init__(self):
        pass
    
    def simulate_packet(self, protocol, source_ip, dest_ip, source_port, dest_port):
        """Simulate packet flow between two endpoints"""
        
        packet = {
            'protocol': protocol,
            'source': {
                'ip': source_ip,
                'port': source_port
            },
            'destination': {
                'ip': dest_ip,
                'port': dest_port
            },
            'header': self._generate_header(protocol),
            'flow': self._generate_flow_diagram(protocol),
            'timeline': self._generate_timeline(protocol)
        }
        
        return {
            'success': True,
            'packet': packet
        }
    
    def _generate_header(self, protocol):
        """Generate packet header based on protocol"""
        headers = {
            'TCP': {
                'source_port': 'Random high port (e.g., 54321)',
                'dest_port': 'Service port (e.g., 80 for HTTP)',
                'sequence_number': 'Random 32-bit number',
                'ack_number': '0 (initial)',
                'flags': ['SYN'],
                'window_size': '65535',
                'checksum': 'Calculated checksum',
                'description': 'TCP Header - 20+ bytes'
            },
            'UDP': {
                'source_port': 'Random port',
                'dest_port': 'Service port',
                'length': '8 + data length',
                'checksum': 'Optional checksum',
                'description': 'UDP Header - 8 bytes'
            },
            'HTTP': {
                'method': 'GET/POST',
                'path': '/index.html',
                'version': 'HTTP/1.1',
                'headers': ['Host', 'User-Agent', 'Accept'],
                'description': 'HTTP Request Header'
            },
            'HTTPS': {
                'method': 'GET/POST',
                'path': '/index.html',
                'version': 'HTTP/2',
                'encrypted': 'True',
                'description': 'HTTPS (TLS encrypted) Request'
            }
        }
        
        return headers.get(protocol, headers['TCP'])
    
    def _generate_flow_diagram(self, protocol):
        """Generate flow diagram steps"""
        
        if protocol == 'TCP':
            return [
                {
                    'step': 1,
                    'action': 'SYN',
                    'from': 'Client',
                    'to': 'Server',
                    'description': 'Client sends SYN to initiate connection'
                },
                {
                    'step': 2,
                    'action': 'SYN-ACK',
                    'from': 'Server',
                    'to': 'Client',
                    'description': 'Server responds with SYN-ACK'
                },
                {
                    'step': 3,
                    'action': 'ACK',
                    'from': 'Client',
                    'to': 'Server',
                    'description': 'Client sends ACK (3-way handshake complete)'
                },
                {
                    'step': 4,
                    'action': 'DATA',
                    'from': 'Client',
                    'to': 'Server',
                    'description': 'Data transmission begins'
                },
                {
                    'step': 5,
                    'action': 'FIN',
                    'from': 'Client',
                    'to': 'Server',
                    'description': 'Connection termination'
                }
            ]
        else:
            return [
                {
                    'step': 1,
                    'action': 'REQUEST',
                    'from': 'Client',
                    'to': 'Server',
                    'description': f'{protocol} request sent'
                },
                {
                    'step': 2,
                    'action': 'RESPONSE',
                    'from': 'Server',
                    'to': 'Client',
                    'description': f'{protocol} response received'
                }
            ]
    
    def _generate_timeline(self, protocol):
        """Generate timeline of packet events"""
        return [
            {
                'time': '0ms',
                'event': 'Packet created',
                'details': 'Application layer generates data'
            },
            {
                'time': '1ms',
                'event': 'Transport layer',
                'details': f'{protocol} header added'
            },
            {
                'time': '2ms',
                'event': 'Network layer',
                'details': 'IP header added (source/dest IP)'
            },
            {
                'time': '3ms',
                'event': 'Network interface',
                'details': 'Ethernet frame added'
            },
            {
                'time': '5ms',
                'event': 'Transmission',
                'details': 'Packet sent over network'
            },
            {
                'time': '15ms',
                'event': 'Reception',
                'details': 'Packet received by destination'
            }
        ]
    
    def get_tcp_ip_layers(self):
        """Return educational TCP/IP layer information"""
        return {
            'layers': [
                {
                    'level': 5,
                    'name': 'Application Layer',
                    'protocols': ['HTTP', 'HTTPS', 'FTP', 'SMTP', 'DNS'],
                    'description': 'User applications and data',
                    'example': 'Browser requesting website'
                },
                {
                    'level': 4,
                    'name': 'Transport Layer',
                    'protocols': ['TCP', 'UDP'],
                    'description': 'End-to-end communication, reliability',
                    'example': 'TCP 3-way handshake'
                },
                {
                    'level': 3,
                    'name': 'Network Layer',
                    'protocols': ['IP', 'ICMP', 'ARP'],
                    'description': 'Routing, IP addressing',
                    'example': 'IP packet with source/dest addresses'
                },
                {
                    'level': 2,
                    'name': 'Data Link Layer',
                    'protocols': ['Ethernet', 'Wi-Fi'],
                    'description': 'Physical network addressing',
                    'example': 'Ethernet frame with MAC addresses'
                },
                {
                    'level': 1,
                    'name': 'Physical Layer',
                    'protocols': ['DSL', 'Fiber', 'Cable'],
                    'description': 'Physical transmission medium',
                    'example': 'Bits transmitted as electrical/optical signals'
                }
            ]
        }