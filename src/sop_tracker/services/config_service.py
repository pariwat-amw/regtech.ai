"""
SOP Configuration Service
"""

from typing import List, Optional, Dict, Any
from datetime import timedelta
import json
import logging

from ..models import Process, Step, SLA, Owner, WorkTemplate, Priority, SOPStatus


class SOPConfigService:
    """Service for managing SOP configurations"""
    
    def __init__(self):
        self.owners: Dict[str, Owner] = {}
        self.slas: Dict[str, SLA] = {}
        self.work_templates: Dict[str, WorkTemplate] = {}
        self.logger = logging.getLogger(__name__)
    
    # Owner management
    def create_owner(self, name: str, email: str, department: str = "", role: str = "") -> Owner:
        """Create a new owner"""
        owner = Owner(
            name=name,
            email=email,
            department=department,
            role=role
        )
        self.owners[owner.id] = owner
        self.logger.info(f"Created owner: {name} (ID: {owner.id})")
        return owner
    
    def get_owner(self, owner_id: str) -> Optional[Owner]:
        """Get an owner by ID"""
        return self.owners.get(owner_id)
    
    def get_owner_by_name(self, name: str) -> Optional[Owner]:
        """Get an owner by name"""
        return next((owner for owner in self.owners.values() if owner.name == name), None)
    
    def list_owners(self) -> List[Owner]:
        """List all owners"""
        return list(self.owners.values())
    
    def update_owner(self, owner_id: str, **kwargs) -> bool:
        """Update an owner"""
        owner = self.get_owner(owner_id)
        if not owner:
            return False
        
        for key, value in kwargs.items():
            if hasattr(owner, key):
                setattr(owner, key, value)
        
        self.logger.info(f"Updated owner: {owner.name} (ID: {owner_id})")
        return True
    
    # SLA management
    def create_sla(self, name: str, duration: timedelta, warning_threshold: float = 0.8,
                   escalation_rules: List[Dict[str, Any]] = None) -> SLA:
        """Create a new SLA"""
        sla = SLA(
            name=name,
            duration=duration,
            warning_threshold=warning_threshold,
            escalation_rules=escalation_rules or []
        )
        self.slas[sla.id] = sla
        self.logger.info(f"Created SLA: {name} (ID: {sla.id})")
        return sla
    
    def get_sla(self, sla_id: str) -> Optional[SLA]:
        """Get an SLA by ID"""
        return self.slas.get(sla_id)
    
    def get_sla_by_name(self, name: str) -> Optional[SLA]:
        """Get an SLA by name"""
        return next((sla for sla in self.slas.values() if sla.name == name), None)
    
    def list_slas(self) -> List[SLA]:
        """List all SLAs"""
        return list(self.slas.values())
    
    def update_sla(self, sla_id: str, **kwargs) -> bool:
        """Update an SLA"""
        sla = self.get_sla(sla_id)
        if not sla:
            return False
        
        for key, value in kwargs.items():
            if hasattr(sla, key):
                setattr(sla, key, value)
        
        self.logger.info(f"Updated SLA: {sla.name} (ID: {sla_id})")
        return True
    
    # Work Template management
    def create_work_template(self, name: str, description: str = "", 
                           checklist: List[str] = None,
                           required_documents: List[str] = None,
                           instructions: str = "",
                           estimated_duration: timedelta = timedelta(hours=1)) -> WorkTemplate:
        """Create a new work template"""
        template = WorkTemplate(
            name=name,
            description=description,
            checklist=checklist or [],
            required_documents=required_documents or [],
            instructions=instructions,
            estimated_duration=estimated_duration
        )
        self.work_templates[template.id] = template
        self.logger.info(f"Created work template: {name} (ID: {template.id})")
        return template
    
    def get_work_template(self, template_id: str) -> Optional[WorkTemplate]:
        """Get a work template by ID"""
        return self.work_templates.get(template_id)
    
    def get_work_template_by_name(self, name: str) -> Optional[WorkTemplate]:
        """Get a work template by name"""
        return next((template for template in self.work_templates.values() if template.name == name), None)
    
    def list_work_templates(self) -> List[WorkTemplate]:
        """List all work templates"""
        return list(self.work_templates.values())
    
    def update_work_template(self, template_id: str, **kwargs) -> bool:
        """Update a work template"""
        template = self.get_work_template(template_id)
        if not template:
            return False
        
        for key, value in kwargs.items():
            if hasattr(template, key):
                setattr(template, key, value)
        
        self.logger.info(f"Updated work template: {template.name} (ID: {template_id})")
        return True
    
    # Process and Step configuration
    def create_process_from_config(self, config: Dict[str, Any]) -> Process:
        """Create a process from configuration dictionary"""
        process = Process(
            name=config.get('name', ''),
            description=config.get('description', ''),
            version=config.get('version', '1.0.0'),
            priority=Priority(config.get('priority', 'medium')),
            metadata=config.get('metadata', {})
        )
        
        # Set owner if specified
        if 'owner' in config:
            owner_config = config['owner']
            if isinstance(owner_config, str):
                # Owner ID or name
                owner = self.get_owner(owner_config) or self.get_owner_by_name(owner_config)
            else:
                # Owner configuration dict
                owner = self.create_owner(**owner_config)
            process.owner = owner
        
        # Add steps
        for step_config in config.get('steps', []):
            step = self.create_step_from_config(step_config)
            process.add_step(step)
        
        self.logger.info(f"Created process from config: {process.name}")
        return process
    
    def create_step_from_config(self, config: Dict[str, Any]) -> Step:
        """Create a step from configuration dictionary"""
        step = Step(
            name=config.get('name', ''),
            description=config.get('description', ''),
            sequence_order=config.get('sequence_order', 0),
            dependencies=config.get('dependencies', []),
            priority=Priority(config.get('priority', 'medium')),
            metadata=config.get('metadata', {})
        )
        
        # Set owner
        if 'owner' in config:
            owner_config = config['owner']
            if isinstance(owner_config, str):
                # Owner ID or name
                owner = self.get_owner(owner_config) or self.get_owner_by_name(owner_config)
            else:
                # Owner configuration dict
                owner = self.create_owner(**owner_config)
            step.owner = owner
        
        # Set SLA
        if 'sla' in config:
            sla_config = config['sla']
            if isinstance(sla_config, str):
                # SLA ID or name
                sla = self.get_sla(sla_config) or self.get_sla_by_name(sla_config)
            else:
                # SLA configuration dict
                duration_str = sla_config.get('duration', '1d')
                duration = self._parse_duration(duration_str)
                sla = self.create_sla(
                    name=sla_config.get('name', f"SLA-{step.name}"),
                    duration=duration,
                    warning_threshold=sla_config.get('warning_threshold', 0.8),
                    escalation_rules=sla_config.get('escalation_rules', [])
                )
            step.sla = sla
        
        # Set work template
        if 'work_template' in config:
            template_config = config['work_template']
            if isinstance(template_config, str):
                # Template ID or name
                template = self.get_work_template(template_config) or self.get_work_template_by_name(template_config)
            else:
                # Template configuration dict
                estimated_duration_str = template_config.get('estimated_duration', '1h')
                estimated_duration = self._parse_duration(estimated_duration_str)
                template = self.create_work_template(
                    name=template_config.get('name', f"Template-{step.name}"),
                    description=template_config.get('description', ''),
                    checklist=template_config.get('checklist', []),
                    required_documents=template_config.get('required_documents', []),
                    instructions=template_config.get('instructions', ''),
                    estimated_duration=estimated_duration
                )
            step.work_template = template
        
        self.logger.info(f"Created step from config: {step.name}")
        return step
    
    def _parse_duration(self, duration_str: str) -> timedelta:
        """Parse duration string like '1h', '2d', '30m' or '2 days, 0:00:00' into timedelta"""
        duration_str = duration_str.strip().lower()
        
        # Handle timedelta string representation like "2 days, 0:00:00"
        if 'days' in duration_str or ':' in duration_str:
            # Parse timedelta string representation
            parts = duration_str.split(',')
            days = 0
            hours = 0
            minutes = 0
            seconds = 0
            
            for part in parts:
                part = part.strip()
                if 'days' in part or 'day' in part:
                    days = int(part.split()[0])
                elif ':' in part:
                    time_parts = part.split(':')
                    hours = int(time_parts[0])
                    if len(time_parts) > 1:
                        minutes = int(time_parts[1])
                    if len(time_parts) > 2:
                        seconds = int(time_parts[2])
            
            return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        
        # Extract number and unit for simple format like "1h", "2d"
        for i, char in enumerate(duration_str):
            if char.isalpha():
                number = int(duration_str[:i])
                unit = duration_str[i:]
                break
        else:
            raise ValueError(f"Invalid duration format: {duration_str}")
        
        unit_map = {
            's': 'seconds',
            'm': 'minutes', 'min': 'minutes',
            'h': 'hours', 'hr': 'hours',
            'd': 'days',
            'w': 'weeks'
        }
        
        if unit not in unit_map:
            raise ValueError(f"Unknown duration unit: {unit}")
        
        kwargs = {unit_map[unit]: number}
        return timedelta(**kwargs)
    
    def export_config(self, process: Process) -> Dict[str, Any]:
        """Export process configuration to dictionary"""
        config = {
            'name': process.name,
            'description': process.description,
            'version': process.version,
            'priority': process.priority.value,
            'metadata': process.metadata,
            'steps': []
        }
        
        if process.owner:
            config['owner'] = {
                'name': process.owner.name,
                'email': process.owner.email,
                'department': process.owner.department,
                'role': process.owner.role
            }
        
        for step in process.steps:
            step_config = {
                'name': step.name,
                'description': step.description,
                'sequence_order': step.sequence_order,
                'dependencies': step.dependencies,
                'priority': step.priority.value,
                'metadata': step.metadata
            }
            
            if step.owner:
                step_config['owner'] = {
                    'name': step.owner.name,
                    'email': step.owner.email,
                    'department': step.owner.department,
                    'role': step.owner.role
                }
            
            if step.sla:
                # Format duration in a more parseable way
                total_seconds = int(step.sla.duration.total_seconds())
                if total_seconds >= 86400:  # days
                    days = total_seconds // 86400
                    hours = (total_seconds % 86400) // 3600
                    if hours > 0:
                        duration_str = f"{days}d{hours}h"
                    else:
                        duration_str = f"{days}d"
                elif total_seconds >= 3600:  # hours
                    hours = total_seconds // 3600
                    duration_str = f"{hours}h"
                else:  # minutes
                    minutes = total_seconds // 60
                    duration_str = f"{minutes}m"
                
                step_config['sla'] = {
                    'name': step.sla.name,
                    'duration': duration_str,
                    'warning_threshold': step.sla.warning_threshold,
                    'escalation_rules': step.sla.escalation_rules
                }
            
            if step.work_template:
                # Format duration in a more parseable way
                total_seconds = int(step.work_template.estimated_duration.total_seconds())
                if total_seconds >= 86400:  # days
                    days = total_seconds // 86400
                    hours = (total_seconds % 86400) // 3600
                    if hours > 0:
                        duration_str = f"{days}d{hours}h"
                    else:
                        duration_str = f"{days}d"
                elif total_seconds >= 3600:  # hours
                    hours = total_seconds // 3600
                    duration_str = f"{hours}h"
                else:  # minutes
                    minutes = total_seconds // 60
                    duration_str = f"{minutes}m"
                
                step_config['work_template'] = {
                    'name': step.work_template.name,
                    'description': step.work_template.description,
                    'checklist': step.work_template.checklist,
                    'required_documents': step.work_template.required_documents,
                    'instructions': step.work_template.instructions,
                    'estimated_duration': duration_str
                }
            
            config['steps'].append(step_config)
        
        return config
    
    def load_from_json(self, json_data: str) -> Process:
        """Load process configuration from JSON string"""
        config = json.loads(json_data)
        return self.create_process_from_config(config)
    
    def save_to_json(self, process: Process) -> str:
        """Save process configuration to JSON string"""
        config = self.export_config(process)
        return json.dumps(config, indent=2, default=str)