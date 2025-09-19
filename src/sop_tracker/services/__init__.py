"""
Workflow Management Service for SOP Control & Tracker
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

from ..models import Process, Step, SOPStatus, Priority


class WorkflowManager:
    """Manages workflow execution and orchestration for SOP processes"""
    
    def __init__(self):
        self.processes: Dict[str, Process] = {}
        self.logger = logging.getLogger(__name__)
    
    def create_process(self, name: str, description: str = "", **kwargs) -> Process:
        """Create a new SOP process"""
        process = Process(
            name=name,
            description=description,
            **kwargs
        )
        self.processes[process.id] = process
        self.logger.info(f"Created new process: {process.name} (ID: {process.id})")
        return process
    
    def get_process(self, process_id: str) -> Optional[Process]:
        """Get a process by ID"""
        return self.processes.get(process_id)
    
    def list_processes(self, status: Optional[SOPStatus] = None) -> List[Process]:
        """List all processes, optionally filtered by status"""
        processes = list(self.processes.values())
        if status:
            processes = [p for p in processes if p.status == status]
        return sorted(processes, key=lambda p: p.created_at, reverse=True)
    
    def start_process(self, process_id: str) -> bool:
        """Start a process execution"""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
        
        if process.status != SOPStatus.DRAFT:
            self.logger.warning(f"Process {process_id} is not in draft status")
            return False
        
        process.start()
        
        # Auto-start available steps
        available_steps = process.get_available_steps()
        for step in available_steps:
            if step.owner:  # Only auto-start if owner is assigned
                self.start_step(process_id, step.id)
        
        self.logger.info(f"Started process: {process.name} (ID: {process_id})")
        return True
    
    def start_step(self, process_id: str, step_id: str) -> bool:
        """Start a specific step in a process"""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
        
        step = process.get_step(step_id)
        if not step:
            self.logger.error(f"Step not found: {step_id}")
            return False
        
        if step.status != SOPStatus.DRAFT:
            self.logger.warning(f"Step {step_id} is not in draft status")
            return False
        
        # Check dependencies
        for dep_id in step.dependencies:
            dep_step = process.get_step(dep_id)
            if not dep_step or dep_step.status != SOPStatus.COMPLETED:
                self.logger.error(f"Step {step_id} has unmet dependencies")
                return False
        
        step.start()
        self.logger.info(f"Started step: {step.name} (ID: {step_id})")
        return True
    
    def complete_step(self, process_id: str, step_id: str) -> bool:
        """Complete a specific step in a process"""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
        
        step = process.get_step(step_id)
        if not step:
            self.logger.error(f"Step not found: {step_id}")
            return False
        
        if step.status != SOPStatus.IN_PROGRESS:
            self.logger.warning(f"Step {step_id} is not in progress")
            return False
        
        step.complete()
        self.logger.info(f"Completed step: {step.name} (ID: {step_id})")
        
        # Auto-start next available steps
        available_steps = process.get_available_steps()
        for next_step in available_steps:
            if next_step.owner:  # Only auto-start if owner is assigned
                self.start_step(process_id, next_step.id)
        
        # Check if process is complete
        if all(s.status == SOPStatus.COMPLETED for s in process.steps):
            process.complete()
            self.logger.info(f"Completed process: {process.name} (ID: {process_id})")
        
        return True
    
    def suspend_process(self, process_id: str) -> bool:
        """Suspend a process execution"""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
        
        if process.status not in [SOPStatus.IN_PROGRESS]:
            self.logger.warning(f"Process {process_id} cannot be suspended")
            return False
        
        process.status = SOPStatus.SUSPENDED
        process.updated_at = datetime.now()
        
        # Suspend all in-progress steps
        for step in process.steps:
            if step.status == SOPStatus.IN_PROGRESS:
                step.status = SOPStatus.SUSPENDED
        
        self.logger.info(f"Suspended process: {process.name} (ID: {process_id})")
        return True
    
    def resume_process(self, process_id: str) -> bool:
        """Resume a suspended process"""
        process = self.get_process(process_id)
        if not process:
            self.logger.error(f"Process not found: {process_id}")
            return False
        
        if process.status != SOPStatus.SUSPENDED:
            self.logger.warning(f"Process {process_id} is not suspended")
            return False
        
        process.status = SOPStatus.IN_PROGRESS
        process.updated_at = datetime.now()
        
        # Resume suspended steps
        for step in process.steps:
            if step.status == SOPStatus.SUSPENDED:
                step.status = SOPStatus.IN_PROGRESS
        
        self.logger.info(f"Resumed process: {process.name} (ID: {process_id})")
        return True
    
    def get_process_status(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a process"""
        process = self.get_process(process_id)
        if not process:
            return None
        
        step_statuses = []
        sla_breaches = []
        
        for step in process.steps:
            step_info = {
                'id': step.id,
                'name': step.name,
                'status': step.status.value,
                'sequence_order': step.sequence_order,
                'owner': step.owner.name if step.owner else None,
                'started_at': step.started_at,
                'completed_at': step.completed_at,
                'sla_breached': step.is_sla_breached()
            }
            step_statuses.append(step_info)
            
            if step.is_sla_breached():
                sla_breaches.append(step_info)
        
        return {
            'process_id': process.id,
            'name': process.name,
            'status': process.status.value,
            'progress': process.get_progress(),
            'created_at': process.created_at,
            'updated_at': process.updated_at,
            'steps': step_statuses,
            'sla_breaches': sla_breaches,
            'total_steps': len(process.steps),
            'completed_steps': sum(1 for s in process.steps if s.status == SOPStatus.COMPLETED),
            'in_progress_steps': sum(1 for s in process.steps if s.status == SOPStatus.IN_PROGRESS)
        }
    
    def get_sla_alerts(self) -> List[Dict[str, Any]]:
        """Get all SLA breach alerts across all processes"""
        alerts = []
        
        for process in self.processes.values():
            for step in process.steps:
                if step.is_sla_breached():
                    alerts.append({
                        'process_id': process.id,
                        'process_name': process.name,
                        'step_id': step.id,
                        'step_name': step.name,
                        'owner': step.owner.name if step.owner else None,
                        'started_at': step.started_at,
                        'sla_duration': step.sla.duration if step.sla else None,
                        'breach_time': datetime.now() - step.started_at if step.started_at else None
                    })
        
        return sorted(alerts, key=lambda a: a['started_at'] or datetime.min)
    
    def get_workload_by_owner(self, owner_name: str) -> Dict[str, Any]:
        """Get workload statistics for a specific owner"""
        assigned_steps = []
        
        for process in self.processes.values():
            for step in process.steps:
                if step.owner and step.owner.name == owner_name:
                    assigned_steps.append({
                        'process_id': process.id,
                        'process_name': process.name,
                        'step_id': step.id,
                        'step_name': step.name,
                        'status': step.status.value,
                        'priority': step.priority.value,
                        'started_at': step.started_at,
                        'sla_breached': step.is_sla_breached()
                    })
        
        in_progress = [s for s in assigned_steps if s['status'] == SOPStatus.IN_PROGRESS.value]
        completed = [s for s in assigned_steps if s['status'] == SOPStatus.COMPLETED.value]
        breached = [s for s in assigned_steps if s['sla_breached']]
        
        return {
            'owner_name': owner_name,
            'total_assigned': len(assigned_steps),
            'in_progress': len(in_progress),
            'completed': len(completed),
            'sla_breached': len(breached),
            'steps': assigned_steps
        }