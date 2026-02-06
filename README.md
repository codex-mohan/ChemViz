<div align="center">

  <h1>🔬 Chemical Equipment Parameter Visualizer</h1>
  
  <p>
    <b>A State-of-the-Art Hybrid Application for Industrial Analytics</b>
  </p>

  <p>
    <!-- Badges -->
    <a href="https://github.com/codexmohan">
      <img src="https://img.shields.io/badge/AUTHOR-MOHANA%20KRISHNA-181717?style=for-the-badge&logo=github&logoColor=white&labelColor=0D0D0D" alt="Author">
    </a>
    <a href="mailto:codexmohan@gmail.com">
      <img src="https://img.shields.io/badge/EMAIL-CODEXMOHAN%40GMAIL.COM-EA4335?style=for-the-badge&logo=gmail&logoColor=white&labelColor=0D0D0D" alt="Email">
    </a>
    <br />
    <img src="https://img.shields.io/badge/FRONTEND-REACT%20_%7C_TAILWIND-61DAFB?style=for-the-badge&logo=react&logoColor=white&labelColor=0D0D0D" alt="Frontend">
    <img src="https://img.shields.io/badge/BACKEND-DJANGO%20_%7C_DRF-092E20?style=for-the-badge&logo=django&logoColor=white&labelColor=0D0D0D" alt="Backend">
    <img src="https://img.shields.io/badge/DESKTOP-PYQT5-41CD52?style=for-the-badge&logo=qt&logoColor=white&labelColor=0D0D0D" alt="Desktop">
  </p>

  <p>
    <i>Designed & Developed with ❤️ by <b>Mohana Krishna</b></i>
  </p>

</div>

---

## 🚀 About The Project

**Chemical Equipment Parameter Visualizer** is a cutting-edge, hybrid application suite designed to revolutionize how chemical engineering data is analyzed and visualized. Built as a flagship project for **Internship Evaluation**, this tool bridges the gap between web portability and desktop power.

It provides a seamless interface for engineers to upload raw equipment data (CSV), visualize critical parameters like **Flowrate**, **Pressure**, and **Temperature** in real-time, and generate enterprise-grade PDF reports with deep statistical insights.

Whether you are on the web using the **Modern React Dashboard** or on the shop floor using the **Native Desktop Application**, this tool ensures you have access to your data, everywhere.

## ✨ Key Features

### 🌐 Web Application (React + Vite)
- **Modern Dashboard**: A visually stunning dark-themed dashboard featuring glassmorphism effects, gradient backgrounds, and fluid animations powered by `framer-motion`.
- **Advanced Visualization Suite**:
  - 📊 **Bar Charts**: Compare average performance metrics across different equipment types.
  - 🍩 **Pie Charts**: Visualize the distribution of equipment types in your dataset.
  - 📉 **Scatter Plots**: Analyze complex correlations, such as Temperature vs. Pressure trends.
  - 📶 **Histograms**: Understand the statistical distribution of key parameters.
  - 🌡️ **Correlation Matrix**: A heatmap to identify hidden relationships between variables.
- **Interactive Reports**: Generate and download comprehensive PDF reports directly from the web interface.
- **History Management**: View past uploads and clear search history with a single click to maintain a clean workspace.
- **Drag & Drop Upload**: Seamless CSV file upload with validation and progress tracking.

### 🖥️ Desktop Application (PyQt5)
- **Native Experience**: A robust, standalone application built with Python and Qt.
- **Offline Capabilities**: Analyze data locally without needing a web server.
- **Matplotlib Integration**: High-fidelity scientific plotting directly within the application window.

### 🔙 Robust Backend (Django REST Framework)
- **Secure API**: A RESTful API powering both the web and desktop clients.
- **Data Processing**: Leverages `Pandas` and `NumPy` for high-performance statistical calculations (Mean, Median, Std Dev).
- **Report Generation**: Uses `ReportLab` and `Matplotlib` to dynamically create rich PDF reports with embedded charts and tables.

## 🛠️ Technology Stack

| Component | Technologies |
|-----------|--------------|
| **Frontend** | ![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=white&labelColor=0D0D0D) ![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat-square&logo=vite&logoColor=white&labelColor=0D0D0D) ![Tailwind](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white&labelColor=0D0D0D) ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat-square&logo=chartdotjs&logoColor=white&labelColor=0D0D0D) |
| **Backend** | ![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white&labelColor=0D0D0D) ![DRF](https://img.shields.io/badge/Django_REST-A30000?style=flat-square&logo=django&logoColor=white&labelColor=0D0D0D) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white&labelColor=0D0D0D) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy&logoColor=white&labelColor=0D0D0D) |
| **Desktop** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white&labelColor=0D0D0D) ![Qt](https://img.shields.io/badge/PyQt5-41CD52?style=flat-square&logo=qt&logoColor=white&labelColor=0D0D0D) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3E5F8A?style=flat-square&logo=python&logoColor=white&labelColor=0D0D0D) |
| **Tools** | ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white&labelColor=0D0D0D) ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white&labelColor=0D0D0D) ![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white&labelColor=0D0D0D) |

