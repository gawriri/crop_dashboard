Crop Production Dashboard

Problem Statement
Agricultural production varies across seasons and years, making it difficult to identify patterns and trends. This project aims to analyze crop production data and present insights through an interactive dashboard.

Project Overview
This is a full-stack data analytics project that processes real-world crop data and visualizes production trends. The dashboard allows users to explore seasonal patterns and year-wise variations in crop production.

Features
Data cleaning and preprocessing of raw agricultural data
Year-wise production trend analysis
Season-wise production comparison
Interactive dashboard with dynamic filtering
API-based data fetching using FastAPI

Tech Stack
Backend: FastAPI, Python, Pandas
Frontend: HTML, CSS, Chart.js
Visualization: Chart.js

Project Structure
backend: FastAPI application and data processing
frontend: dashboard UI
data: raw datasets
notebooks: exploratory analysis

Key Insights
Rabi production is significantly higher than Kharif
Production increased steadily from 2018 to 2022
A noticeable decline is observed after 2022
Seasonal patterns strongly influence crop yield

How to Run Locally
Run backend
cd backend
python -m uvicorn main:app --reload

Open frontend
Open frontend/index.html in browser

Future Improvements
Add more crop diversity
Improve UI design
Deploy dashboard online
Add predictive analysis

Live Demo  
https://playful-paletas-5a829a.netlify.app/
Backend API  
https://crop-dashboard-abwy.onrender.com
