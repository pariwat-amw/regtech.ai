# Smart Workplace - Regtech.AI

An AI-powered smart workplace management system that provides comprehensive employee management, workspace optimization, meeting scheduling, and regulatory compliance monitoring.

## Features

### 🧠 AI-Powered Workspace Optimization
- Intelligent workspace allocation using machine learning clustering
- Team collaboration optimization
- Real-time space utilization monitoring

### 👥 Employee Management
- Complete employee lifecycle management
- Department-based organization
- Team size and collaboration scoring

### 📅 Smart Meeting Scheduler
- AI-powered meeting time optimization
- Automatic room allocation based on attendee count
- Conflict detection and resolution

### 🛡️ Regulatory Compliance
- Real-time compliance monitoring
- Automated compliance scoring
- Data privacy and security tracking
- Regulatory update notifications

### 📊 Advanced Analytics
- Workspace utilization metrics
- Productivity analytics
- Compliance overview dashboards
- Real-time reporting

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/pariwat-amw/regtech.ai.git
cd regtech.ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### Employee Management
- `GET /api/employees` - List all employees
- `POST /api/employees` - Add new employee

### Workspace Optimization
- `POST /api/workspace/optimize` - Optimize workspace allocation

### Meeting Scheduling
- `GET /api/meetings` - List all meetings
- `POST /api/meetings` - Schedule new meeting

### Compliance Monitoring
- `GET /api/compliance/{employee_id}` - Check employee compliance

### Analytics
- `GET /api/analytics` - Get workspace analytics

### Health Check
- `GET /api/health` - Application health status

## Usage Examples

### Adding an Employee
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@company.com",
    "department": "IT",
    "team_size": 5
  }'
```

### Scheduling a Meeting
```bash
curl -X POST http://localhost:5000/api/meetings \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Standup",
    "attendees": ["john@company.com", "jane@company.com"],
    "duration_minutes": 30,
    "preferred_time": "09:00"
  }'
```

### Workspace Optimization
```bash
curl -X POST http://localhost:5000/api/workspace/optimize
```

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI/ML**: scikit-learn for clustering and optimization
- **Data Processing**: pandas, numpy
- **Styling**: Font Awesome, Bootstrap

## Architecture

The application follows a clean architecture pattern:

```
regtech.ai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md             # Documentation
```

## Configuration

The application can be configured through environment variables:

- `FLASK_ENV` - Set to 'development' for debug mode
- `FLASK_PORT` - Port number (default: 5000)
- `FLASK_HOST` - Host address (default: 0.0.0.0)

## Smart Features

### AI Workspace Optimization
The system uses K-means clustering to group employees based on:
- Department affiliation
- Team size
- Work hours
- Collaboration score

### Compliance Monitoring
Automated checks for:
- Data privacy training completion
- Security clearance status
- Workspace safety compliance
- Regulatory updates acknowledgment

### Meeting Intelligence
Smart scheduling considers:
- Attendee availability patterns
- Optimal meeting room allocation
- Time zone optimization
- Conflict resolution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For support and questions, please open an issue on GitHub or contact the development team.

---

**Smart Workplace - Regtech.AI**: Transforming workplaces through intelligent automation and regulatory compliance.