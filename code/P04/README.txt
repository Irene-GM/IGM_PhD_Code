---------------------------------------------------------------------------------------------------------------------
Publication associated to this work:
Modelling tick bite risk by combining random forests and count data regression models (2019, pre-print)
In review for PLOS ONE Journal.
https://www.biorxiv.org/content/10.1101/642728v1.article-metrics
---------------------------------------------------------------------------------------------------------------------

NOTES:

    + Modelling
    -------------------
        -   In this work we modify a canonical Random Forest to be able to learn from highly-skewed and zero-inflated
            distributions. The tick bites, when aggregated to a grid cell, conform a distribution of this type and, which
            poses challenges for machine learning algorithms.
        -   We plug count data models (i.e. Poisson, negative binomial, zero-inflated Poisson, and zero-inflated negative
            binomial) to the leaf nodes of each tree estimator of the ensemble. RF will resolve most of the non-linearities
            inherent in the samples, thus leaving homogeneous samples in the leaf node, still presenting skewness and
            zero inflation. Count data models are better suited to model this type of data.

    + Visualization
    -------------------
        -   The modelling process creates raster layers in TIFF format that were visualized using cartopy, a Python
            library for mapping.
        -   The plots are created using matplotlib and seaborn libraries in Python.

    + Data
    -------------------
        -   Based in the insights obtained in the previous works, we devised a set of 21 features (covariates). Out of
            these 21, 19 are designed to represent human exposure (E), and 2 represent the hazard (H).
