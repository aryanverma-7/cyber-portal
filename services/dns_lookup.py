import socket
import re

class DNSLookup:
    """DNS lookup simulator and educational tool"""
    
    def __init__(self):
        self.dns_records = {}
    
    def lookup(self, domain):
        """Perform DNS lookup for a domain"""
        if not domain or not self._is_valid_domain(domain):
            return {
                'success': False,
                'error': 'Invalid domain name',
                'records': []
            }
        
        records = []
        
        # Simulate DNS resolution
        try:
            # A record
            try:
                ip = socket.gethostbyname(domain)
                records.append({
                    'type': 'A',
                    'value': ip,
                    'description': 'IPv4 address'
                })
            except:
                records.append({
                    'type': 'A',
                    'value': 'Not found',
                    'description': 'IPv4 address'
                })
            
            # AAAA record (simulated)
            records.append({
                'type': 'AAAA',
                'value': 'Simulated IPv6 address',
                'description': 'IPv6 address'
            })
            
            # MX record (simulated)
            records.append({
                'type': 'MX',
                'value': f'mail.{domain}',
                'priority': 10,
                'description': 'Mail exchange'
            })
            
            # NS record (simulated)
            records.append({
                'type': 'NS',
                'value': f'ns1.{domain}',
                'description': 'Name server'
            })
            
            # TXT record (simulated)
            records.append({
                'type': 'TXT',
                'value': 'v=spf1 include:_spf.google.com ~all',
                'description': 'Text record (SPF)'
            })
            
            return {
                'success': True,
                'domain': domain,
                'records': records,
                'query_time': '23ms'
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'records': []
            }
    
    def _is_valid_domain(self, domain):
        """Validate domain name format"""
        pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
        return re.match(pattern, domain) and len(domain) <= 255
    
    def get_dns_process_explanation(self):
        """Return educational explanation of DNS process"""
        return {
            'steps': [
                {
                    'step': 1,
                    'name': 'User Request',
                    'description': 'User enters a domain name (e.g., example.com) in browser'
                },
                {
                    'step': 2,
                    'name': 'Browser Cache Check',
                    'description': 'Browser checks if it has cached the DNS result'
                },
                {
                    'step': 3,
                    'name': 'OS Cache Check',
                    'description': 'Operating system checks its DNS cache (hosts file)'
                },
                {
                    'step': 4,
                    'name': 'DNS Query',
                    'description': 'Request sent to configured DNS server (usually ISP)'
                },
                {
                    'step': 5,
                    'name': 'Recursive Resolution',
                    'description': 'DNS server queries root → TLD → authoritative servers'
                },
                {
                    'step': 6,
                    'name': 'Response',
                    'description': 'IP address returned to browser'
                },
                {
                    'step': 7,
                    'name': 'Connection',
                    'description': 'Browser connects to IP address and loads website'
                }
            ],
            'record_types': [
                {'type': 'A', 'description': 'Maps domain to IPv4 address'},
                {'type': 'AAAA', 'description': 'Maps domain to IPv6 address'},
                {'type': 'MX', 'description': 'Mail exchange server'},
                {'type': 'NS', 'description': 'Name server'},
                {'type': 'CNAME', 'description': 'Canonical name (alias)'},
                {'type': 'TXT', 'description': 'Text record (SPF, verification)'},
                {'type': 'SOA', 'description': 'Start of authority'}
            ]
        }