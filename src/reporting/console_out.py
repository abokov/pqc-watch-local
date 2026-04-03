from core.logger import logger

class ConsoleReporter:
    """Formats and prints PQC analysis results to the console."""

    @staticmethod
    def report_scan_results(results: dict):
        """Prints a summary of the application library scan."""
        if not results:
            print("\n--- [ System Scan: No Legacy Crypto Libraries Found ] ---")
            return

        print("\n" + "="*60)
        print("PQC WATCH: SYSTEM SCAN REPORT (LEGACY CRYPTO DETECTED)")
        print("="*60)
        
        for pid, data in results.items():
            print(f"\n[PID {pid}] Process: {data['name']}")
            print(f"Path: {data['exe']}")
            print("-" * 20)
            for lib in data['libs']:
                status = "!!! LEGACY !!!" if lib['legacy'] else "PQC-READY"
                print(f"  - {lib['name']}: {lib['path']} [{status}]")
        
        print("\n" + "="*60)

    @staticmethod
    def report_pqc_detection(summary: dict):
        """Prints a real-time notification for PQC network traffic."""
        print(f"\n[!] PQC TRAFFIC ALERT")
        print(f"    Source: {summary['src_ip']}")
        print(f"    Target: {summary['dst_ip']}")
        if summary['groups']:
            print(f"    Key Exchange Groups: {summary['groups']}")
        print("-" * 30)

def print_banner():
    """Prints the application startup banner."""
    banner = """
    =========================================
       PQC-WATCH-LOCAL: Post-Quantum Agent
    =========================================
    Monitoring traffic and binaries for PQC...
    """
    print(banner)
