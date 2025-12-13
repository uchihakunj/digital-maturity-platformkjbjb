# Digital Maturity Assessment Platform

## Overview
The **Digital Maturity Assessment Platform** is an enterprise analytics tool designed to help organizations benchmark their digital readiness. It provides a centralized interface to evaluate departments across five critical dimensions: **Technology, Culture, Process, Skills, and Risk**.

This repository contains the source code for the Streamlit-based web application, which offers real-time visualization, bulk data processing, and automated strategic roadmap generation.

## Features
*   **Interactive Assessment:** Intuitive form-based scoring for individual departments.
*   **Bulk Ingestion:** Upload CSV files to process enterprise-wide data instantly.
*   **Dynamic Dashboard:**
    *   **Heatmaps:** Visualize maturity scores across the entire organization.
    *   **Radar Charts:** Compare specific departments side-by-side.
*   **Strategic Roadmap:** Auto-generated recommendations based on maturity gaps with downloadable PDF reports.
*   **Weighted Scoring Model:** Implements a strategic algorithm that prioritizes Technology (30%) and Process (25%) over softer metrics, ensuring the score reflects true operational readiness.
*   **Dark Mode:** Professional UI with toggleable themes.
*   **

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    Ensure you have Python 3.8+ installed.
    ```bash
    pip install -r requirements.txt
# Or manually: pip install streamlit pandas plotly fpdf kaleido
    ```

## Usage

1.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

2.  **Navigate the App:**
    *   **Home:** Overview of capabilities.
    *   **Assessment:** Submit a new maturity score for a department.
    *   **Upload Data:** Import existing data via CSV.
    *   **Dashboard:** View analytics and charts.
    *   **Roadmap:** Get specific improvement advice.

## Project Structure

*   `app.py`: Main application entry point handling UI and routing.
*   `logic.py`: Core business logic for maturity index calculation and recommendation rules.
*   `database.py`: SQLite database handler for storage and retrieval.
*   `requirements.txt`: Python dependencies.

## Contributors (**Team-9**)

*   **Sunil Kerketta**
*   **Raghwendra Kunjam**
*   **Vineet**
*   **Tejendra Kanwar**
*   **Vikas Rajput**

# digital-maturity-platform-
