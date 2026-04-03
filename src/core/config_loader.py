import yaml
import os
from typing import Any, Dict

class ConfigLoader:
    """Loads and provides access to project configuration."""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
        self.settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found at: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            try:
                return yaml.safe_load(f)
            except yaml.YAMLError as exc:
                raise ValueError(f"Error parsing YAML configuration: {exc}")

    def get(self, key: str, default: Any = None) -> Any:
        """Helper to get nested keys using dot notation (e.g., 'network.port')."""
        keys = key.split('.')
        value = self.settings
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

# Global instance for easy access
config = ConfigLoader()
