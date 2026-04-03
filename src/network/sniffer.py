import pyshark
from core.logger import logger
from core.config_loader import config
from .tls_parser import TLSParser

class NetworkSniffer:
    """Network sniffer for identifying PQC traffic via pyshark."""
    
    def __init__(self):
        self.interface = config.get("network.interface", "any")
        self.port = config.get("network.port", 443)
        # Filter for TLS handshakes specifically (TLS 1.2 and 1.3)
        self.display_filter = f"tcp.port == {self.port} && tls.handshake"
        self.capture = None

    def _process_packet(self, packet):
        """Processes each captured packet to check for PQC."""
        try:
            summary = TLSParser.get_handshake_summary(packet)
            if summary.get("pqc_detected"):
                logger.info(f"PQC traffic identified! Source: {summary['src_ip']}, Target: {summary['dst_ip']}")
                logger.debug(f"PQC groups: {summary['groups']}")
            else:
                logger.debug(f"Legacy handshake from {summary['src_ip']} to {summary['dst_ip']}")
        except Exception as e:
            logger.error(f"Error processing packet: {e}")

    def start_capture(self):
        """Starts a live capture with the specified filters."""
        logger.info(f"Initializing live capture on interface '{self.interface}', port {self.port}...")
        
        try:
            self.capture = pyshark.LiveCapture(
                interface=self.interface,
                display_filter=self.display_filter,
                # Explicitly decode TLS for analysis
                decode_as={f"tcp.port=={self.port}": "tls"}
            )
            
            logger.info("Sniffer running. Press Ctrl+C to stop.")
            self.capture.apply_on_packets(self._process_packet)
        except Exception as e:
            logger.critical(f"Failed to start live capture: {e}")
            raise

def run_sniffer_service():
    """Helper function to run the sniffer as a background service."""
    sniffer = NetworkSniffer()
    sniffer.start_capture()
