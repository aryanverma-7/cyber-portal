from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from services.dns_lookup import DNSLookup
from services.packet_visualizer import PacketVisualizer

bp = Blueprint('networking', __name__, url_prefix='/networking')

@bp.route('/')
@login_required
def index():
    return render_template('networking/index.html')

@bp.route('/dns-lookup')
@login_required
def dns_lookup():
    return render_template('networking/dns_lookup.html')

@bp.route('/dns-lookup/execute', methods=['POST'])
@login_required
def execute_dns_lookup():
    domain = request.json.get('domain', '')
    
    if not domain:
        return jsonify({'error': 'Domain required'}), 400
    
    dns = DNSLookup()
    result = dns.lookup(domain)
    
    return jsonify(result)

@bp.route('/packet-visualizer')
@login_required
def packet_visualizer():
    return render_template('networking/packet_visualizer.html')

@bp.route('/packet-visualizer/simulate', methods=['POST'])
@login_required
def simulate_packet():
    protocol = request.json.get('protocol', 'TCP')
    source_ip = request.json.get('source_ip', '192.168.1.100')
    dest_ip = request.json.get('dest_ip', '10.0.0.1')
    source_port = int(request.json.get('source_port', 54321))
    dest_port = int(request.json.get('dest_port', 80))
    
    visualizer = PacketVisualizer()
    result = visualizer.simulate_packet(
        protocol=protocol,
        source_ip=source_ip,
        dest_ip=dest_ip,
        source_port=source_port,
        dest_port=dest_port
    )
    
    return jsonify(result)

@bp.route('/tcp-ip-learning')
@login_required
def tcp_ip_learning():
    return render_template('networking/tcp_ip.html')

@bp.route('/request-simulation')
@login_required
def request_simulation():
    return render_template('networking/request_simulation.html')