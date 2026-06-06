import os
from weasyprint import HTML

def build_pdf_report():
    print("=" * 60)
    print("        COMPILING ARTIFACT: PDF REPORT OF FINDINGS        ")
    print("=" * 60)
    
    # Define absolute paths for local visual assets generated from EDA
    current_dir = os.getcwd()
    dist_img = os.path.join(current_dir, 'outputs', 'age_fare_distributions.png').replace('\\', '/')
    surv_img = os.path.join(current_dir, 'outputs', 'survival_relationships.png').replace('\\', '/')
    heat_img = os.path.join(current_dir, 'outputs', 'correlation_heatmap.png').replace('\\', '/')

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{
                size: A4;
                margin: 20mm 15mm;
                background-color: #ffffff;
                @bottom-right {{
                    content: "Page " counter(page);
                    font-family: 'Segoe UI', sans-serif;
                    font-size: 9pt;
                    color: #6b7280;
                }}
            }}
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                color: #1f2937;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }}
            .header-banner {{
                background-color: #1e3a8a;
                color: #ffffff;
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 6px;
            }}
            .header-banner h1 {{
                margin: 0;
                font-size: 22pt;
                font-weight: 700;
                letter-spacing: -0.5px;
            }}
            .header-banner p {{
                margin: 5px 0 0 0;
                font-size: 11pt;
                color: #93c5fd;
            }}
            h2 {{
                color: #1e3a8a;
                font-size: 14pt;
                border-bottom: 2px solid #e5e7eb;
                padding-bottom: 5px;
                margin-top: 25px;
            }}
            p, li {{
                font-size: 10.5pt;
                text-align: justify;
            }}
            .insight-box {{
                background-color: #f8fafc;
                border-left: 4px solid #3b82f6;
                padding: 12px 15px;
                margin: 15px 0;
                border-radius: 0 6px 6px 0;
            }}
            .insight-box strong {{
                color: #1e3a8a;
            }}
            .visual-container {{
                text-align: center;
                margin: 20px 0;
                page-break-inside: avoid;
            }}
            .visual-container img {{
                width: 100%;
                max-height: 280px;
                object-fit: contain;
                border: 1px solid #e5e7eb;
                border-radius: 6px;
            }}
            .meta-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
            }}
            .meta-table th, .meta-table td {{
                border: 1px solid #e5e7eb;
                padding: 8px 12px;
                font-size: 10pt;
                text-align: left;
            }}
            .meta-table th {{
                background-color: #f1f5f9;
                color: #1e3a8a;
            }}
        </style>
    </head>
    <body>

        <div class="header-banner">
            <h1>Titanic Disaster: Exploratory Data Analysis Report</h1>
            <p>Data Science Portfolio Practice — Statistical & Visual Exploration</p>
        </div>

        <h2>1. Executive Summary & Data Integrity Audit</h2>
        <p>This comprehensive analytical report evaluates the historical passenger manifest records of the RMS Titanic (891 rows, 12 core features). The purpose of this pipeline is to visually and statistically explore demographic trends, pricing structures, and socio-economic variables to isolate the primary indicators of passenger survival probability.</p>
        
        <table class="meta-table">
            <tr>
                <th>Feature Metric Group</th>
                <th>Observed Baseline Profile & Treatment Strategy</th>
            </tr>
            <tr>
                <td><strong>Age Vector</strong></td>
                <td>177 missing inputs. Repaired using stratified median values across Passenger Classes (Pclass).</td>
            </tr>
            <tr>
                <td><strong>Cabin Identifier</strong></td>
                <td>687 missing inputs (>77% missing data). Excluded completely from downstream dataframe blocks.</td>
            </tr>
            <tr>
                <td><strong>Embarked Port</strong></td>
                <td>2 missing inputs. Imputed using the global column mode ('S').</td>
            </tr>
        </table>

        <h2>2. Univariate Analysis: Feature Distributions & Outliers</h2>
        <p>Statistical distribution analysis shows a near-normal age distribution across the ship's demographic footprint, peaking within the 20 to 38 chronological range. Conversely, financial ticket fares display an extreme right-skewed layout ($0.00 to $512.33), highlighting heavily isolated luxury anomalies on upper-deck decks.</p>

        <div class="visual-container">
            <img src="file:///{dist_img}" alt="Univariate Distributions">
        </div>

        <div class="insight-box">
            <strong>Statistical Trajectory Insight:</strong> The severe skewness in ticket pricing indicates distinct income tiers. The massive spread in variance ($std = 49.69$) requires log-transformations or standard scaling adjustments before training linear estimators.
        </div>

        <div style="page-break-before: always;"></div>

        <h2>3. Bivariate Analysis: Target Survival Correlates</h2>
        <p>Evaluating categorical splits against survival flags reveals deep systemic socio-demographic stratification factors during emergency evacuations.</p>

        <div class="visual-container">
            <img src="file:///{surv_img}" alt="Survival Relationships">
        </div>

        <div class="insight-box">
            <strong>Evacuation Disparity Insights:</strong>
            <ul>
                <li><strong>Gender Demographics:</strong> Females achieved a <strong>74.2%</strong> survival probability, contrasted against a minor <strong>18.9%</strong> rate for male counterparts, validating the historical execution of maritime safety priorities.</li>
                <li><strong>Socioeconomic Class:</strong> Class 1 premium travelers secured a <strong>63.0%</strong> survival rate, significantly outperforming Class 3 lower-deck travelers who dropped to <strong>24.2%</strong>.</li>
            </ul>
        </div>

        <h2>4. Multivariate Analysis: Pearson Linear Interaction Matrix</h2>
        <p>Isolating numerical parameters allows us to identify multicollinearity issues across tracking features.</p>

        <div class="visual-container">
            <img src="file:///{heat_img}" alt="Correlation Heatmap">
        </div>

        <div class="insight-box">
            <strong>Collinearity Matrix Takeaway:</strong> A strong negative correlation coefficient of <strong>-0.55</strong> exists between Passenger Class (`Pclass`) and Ticket Fare, mapping out pricing divisions. This confirmed structure indicates that multicollinearity must be tracked carefully using Variance Inflation Factors (VIF) prior to feature selection.
        </div>

    </body>
    </html>
    """
    
    output_path = 'outputs/titanic_eda_report.pdf'
    HTML(string=html_content).write_pdf(output_path)
    print(f"✓ Executive Report Compiled Successfully: '{output_path}'")
    print("=" * 60)

if __name__ == "__main__":
    build_pdf_report()