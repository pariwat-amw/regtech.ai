"""
SOP Control & Tracker System

A comprehensive system for managing Standard Operating Procedures (SOPs)
with workflow management, configuration, and tracking capabilities.
"""

__version__ = "1.0.0"
__author__ = "RegTech.AI Team"

from .models import Process, Step, SLA, Owner, WorkTemplate, SOPStatus, Priority
from .services import WorkflowManager
from .services.config_service import SOPConfigService
from .controllers import SOPController

__all__ = [
    'Process', 'Step', 'SLA', 'Owner', 'WorkTemplate', 'SOPStatus', 'Priority',
    'WorkflowManager', 'SOPConfigService', 'SOPController'
]