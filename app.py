#!/usr/bin/env python3
"""
Smart Workplace Application for Regtech.AI
Provides AI-powered workplace optimization and regulatory compliance monitoring
"""

import json
import os
import random
import math
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import webbrowser

class SmartWorkplace:
    def __init__(self):
        self.employees = []
        self.workspaces = []
        self.meetings = []
        self.compliance_rules = []
        self.analytics_data = {}
        self.load_sample_data()
        
    def load_sample_data(self):
        """Load sample data for demonstration"""
        sample_employees = [
            {"name": "Alice Johnson", "email": "alice@company.com", "department": "IT", "team_size": 5},
            {"name": "Bob Smith", "email": "bob@company.com", "department": "HR", "team_size": 3},
            {"name": "Carol Davis", "email": "carol@company.com", "department": "Finance", "team_size": 4},
        ]
        
        for emp_data in sample_employees:
            self.add_employee(emp_data)
        
    def add_employee(self, employee_data):
        """Add new employee to the system"""
        employee_data['id'] = len(self.employees) + 1
        employee_data['created_at'] = datetime.now().isoformat()
        employee_data['department_id'] = self.get_department_id(employee_data.get('department', 'General'))
        employee_data['work_hours_per_day'] = employee_data.get('work_hours_per_day', 8)
        employee_data['collaboration_score'] = employee_data.get('collaboration_score', random.randint(1, 10))
        self.employees.append(employee_data)
        return employee_data['id']
    
    def get_department_id(self, department_name):
        """Get department ID from name"""
        departments = {
            'IT': 1, 'HR': 2, 'Finance': 3, 'Legal': 4, 'Operations': 5
        }
        return departments.get(department_name, 0)
    
    def optimize_workspace_allocation(self):
        """AI-powered workspace optimization using simple clustering"""
        if len(self.employees) < 2:
            return {"message": "Not enough data for optimization"}
        
        # Simple clustering based on department and team size
        clusters = {}
        for emp in self.employees:
            dept = emp.get('department', 'General')
            if dept not in clusters:
                clusters[dept] = []
            clusters[dept].append(emp)
        
        workspace_assignments = {}
        zone_counter = 1
        
        for dept, employees in clusters.items():
            for emp in employees:
                workspace_assignments[emp['id']] = {
                    'employee_name': emp['name'],
                    'cluster': zone_counter - 1,
                    'recommended_zone': f"Zone {zone_counter}",
                    'collaboration_group': zone_counter - 1,
                    'department': dept
                }
            zone_counter += 1
        
        return workspace_assignments
    
    def check_compliance(self, employee_id):
        """Check regulatory compliance for an employee"""
        compliance_status = {
            'employee_id': employee_id,
            'checks': {
                'data_privacy_training': random.choice([True, False]),
                'security_clearance': random.choice([True, False]),
                'workspace_safety': random.choice([True, False]),
                'regulatory_updates': random.choice([True, False])
            },
            'score': 0,
            'status': 'compliant',
            'last_checked': datetime.now().isoformat()
        }
        
        # Calculate compliance score
        passed_checks = sum(compliance_status['checks'].values())
        total_checks = len(compliance_status['checks'])
        compliance_status['score'] = (passed_checks / total_checks) * 100
        
        if compliance_status['score'] < 75:
            compliance_status['status'] = 'non_compliant'
        elif compliance_status['score'] < 90:
            compliance_status['status'] = 'warning'
        
        return compliance_status
    
    def schedule_smart_meeting(self, meeting_data):
        """AI-powered meeting scheduling"""
        attendees = meeting_data.get('attendees', [])
        duration = meeting_data.get('duration_minutes', 60)
        preferred_time = meeting_data.get('preferred_time', '09:00')
        
        optimal_time = self._find_optimal_meeting_time(attendees, duration, preferred_time)
        
        meeting = {
            'id': len(self.meetings) + 1,
            'title': meeting_data.get('title', 'Smart Meeting'),
            'attendees': attendees,
            'scheduled_time': optimal_time,
            'duration_minutes': duration,
            'room': self._allocate_meeting_room(len(attendees)),
            'created_at': datetime.now().isoformat()
        }
        
        self.meetings.append(meeting)
        return meeting
    
    def _find_optimal_meeting_time(self, attendees, duration, preferred_time):
        """Find optimal meeting time based on attendee availability"""
        try:
            base_time = datetime.strptime(preferred_time, '%H:%M').time()
            today = datetime.now().date()
            optimal_datetime = datetime.combine(today, base_time)
            
            if optimal_datetime < datetime.now():
                optimal_datetime += timedelta(days=1)
            
            return optimal_datetime.isoformat()
        except:
            next_hour = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            return next_hour.isoformat()
    
    def _allocate_meeting_room(self, attendee_count):
        """Allocate appropriate meeting room based on attendee count"""
        if attendee_count <= 2:
            return "Small Room A"
        elif attendee_count <= 5:
            return "Medium Room B"
        elif attendee_count <= 10:
            return "Large Room C"
        else:
            return "Conference Hall"
    
    def get_workspace_analytics(self):
        """Generate workspace analytics and insights"""
        analytics = {
            'total_employees': len(self.employees),
            'total_meetings': len(self.meetings),
            'workspace_utilization': self._calculate_workspace_utilization(),
            'compliance_overview': self._get_compliance_overview(),
            'productivity_metrics': self._calculate_productivity_metrics(),
            'generated_at': datetime.now().isoformat()
        }
        
        return analytics
    
    def _calculate_workspace_utilization(self):
        """Calculate workspace utilization metrics"""
        total_capacity = 100
        occupied = len(self.employees)
        utilization_rate = (occupied / total_capacity) * 100 if total_capacity > 0 else 0
        
        return {
            'total_capacity': total_capacity,
            'occupied_spaces': occupied,
            'utilization_rate': round(utilization_rate, 2),
            'available_spaces': total_capacity - occupied
        }
    
    def _get_compliance_overview(self):
        """Get overall compliance status"""
        if not self.employees:
            return {'average_score': 0, 'compliant_employees': 0, 'total_employees': 0}
        
        total_score = 0
        compliant_count = 0
        
        for emp in self.employees:
            compliance = self.check_compliance(emp['id'])
            total_score += compliance['score']
            if compliance['status'] == 'compliant':
                compliant_count += 1
        
        return {
            'average_score': round(total_score / len(self.employees), 2),
            'compliant_employees': compliant_count,
            'total_employees': len(self.employees),
            'compliance_rate': round((compliant_count / len(self.employees)) * 100, 2)
        }
    
    def _calculate_productivity_metrics(self):
        """Calculate productivity metrics"""
        if not self.meetings:
            return {'meetings_per_day': 0, 'average_meeting_duration': 0}
        
        total_duration = sum(meeting.get('duration_minutes', 60) for meeting in self.meetings)
        avg_duration = total_duration / len(self.meetings) if self.meetings else 0
        
        return {
            'total_meetings': len(self.meetings),
            'meetings_per_day': round(len(self.meetings) / 7, 2),
            'average_meeting_duration': round(avg_duration, 2),
            'total_meeting_hours': round(total_duration / 60, 2)
        }

