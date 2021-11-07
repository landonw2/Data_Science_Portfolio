library(tidyverse)
library(ggplot2)
library(cluster)

data <- read.csv("SVI.csv")

###############################################################################
#                                                                             #
#                             Data Posturing                                  #
#                                                                             #
###############################################################################

# filtering rows where state is equal Kentucky
data <- data %>%
  filter(data$STATE == ' Kentucky')

# subsetting variables from original dataset
data <- data[, c('COUNTY', 'FIPS', 'EP_POV', 'EP_UNEMP', 'EP_PCI', 
                 'EP_NOHSDP','EP_AGE65','EP_AGE17', 'EP_DISABL', 'EP_SNGPNT', 
                 'EP_MINRTY','EP_LIMENG','EP_MUNIT', 'EP_MOBILE', 'EP_CROWD', 
                 'EP_NOVEH', 'EP_GROUPQ')]

# examine the data structure
str(data)

# check for missing values in each column
sapply(data, function(x) sum(is.na(x)))

# another method for checkin missing vlaues
which(complete.cases(data)==FALSE)

# print the summary of the data
summary(data)

# function for performing the normalization
normalize.feature <- function( feature ) {
  if ( sum(feature, na.rm = T) == 0 ) feature
  else ((feature - min(feature, na.rm = T))/(max(feature, na.rm = T) - min(feature, na.rm = T)))
}

# normalize variables
data.norm <- as.data.frame(apply(data[-c('COUNTY', 'FIPS')] , 2, normalize.feature))


###############################################################################
#                                                                             #
#                    K-Means Clustering - 15 variables                        #
#                                                                             #
###############################################################################


# Elbow method to determine number of clusters
# run many models with varying value of k (centers)
tot_withinss <- map_dbl(1:10,  function(k){
  model <- kmeans(x = data[, 3:17], centers = k)
  model$tot.withinss
})

# Generate a data frame containing both k and tot_withinss
elbow_df <- data.frame(
  k = 1:10,
  tot_withinss = tot_withinss
)

# Elbow method plot
ggplot(elbow_df, aes(x = k, y = tot_withinss)) +
  geom_line() + geom_point()+
  scale_x_continuous(breaks = 1:10) +
  labs(title = "Elbow Method", x = "Number of Clusters", y = "Within-cluster Sum of Squares") +
  theme(plot.title = element_text(hjust = 0.5))


# run the clustering with 5 clusters, iter.max=20, nstart=1000
simple.3k <- kmeans(x = data[, 3:17], centers=5, iter.max=20, nstart=1000)

# print the model
simple.5k

# add the cluster as a new variable to the dataset
data$cluster <- factor(simple.5k$cluster)