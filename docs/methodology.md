# PharmaPulse Statistical & Commercial Analytics Methodology
## Type 2 Diabetes Commercial Market Research Engagement

This document outlines the mathematical formulas, inferential statistical methods, and commercial gap models implemented across the PharmaPulse platform.

---

## 1. Survey Sampling & Binomial Confidence Intervals

### Wilson Score Interval for Proportions
Standard normal approximation intervals ($\hat{p} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$) fail when sample proportions approach 0 or 1, or when subgroup sample sizes are modest. We implement the **Wilson Score Interval** with continuity adjustments:

$$\tilde{p} = \frac{n_s + \frac{z^2}{2}}{n + z^2}$$

$$\text{CI}_{95\%} = \frac{\hat{p} + \frac{z^2}{2n} \pm z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

Where:
- $\hat{p} = \frac{n_s}{n}$ is the observed sample proportion of respondents selecting a given therapy.
- $z = 1.95996$ corresponds to the two-tailed 95% confidence level.
- $n$ is the active sample size in the analyzed physician subgroup.

---

## 2. Hypothesis Testing & Invariance Analysis

### Pearson's Chi-Square Test of Independence ($\chi^2$)
To test whether physician treatment choice ($Y$) is statistically independent of physician specialty ($X$):

$$\chi^2 = \sum_{i=1}^{r} \sum_{j=1}^{c} \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

Where:
- $O_{ij}$ is the observed count of physicians of specialty $i$ selecting therapy $j$.
- $E_{ij} = \frac{R_i \cdot C_j}{N}$ is the expected cell frequency under the null hypothesis of independence ($H_0$).
- Degrees of freedom: $\text{df} = (r - 1)(c - 1)$.

#### Cochran's Rule of Verification
Before inferring statistical significance, the model validates Cochran's criteria:
1. Expected cell frequency $E_{ij} \ge 1.0$ for all cells.
2. No more than 20% of expected cells have $E_{ij} < 5.0$.

#### Cramér's V Effect Size
To evaluate the practical magnitude of association independent of sample size:

$$V = \sqrt{\frac{\chi^2}{N \cdot \min(r - 1, c - 1)}}$$

Interpretation guidelines:
- $V < 0.10$: Negligible association
- $0.10 \le V < 0.30$: Moderate practical association
- $V \ge 0.30$: Strong clinical/commercial divergence

---

## 3. Likert Scale Barrier Evaluation

### Top-Box and Net Severity Scoring
Adoption barriers (Q11-Q15) are captured on a 5-point Likert scale (1 = Not a Barrier, 5 = Critical Barrier).

1. **Top-Box % ($\text{TB}$)**:
   $$\text{TB} = \frac{\sum_{i=1}^{n} \mathbb{I}(y_i \in \{4, 5\})}{n} \times 100$$
2. **Bottom-Box % ($\text{BB}$)**:
   $$\text{BB} = \frac{\sum_{i=1}^{n} \mathbb{I}(y_i \in \{1, 2\})}{n} \times 100$$
3. **Net Severity Score ($\text{NSS}$)**:
   $$\text{NSS} = \text{TB} - \text{BB}$$
   A Net Severity Score $> +50\%$ identifies critical market access bottlenecks requiring immediate field intervention.

### Non-Parametric Group Comparisons (Kruskal-Wallis)
Because Likert responses are ordinal and may not be normally distributed, differences in barrier ratings across specialties are evaluated using the **Kruskal-Wallis H-test**:

$$H = \frac{12}{N(N+1)} \sum_{j=1}^{k} \frac{R_j^2}{n_j} - 3(N+1)$$

Where $R_j$ is the sum of ranks for specialty group $j$.

---

## 4. Commercial Stated vs. Observed Gap Model

To bridge stated clinical intent (survey) with Medicare Part D market reality, we formulate:

### Adoption Gap Percentage Points ($\Delta_{\text{Gap}}$)
$$\Delta_{\text{Gap}} = P_{\text{Stated}} - S_{\text{Observed}}$$

Where:
- $P_{\text{Stated}}$ is the survey percentage prioritizing a drug class as second-line therapy in ASCVD.
- $S_{\text{Observed}}$ is the empirical share of Medicare Part D claims captured by that drug class.

### Adoption Realization Ratio ($\text{ARR}$)
$$\text{ARR} = \frac{S_{\text{Observed}}}{P_{\text{Stated}}}$$

- $\text{ARR} < 0.50$: **High Unmet Access Demand**. Clinical interest is robust, but commercial access hurdles (prior authorization, co-pays) severely depress dispensing.
- $\text{ARR} \approx 1.00$: **Equilibrium Realization**. Formulary access matches clinical preference.
- $\text{ARR} > 1.50$: **Legacy Prescribing Inertia**. Real-world volume outpaces guideline preference, driven by zero-cost generic access and habitual refills.
