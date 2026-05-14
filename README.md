# Land Use Land Cover Change Misclassification Time Series Analysis of Danish Agricultural Land

This Repository contains the code used for the analysis performed in the Research Project "Land Use Land Cover Change Misclassification Time Series
Analysis of Danish Agricultural Land".

Agricultural expansion and afforestation are some of the most common land use change processes.Accurately quantifying how much land has undergone these processes is critical in tackling global societal challenges. However, the time evolution of agricultural and other vegetation related types of land is unstable by nature. This creates a challenge for Land Cover Land Use (LULC) change analysis, because year to year differences in classification may reflect genuine land transformation, but may also reflect class ambiguity, seasonal surface conditions, or product misclassifications. This study examines how Dynamic World classifies Danish agricultural land from 2020 to 2025 using Danish Agency of Agriculture (DAA) field block data as a reference geometry. Annual Dynamic World mode classifications were compared with the DAA agricultural area, the yearly changes were analysed through change matrices and classification alternation counting. 

The results show that Dynamic World classifies most Danish agricultural area as Crops, supporting its usefulness for agricultural mapping. However, frequent short changes occur between the classes of Crops, Grass, and Trees. These vegetation related changes in class account for the majority of detected change inside the DAA area. Filtering changes that only lasted one year and returned to the original classification reduces the number of different classifications per pixel in the study period, It is especially promising when otherwise stable pixels change class for a brief period, but it does not remove total temporal instability across a six year period. More complex cyclic change patterns still remain, suggesting that an A→B→A filtering capture only part of the temporal uncertainty. This study concludes that Dynamic World is valuable for agricultural LULC classification with the caveat that historical context is needed to correctly interpret LULC change

This study aims to address two questions.The first being, do DW temporal misclassification affect our analysis of LULC change, in the case of Danish agricultural land. To do so we investigates how DW classifications behave within Danish agricultural land from 2020 to 2025. Using Danish Agency of Agriculture (Landbrugsstyrelsen) (DAA) field-block data as ground truth, we examine how DW classifies administratively defined agricultural land, how these classifications change across time, and when do classification change agree with ground truth change.The second question, does temporal filtering, based on historic classifications, improve DW classifications reliability in the study of LULC change and what classification alternation patterns remain. Based on other studies, we define what consists of a Rapid Sequence Change (RSC), modify our yearly classifications to not consider this type of changes and compare the results.The study focuses especially on transitions between Crops, Grass, and Trees, as these vegetation related classes dominate both the agricultural reference area and the observed annual changes. The central aim is to assess whether DW can be used reliably for agricultural LULC change analysis in a country like Denmark, and to identify where apparent change may instead reflect temporal uncertainty, class ambiguity, or mismatch between visual land cover categories and administrative agricultural definitions.

Authors:
* [Mike Raemann Palmer](mirp@itu.dk)
* [Sara Vieira](sapi@itu.dk)

Supervisor:
* [Maria Sinziiana Astefanoaeie](msia@itu.dk)

IT University of Copenhagen Spring 2026

