# RegTech.AI - SOP Control & Tracker

A comprehensive Standard Operating Procedure (SOP) control and tracking system designed for regulatory technology compliance workflows.

## Overview

The SOP Control & Tracker system provides:

- **Workflow Management**: Complete lifecycle management for SOP processes
- **SOP Configuration**: Flexible configuration system with Process, Step, SLA, Owner, and Work Template components
- **Real-time Tracking**: Monitor progress, SLA compliance, and workload distribution
- **Alerting & Reporting**: Automated alerts for SLA breaches and comprehensive reporting

## Key Components

### 1. Process
The top-level container for SOP workflows, containing multiple steps executed in sequence.

### 2. Step  
Individual tasks within a process, each with:
- Owner assignment
- SLA requirements
- Work templates
- Dependencies
- Status tracking

### 3. SLA (Service Level Agreement)
Defines time-based requirements with:
- Duration limits
- Warning thresholds
- Escalation rules
- Breach monitoring

### 4. Owner
People responsible for executing steps:
- Contact information
- Department/role details
- Workload tracking

### 5. Work Template
Reusable templates for standardizing work:
- Checklists
- Required documents
- Instructions
- Estimated duration

## Quick Start

```python
from sop_tracker import SOPController

# Initialize the controller
controller = SOPController()

# Create sample data
process = controller.create_sample_data()

# Start the process
controller.start_process(process.id)

# Complete a step
first_step = process.steps[0]
controller.complete_step(process.id, first_step.id)

# Check status
status = controller.get_process_status(process.id)
print(f"Progress: {status['progress']:.1%}")
```

## Example Usage

Run the provided example to see the system in action:

```bash
python example.py
```

This demonstrates:
- Creating owners, SLAs, and work templates
- Building a multi-step compliance process
- Starting and executing workflow steps
- Monitoring progress and SLA compliance
- Generating reports and dashboards

## Configuration Format

Processes can be defined using JSON configuration:

```json
{
  "name": "Regulatory Compliance Review",
  "description": "Standard process for reviewing regulatory compliance issues",
  "priority": "high",
  "steps": [
    {
      "name": "Initial Assessment",
      "sequence_order": 1,
      "owner": "John Smith",
      "sla": "Standard SLA",
      "work_template": "Risk Analysis Template"
    }
  ]
}
```

## Architecture

```
├── src/sop_tracker/
│   ├── models/          # Data models (Process, Step, SLA, etc.)
│   ├── services/        # Business logic (WorkflowManager, ConfigService)
│   ├── controllers/     # Main API interface (SOPController)
│   └── utils/           # Utility functions
├── example.py           # Demonstration script
└── README.md           # This file
```

## Features

- **Process Lifecycle Management**: Draft → In Progress → Completed/Suspended
- **Dependency Management**: Steps can depend on completion of other steps
- **SLA Monitoring**: Real-time tracking of service level agreements
- **Workload Distribution**: Track assignments across team members
- **Configuration Export/Import**: Save and load process configurations
- **Dashboard & Reporting**: Comprehensive metrics and status views
- **Escalation Support**: Configurable escalation rules for SLA breaches

## Use Cases

- Regulatory compliance workflows
- Document review processes
- Approval workflows
- Quality assurance procedures
- Audit preparation processes
- Risk assessment workflows

## Getting Started

1. Clone the repository
2. Run `python example.py` to see the system in action
3. Explore the generated `sample_sop_config.json` for configuration examples
4. Start building your own SOP processes using the API

The system is designed to be flexible and extensible, supporting various regulatory technology use cases while maintaining simplicity and ease of use.