---------------------------------------------------------------------------------------------------------------------
Publication associated to this work:
Using volunteered observations to map human exposure to ticks (2018)
https://www.nature.com/articles/s41598-018-33900-2
---------------------------------------------------------------------------------------------------------------------

NOTES:

    + Modelling
    -------------------
        -   The previous two publications provide an estimate of the hazard (H) and tick bite risk (R). With these
            two components, we propose a procedure to obtain human exposure (E) tick bites at the national scale, given
            that R = H * E --> E = R / H.
        -   This work is a pre-step to assess the feasiblity of developing a full tick bite risk model using features
            that help characterizing tick bite risk.

    + Visualization
    -------------------
        -   The modelling process creates raster layers in TIFF format that were visualized using cartopy, a Python
            library for mapping.
        -   The plots are created using matplotlib and seaborn libraries in Python.

    + Data
    -------------------
        -   The data used in this work come from the two previous works. We used the model in P02 to create daily
            maps of tick activity for the period 2006-2014. Then we calculated the maximum mean and maximum
            standard deviation of the tick activity throughout the period, to have a robust estimator of the
            potential maximum activity in each location. The tick bite reports in the collection were aggregated
            to a grid cell of 1km.
