from core.logger import logger
from core.config_loader import config

class TLSParser:
    """Parses TLS handshake packets to identify PQC algorithm usage."""

    # Common PQC and Hybrid identifier substrings (e.g., from OQS or standard drafts)
    PQC_IDENTIFIERS = config.get("network.pqc_algorithms", ["Kyber", "ML-KEM", "Dilithium", "ML-DSA"])

    @staticmethod
    def is_pqc_negotiated(packet) -> bool:
        """
        Analyzes a packet for PQC identifiers in ciphersuites or supported groups.
        Returns True if PQC is detected, False otherwise.
        """
        try:
            if not hasattr(packet, 'tls'):
                return False

            # Check Supported Groups (where PQC Key Exchange often lives in TLS 1.3)
            if hasattr(packet.tls, 'handshake_extensions_supported_group'):
                groups = packet.tls.handshake_extensions_supported_group
                # pyshark might return a single value or a list
                if isinstance(groups, str):
                    groups = [groups]
                
                for group in groups:
                    if any(pqc.lower() in group.lower() for pqc in TLSParser.PQC_IDENTIFIERS):
                        logger.info(f"PQC detected in supported groups: {group}")
                        return True

            # Check Cipher Suites
            if hasattr(packet.tls, 'handshake_ciphersuite'):
                ciphers = packet.tls.handshake_ciphersuite
                if isinstance(ciphers, str):
                    ciphers = [ciphers]

                for cipher in ciphers:
                    if any(pqc.lower() in cipher.lower() for pqc in TLSParser.PQC_IDENTIFIERS):
                        logger.info(f"PQC detected in ciphersuite: {cipher}")
                        return True

        except Exception as e:
            logger.error(f"Error parsing TLS packet: {e}")

        return False

    @staticmethod
    def get_handshake_summary(packet) -> dict:
        """Extracts a summary of the handshake for logging."""
        summary = {
            "src_ip": packet.ip.src if hasattr(packet, 'ip') else "unknown",
            "dst_ip": packet.ip.dst if hasattr(packet, 'ip') else "unknown",
            "pqc_detected": False,
            "groups": [],
            "ciphers": []
        }
        
        try:
            if hasattr(packet, 'tls'):
                if hasattr(packet.tls, 'handshake_extensions_supported_group'):
                    summary["groups"] = packet.tls.handshake_extensions_supported_group
                if hasattr(packet.tls, 'handshake_ciphersuite'):
                    summary["ciphers"] = packet.tls.handshake_ciphersuite
                summary["pqc_detected"] = TLSParser.is_pqc_negotiated(packet)
        except Exception:
            pass
            
        return summary
