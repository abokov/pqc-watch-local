import psutil
from core.logger import logger

class ProcessList:
    """Utility to iterate through and filter running system processes."""

    @staticmethod
    def get_running_processes():
        """
        Returns a list of dictionaries containing 'pid' and 'exe' path.
        Handles AccessDenied and NoSuchProcess exceptions gracefully.
        """
        process_info_list = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # Get process details as a dictionary
                info = proc.info
                if info['exe']:  # Only include processes with a valid executable path
                    process_info_list.append({
                        'pid': info['pid'],
                        'name': info['name'],
                        'exe': info['exe']
                    })
            except (psutil.AccessDenied, psutil.ZombieProcess):
                # Common for system processes or processes owned by other users
                continue
            except psutil.NoSuchProcess:
                # Process terminated during iteration
                continue
            except Exception as e:
                logger.debug(f"Unexpected error retrieving info for PID {proc.pid}: {e}")
                
        return process_info_list

def get_processes_to_scan():
    """Helper for the app scanner to get a fresh list of targets."""
    procs = ProcessList.get_running_processes()
    logger.debug(f"Retrieved {len(procs)} active processes for analysis.")
    return procs
