// Smart Workplace JavaScript Application
class SmartWorkplaceApp {
    constructor() {
        this.apiBaseUrl = '/api';
        this.employees = [];
        this.meetings = [];
        this.analytics = {};
        this.init();
    }

    async init() {
        await this.loadData();
        this.updateDashboard();
        this.setupEventListeners();
    }

    async loadData() {
        try {
            await Promise.all([
                this.loadEmployees(),
                this.loadMeetings(),
                this.loadAnalytics()
            ]);
        } catch (error) {
            console.error('Error loading data:', error);
            this.showAlert('Error loading data. Please refresh the page.', 'danger');
        }
    }

    async loadEmployees() {
        const response = await fetch(`${this.apiBaseUrl}/employees`);
        this.employees = await response.json();
        this.renderEmployeesTable();
    }

    async loadMeetings() {
        const response = await fetch(`${this.apiBaseUrl}/meetings`);
        this.meetings = await response.json();
        this.renderMeetingsTable();
    }

    async loadAnalytics() {
        const response = await fetch(`${this.apiBaseUrl}/analytics`);
        this.analytics = await response.json();
        this.updateAnalyticsOverview();
    }

    updateDashboard() {
        document.getElementById('total-employees').textContent = this.employees.length;
        document.getElementById('total-meetings').textContent = this.meetings.length;
        
        if (this.analytics.workspace_utilization) {
            document.getElementById('workspace-utilization').textContent = 
                `${this.analytics.workspace_utilization.utilization_rate}%`;
        }
        
        if (this.analytics.compliance_overview) {
            document.getElementById('compliance-rate').textContent = 
                `${this.analytics.compliance_overview.compliance_rate}%`;
        }
    }

    renderEmployeesTable() {
        const tbody = document.getElementById('employees-table');
        
        if (this.employees.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No employees found</td></tr>';
            return;
        }

        tbody.innerHTML = this.employees.map(emp => `
            <tr>
                <td>${emp.id}</td>
                <td>${emp.name}</td>
                <td>${emp.department || 'N/A'}</td>
                <td>${emp.email}</td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="app.checkEmployeeCompliance(${emp.id})">
                        <i class="fas fa-shield-alt"></i> Check Compliance
                    </button>
                </td>
            </tr>
        `).join('');
    }

    renderMeetingsTable() {
        const tbody = document.getElementById('meetings-table');
        
        if (this.meetings.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No meetings scheduled</td></tr>';
            return;
        }

        tbody.innerHTML = this.meetings.map(meeting => `
            <tr>
                <td>${meeting.id}</td>
                <td>${meeting.title}</td>
                <td>${this.formatDateTime(meeting.scheduled_time)}</td>
                <td>${meeting.duration_minutes} min</td>
                <td>${meeting.room}</td>
                <td>${meeting.attendees.length} attendees</td>
            </tr>
        `).join('');
    }

    updateAnalyticsOverview() {
        if (!this.analytics) return;

        // Update dashboard cards
        if (this.analytics.total_employees !== undefined) {
            document.getElementById('total-employees').textContent = this.analytics.total_employees;
        }
        
        if (this.analytics.total_meetings !== undefined) {
            document.getElementById('total-meetings').textContent = this.analytics.total_meetings;
        }
        
        if (this.analytics.workspace_utilization) {
            document.getElementById('workspace-utilization').textContent = 
                `${this.analytics.workspace_utilization.utilization_rate}%`;
        }
        
        if (this.analytics.compliance_overview) {
            document.getElementById('compliance-rate').textContent = 
                `${this.analytics.compliance_overview.compliance_rate}%`;
        }
    }

