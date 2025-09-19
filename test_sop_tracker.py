"""
Basic tests for SOP Control & Tracker
"""

import unittest
import sys
import os
from datetime import timedelta

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sop_tracker import SOPController, SOPStatus, Priority


class TestSOPTracker(unittest.TestCase):
    """Test cases for SOP Control & Tracker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.controller = SOPController()
    
    def test_create_owner(self):
        """Test owner creation"""
        owner = self.controller.create_owner("Test User", "test@example.com", "IT", "Developer")
        self.assertEqual(owner.name, "Test User")
        self.assertEqual(owner.email, "test@example.com")
        self.assertEqual(owner.department, "IT")
        self.assertEqual(owner.role, "Developer")
    
    def test_create_sla(self):
        """Test SLA creation"""
        sla = self.controller.create_sla("Test SLA", timedelta(hours=24))
        self.assertEqual(sla.name, "Test SLA")
        self.assertEqual(sla.duration, timedelta(hours=24))
        self.assertEqual(sla.warning_threshold, 0.8)
    
    def test_create_work_template(self):
        """Test work template creation"""
        template = self.controller.create_work_template(
            "Test Template", 
            "Description",
            ["Task 1", "Task 2"],
            "Follow these instructions"
        )
        self.assertEqual(template.name, "Test Template")
        self.assertEqual(len(template.checklist), 2)
        self.assertEqual(template.instructions, "Follow these instructions")
    
    def test_create_process(self):
        """Test process creation"""
        process = self.controller.create_process("Test Process", "Test Description")
        self.assertEqual(process.name, "Test Process")
        self.assertEqual(process.description, "Test Description")
        self.assertEqual(process.status, SOPStatus.DRAFT)
        self.assertEqual(len(process.steps), 0)
    
    def test_process_workflow(self):
        """Test complete workflow"""
        # Create sample data
        process = self.controller.create_sample_data()
        
        # Verify initial state
        self.assertEqual(process.status, SOPStatus.DRAFT)
        self.assertEqual(process.get_progress(), 0.0)
        
        # Start process
        success = self.controller.start_process(process.id)
        self.assertTrue(success)
        self.assertEqual(process.status, SOPStatus.IN_PROGRESS)
        
        # Complete first step
        first_step = process.steps[0]
        success = self.controller.complete_step(process.id, first_step.id)
        self.assertTrue(success)
        self.assertEqual(first_step.status, SOPStatus.COMPLETED)
        self.assertEqual(process.get_progress(), 0.25)  # 1 of 4 steps completed
    
    def test_process_status(self):
        """Test process status reporting"""
        process = self.controller.create_sample_data()
        status = self.controller.get_process_status(process.id)
        
        self.assertIsNotNone(status)
        self.assertEqual(status['process_id'], process.id)
        self.assertEqual(status['name'], process.name)
        self.assertEqual(status['status'], 'draft')
        self.assertEqual(status['total_steps'], 4)
        self.assertEqual(status['completed_steps'], 0)
    
    def test_dashboard_summary(self):
        """Test dashboard summary"""
        # Create sample data
        self.controller.create_sample_data()
        
        summary = self.controller.get_dashboard_summary()
        
        self.assertIn('processes', summary)
        self.assertIn('steps', summary)
        self.assertIn('sla_alerts', summary)
        self.assertIn('owners', summary)
        
        self.assertEqual(summary['processes']['total'], 1)
        self.assertEqual(summary['steps']['total'], 4)
        self.assertEqual(summary['owners']['total'], 4)  # 3 + 1 process owner
    
    def test_config_export_import(self):
        """Test configuration export and import"""
        # Create sample data
        original_process = self.controller.create_sample_data()
        
        # Export configuration
        config_json = self.controller.export_process_config(original_process.id)
        self.assertIsNotNone(config_json)
        self.assertIn(original_process.name, config_json)
        
        # Import configuration
        imported_process = self.controller.import_process_config(config_json)
        self.assertIsNotNone(imported_process)
        self.assertEqual(imported_process.name, original_process.name)
        self.assertEqual(len(imported_process.steps), len(original_process.steps))


if __name__ == '__main__':
    unittest.main()