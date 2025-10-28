import logging
import sys
from datetime import datetime

def setup_logger(name: str = "homeopathic_app") -> logging.Logger:
    """Setup structured logging"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger