# Team Plot Rankr
Sterenborg: automatically rank plots based on NDVI maps that stem from satellite and drone images.

Team members: Rowley Cowper and Simeon Nedkov

The idea of this data interaction is to make a tool that can identify, in graph form, any potential deviation in field performance or between fields, that might reveal a growing or emerging problem. The concept revolves around the fact that the dataset in the current visual form may hide emerging problems if the problem is evenly distributed throughout the image. By taking the histogram of a field it is hoped to reveal additional peaks emerging that would cause the farmer to look at the data/field in more detail.

The final output should look something like this:

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/01%20-%20Field%20A.jpg" height="300px">

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/02%20-%20Field%20B.jpg" height="220px">

# Methodology

Take the dataset

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/03%20-%20Fields%20Rast.jpg" height="350px">

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/04%20-%20Fields%20Vect.jpg" height="350px">

The farmer can select the fields to consider or to rank

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/05%20-%20Field%20Select.jpg" height="350px">

These are masked, breaking it down into individual field, removing the pixel bordering effect

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/06%20-%20Field%20Select%202.jpg" height="250px">

<img src="https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/07%20-%20Field%20Select%203.jpg" height="300px">

Convert to a histogram, with the intent of looking for significant deviations in the form of dual peaks

![](https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/08%20-%20Normal%20Distribution.jpg)
![](https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/09%20-Bimodal.jpg)

Set a threshold point at which to calculate the number of peaks, possibly by scanning the image from bottom to top, looking for gaps

![](https://raw.githubusercontent.com/FarmHackNL/plot-rankr/master/documentation/images/10%20-%20Threshold%20distribution.jpg)

If a count=2 scenario is encountered, then there is the potential that a problem is developing. This may only be able to look at visually.

A time based evaluation of this would also be quite valuable, as it may show an emerging area problem.

For example, if the problem is evenly distributed, it is hard to see in the picture visually, but would be very apparent in the histogram representation.

Things that need to be done/considered - Exporting the raster data measurements into a stats program or algorithm that computes a minimum threshold count for the histogram to give a good distribution

# Implementation

The methodology is implemented in `rank.py`. The script takes a satellite/drone image, intersects it with the farmer's plots
and calculates a number of zonal statistics and a histogram.

# TODO

- automatically detect peaks in the histogram
