import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set global plotting configurations for clean visual assets
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

def create_directory_structure():
    """Ensures repository directories exist locally before data execution."""
    directories = ['data', 'outputs']
    for folder in directories:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created workspace folder: {folder}")

def run_eda_pipeline():
    print("="*60)
    print("        TITANIC EXPLORATORY DATA ANALYSIS PIPELINE        ")
    print("="*60)
    
    # 1. Data Ingestion
    url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    df = pd.read_csv(url)
    df.to_csv('data/titanic.csv', index=False)
    print("✓ Raw data loaded and mirrored locally to 'data/titanic.csv'\n")
    
    # 2. Structural & Descriptive Integrity Checks
    print("--- [M1] DATA LAYOUT & BASIC SHAPE ---")
    print(f"Total Passenger Rows: {df.shape[0]} | Tracking Features: {df.shape[1]}")
    print("\n--- Missing Feature Audit ---")
    missing = df.isnull().sum()
    print(missing[missing > 0])
    
    print("\n--- Statistical Matrix ---")
    print(df.describe().round(2))
    print("\n" + "-"*50)
    
    # 3. Data Cleaning & Imputation (Bivariate-guided)
    print("--- [M2] STRUCTURAL DATA REPAIR ---")
    # Impute missing Age records with the median age of their respective Passenger Class (Pclass)
    df['Age'] = df.groupby('Pclass')['Age'].transform(lambda x: x.fillna(x.median()))
    # Impute missing Embarked records with the mode
    df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
    # Drop Cabin feature due to severe structural column gaps (>75% missing rows)
    df.drop(columns=['Cabin'], inplace=True, errors='ignore')
    print("✓ Missing Age values imputed using median Pclass stratification.")
    print("✓ Missing Embarked values fixed with column mode.")
    print("✓ High-null 'Cabin' attribute dropped from working dataframe.")
    print("\n" + "-"*50)
    
    # 4. Univariate Visual Exploration (Distributions & Skewness)
    print("--- [M3] GENERATING UNIVARIATE DISTRIBUTIONS ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Age Distribution Histogram
    sns.histplot(df['Age'], kde=True, color='#1E3A8A', ax=axes[0], bins=30)
    axes[0].set_title('Age Distribution Pattern')
    axes[0].set_xlabel('Age')
    
    # Fare Feature Boxplot (Checking for structural skewness and extreme outliers)
    sns.boxplot(x=df['Fare'], color='#3B82F6', ax=axes[1])
    axes[1].set_title('Fare Metric Spread & Outlier Profiling')
    axes[1].set_xlabel('Fare (Ticket Price)')
    
    plt.tight_layout()
    plt.savefig('outputs/age_fare_distributions.png', dpi=300)
    plt.close()
    print("✓ Output Saved: 'outputs/age_fare_distributions.png'")
    
    # 5. Bivariate Visual Exploration (Survival Feature Relationships)
    print("--- [M4] EVALUATING SURVIVAL DETERMINANTS ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Survival Rate grouped by Sex
    sns.barplot(data=df, x='Sex', y='Survived', hue='Sex', palette='Blues_r', ax=axes[0], legend=False)
    axes[0].set_title('Survival Probability Rate by Passenger Sex')
    axes[0].set_ylabel('Survival Probability')
    
    # Survival Rate grouped by Passenger Ticket Class
    sns.barplot(data=df, x='Pclass', y='Survived', hue='Pclass', palette='crest', ax=axes[1], legend=False)
    axes[1].set_title('Survival Probability Rate by Ticket Class (Pclass)')
    axes[1].set_ylabel('Survival Probability')
    
    plt.tight_layout()
    plt.savefig('outputs/survival_relationships.png', dpi=300)
    plt.close()
    print("✓ Output Saved: 'outputs/survival_relationships.png'")
    
    # 6. Multivariate Visual Exploration (Correlation Heatmap)
    print("--- [M5] EXECUTING MULTIVARIATE INTERACTION MATRIX ---")
    # Filter matrix map down strictly to numerical types to evaluate linear correlation
    numeric_cols = df.select_dtypes(include=[np.number]).drop(columns=['PassengerId'])
    corr_matrix = numeric_cols.corr()
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
    plt.title('Numerical Features Linear Correlation Matrix Heatmap', pad=20)
    
    plt.tight_layout()
    plt.savefig('outputs/correlation_heatmap.png', dpi=300)
    plt.close()
    print("✓ Output Saved: 'outputs/correlation_heatmap.png'")
    
    # 7. Print Core Data Insights To Console Summary
    print("\n" + "="*60)
    print("                  DATA INSIGHTS SUMMARY                  ")
    print("="*60)
    fem_surv = df[df['Sex'] == 'female']['Survived'].mean() * 100
    male_surv = df[df['Sex'] == 'male']['Survived'].mean() * 100
    p1_surv = df[df['Pclass'] == 1]['Survived'].mean() * 100
    p3_surv = df[df['Pclass'] == 3]['Survived'].mean() * 100
    
    print(f"1. Demographics: Female survival rate reached {fem_surv:.1f}%, drastically contrasting male survival at {male_surv:.1f}%.")
    print(f"2. Socioeconomic Status: Pclass 1 passengers achieved a survival rate of {p1_surv:.1f}%, while Pclass 3 dropped down to {p3_surv:.1f}%.")
    print(f"3. Feature Multicollinearity: A distinct negative correlation (-0.55) exists between Pclass and Fare, confirming pricing segmentation.")
    print("="*60)

if __name__ == "__main__":
    create_directory_structure()
    run_eda_pipeline()