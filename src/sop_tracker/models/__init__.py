"""
Data models for SOP Control & Tracker System
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from enum import Enum
import uuid


class SOPStatus(Enum):
    """Status enumeration for SOP items"""
    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    EXPIRED = "expired"


class Priority(Enum):
    """Priority levels for SOP items"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Owner:
    """Represents an owner/assignee of SOP items"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    email: str = ""
    department: str = ""
    role: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Owner name cannot be empty")


@dataclass
class SLA:
    """Service Level Agreement configuration"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    duration: timedelta = field(default=timedelta(hours=24))
    warning_threshold: float = 0.8  # 80% of duration
    escalation_rules: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("SLA name cannot be empty")
        if self.duration <= timedelta(0):
            raise ValueError("SLA duration must be positive")
    
    def is_breached(self, start_time: datetime) -> bool:
        """Check if SLA is breached based on start time"""
        return datetime.now() - start_time > self.duration
    
    def warning_time_reached(self, start_time: datetime) -> bool:
        """Check if warning threshold is reached"""
        elapsed = datetime.now() - start_time
        return elapsed >= self.duration * self.warning_threshold


@dataclass
class WorkTemplate:
    """Template for work items in SOP steps"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    checklist: List[str] = field(default_factory=list)
    required_documents: List[str] = field(default_factory=list)
    instructions: str = ""
    estimated_duration: timedelta = field(default=timedelta(hours=1))
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Work template name cannot be empty")


@dataclass
class Step:
    """Represents a step in an SOP process"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    sequence_order: int = 0
    owner: Optional[Owner] = None
    sla: Optional[SLA] = None
    work_template: Optional[WorkTemplate] = None
    dependencies: List[str] = field(default_factory=list)  # Step IDs
    status: SOPStatus = SOPStatus.DRAFT
    priority: Priority = Priority.MEDIUM
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Step name cannot be empty")
        if self.sequence_order < 0:
            raise ValueError("Sequence order must be non-negative")
    
    def start(self) -> None:
        """Start the step"""
        if self.status == SOPStatus.DRAFT:
            self.status = SOPStatus.IN_PROGRESS
            self.started_at = datetime.now()
    
    def complete(self) -> None:
        """Complete the step"""
        if self.status == SOPStatus.IN_PROGRESS:
            self.status = SOPStatus.COMPLETED
            self.completed_at = datetime.now()
    
    def is_sla_breached(self) -> bool:
        """Check if step SLA is breached"""
        if not self.sla or not self.started_at:
            return False
        return self.sla.is_breached(self.started_at)


@dataclass
class Process:
    """Represents an SOP process containing multiple steps"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    steps: List[Step] = field(default_factory=list)
    owner: Optional[Owner] = None
    status: SOPStatus = SOPStatus.DRAFT
    priority: Priority = Priority.MEDIUM
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name:
            raise ValueError("Process name cannot be empty")
    
    def add_step(self, step: Step) -> None:
        """Add a step to the process"""
        # Ensure unique sequence order
        existing_orders = {s.sequence_order for s in self.steps}
        if step.sequence_order in existing_orders:
            raise ValueError(f"Step with sequence order {step.sequence_order} already exists")
        
        self.steps.append(step)
        self.steps.sort(key=lambda s: s.sequence_order)
        self.updated_at = datetime.now()
    
    def remove_step(self, step_id: str) -> bool:
        """Remove a step from the process"""
        initial_count = len(self.steps)
        self.steps = [s for s in self.steps if s.id != step_id]
        if len(self.steps) < initial_count:
            self.updated_at = datetime.now()
            return True
        return False
    
    def get_step(self, step_id: str) -> Optional[Step]:
        """Get a step by ID"""
        return next((s for s in self.steps if s.id == step_id), None)
    
    def get_next_step(self, current_step_id: str) -> Optional[Step]:
        """Get the next step in sequence"""
        current_step = self.get_step(current_step_id)
        if not current_step:
            return None
        
        next_steps = [s for s in self.steps if s.sequence_order > current_step.sequence_order]
        return min(next_steps, key=lambda s: s.sequence_order) if next_steps else None
    
    def get_available_steps(self) -> List[Step]:
        """Get steps that can be started (dependencies met)"""
        available = []
        for step in self.steps:
            if step.status != SOPStatus.DRAFT:
                continue
            
            # Check if all dependencies are completed
            dependencies_met = all(
                self.get_step(dep_id) and self.get_step(dep_id).status == SOPStatus.COMPLETED
                for dep_id in step.dependencies
            )
            
            if dependencies_met:
                available.append(step)
        
        return available
    
    def start(self) -> None:
        """Start the process"""
        if self.status == SOPStatus.DRAFT:
            self.status = SOPStatus.IN_PROGRESS
            self.updated_at = datetime.now()
    
    def complete(self) -> None:
        """Complete the process"""
        if all(step.status == SOPStatus.COMPLETED for step in self.steps):
            self.status = SOPStatus.COMPLETED
            self.updated_at = datetime.now()
    
    def get_progress(self) -> float:
        """Get process completion progress (0.0 to 1.0)"""
        if not self.steps:
            return 0.0
        
        completed_steps = sum(1 for step in self.steps if step.status == SOPStatus.COMPLETED)
        return completed_steps / len(self.steps)