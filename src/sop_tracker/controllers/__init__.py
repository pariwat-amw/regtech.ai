"""
Main SOP Controller - Central interface for SOP Control & Tracker
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from ..models import Process, Step, SLA, Owner, WorkTemplate, SOPStatus, Priority
from ..services import WorkflowManager
from ..services.config_service import SOPConfigService


class SOPController:
    """Main controller for SOP Control & Tracker system"""
    
    def __init__(self):
        self.workflow_manager = WorkflowManager()
        self.config_service = SOPConfigService()
        self.logger = logging.getLogger(__name__)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # Process management
    def create_process(self, name: str, description: str = "", **kwargs) -> Process:
        """Create a new SOP process"""
        return self.workflow_manager.create_process(name, description, **kwargs)
    
    def create_process_from_config(self, config: Dict[str, Any]) -> Process:
        """Create a process from configuration"""
        process = self.config_service.create_process_from_config(config)
        self.workflow_manager.processes[process.id] = process
        return process
    
    def get_process(self, process_id: str) -> Optional[Process]:
        """Get a process by ID"""
        return self.workflow_manager.get_process(process_id)
    
    def list_processes(self, status: Optional[SOPStatus] = None) -> List[Process]:
        """List all processes"""
        return self.workflow_manager.list_processes(status)
    
    def start_process(self, process_id: str) -> bool:
        """Start a process"""
        return self.workflow_manager.start_process(process_id)
    
    def suspend_process(self, process_id: str) -> bool:
        """Suspend a process"""
        return self.workflow_manager.suspend_process(process_id)
    
    def resume_process(self, process_id: str) -> bool:
        """Resume a process"""
        return self.workflow_manager.resume_process(process_id)
    
    # Step management
    def add_step_to_process(self, process_id: str, step_config: Dict[str, Any]) -> bool:
        """Add a step to a process"""
        process = self.get_process(process_id)
        if not process:
            return False
        
        step = self.config_service.create_step_from_config(step_config)
        process.add_step(step)
        return True
    
    def start_step(self, process_id: str, step_id: str) -> bool:
        """Start a step"""
        return self.workflow_manager.start_step(process_id, step_id)
    
    def complete_step(self, process_id: str, step_id: str) -> bool:
        """Complete a step"""
        return self.workflow_manager.complete_step(process_id, step_id)
    
    # Configuration management
    def create_owner(self, name: str, email: str, department: str = "", role: str = "") -> Owner:
        """Create a new owner"""
        return self.config_service.create_owner(name, email, department, role)
    
    def create_sla(self, name: str, duration: timedelta, warning_threshold: float = 0.8) -> SLA:
        """Create a new SLA"""
        return self.config_service.create_sla(name, duration, warning_threshold)
    
    def create_work_template(self, name: str, description: str = "", 
                           checklist: List[str] = None,
                           instructions: str = "") -> WorkTemplate:
        """Create a new work template"""
        return self.config_service.create_work_template(
            name, description, checklist, instructions=instructions
        )
    
    def list_owners(self) -> List[Owner]:
        """List all owners"""
        return self.config_service.list_owners()
    
    def list_slas(self) -> List[SLA]:
        """List all SLAs"""
        return self.config_service.list_slas()
    
    def list_work_templates(self) -> List[WorkTemplate]:
        """List all work templates"""
        return self.config_service.list_work_templates()
    
    # Monitoring and reporting
    def get_process_status(self, process_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a process"""
        return self.workflow_manager.get_process_status(process_id)
    
    def get_sla_alerts(self) -> List[Dict[str, Any]]:
        """Get all SLA breach alerts"""
        return self.workflow_manager.get_sla_alerts()
    
    def get_workload_by_owner(self, owner_name: str) -> Dict[str, Any]:
        """Get workload statistics for an owner"""
        return self.workflow_manager.get_workload_by_owner(owner_name)
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary with key metrics"""
        all_processes = self.list_processes()
        active_processes = self.list_processes(SOPStatus.IN_PROGRESS)
        completed_processes = self.list_processes(SOPStatus.COMPLETED)
        sla_alerts = self.get_sla_alerts()
        
        # Calculate step statistics
        total_steps = 0
        completed_steps = 0
        in_progress_steps = 0
        overdue_steps = 0
        
        for process in all_processes:
            total_steps += len(process.steps)
            for step in process.steps:
                if step.status == SOPStatus.COMPLETED:
                    completed_steps += 1
                elif step.status == SOPStatus.IN_PROGRESS:
                    in_progress_steps += 1
                    if step.is_sla_breached():
                        overdue_steps += 1
        
        # Owner workload summary
        owner_workloads = {}
        for owner in self.list_owners():
            workload = self.get_workload_by_owner(owner.name)
            owner_workloads[owner.name] = {
                'total_assigned': workload['total_assigned'],
                'in_progress': workload['in_progress'],
                'sla_breached': workload['sla_breached']
            }
        
        return {
            'timestamp': datetime.now(),
            'processes': {
                'total': len(all_processes),
                'active': len(active_processes),
                'completed': len(completed_processes),
                'completion_rate': len(completed_processes) / len(all_processes) if all_processes else 0
            },
            'steps': {
                'total': total_steps,
                'completed': completed_steps,
                'in_progress': in_progress_steps,
                'overdue': overdue_steps,
                'completion_rate': completed_steps / total_steps if total_steps else 0
            },
            'sla_alerts': {
                'total_breaches': len(sla_alerts),
                'recent_breaches': [a for a in sla_alerts if 
                                   a['started_at'] and 
                                   datetime.now() - a['started_at'] <= timedelta(hours=24)]
            },
            'owners': {
                'total': len(self.list_owners()),
                'workload_summary': owner_workloads
            }
        }
    
    def export_process_config(self, process_id: str) -> Optional[str]:
        """Export process configuration as JSON"""
        process = self.get_process(process_id)
        if not process:
            return None
        return self.config_service.save_to_json(process)
    
    def import_process_config(self, json_data: str) -> Optional[Process]:
        """Import process configuration from JSON"""
        try:
            process = self.config_service.load_from_json(json_data)
            self.workflow_manager.processes[process.id] = process
            return process
        except Exception as e:
            self.logger.error(f"Failed to import process config: {e}")
            return None
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        # Create owners
        john = self.create_owner("John Smith", "john@company.com", "Compliance", "Senior Analyst")
        mary = self.create_owner("Mary Johnson", "mary@company.com", "Legal", "Legal Counsel")
        bob = self.create_owner("Bob Wilson", "bob@company.com", "Operations", "Operations Manager")
        
        # Create SLAs
        standard_sla = self.create_sla("Standard SLA", timedelta(days=2), 0.75)
        urgent_sla = self.create_sla("Urgent SLA", timedelta(hours=8), 0.8)
        review_sla = self.create_sla("Review SLA", timedelta(hours=24), 0.9)
        
        # Create work templates
        analysis_template = self.create_work_template(
            "Risk Analysis Template",
            "Template for conducting risk analysis",
            ["Review documentation", "Identify risks", "Assess impact", "Document findings"],
            "Conduct thorough risk analysis following company guidelines"
        )
        
        approval_template = self.create_work_template(
            "Approval Template",
            "Template for approval processes",
            ["Review submission", "Check compliance", "Make decision", "Document approval"],
            "Review and approve/reject based on established criteria"
        )
        
        # Create sample process
        sample_config = {
            "name": "Regulatory Compliance Review",
            "description": "Standard process for reviewing regulatory compliance issues",
            "version": "1.0.0",
            "priority": "high",
            "owner": {
                "name": "Compliance Manager",
                "email": "compliance@company.com",
                "department": "Compliance",
                "role": "Manager"
            },
            "steps": [
                {
                    "name": "Initial Assessment",
                    "description": "Conduct initial assessment of compliance issue",
                    "sequence_order": 1,
                    "owner": john.name,
                    "sla": standard_sla.name,
                    "work_template": analysis_template.name,
                    "priority": "high"
                },
                {
                    "name": "Legal Review",
                    "description": "Legal team reviews the compliance issue",
                    "sequence_order": 2,
                    "dependencies": [],
                    "owner": mary.name,
                    "sla": review_sla.name,
                    "work_template": approval_template.name,
                    "priority": "high"
                },
                {
                    "name": "Operations Impact Assessment",
                    "description": "Assess impact on operations",
                    "sequence_order": 3,
                    "dependencies": [],
                    "owner": bob.name,
                    "sla": standard_sla.name,
                    "work_template": analysis_template.name,
                    "priority": "medium"
                },
                {
                    "name": "Final Decision",
                    "description": "Make final decision and document outcome",
                    "sequence_order": 4,
                    "dependencies": [],
                    "owner": john.name,
                    "sla": urgent_sla.name,
                    "work_template": approval_template.name,
                    "priority": "critical"
                }
            ]
        }
        
        process = self.create_process_from_config(sample_config)
        
        self.logger.info("Sample data created successfully")
        return process