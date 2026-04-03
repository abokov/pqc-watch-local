import threading
import time
import sys
from core.logger import logger
from core.config_loader import config
from network.sniffer import run_sniffer_service
from system.process_list import get_processes_to_scan
from system.lib_scanner import run_system_scan
from reporting.console_out import ConsoleReporter, print_banner

def run_network_sniffer():
    """Continuously monitors network traffic for PQC usage."""
    logger.info("Starting network sniffer service...")
    try:
        run_sniffer_service()
    except Exception as e:
        logger.critical(f"Network sniffer service failed: {e}")

def run_app_scanner():
    """Periodically scans local binary files for PQC library status."""
    logger.info("Starting periodic app scanner service...")
    while True:
        try:
            # Retrieve currently running processes
            processes = get_processes_to_scan()
            
            # Scan their libraries
            results = run_system_scan(processes)
            
            # Report results to console
            ConsoleReporter.report_scan_results(results)
            
            # Wait for the next scheduled scan (default 1 hour)
            time.sleep(3600)
        except Exception as e:
            logger.error(f"App scanner iteration failed: {e}")
            time.sleep(60) # Retry after 1 minute on error

def main():
    """Main entry point for the pqc-watch-local daemon."""
    print_banner()
    logger.info("Initializing PQC Watch Local Daemon...")
    
    # Start Network Sniffer in its own thread
    sniffer_thread = threading.Thread(target=run_network_sniffer, name="NetworkSniffer", daemon=True)
    sniffer_thread.start()
    
    # Start App Scanner in its own thread
    scanner_thread = threading.Thread(target=run_app_scanner, name="AppScanner", daemon=True)
    scanner_thread.start()
    
    try:
        # Keep the main thread alive while daemon threads work
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Daemon shutting down...")
        sys.exit(0)

if __name__ == "__main__":
    main()
