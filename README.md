# Statistical Modeling Final Project  
### **Linear Modeling Analysis of a Simulated msprime Cohort**

**Author:** Makenna Worley & Kate Regilski  
**Course:** Statistical Modeling (Spring 2026)  
**Dataset:** Generated using `make_msprime_dataset.py` with seed 3195663216 
**Output File:** `data350.ipynb` - Jupyter notebook with HTML export  
**Tools:** Python 3, pandas, numpy, scipy, statsmodels, matplotlib, seaborn

---

## 📌 Project Overview

This project demonstrates proficiency with fundamental statistical modeling techniques through analysis of a simulated genetic dataset generated via **msprime**. The analysis follows a structured curriculum approach with three main components:

1. **Introduction & Exploratory Data Analysis (EDA)** - Understand data structure and relationships
2. **Mechanical Tasks** - Demonstrate technical competency with standard methods
3. **Meaningful Model** - Apply domain knowledge to test a contextual hypothesis

---

## 🧬 Dataset Description

The dataset is a **simulated cohort of 10,000 individuals** generated using the msprime coalescent simulator. The simulation produces a realistic genetic background with demographic and environmental covariates, enabling analysis under known conditions.

### **Variables in the Dataset**

**Numerical Variables:**
- `age` — Individual age (20-78 years, uniformly distributed)
- `env_index` — Environmental exposure index (standardized, mean = 0, sd = 1)
- `polygenic_score` — Standardized polygenic risk score from causal variants (mean = 0, sd = 1)
- `quant_trait` — Quantitative trait response variable (standardized)

**Categorical Variables:**
- `sex` — Biological sex (Female / Male, ~50/50 split)
- `disease_status` — Binary disease status (0 = no disease, 1 = disease, ~50/50 split)

**Additional Variables:**
- `disease_prob` — Probability of disease based on simulation parameters
- `PC1`, `PC2` — Principal components from genotype PCA (population structure)

### **Data Source**
- Generated via msprime coalescent simulation with Wright-Fischer model
- Includes realistic linkage disequilibrium and recombination patterns
- Demographic variables and environmental factors added to simulate real-world complexity
- File: `data/3195663216_msprime_sim_cohort.csv`

---

## 📋 Project Components

### **1. Introduction & Exploratory Data Analysis**

The report begins with background on the msprime dataset and its generation process. The EDA section includes:
- Summary statistics for all variables
- Distribution plots (histograms, violin plots) for numerical variables
- Count plots for categorical variables
- Pairwise correlation analysis with heatmaps
- Variance Inflation Factor (VIF) assessment for multicollinearity
- Scatterplots showing relationships between predictors and the response variable
- Outlier detection via z-scores and box plots

**Key EDA Findings:**
- Strong positive correlation between polygenic score and quantitative trait ($r ≈ 0.66$)
- Moderate positive correlation between environmental index and trait ($r ≈ 0.35$)
- No significant sex difference in trait distribution
- Age shows negligible correlation with trait
- High multicollinearity in raw variables (VIF: age = 10.34, disease_prob = 12.33)
- Principal components successfully reduce multicollinearity (PC1 VIF = 1.32, PC2 VIF = 1.13)

---

### **2. Mechanical Tasks**

These tasks demonstrate core technical competency with standard linear modeling approaches.

#### **Task 1: Multiple Regression**

**Model Specification:**
```
quant_trait ~ polygenic_score + sex + (polygenic_score × sex)
```

**Analysis includes:**
- ✓ Scatterplots of response vs predictors (colored by sex)
- ✓ Multiple regression without interaction
- ✓ Multiple regression with interaction term
- ✓ F-test for statistical significance of interaction
- ✓ Residual diagnostic plots (fitted vs residuals, Q-Q plot, histogram, scale-location)
- ✓ ANOVA table interpretation
- ✓ Coefficient interpretation (intercept, main effects, interaction)
- ✓ Shapiro-Wilk normality test

**Expected Findings:**
- Polygenic score is a strong predictor of trait (positive coefficient)
- Sex may show main effect and/or interaction with polygenic score
- Residuals approximately normally distributed with homogeneous variance
- Interaction may or may not be significant (analysis proceeds regardless)

