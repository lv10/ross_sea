# Installation #

```
#!bash

python setup.py install
```


# HOWTO: Using this project #

## Showing an image ##


```
#!bash

python app.py --show -img G_2015_336_0041_RS_N_VIR.mat --sensor mw_sic
```


## Histogram Matching ##

Since we have 2 instruments we use `-i vir` for VIRS and `-i mod` for MODIS.

### Histogram matching between two images ###
```
#!bash

python app.py --hist -img G_2015_336_0041_RS_N_VIR.mat -img2 G_2015_336_2025_RS_T_MOD.mat --sensor mw_sic
```

### Histogram matching to the get an image of the day for a one instrument ###

```
#!bash

python app.py -i vir --imgday --sensor mw_sic
```
### Single Image Full (Images and histogram) ###

```
#!bash

python app.py -shist -img G_2015_336_0041_RS_N_VIR.mat -img2 G_2015_336_0219_RS_N_VIR.mat --sensor mw_sic
```


### Plot histogram for 2 images

```
#!bash

python app.py -histplot -img G_2015_336_0041_RS_N_VIR.mat -img2 G_2015_336_0219_RS_N_VIR.mat --sensor mw_sic
```



### Plot the histograms for histogram match in 2 images ###


```
#!bash

python app.py -multiplot -img G_2015_336_0041_RS_N_VIR.mat -img2 G_2015_336_0219_RS_N_VIR.mat --sensor mw_sic
```

### Plot Source and Template and Match (Hist. Matched) images side-by-side.

```
#!bash

python app.py -sideplot -img G_2015_336_0041_RS_N_VIR.mat -img2 G_2015_336_0219_RS_N_VIR.mat --sensor mw_sic
```


## Sea Ice Report ##

### Run the full Sea Ice Report ###

Lense can be specified, however it defaults to using the lense argument: `--sensor 'mw_sic'`

```
#!bash

python app.py -i vir --sic
```

### Run a Sea Ice or Land Distribution (pie chart) ###


```
#!bash

python app.py -d -img G_2015_336_0041_RS_N_VIR.mat --sensor mw_sic
```

### Runa SIC or Land Silhoutte Report ###

```
#!bash


python app.py -s -img G_2015_336_0041_RS_N_VIR.mat --sensor mw_sic
```

### Run a surface analysys Report ###

```
#!bash

python app.py -srf -img G_2015_336_0041_RS_N_VIR.mat
```

### Show SIC, LM Overlapping ###

```
#!bash

python app.py -overlap -img G_2015_336_0041_RS_N_VIR.mat
```


## Color Report ##

### Run a full report on an image ###

```
#!bash


python app.py -c -img G_2015_336_1041_RS_N_VIR.mat
```

### get the RGB of an image ###

```
#!bash

python app.py -rgb -img G_2015_336_0041_RS_N_VIR.mat --sensor ibands
```

### Show Water Ice Cluster with K-means ###

```
#!bash

python app.py -water -img G_2015_336_0041_RS_N_VIR.mat
```