    async addEmployee() {
        const name = document.getElementById('employee-name').value;
        const email = document.getElementById('employee-email').value;
        const department = document.getElementById('employee-department').value;
        const teamSize = parseInt(document.getElementById('employee-team-size').value);

        if (!name || !email || !department) {
            this.showAlert('Please fill in all required fields.', 'warning');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/employees`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    name,
                    email,
                    department,
                    team_size: teamSize,
                    department_id: this.getDepartmentId(department),
                    work_hours_per_day: 8,
                    collaboration_score: Math.floor(Math.random() * 10) + 1
                }),
            });

            if (response.ok) {
                const result = await response.json();
                this.showAlert('Employee added successfully!', 'success');
                await this.loadEmployees();
                await this.loadAnalytics();
                this.updateDashboard();
                this.hideModal('addEmployeeModal');
                this.clearForm('addEmployeeForm');
            } else {
                throw new Error('Failed to add employee');
            }
        } catch (error) {
            console.error('Error adding employee:', error);
            this.showAlert('Error adding employee. Please try again.', 'danger');
        }
    }

    async scheduleMeeting() {
        const title = document.getElementById('meeting-title').value;
        const attendeesText = document.getElementById('meeting-attendees').value;
        const duration = parseInt(document.getElementById('meeting-duration').value);
        const time = document.getElementById('meeting-time').value;

        if (!title || !attendeesText) {
            this.showAlert('Please fill in all required fields.', 'warning');
            return;
        }

        const attendees = attendeesText.split(',').map(email => email.trim()).filter(email => email);

        try {
            const response = await fetch(`${this.apiBaseUrl}/meetings`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    title,
                    attendees,
                    duration_minutes: duration,
                    preferred_time: time
                }),
            });

            if (response.ok) {
                const result = await response.json();
                this.showAlert('Meeting scheduled successfully!', 'success');
                await this.loadMeetings();
                await this.loadAnalytics();
                this.updateDashboard();
                this.hideModal('addMeetingModal');
                this.clearForm('addMeetingForm');
            } else {
                throw new Error('Failed to schedule meeting');
            }
        } catch (error) {
            console.error('Error scheduling meeting:', error);
            this.showAlert('Error scheduling meeting. Please try again.', 'danger');
        }
    }

    async optimizeWorkspace() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/workspace/optimize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            const result = await response.json();
            this.renderWorkspaceOptimization(result);
        } catch (error) {
            console.error('Error optimizing workspace:', error);
            this.showAlert('Error optimizing workspace. Please try again.', 'danger');
        }
    }

    renderWorkspaceOptimization(result) {
        const container = document.getElementById('workspace-optimization-result');
        
        if (result.message) {
            container.innerHTML = `<div class="alert alert-info">${result.message}</div>`;
            return;
        }

        const zones = {};
        Object.values(result).forEach(assignment => {
            const zone = assignment.recommended_zone;
            if (!zones[zone]) zones[zone] = [];
            zones[zone].push(assignment);
        });

        container.innerHTML = `
            <div class="alert alert-success">
                <i class="fas fa-check-circle me-2"></i>Workspace optimization complete!
            </div>
            ${Object.entries(zones).map(([zone, assignments]) => `
                <div class="workspace-zone">
                    <h5><i class="fas fa-map-marker-alt me-2"></i>${zone}</h5>
                    <div class="row">
                        ${assignments.map(assignment => `
                            <div class="col-md-4 mb-2">
                                <div class="card">
                                    <div class="card-body p-2">
                                        <h6 class="card-title mb-1">${assignment.employee_name}</h6>
                                        <small class="text-muted">Collaboration Group ${assignment.collaboration_group + 1}</small>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('')}
        `;
    }

    async checkEmployeeCompliance(employeeId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/compliance/${employeeId}`);
            const compliance = await response.json();
            this.renderComplianceResults([compliance]);
            this.showSection('compliance');
        } catch (error) {
            console.error('Error checking compliance:', error);
            this.showAlert('Error checking compliance. Please try again.', 'danger');
        }
    }

    async loadAllCompliance() {
        try {
            const complianceResults = await Promise.all(
                this.employees.map(emp => 
                    fetch(`${this.apiBaseUrl}/compliance/${emp.id}`).then(r => r.json())
                )
            );
            this.renderComplianceResults(complianceResults);
        } catch (error) {
            console.error('Error loading compliance data:', error);
            this.showAlert('Error loading compliance data. Please try again.', 'danger');
        }
    }