---

#### **Task 2: ANOVA Analysis**

**Model Specification (with Deviance Coding):**
```
quant_trait ~ C(sex, Sum) + C(disease_status, Sum) + C(sex, Sum):C(disease_status, Sum)
```

**Analysis includes:**
- ✓ Deviance (sum) coding applied to both categorical variables
- ✓ Two-way ANOVA with both main and interaction terms
- ✓ F-test comparing model with vs without interaction
- ✓ Type III ANOVA table
- ✓ **Group mean recovery** - Calculate predicted means from model coefficients and verify against observed means
- ✓ Interaction plot visualization
- ✓ Box plots by group

**Key Insight:**
Demonstrates that model coefficients (with deviance coding) can be used to reconstruct all group means through coefficient combinations, validating the model parameterization.

---

### **3. Meaningful Model**

**Hypothesis:** 
How much does the quantitative trait vary due to combined genetic (polygenic_score) and environmental (env_index) factors, after controlling for demographic differences (sex)?

**Model Specification:**
```
quant_trait ~ polygenic_score + env_index + sex
```

**Advanced Diagnostics:**
- ✓ Variable transformation assessment (if needed)
- ✓ Thorough outlier detection and influence analysis
  - Cook's distance plots
  - Leverage-residual plots
  - Identification of high-influence points
- ✓ Residual diagnostics and assumption checking
- ✓ Multicollinearity assessment
- ✓ Model interpretation with biological/contextual significance

**Expected Interpretation:**
- Strong positive effect of polygenic score on trait
- Moderate positive effect of environmental index
- Possible sex difference in baseline trait level
- Model explains ~56% of trait variance (R² ≈ 0.567 based on EDA findings)
- Conclusion about relative importance of genetic vs environmental factors

---

## 🔍 Key Analysis Methods

### **Statistical Techniques Used**

1. **Exploratory Data Analysis**
   - Summary statistics
   - Correlation matrices
   - VIF for multicollinearity
   - Outlier detection (z-scores)

2. **Hypothesis Testing**
   - F-tests for model comparison
   - T-tests for coefficient significance
   - Shapiro-Wilk test for normality

