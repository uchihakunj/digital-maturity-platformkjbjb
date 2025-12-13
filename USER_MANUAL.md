# User Manual: Digital Maturity Assessment Platform

## 1. Getting Started
Launch the application designated by your IT administrator. Use the **Sidebar** on the left to navigate between different modules.

> **Tip:** You can toggle **Dark Mode** in the sidebar for a different viewing experience.

## 2. Performing an Assessment
Navigate to the **Assessment** page to evaluate a single department.

1.  **Department Info:** Enter the name of the department (e.g., "Finance") and your name.
2.  **Maturity Dimensions:** Rate the department on a scale of 1.0 to 5.0 for each category:
    *   **Tech Stack:** 1 (Legacy) to 5 (Cutting Edge).
    *   **Culture:** 1 (Resistant) to 5 (Agile).
    *   **Process:** 1 (Manual) to 5 (Autonomous).
    *   **Skills:** 1 (Skill Gap) to 5 (Expertise).
    *   **Risk:** 1 (High Risk) to 5 (Secure).
3.  **Submit:** Click "Submit Assessment" to save the record to the database.

## 3. Uploading Bulk Data
If you have data in a spreadsheet, use the **Upload Data** page.

1.  Prepare a CSV file with these exact headers: `Department`, `Tech`, `Culture`, `Process`, `Skills`, `Risk`.
2.  Drag and drop the file into the upload area.
3.  Preview the data and click **Import Data to Database**.

## 4. Viewing the Dashboard
The **Dashboard** provides high-level insights.

*   **KPIs:** View total assessments and the organization-wide average Maturity Index.
*   **Heatmap:** A color-coded grid showing scores for all departments. Darker greens indicate higher maturity.
*   **Radar Chart:** Select specific departments from the dropdown to compare their shapes. Ideally, you want a full, wide pentagon.

## 5. How is the Maturity Score Calculated?
The Dashboard does not use a simple average. It uses a **Strategic Weighted Formula** to give more importance to foundational capabilities.

**The Formula:**

$$\text{Score} = (\text{Tech} \times 0.30) + (\text{Process} \times 0.25) + (\text{Skills} \times 0.20) + (\text{Risk} \times 0.15) + (\text{Culture} \times 0.10)$$

**Example:** If your Tech score is low (2.0), your overall score will drop
significantly, even if your Culture score is high (5.0). This alerts you to fix
critical infrastructure issues first.


## 6. Generating a Roadmap
Go to the **Roadmap** page to get actionable advice.

1.  Select a department from the dropdown.
2.  The system will display cards for each dimension.
    *   **Red (Foundation):** Needs immediate attention.
    *   **Yellow (Developing):** Good progress, needs optimization.
    *   **Green (Mature):** Leadership level, focus on innovation.
3.  Read the specific recommendation text (e.g., "Implement cross-functional agile squads") to guide your strategy.
4.  Download Report: Click the "Download Report (PDF)" button to generate a comprehensive PDF containing the organizational heatmap and the detailed recommendation strategy.
