# Chemical Equipment Visualizer

## Quick Start Guide

### 1. Start the Backend Server

```bash
cd backend
python manage.py runserver
```

Server runs at: `http://localhost:8000`

### 2. Start the Web Application

```bash
cd web
npm install
npm start
```

Web app opens at: `http://localhost:3000`

### 3. Start the Desktop Application

```bash
pip install -r desktop/requirements.txt
python desktop/main.py
```

## Features Demo

1. Click "Load Sample Data" to instantly analyze the provided CSV
2. View summary statistics (averages, counts, ranges)
3. Switch between Overview/Charts/Data tabs
4. Generate PDF reports
5. Check upload history

## Troubleshooting

- **Connection refused**: Make sure Django backend is running on port 8000
- **Module not found**: Install dependencies with `pip install -r backend/requirements.txt`
- **Port already in use**: Kill existing processes or use different ports
