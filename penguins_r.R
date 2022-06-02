#short example script
library(tidyverse)
library(palmerpenguins)
data(package = 'palmerpenguins')

peng<-palmerpenguins::penguins

#number of penguins
total_penguins <-nrow(peng)

#Adelie penguins
adelie <- filter(peng, species == "Adelie")

#percentage of adelie penguins from all
(nrow(adelie)/total_penguins)*100
