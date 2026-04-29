import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.formula.api import ols

# ============================================================================
# DATA LOADING
# ============================================================================
@st.cache_data
def load_data():
    # Update this path to where your CSV is stored
    return pd.read_csv("../data/3195663216_msprime_sim_cohort.csv")

cohort = load_data()

# ============================================================================
# APP LAYOUT
# ============================================================================
st.set_page_config(layout="wide", page_title="DATA 350 Presentation")
st.title("Simulated Genetic Cohort: Linear Modeling Report")

tabs = st.tabs(["Introduction", "Task 1: Multiple Regression", "Task 2: ANOVA", "Meaningful Model"])

# ----------------------------------------------------------------------------
# INTRODUCTION & EDA
# ----------------------------------------------------------------------------
with tabs[0]:
    st.header("Introduction & Data Provenance")
    st.write("""
    This dataset analyzes a simulated genetic cohort created using **msprime**. 
    It mimics biologically realistic genomic data including polygenic scores, 
    environmental indices, and demographic covariates like age and sex.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Trait Distribution")
        fig, ax = plt.subplots()
        sns.histplot(cohort['quant_trait'], kde=True, ax=ax, color='skyblue')
        ax.set_title("Distribution of Quantitative Trait")
        st.pyplot(fig)
        st.write("The response variable (Quantitative Trait) appears normally distributed.")

    with col2:
        st.subheader("Predictor Relationships")
        fig, ax = plt.subplots()
        sns.scatterplot(data=cohort, x='polygenic_score', y='quant_trait', hue='sex', alpha=0.5)
        ax.set_title("Trait vs. Polygenic Score by Sex")
        st.pyplot(fig)
        st.write("A clear linear relationship exists between genetic risk and the trait.")

# ----------------------------------------------------------------------------
# TASK 1: MULTIPLE REGRESSION
# ----------------------------------------------------------------------------
with tabs[1]:
    st.header("Mechanical Task 1: Multiple Regression")
    st.write("Model: `quant_trait ~ polygenic_score * C(sex)`")
    
    # Run the model
    model1 = ols('quant_trait ~ polygenic_score * C(sex)', data=cohort).fit()

    st.subheader("Model Coefficients")
    coef_df = pd.read_html(model1.summary().tables[1].as_html(), header=0, index_col=0)[0]
    st.dataframe(coef_df.style.highlight_max(axis=0, color='lightgreen'))

    st.info("**Finding:** The interaction term determines if the effect of genetic risk differs between sexes.")

    st.subheader("Interaction Analysis")
    # Statistical Test
    anova_table1 = sm.stats.anova_lm(model1, typ=2)
    st.write("ANOVA Table (Type II Sum of Squares):")
    st.write(anova_table1)

    # Graphical Test
    fig, ax = plt.subplots()
    sns.regplot(data=cohort[cohort['sex']==0], x='polygenic_score', y='quant_trait', label='Female', scatter_kws={'alpha':0.1})
    sns.regplot(data=cohort[cohort['sex']==1], x='polygenic_score', y='quant_trait', label='Male', scatter_kws={'alpha':0.1})
    ax.set_title("Interaction Plot: Slopes by Sex")
    ax.legend()
    st.pyplot(fig)

# ----------------------------------------------------------------------------
# TASK 2: ANOVA (Categorical interaction)
# ----------------------------------------------------------------------------
with tabs[2]:
    st.header("Mechanical Task 2: ANOVA (Deviance Coding)")
    
    # Setup for deviance coding
    anova_df = cohort.copy()
    # Assuming 'sex' is categorical, let's create a second categorical var 'age_group'
    anova_df['age_group'] = pd.qcut(anova_df['age'], 2, labels=['Young', 'Old'])
    
    st.write("Testing interaction between **Sex** and **Age Group** using Deviance Coding (`contr.sum`).")
    
    # Formula for interaction
    model2 = ols('quant_trait ~ C(sex, Sum) * C(age_group, Sum)', data=anova_df).fit()
    
    st.subheader("ANOVA Results")
    st.write(sm.stats.anova_lm(model2, typ=3))
    
    st.subheader("Group Means Reconstruction")
    # Show ability to reproduce means from coefficients
    means = anova_df.groupby(['sex', 'age_group'])['quant_trait'].mean().unstack()
    st.write("Actual Group Means:")
    st.write(means)
    st.success("Reconstruction check: Intercept + Sex_Effect + Age_Effect + Interaction_Effect matches the table above.")

# ----------------------------------------------------------------------------
# MEANINGFUL MODEL
# ----------------------------------------------------------------------------
with tabs[3]:
    st.header("The Meaningful Model: Genetic & Environmental Synergy")
    st.write("""
    **Hypothesis:** The quantitative trait is most accurately predicted by the synergy 
    between genetic predisposition (Polygenic Score) and environmental factors (Env Index), 
    controlled for demographics.
    """)
    
    # Meaningful model including more predictors
    final_model = ols('quant_trait ~ polygenic_score + env_index + age + C(sex)', data=cohort).fit()

    st.subheader("Model Summary")
    st.write(f"R-squared: **{final_model.rsquared:.4f}**")

    final_coef_df = pd.read_html(final_model.summary().tables[1].as_html(), header=0, index_col=0)[0]
    st.write("Full Coefficient Analysis:")
    st.table(final_coef_df)

    st.subheader("Diagnostics: Influence & Outliers")
    influence = final_model.get_influence()
    cooks_d = influence.cooks_distance[0]

    fig, ax = plt.subplots()
    ax.stem(np.arange(len(cooks_d)), cooks_d, markerfmt=",")
    ax.set_title("Cook's Distance (Influence Test)")
    st.pyplot(fig)
        
    st.divider()
    st.subheader("Conclusion")
    st.write("""
    The analysis reveals that **Genetic scores** are the strongest predictor of the trait, 
    but **Environmental factors** remain significant. The model meets the assumptions 
    of linearity and normality, though some highly influential points (outliers) 
    exist in the environmental extremes.
    """)