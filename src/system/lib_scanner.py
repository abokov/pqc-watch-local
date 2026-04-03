import subprocess
import sys
import re
import os
from core.logger import logger
from core.config_loader import config

class LibScanner:
    """Scans executables for legacy versus PQC-ready crypto libraries."""
    
    TARGET_LIBS = config.get("app_analysis.target_libraries", ["libssl", "libcrypto", "libnss"])

    def __init__(self):
        self.platform = sys.platform
        self._check_binary_availability()

    def _check_binary_availability(self):
        """Verifies if the platform's library-scanning tool is available."""
        if self.platform == "darwin":
            self.command = ["otool", "-L"]
        else:
            self.command = ["ldd"]

    def scan_executable(self, exe_path: str) -> list:
        """Runs otool/ldd on a path and returns a list of target libraries found."""
        if not os.path.exists(exe_path):
            return []

        try:
            result = subprocess.run(
                self.command + [exe_path],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                logger.debug(f"Scan failed for {exe_path}: {result.stderr.strip()}")
                return []

            return self._parse_output(result.stdout, exe_path)

        except subprocess.TimeoutExpired:
            logger.warning(f"Scan timed out for {exe_path}")
        except Exception as e:
            logger.error(f"Error scanning {exe_path}: {e}")
        
        return []

    def _parse_output(self, output: str, exe_path: str) -> list:
        """Parses output lines for target libraries and flags legacy versions."""
        found_libs = []
        
        for line in output.splitlines():
            # Look for lines matching our target crypto libraries
            for target in self.TARGET_LIBS:
                if target.lower() in line.lower():
                    # Attempt to extract version/path info from the line
                    lib_info = line.strip().split(' ')[0]
                    is_legacy = self._is_legacy_version(line)
                    
                    found_libs.append({
                        "name": target,
                        "path": lib_info,
                        "legacy": is_legacy
                    })
                    
                    if is_legacy:
                        logger.warning(f"Legacy crypto library found in {exe_path}: {lib_info}")

        return found_libs

    def _is_legacy_version(self, line: str) -> bool:
        """
        Heuristic to identify legacy versions of common crypto libraries.
        e.g., OpenSSL 1.1 or earlier, NSS 3.x pre-PQC.
        """
        # Very basic heuristic: look for "1.1" or "1.0" in OpenSSL paths
        if "libssl.1.1" in line or "libssl.1.0" in line or "libcrypto.1.1" in line:
            return True
        # NSS versions below 3.90+ generally don't have stable PQC defaults
        if "nss3" in line and ".so" in line:
            # Simplistic check - a more robust version would parse 'nss-config' or similar
            return True
            
        return False

def run_system_scan(processes: list):
    """Orchestrates a scan of all provided processes."""
    scanner = LibScanner()
    results = {}
    
    logger.info(f"Scanning {len(processes)} processes for legacy crypto...")
    
    for proc in processes:
        libs = scanner.scan_executable(proc['exe'])
        if libs:
            results[proc['pid']] = {
                "name": proc['name'],
                "exe": proc['exe'],
                "libs": libs
            }
            
    return results