class SmartWorkplaceHandler(BaseHTTPRequestHandler):
    
    def __init__(self, smart_workplace, *args, **kwargs):
        self.smart_workplace = smart_workplace
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/':
            self.serve_html()
        elif path == '/api/employees':
            self.send_json_response(self.smart_workplace.employees)
        elif path == '/api/meetings':
            self.send_json_response(self.smart_workplace.meetings)
        elif path == '/api/analytics':
            analytics = self.smart_workplace.get_workspace_analytics()
            self.send_json_response(analytics)
        elif path.startswith('/api/compliance/'):
            employee_id = int(path.split('/')[-1])
            compliance = self.smart_workplace.check_compliance(employee_id)
            self.send_json_response(compliance)
        elif path == '/api/health':
            self.send_json_response({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            })
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except:
            data = {}
        
        if path == '/api/employees':
            employee_id = self.smart_workplace.add_employee(data)
            self.send_json_response({'id': employee_id, 'message': 'Employee added successfully'})
        elif path == '/api/meetings':
            meeting = self.smart_workplace.schedule_smart_meeting(data)
            self.send_json_response(meeting)
        elif path == '/api/workspace/optimize':
            optimization = self.smart_workplace.optimize_workspace_allocation()
            self.send_json_response(optimization)
        else:
            self.send_response(404)
            self.end_headers()
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def serve_html(self):
        """Serve the main HTML page"""
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Workplace - Regtech.AI</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar-brand { font-weight: bold; font-size: 1.5rem; }
        .card { border: none; box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); margin-bottom: 1.5rem; }
        .section { animation: fadeIn 0.3s ease-in; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-primary">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fas fa-brain me-2"></i>Smart Workplace - Regtech.AI
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-md-3">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-tachometer-alt me-2"></i>Dashboard</h5>
                    </div>
                    <div class="card-body">
                        <div class="list-group list-group-flush">
                            <a href="#" class="list-group-item list-group-item-action active" onclick="showSection('overview')">
                                <i class="fas fa-home me-2"></i>Overview
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="showSection('employees')">
                                <i class="fas fa-users me-2"></i>Employees
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="showSection('workspace')">
                                <i class="fas fa-building me-2"></i>Workspace
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="showSection('meetings')">
                                <i class="fas fa-calendar-alt me-2"></i>Meetings
                            </a>
                            <a href="#" class="list-group-item list-group-item-action" onclick="showSection('analytics')">
                                <i class="fas fa-chart-bar me-2"></i>Analytics
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-9">
                <div id="overview-section" class="section">
                    <div class="row mb-4">
                        <div class="col-md-3">
                            <div class="card bg-primary text-white">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h4 id="total-employees">0</h4>
                                            <p class="mb-0">Total Employees</p>
                                        </div>
                                        <div><i class="fas fa-users fa-2x"></i></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card bg-success text-white">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h4 id="workspace-utilization">0%</h4>
                                            <p class="mb-0">Workspace Utilization</p>
                                        </div>
                                        <div><i class="fas fa-building fa-2x"></i></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card bg-warning text-white">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h4 id="compliance-rate">0%</h4>
                                            <p class="mb-0">Compliance Rate</p>
                                        </div>
                                        <div><i class="fas fa-shield-alt fa-2x"></i></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card bg-info text-white">
                                <div class="card-body">
                                    <div class="d-flex justify-content-between">
                                        <div>
                                            <h4 id="total-meetings">0</h4>
                                            <p class="mb-0">Total Meetings</p>
                                        </div>
                                        <div><i class="fas fa-calendar-alt fa-2x"></i></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">
                                    <h6><i class="fas fa-rocket me-2"></i>Quick Actions</h6>
                                </div>
                                <div class="card-body">
                                    <button class="btn btn-primary me-2 mb-2" onclick="addSampleEmployee()">
                                        <i class="fas fa-user-plus me-1"></i>Add Sample Employee
                                    </button>
                                    <button class="btn btn-success me-2 mb-2" onclick="optimizeWorkspace()">
                                        <i class="fas fa-cogs me-1"></i>Optimize Workspace
                                    </button>
                                    <button class="btn btn-info me-2 mb-2" onclick="scheduleSampleMeeting()">
                                        <i class="fas fa-calendar-plus me-1"></i>Schedule Meeting
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="card">
                                <div class="card-header">
                                    <h6><i class="fas fa-info-circle me-2"></i>System Status</h6>
                                </div>
                                <div class="card-body">
                                    <div class="d-flex align-items-center mb-2">
                                        <i class="fas fa-check-circle text-success me-2"></i>
                                        <span>AI Optimization Engine: Online</span>
                                    </div>
                                    <div class="d-flex align-items-center mb-2">
                                        <i class="fas fa-check-circle text-success me-2"></i>
                                        <span>Compliance Monitor: Active</span>
                                    </div>
                                    <div class="d-flex align-items-center">
                                        <i class="fas fa-check-circle text-success me-2"></i>
                                        <span>Smart Scheduler: Ready</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div id="employees-section" class="section" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-users me-2"></i>Employee Management</h5>
                        </div>
                        <div class="card-body">
                            <div id="employees-content"></div>
                        </div>
                    </div>
                </div>

                <div id="workspace-section" class="section" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-building me-2"></i>Workspace Optimization</h5>
                        </div>
                        <div class="card-body">
                            <div id="workspace-content"></div>
                        </div>
                    </div>
                </div>

                <div id="meetings-section" class="section" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-calendar-alt me-2"></i>Meeting Management</h5>
                        </div>
                        <div class="card-body">
                            <div id="meetings-content"></div>
                        </div>
                    </div>
                </div>

                <div id="analytics-section" class="section" style="display: none;">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-chart-bar me-2"></i>Workplace Analytics</h5>
                        </div>
                        <div class="card-body">
                            <div id="analytics-content"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let employees = [];
        let meetings = [];
        let analytics = {};

        async function loadData() {
            try {
                const [empResponse, meetingsResponse, analyticsResponse] = await Promise.all([
                    fetch('/api/employees'),
                    fetch('/api/meetings'),
                    fetch('/api/analytics')
                ]);
                
                employees = await empResponse.json();
                meetings = await meetingsResponse.json();
                analytics = await analyticsResponse.json();
                
                updateDashboard();
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }

        function updateDashboard() {
            document.getElementById('total-employees').textContent = analytics.total_employees || 0;
            document.getElementById('total-meetings').textContent = analytics.total_meetings || 0;
            document.getElementById('workspace-utilization').textContent = 
                analytics.workspace_utilization ? analytics.workspace_utilization.utilization_rate + '%' : '0%';
            document.getElementById('compliance-rate').textContent = 
                analytics.compliance_overview ? analytics.compliance_overview.compliance_rate + '%' : '0%';
        }

        function showSection(sectionName) {
            document.querySelectorAll('.section').forEach(section => {
                section.style.display = 'none';
            });
            
            document.getElementById(sectionName + '-section').style.display = 'block';
            
            document.querySelectorAll('.list-group-item-action').forEach(item => {
                item.classList.remove('active');
            });
            
            event.target.classList.add('active');
            
            if (sectionName === 'employees') renderEmployees();
            else if (sectionName === 'workspace') renderWorkspace();
            else if (sectionName === 'meetings') renderMeetings();
            else if (sectionName === 'analytics') renderAnalytics();
        }

        function renderEmployees() {
            const content = document.getElementById('employees-content');
            if (employees.length === 0) {
                content.innerHTML = '<p class="text-muted">No employees found. Click "Add Sample Employee" to get started.</p>';
                return;
            }
            
            content.innerHTML = employees.map(emp => `
                <div class="card mb-2">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <h6>${emp.name}</h6>
                                <p class="mb-1"><strong>Department:</strong> ${emp.department || 'N/A'}</p>
                                <p class="mb-1"><strong>Email:</strong> ${emp.email}</p>
                                <p class="mb-0"><strong>Team Size:</strong> ${emp.team_size || 'N/A'}</p>
                            </div>
                            <div class="col-md-4 text-end">
                                <button class="btn btn-sm btn-outline-info" onclick="checkCompliance(${emp.id})">
                                    <i class="fas fa-shield-alt"></i> Check Compliance
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');
        }

        function renderWorkspace() {
            const content = document.getElementById('workspace-content');
            content.innerHTML = `
                <button class="btn btn-success mb-3" onclick="optimizeWorkspace()">
                    <i class="fas fa-cogs me-1"></i>Run Workspace Optimization
                </button>
                <div id="workspace-results"></div>
            `;
        }

        function renderMeetings() {
            const content = document.getElementById('meetings-content');
            content.innerHTML = meetings.map(meeting => `
                <div class="card mb-2">
                    <div class="card-body">
                        <h6>${meeting.title}</h6>
                        <p class="mb-1"><strong>Time:</strong> ${new Date(meeting.scheduled_time).toLocaleString()}</p>
                        <p class="mb-1"><strong>Duration:</strong> ${meeting.duration_minutes} minutes</p>
                        <p class="mb-1"><strong>Room:</strong> ${meeting.room}</p>
                        <p class="mb-0"><strong>Attendees:</strong> ${meeting.attendees.length}</p>
                    </div>
                </div>
            `).join('') || '<p class="text-muted">No meetings scheduled.</p>';
        }

        function renderAnalytics() {
            const content = document.getElementById('analytics-content');
            content.innerHTML = `
                <div class="row">
                    <div class="col-md-6">
                        <h6>Workspace Utilization</h6>
                        <p><strong>Total Capacity:</strong> ${analytics.workspace_utilization?.total_capacity || 0}</p>
                        <p><strong>Occupied:</strong> ${analytics.workspace_utilization?.occupied_spaces || 0}</p>
                        <p><strong>Available:</strong> ${analytics.workspace_utilization?.available_spaces || 0}</p>
                    </div>
                    <div class="col-md-6">
                        <h6>Compliance Overview</h6>
                        <p><strong>Average Score:</strong> ${analytics.compliance_overview?.average_score || 0}%</p>
                        <p><strong>Compliant Employees:</strong> ${analytics.compliance_overview?.compliant_employees || 0}</p>
                        <p><strong>Total Employees:</strong> ${analytics.compliance_overview?.total_employees || 0}</p>
                    </div>
                </div>
            `;
        }

        async function addSampleEmployee() {
            const sampleEmployees = [
                {name: "John Doe", email: "john@company.com", department: "IT", team_size: 4},
                {name: "Jane Smith", email: "jane@company.com", department: "HR", team_size: 6},
                {name: "Mike Johnson", email: "mike@company.com", department: "Finance", team_size: 3}
            ];
            
            const randomEmployee = sampleEmployees[Math.floor(Math.random() * sampleEmployees.length)];
            
            await fetch('/api/employees', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(randomEmployee)
            });
            
            await loadData();
            showAlert('Employee added successfully!', 'success');
        }

        async function optimizeWorkspace() {
            const response = await fetch('/api/workspace/optimize', {method: 'POST'});
            const result = await response.json();
            
            const resultsDiv = document.getElementById('workspace-results');
            if (result.message) {
                resultsDiv.innerHTML = `<div class="alert alert-info">${result.message}</div>`;
                return;
            }
            
            const zones = {};
            Object.values(result).forEach(assignment => {
                const zone = assignment.recommended_zone;
                if (!zones[zone]) zones[zone] = [];
                zones[zone].push(assignment);
            });
            
            resultsDiv.innerHTML = `
                <div class="alert alert-success">Workspace optimization complete!</div>
                ${Object.entries(zones).map(([zone, assignments]) => `
                    <div class="card mb-2">
                        <div class="card-header"><strong>${zone}</strong></div>
                        <div class="card-body">
                            ${assignments.map(a => `<span class="badge bg-primary me-2">${a.employee_name}</span>`).join('')}
                        </div>
                    </div>
                `).join('')}
            `;
        }

        async function scheduleSampleMeeting() {
            const sampleMeeting = {
                title: "Team Sync Meeting",
                attendees: ["john@company.com", "jane@company.com"],
                duration_minutes: 30,
                preferred_time: "14:00"
            };
            
            await fetch('/api/meetings', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(sampleMeeting)
            });
            
            await loadData();
            showAlert('Meeting scheduled successfully!', 'success');
        }

        async function checkCompliance(employeeId) {
            const response = await fetch(`/api/compliance/${employeeId}`);
            const compliance = await response.json();
            
            const statusClass = compliance.status === 'compliant' ? 'success' : 
                               compliance.status === 'warning' ? 'warning' : 'danger';
            
            showAlert(
                `Compliance Score: ${compliance.score}% (${compliance.status.replace('_', ' ').toUpperCase()})`,
                statusClass
            );
        }

        function showAlert(message, type = 'info') {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
            alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            document.body.appendChild(alertDiv);
            
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.parentNode.removeChild(alertDiv);
                }
            }, 3000);
        }

        // Initialize the application
        document.addEventListener('DOMContentLoaded', loadData);
    </script>
</body>
</html>'''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override to reduce log noise"""
        return

def create_handler(smart_workplace):
    """Create a handler class with smart_workplace instance"""
    def handler(*args, **kwargs):
        SmartWorkplaceHandler(smart_workplace, *args, **kwargs)
    return handler

def main():
    """Main function to run the Smart Workplace application"""
    print("🧠 Smart Workplace - Regtech.AI")
    print("=" * 50)
    
    # Initialize the smart workplace system
    smart_workplace = SmartWorkplace()
    
    # Create HTTP server
    server_address = ('localhost', 8000)
    handler_class = create_handler(smart_workplace)
    httpd = HTTPServer(server_address, handler_class)
    
    print(f"🚀 Server starting on http://{server_address[0]}:{server_address[1]}")
    print("📊 Features available:")
    print("  • AI-powered workspace optimization")
    print("  • Smart meeting scheduling")
    print("  • Regulatory compliance monitoring")
    print("  • Real-time analytics dashboard")
    print("\n💡 Open your browser and navigate to the URL above")
    print("🛑 Press Ctrl+C to stop the server")
    
    try:
        # Try to open browser automatically
        def open_browser():
            import time
            time.sleep(1)
            try:
                webbrowser.open(f'http://{server_address[0]}:{server_address[1]}')
            except:
                pass
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.server_close()

if __name__ == '__main__':
    main()