3. **Model Diagnostics**
   - Residual plots (fitted vs residuals, Q-Q plots)
   - Scale-location plots (homogeneity of variance)
   - Influence diagnostics (Cook's distance, leverage)
   - Normality testing

4. **Coding Schemes**
   - Default (dummy) coding for Task 1
   - Deviance (sum) coding for Task 2
   - Proper contrast specification

---

## 📂 Repository Structure

```
data350_final/
│
├── data/
│   ├── 3195663216_msprime_sim_cohort.csv          # Main analysis dataset (10,000 obs)
│   └── 3195663216_msprime_effect_sizes.csv        # True causal effect sizes
│
├── notebooks/
│   ├── data350.ipynb                              # Main analysis notebook
│   └── presentation_report.qmd                    # R version of data350.ipynb
│
├── streamlit/
│   ├── app.py                                     # Optional visualization dashboard
│   └── requirements.txt
│
├── environment.yml                                # Conda environment specification
├── README.md                                      # This file
│
└── [Output files]
│   ├── presentation_report.py                     # HTML export
    └── data350.html                               # HTML export
```

---

## 💻 Software & Dependencies

### **Python Libraries**
- **Data manipulation:** pandas, numpy
- **Statistical modeling:** statsmodels, scipy.stats
- **Machine learning:** scikit-learn
- **Visualization:** matplotlib, seaborn
- **Environment:** conda/Python 3.8+

### **Installation**

Create the environment using the provided `environment.yml`:
```bash
conda env create -f environment.yml
conda activate data350
```

Or install packages manually:
```bash
pip install pandas numpy scipy statsmodels scikit-learn matplotlib seaborn statsmodels
```

---

## 🚀 Running the Analysis

### **Generate HTML Report (from Quarto)**

After modifying or executing cells in `data350.ipynb`, export to HTML:

```bash
# Using Quarto (recommended for course submission)
quarto render data350.ipynb --to html

# Or using jupyter nbconvert
jupyter nbconvert --to html data350.ipynb
```

This generates `data350.html` for Canvas submission.

### **Execute Notebook Cells**

Open the notebook in Jupyter and run cells sequentially:
```bash
jupyter notebook notebooks/data350.ipynb
```

---

## 📊 Expected Output

### **From data350.ipynb:**

1. **Introduction Section**
   - Background on msprime simulation
   - Summary statistics table
   - Distribution plots for all variables
   - Correlation heatmap
   - VIF multicollinearity assessment

2. **Task 1: Multiple Regression**
   - Scatterplots with regression lines
   - Model summary table (coefficients, p-values, R²)
   - Residual diagnostic plots (4-panel figure)
   - Interaction test results
   - Coefficient interpretation

3. **Task 2: ANOVA**
   - ANOVA table (Type III)
   - Group means table (observed and predicted)
   - Interaction plot
   - Box plots by group

4. **Meaningful Model**
   - Model summary with interpretation
   - Residual diagnostics
   - Influence and outlier analysis
   - Summary findings and conclusions

---

## 📋 Grading Rubric Alignment

✓ **Introduction** - Data background, EDA with integrated graphs, properly labeled axes
✓ **Task 1** - Multiple regression with interaction testing and interpretation
✓ **Task 2** - ANOVA with deviance coding and group mean recovery from coefficients
✓ **Meaningful Model** - Contextual hypothesis, diagnostics, transformation assessment, outlier analysis, conclusions
✓ **Format** - Jupyter notebook with HTML export ready for Canvas submission
✓ **Audience** - Written for readers familiar with linear modeling but not this specific dataset

---

## 📝 Notes

### **Data Characteristics**
- Clean, complete dataset (no missing values)
- Appropriate for linear modeling (meets normality assumptions reasonably well)
- Includes both numerical and categorical predictors
- Multiple potential response variables (quant_trait primary, disease_status alternative)
- Good sample size (n = 10,000) for reliable estimation

### **Common Extensions** (beyond rubric requirements)
- Compare models using cross-validation or AIC/BIC
- Assess coefficient stability via bootstrap
- Explore non-linear transformations
- Test more complex interactions or polynomial terms
- Compare with alternative coding schemes for categorical variables

---

## 🎓 Learning Objectives Demonstrated

By completing this project, you will show proficiency with:

✓ Exploratory data analysis and visualization
✓ Multiple regression modeling (dummy coding, interaction terms)
✓ ANOVA design and interpretation (deviance coding)
✓ Hypothesis testing and statistical inference
✓ Residual diagnostics and model assumptions
✓ Outlier detection and influence analysis
✓ Contextual model development and interpretation
✓ Report writing for statistical audiences
✓ Jupyter/Quarto notebook authoring
✓ Python-based statistical computing

---

## 📧 Contact & Questions

For questions about:
- **Data handling or cleaning:** See instructor during office hours
- **Statistical methods:** Refer to course notes or discussion section
- **Technical issues:** Check Python/statsmodels documentation or troubleshoot in office hours

---

## 🚀 **How to Run the Project**

### ⚙️ **Installation (Conda)**

#### 1️⃣ **Clone the repository**
```bash
git clone https://github.com/MakennaWorley/SM-Final-PythonR.git
cd SM-Final-PythonR
```

#### 2️⃣ **Create and activate the environment**
```bash
conda env create -f environment.yml
conda activate data350
```

#### 3️⃣ **Run the final notebook**
Open:

```
notebooks/final.ipynb
```

#### 4️⃣ **(Optional) Launch the Streamlit visualization**
```bash
cd streamlit
streamlit run app.py
```

#### 4️⃣ **(Optional) Launch the Streamlit visualization**
```bash
cd streamlit
streamlit run app.py
```

Or go to [Streamlit.io](https://makennaworley-sm-final-python-streamlitapp-7hj55p.streamlit.app/)

This provides an interactive comparison of model performance.