## 🏗️ Project Structure

```bash
chemical-equipment-visualizer/
├── backend/                 # 🧠 Django REST API Logic
│   ├── api/                 # Views, ViewSets, and Serializers
│   ├── project/             # Core Settings and Config
│   └── requirements.txt     # Python Dependencies (matplotlib, pandas, etc.)
├── web/                     # 🌐 React Frontend Application
│   ├── src/
│   │   ├── components/      # UI Components (Cards, Buttons, Charts)
│   │   ├── pages/           # Dashboard, Upload, History Views
│   │   ├── services/        # API Integration (Axios)
│   │   └── utils/           # Analytics Helpers
│   └── package.json         # JS Dependencies (chart.js, tailwind, etc.)
├── desktop/                 # 🖥️ PyQt5 Desktop Application
│   ├── ui/                  # UI Layouts and Styles
│   │   ├── views/           # Chart and Report Views
│   │   └── components/      # Reusable Widgets
│   └── main.py              # Application Entry Point
└── README.md                # 📄 Documentation (You are here!)
```

> [!NOTE]
> **Architectural Decision**: While this project could benefit from a Monorepo structure (e.g., using **Turborepo**) for better dependency management and build orchestration, it is intentionally organized into three distinct directories. This design choice adheres to strict internship screening guidelines regarding library usage and project simplicity.

## 🏁 Getting Started

Follow these steps to set up the environment locally.

### Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.9 or higher)
- **Git**

### 📥 Installation & Setup

#### 1. Backend Setup (Django)

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Migrations
python manage.py migrate

# Start Server
python manage.py runserver
```
> The API will be available at `http://127.0.0.1:8000/`.

#### 2. Web Application Setup (React)

```bash
# Navigate to web
cd web

# Install dependencies
npm install

# Start Development Server
npm run dev
```
> The Web App will launch at `http://localhost:5173/`.

#### 3. Desktop Application Setup (PyQt5)

```bash
# Install desktop-specific requirements
pip install -r desktop/requirements.txt  # Or rely on backend env if shared

# Run the Application
python desktop/main.py
```

## 📖 Usage Guide

1.  **Launch the Suite**: Start the backend server first, then launch either the Web Dashboard or Desktop App.
2.  **Upload Data**: Drag and drop your CSV file containing equipment data.
    -   *Required Columns*: `Equipment Name`, `Type`, `Flowrate`, `Pressure`, `Temperature`.
3.  **Analyze**:
    -   View the **Dashboard** for instant insights.
    -   Check the **Correlation Matrix** to find parameter relationships.
    -   Use **Filters** to drill down into specific equipment types.
4.  **Report**: Click the **Download Report** button to get a full PDF summary, complete with embedded charts and statistical analysis.

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/upload/` | Upload a new CSV dataset |
| `GET` | `/api/datasets/` | List all available datasets |
| `GET` | `/api/datasets/{id}/` | Get detailed equipment data |
| `GET` | `/api/datasets/{id}/report/` | **Generate & Download PDF Report** |
| `GET` | `/api/history/` | View recent upload history |
| `DELETE` | `/api/history/` | Clear full search history |

## ⚠️ Known Limitations

### CSV Format Requirements

This application is designed specifically for **Chemical Equipment data** and requires CSV files to follow a strict schema. The following columns are **mandatory**:

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `Equipment Name` | String | Name/identifier of the equipment |
| `Type` | String | Category/type of equipment (e.g., Pump, Valve, Compressor) |
| `Flowrate` | Numeric | Flow rate value |
| `Pressure` | Numeric | Pressure measurement |
| `Temperature` | Numeric | Temperature value |

**Important Notes:**
- CSV files with different column names or structures will be rejected during upload
- The application does not support dynamic column mapping or generic CSV visualization
- All three numeric columns (`Flowrate`, `Pressure`, `Temperature`) must contain valid numeric values
- Column headers are case-sensitive and must match exactly as shown above

### Sample Data Format

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
```

A sample CSV file is provided at [`data/sample_equipment_data.csv`](data/sample_equipment_data.csv) for reference.

## 👤 Contact

**Mohana Krishna**  
*Full Stack Developer & Data Visualization Enthusiast*

[![Email](https://img.shields.io/badge/Email-codexmohan%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white&labelColor=0D0D0D)](mailto:codexmohan@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-codexmohan-181717?style=flat-square&logo=github&logoColor=white&labelColor=0D0D0D)](https://github.com/codexmohan)

---

<div align="center">
  <p>
    <i>Thank you for checking out this project! 🌟</i>
  </p>
</div>
