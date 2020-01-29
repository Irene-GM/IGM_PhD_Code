---------------------------------------------------------------------------------------------------------------------
Publication associated to this work:
Modelling and mapping tick dynamics using volunteered observations (2017)
https://ij-healthgeographics.biomedcentral.com/articles/10.1186/s12942-017-0114-8
---------------------------------------------------------------------------------------------------------------------

NOTES:

    + Modelling
    -------------------
        -   We use the implementation of Random Forest available in the Python machine learning library scikit-learn
        -   To enable random forest to understand the temporal dynamics of tick activity, we transform the target
            variable (tick counts) into a monthly Z-scores.

    + Visualization
    -------------------
        -   The modelling process creates raster layers in TIFF format that were visualized using QGIS or ArcGIS.
        -   The plots are created using matplotlib library in Python.

    + Data
    -------------------
        -   We obtained an array of 101 features (covariates) for each observation. Out of this 101, 77 refer to
            weather variables (i.e. min. temperature, max. temperature, precipitation, evapotranspiration, relative
            humidity, saturation deficit and vapour pressure) aggregated at 11 time scales (i.e. 1-7 days before sampling,
            14, 30, 90, 365 days before sampling). The remaining of the variables come from remote sensing images
            (i.e. NDVI, EVI, NDWI), land cover, mast years, and tick habitat.
