
---------------------------------------------------------------------------------------------------------------------
Publication associated to this work:
Identifying Environmental and Human Factors Associated With Tick Bites (2016)
using Volunteered Reports and Frequent Pattern Mining
https://onlinelibrary.wiley.com/doi/abs/10.1111/tgis.12211
---------------------------------------------------------------------------------------------------------------------

NOTES:

    + Modelling
    -------------------
        -   Carried out using SPMF software, available here: http://www.philippe-fournier-viger.com/spmf/
        -   The file "mdt_integers.csv" is used in SPMF with different levels of support to find recurrent
            patterns in the enriched tick bites and the random tick bites. After this step, we use Python
            again to translate the rules into an identifiable pattern.

    + Visualization
    -------------------
        - The ringmaps were prepared using D3 Javascript library and developed in Aptana Studio 3.
        - The maps of NL were created using ArcGIS software.

    + Data
    -------------------
        -   Were transformed to accommodate the requirements of SPMF software. Once the table of features was prepared
            we classified the features using Jenks, and subsequently, the categories were transformed to integer
            numbers of 6 digits. You can see this in file "./IGM_PhD_Materials/data/P01/in/mdt_integers.csv"
