#!/usr/bin/env python3
"""
SOP Control & Tracker Example

This script demonstrates the key features of the SOP Control & Tracker system:
- Workflow management
- SOP configuration (Process, Step, SLA, Owner, Work Template)
"""

import sys
import os
from datetime import timedelta

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sop_tracker import SOPController, SOPStatus, Priority


def main():
    """Demonstrate SOP Control & Tracker functionality"""
    print("=== SOP Control & Tracker Demo ===\n")
    
    # Initialize the SOP controller
    controller = SOPController()
    
    # Create sample data
    print("1. Creating sample data...")
    process = controller.create_sample_data()
    print(f"   Created process: {process.name} (ID: {process.id})")
    print(f"   Process has {len(process.steps)} steps")
    
    # Display owners
    print("\n2. Available owners:")
    for owner in controller.list_owners():
        print(f"   - {owner.name} ({owner.department})")
    
    # Display SLAs
    print("\n3. Available SLAs:")
    for sla in controller.list_slas():
        print(f"   - {sla.name}: {sla.duration}")
    
    # Display work templates
    print("\n4. Available work templates:")
    for template in controller.list_work_templates():
        print(f"   - {template.name}")
        if template.checklist:
            print(f"     Checklist: {', '.join(template.checklist[:2])}...")
    
    # Show process status before starting
    print(f"\n5. Process status (before starting):")
    status = controller.get_process_status(process.id)
    if status:
        print(f"   Status: {status['status']}")
        print(f"   Progress: {status['progress']:.1%}")
        print(f"   Steps: {status['completed_steps']}/{status['total_steps']} completed")
    
    # Start the process
    print(f"\n6. Starting process...")
    if controller.start_process(process.id):
        print("   Process started successfully!")
    else:
        print("   Failed to start process")
    
    # Show updated status
    print(f"\n7. Process status (after starting):")
    status = controller.get_process_status(process.id)
    if status:
        print(f"   Status: {status['status']}")
        print(f"   Progress: {status['progress']:.1%}")
        print(f"   In progress steps: {status['in_progress_steps']}")
        
        print("   Step details:")
        for step in status['steps']:
            print(f"     - {step['name']}: {step['status']} (Order: {step['sequence_order']})")
            if step['owner']:
                print(f"       Owner: {step['owner']}")
    
    # Complete first step
    first_step = process.steps[0] if process.steps else None
    if first_step and first_step.status == SOPStatus.IN_PROGRESS:
        print(f"\n8. Completing first step: {first_step.name}")
        if controller.complete_step(process.id, first_step.id):
            print("   Step completed successfully!")
        
        # Show updated status
        status = controller.get_process_status(process.id)
        if status:
            print(f"   Updated progress: {status['progress']:.1%}")
    
    # Show dashboard summary
    print(f"\n9. Dashboard summary:")
    summary = controller.get_dashboard_summary()
    print(f"   Total processes: {summary['processes']['total']}")
    print(f"   Active processes: {summary['processes']['active']}")
    print(f"   Total steps: {summary['steps']['total']}")
    print(f"   Step completion rate: {summary['steps']['completion_rate']:.1%}")
    print(f"   SLA breaches: {summary['sla_alerts']['total_breaches']}")
    
    # Show workload for an owner
    if controller.list_owners():
        first_owner = controller.list_owners()[0]
        print(f"\n10. Workload for {first_owner.name}:")
        workload = controller.get_workload_by_owner(first_owner.name)
        print(f"    Total assigned: {workload['total_assigned']}")
        print(f"    In progress: {workload['in_progress']}")
        print(f"    Completed: {workload['completed']}")
        print(f"    SLA breached: {workload['sla_breached']}")
    
    # Export configuration
    print(f"\n11. Exporting process configuration...")
    config_json = controller.export_process_config(process.id)
    if config_json:
        print("   Configuration exported successfully!")
        print(f"   Size: {len(config_json)} characters")
        
        # Save to file
        with open('sample_sop_config.json', 'w') as f:
            f.write(config_json)
        print("   Saved to: sample_sop_config.json")
    
    print("\n=== Demo completed successfully! ===")


if __name__ == "__main__":
    main()