    renderComplianceResults(results) {
        const container = document.getElementById('compliance-results');
        
        container.innerHTML = results.map(compliance => {
            const employee = this.employees.find(emp => emp.id === compliance.employee_id);
            const statusClass = compliance.status === 'compliant' ? 'success' : 
                               compliance.status === 'warning' ? 'warning' : 'danger';
            
            return `
                <div class="compliance-item compliance-${compliance.status === 'compliant' ? 'passed' : 'failed'}">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h6 class="mb-0">
                            <i class="fas fa-user me-2"></i>${employee ? employee.name : 'Unknown Employee'}
                        </h6>
                        <span class="badge bg-${statusClass} status-badge">${compliance.status.replace('_', ' ').toUpperCase()}</span>
                    </div>
                    <div class="row">
                        <div class="col-md-8">
                            <div class="row">
                                ${Object.entries(compliance.checks).map(([check, passed]) => `
                                    <div class="col-md-6 mb-2">
                                        <small class="d-flex align-items-center">
                                            <i class="fas fa-${passed ? 'check text-success' : 'times text-danger'} me-2"></i>
                                            ${check.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                        </small>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        <div class="col-md-4 text-end">
                            <h4 class="text-${statusClass}">${compliance.score}%</h4>
                            <small class="text-muted">Compliance Score</small>
                        </div>
                    </div>
                    <small class="text-muted">Last checked: ${this.formatDateTime(compliance.last_checked)}</small>
                </div>
            `;
        }).join('');
    }

    renderAnalytics() {
        const container = document.getElementById('analytics-content');
        
        if (!this.analytics) {
            container.innerHTML = '<div class="alert alert-info">Loading analytics...</div>';
            return;
        }

        container.innerHTML = `
            <div class="row mb-4">
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h3>${this.analytics.total_employees || 0}</h3>
                        <p>Total Employees</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h3>${this.analytics.total_meetings || 0}</h3>
                        <p>Total Meetings</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h3>${this.analytics.workspace_utilization ? this.analytics.workspace_utilization.utilization_rate + '%' : '0%'}</h3>
                        <p>Workspace Utilization</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="analytics-metric">
                        <h3>${this.analytics.compliance_overview ? this.analytics.compliance_overview.compliance_rate + '%' : '0%'}</h3>
                        <p>Compliance Rate</p>
                    </div>
                </div>
            </div>
            
            ${this.analytics.workspace_utilization ? `
                <div class="card mb-4">
                    <div class="card-header">
                        <h6><i class="fas fa-building me-2"></i>Workspace Utilization Details</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Total Capacity:</strong> ${this.analytics.workspace_utilization.total_capacity}</p>
                                <p><strong>Occupied Spaces:</strong> ${this.analytics.workspace_utilization.occupied_spaces}</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Available Spaces:</strong> ${this.analytics.workspace_utilization.available_spaces}</p>
                                <p><strong>Utilization Rate:</strong> ${this.analytics.workspace_utilization.utilization_rate}%</p>
                            </div>
                        </div>
                    </div>
                </div>
            ` : ''}
            
            ${this.analytics.productivity_metrics ? `
                <div class="card">
                    <div class="card-header">
                        <h6><i class="fas fa-chart-line me-2"></i>Productivity Metrics</h6>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <p><strong>Meetings per Day:</strong> ${this.analytics.productivity_metrics.meetings_per_day}</p>
                                <p><strong>Average Meeting Duration:</strong> ${this.analytics.productivity_metrics.average_meeting_duration} min</p>
                            </div>
                            <div class="col-md-6">
                                <p><strong>Total Meeting Hours:</strong> ${this.analytics.productivity_metrics.total_meeting_hours} hrs</p>
                                <p><strong>Total Meetings:</strong> ${this.analytics.productivity_metrics.total_meetings}</p>
                            </div>
                        </div>
                    </div>
                </div>
            ` : ''}
        `;
    }

    setupEventListeners() {
        // Add any additional event listeners here
    }

    showSection(sectionName) {
        // Hide all sections
        document.querySelectorAll('.section').forEach(section => {
            section.style.display = 'none';
        });
        
        // Show selected section
        const targetSection = document.getElementById(`${sectionName}-section`);
        if (targetSection) {
            targetSection.style.display = 'block';
        }
        
        // Update active menu item
        document.querySelectorAll('.list-group-item-action').forEach(item => {
            item.classList.remove('active');
        });
        
        const activeItem = document.querySelector(`[onclick="showSection('${sectionName}')"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }
        
        // Load section-specific data
        if (sectionName === 'compliance') {
            this.loadAllCompliance();
        } else if (sectionName === 'analytics') {
            this.renderAnalytics();
        }
    }

    showAddEmployeeModal() {
        const modal = new bootstrap.Modal(document.getElementById('addEmployeeModal'));
        modal.show();
    }

    showAddMeetingModal() {
        const modal = new bootstrap.Modal(document.getElementById('addMeetingModal'));
        modal.show();
    }

    hideModal(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) {
            modal.hide();
        }
    }

    clearForm(formId) {
        document.getElementById(formId).reset();
    }

    getDepartmentId(departmentName) {
        const departments = {
            'IT': 1,
            'HR': 2,
            'Finance': 3,
            'Legal': 4,
            'Operations': 5
        };
        return departments[departmentName] || 0;
    }

    formatDateTime(isoString) {
        try {
            const date = new Date(isoString);
            return date.toLocaleString();
        } catch {
            return isoString;
        }
    }

    showAlert(message, type = 'info') {
        // Create and show a temporary alert
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alertDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.parentNode.removeChild(alertDiv);
            }
        }, 5000);
    }
}

// Global functions for HTML onclick events
function showSection(sectionName) {
    app.showSection(sectionName);
}

function showAddEmployeeModal() {
    app.showAddEmployeeModal();
}

function showAddMeetingModal() {
    app.showAddMeetingModal();
}

function addEmployee() {
    app.addEmployee();
}

function scheduleMeeting() {
    app.scheduleMeeting();
}

function optimizeWorkspace() {
    app.optimizeWorkspace();
}

// Initialize the application when the page loads
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new SmartWorkplaceApp();
});