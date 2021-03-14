These two folder have the scripts for generating the 5 class semantic segmentations mentioned in the paper as well as the analyeses we performed on the segmentations.

In the analysis scripts folder scripts were meant to be run in a particular order
1.Full scanner to individual plates
2.Invidual plates to timeseries with cline of interactions
3.phase plot generate

1). In these threee steps we take segmented images of the whole scanner and break those down into images of individual Physarum.2) These individual plates/ecosystems are measured and used to generate time series of the five classes over time. This is also the step where an interaction zone/mask is created to more succintly quantify the interspecies interactions we care so much about. 3) Finally we use a plotting script to summarize the interactions that take place between Physarum and a red yeast.


