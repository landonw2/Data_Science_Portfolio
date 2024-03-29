# load packages
library(tidyverse)
library(car)
library(DescTools)
library(corrplot)
library(mosaic)
library(modelr)
library(plotly)
library(ggplot2)
library(Hmisc)
library(onehot)
library(jmuOutlier)
library(leaps)
library(glmnet)
library(nortest)
library(lmtest)
library(InformationValue)
library(gmodels)
library(vcdExtra)
library(TSA)
library(carData)
library(epiDisplay)
library(gridExtra)
library(mgcv)
library(Hmisc)
library(hexbin)
library(ROCR)
library(caret)


###############################################################################
#                                                                             #
#                              Load Datasets                                  #
#                                                                             #
###############################################################################

combined = read.csv('combined.csv')

df = readxl::read_xlsx("FoodAccessResearchAtlasData2019.xlsx", sheet = 3)
dictionary = readxl::read_xlsx("FoodAccessResearchAtlasData2019.xlsx", sheet = 2)



###############################################################################
#                                                                             #
#                         Data Posturing and EDA                              #
#                                                                             #
###############################################################################

# Converting CensusTracts to numeric data types
df = df %>%
  mutate(CensusTract = as.numeric(CensusTract))

# Joining Datasets
combined2 = inner_join(combined, df[,c(1, 18:24, 33, 59, 85, 111, 147)], 
                       by = c("FIPS" = "CensusTract"))

# More datatype conversions
combined2 = combined2 %>%
  mutate(lapophalfshare = as.numeric(lapophalfshare)) %>%
  mutate(lapop1share = as.numeric(lapop1share)) %>%
  mutate(lapop10share = as.numeric(lapop10share)) %>%
  mutate(lapop20share = as.numeric(lapop20share))

# Filtering just for Kentucky and creating scatterplot
combined2 %>%
  filter(ST_ABBR == 'KY') %>%
  ggplot(., aes(x = EP_NOVEH , y = lapop10share)) +
  geom_point() +
  geom_label( 
    data=combined2 %>% filter(ST_ABBR == 'KY' & EP_NOVEH > 7 & lapop10share>50), 
    aes(label=COUNTY)
  )

# More Kentucky data exploration
combined2 %>%
  filter(ST_ABBR == 'KY' & EP_NOVEH > 7 & lapop10share > 50) %>%
  group_by(COUNTY) %>%
  tally()

# More Kentucky data exploration
combined2 %>%
  filter(ST_ABBR == 'KY') %>%
  #  group_by(COUNTY) %>%
  summarize(sum = sum(LATracts10)) %>%
  arrange(desc(sum))

combined2 %>%
  tally()

combined2 %>%
  filter(LATracts10==1) %>%
  tally() * 0.7


###############################################################################
#                                                                             #
#                         Logistic Regression Model                           #
#                                                                             #
###############################################################################


#Creating train, validate, and test splits
test_validate_u %>%
  filter(LATracts10==1) %>%
  tally() * 0.67


train_u = combined2 %>%
  group_by(LATracts10) %>%
  sample_n(2223)

test_validate_u = combined2[-train_u$FID,]

validate_u = test_validate_u %>%
  group_by(LATracts10) %>%
  sample_n(1957)

test_u = test_validate_u[-validate_u$FID,]


# Model Creation
# Response: LATracts10
glm_subset = train_u %>%
  select(LATracts10, EP_POV, EP_UNEMP, EP_PCI, EP_NOHSDP, EP_AGE65,
         EP_AGE17, EP_DISABL, EP_SNGPNT, EP_MINRTY, EP_LIMENG,
         EP_MUNIT, EP_MOBILE, EP_CROWD, EP_NOVEH, EP_GROUPQ)

empty_glm_1 = glm(LATracts10~1,
                  data = glm_subset,
                  family = binomial(link = "logit"))
full_glm_1 = glm(LATracts10~.,
                 data = glm_subset,
                 family = binomial(link = "logit"))

back_1 = step(full_glm_1,
              scope = list(lower = empty_glm_1,
                           upper = full_glm_1),
              direction = "backward",
              k = log(nrow(glm_subset)))
summary(back_1)

# turn coefficients into odds ratios
100*(exp(coef(back_1))-1)

# find cutoff
1 - pchisq(log(nrow(glm_subset)), df = 1)# 0.00375

# test assumptions
glm_test = gam(LATracts10 ~ EP_UNEMP + EP_PCI + EP_AGE65 + EP_AGE17 + 
                 EP_SNGPNT + EP_MINRTY + EP_LIMENG + EP_MUNIT + EP_MOBILE + 
                 EP_CROWD + s(EP_GROUPQ), family = binomial(link = "logit"), 
               data = glm_subset,
               method = 'REML')

anova(back_1, glm_test, test = 'Chisq')
plot(glm_test)

glm_subset2 = glm_subset %>%
  mutate(EP_UNEMP_BIN = cut(EP_UNEMP,
                            breaks = c(-Inf, 15, Inf))) %>%
  mutate(EP_PCI_BIN = cut(EP_PCI,
                          breaks = c(-Inf, 20000, 30000, 75000, Inf))) %>%
  mutate(EP_AGE65_BIN = cut(EP_AGE65,
                            breaks = c(-Inf, 25, Inf))) %>%
  mutate(EP_SNGPNT_BIN = cut(EP_SNGPNT,
                             breaks = c(-Inf, 5, 15, Inf))) %>%
  mutate(EP_MINRTY_BIN = cut(EP_MINRTY,
                             breaks = c(-Inf, 20, 50, 70, Inf))) %>%
  mutate(EP_LIMENG_BIN = cut(EP_LIMENG,
                             breaks = c(-Inf, 5, 10, 25, 42, Inf))) %>%
  mutate(EP_MOBILE_BIN = cut(EP_MOBILE,
                             breaks = c(-Inf, 10, 25, 57, Inf))) %>%
  mutate(EP_GROUPQ_BIN = cut(EP_GROUPQ,
                             breaks = c(-Inf, 20, 70, Inf))) %>%
  select(LATracts10, EP_UNEMP_BIN, EP_PCI_BIN, EP_AGE65_BIN, EP_AGE17,
         EP_SNGPNT_BIN, EP_MINRTY_BIN, EP_LIMENG_BIN, EP_MUNIT, EP_MOBILE_BIN,
         EP_CROWD, EP_GROUPQ_BIN)



# Model 2 Creation
# Response: LATracts10
glm_2 = glm(LATracts10~EP_UNEMP_BIN + EP_PCI_BIN + EP_AGE65_BIN + EP_AGE17 +
              EP_SNGPNT_BIN + EP_MINRTY_BIN + EP_LIMENG_BIN + EP_MUNIT + EP_MOBILE_BIN +
              EP_CROWD + EP_GROUPQ_BIN,
            data = glm_subset2,
            family = binomial(link = "logit"))
summary(glm_2)

back_2 = step(glm_2,
              scope = list(lower = empty_glm_1,
                           upper = glm_2),
              direction = "backward",
              k = log(nrow(glm_subset2)))
summary(back_2)

back_2 = glm(LATracts10 ~ EP_PCI_BIN + EP_AGE65_BIN + EP_SNGPNT_BIN +
               EP_MINRTY_BIN + EP_MUNIT + EP_MOBILE_BIN + EP_CROWD,
             family = binomial(link = "logit"), 
             data = glm_subset2)

reduced = glm(LATracts10 ~ EP_PCI_BIN + EP_AGE65_BIN + EP_SNGPNT_BIN +
                EP_MINRTY_BIN + EP_MUNIT + EP_MOBILE_BIN + EP_CROWD,
              family = binomial(link = "logit"),
              data = glm_subset2)

summary1 = anova(back_2, reduced, test = 'LRT')

summary1$`Pr(>Chi)`

# turn coefficients into odds ratios
100*(exp(coef(glm_2))-1)

100*(exp(coef(back_2))-1)


###############################################################################
#                                                                             #
#                                 Score Models                                #
#                                                                             #
###############################################################################

# Create bins
validate_u_subset = validate_u %>%
  mutate(EP_UNEMP_BIN = cut(EP_UNEMP,
                            breaks = c(-Inf, 15, Inf))) %>%
  mutate(EP_PCI_BIN = cut(EP_PCI,
                          breaks = c(-Inf, 20000, 30000, 75000, Inf))) %>%
  mutate(EP_AGE65_BIN = cut(EP_AGE65,
                            breaks = c(-Inf, 25, Inf))) %>%
  mutate(EP_SNGPNT_BIN = cut(EP_SNGPNT,
                             breaks = c(-Inf, 5, 15, Inf))) %>%
  mutate(EP_MINRTY_BIN = cut(EP_MINRTY,
                             breaks = c(-Inf, 20, 50, 70, Inf))) %>%
  mutate(EP_LIMENG_BIN = cut(EP_LIMENG,
                             breaks = c(-Inf, 5, 10, 25, 42, Inf))) %>%
  mutate(EP_MOBILE_BIN = cut(EP_MOBILE,
                             breaks = c(-Inf, 10, 25, 57, Inf))) %>%
  mutate(EP_GROUPQ_BIN = cut(EP_GROUPQ,
                             breaks = c(-Inf, 20, 70, Inf)))

# score both
validate_pred = data.frame(validate_u_subset,
                           'Pred1' = predict(back_1, newdata = validate_u_subset,
                                             type = 'response'),
                           'Pred2' = predict(glm_2, newdata = validate_u_subset,
                                             type = 'response'),
                           'Pred3' = predict(back_2, newdata = validate_u_subset,
                                             type = 'response'))

# concordance
Concordance(validate_pred$LATracts10, validate_pred$Pred1)
# 0.8986
Concordance(validate_pred$LATracts10, validate_pred$Pred2)
# 0.8820
Concordance(validate_pred$LATracts10, validate_pred$Pred3)
# 0.8793

# ROC curves
plotROC(validate_pred$LATracts10, validate_pred$Pred1)
plotROC(validate_pred$LATracts10, validate_pred$Pred2)



# Test Datset
test_u_subset = test_u %>%
  mutate(EP_UNEMP_BIN = cut(EP_UNEMP,
                            breaks = c(-Inf, 15, Inf))) %>%
  mutate(EP_PCI_BIN = cut(EP_PCI,
                          breaks = c(-Inf, 20000, 30000, 75000, Inf))) %>%
  mutate(EP_AGE65_BIN = cut(EP_AGE65,
                            breaks = c(-Inf, 25, Inf))) %>%
  mutate(EP_SNGPNT_BIN = cut(EP_SNGPNT,
                             breaks = c(-Inf, 5, 15, Inf))) %>%
  mutate(EP_MINRTY_BIN = cut(EP_MINRTY,
                             breaks = c(-Inf, 20, 50, 70, Inf))) %>%
  mutate(EP_LIMENG_BIN = cut(EP_LIMENG,
                             breaks = c(-Inf, 5, 10, 25, 42, Inf))) %>%
  mutate(EP_MOBILE_BIN = cut(EP_MOBILE,
                             breaks = c(-Inf, 10, 25, 57, Inf))) %>%
  mutate(EP_GROUPQ_BIN = cut(EP_GROUPQ,
                             breaks = c(-Inf, 20, 70, Inf)))

test_pred = data.frame(test_u_subset,
                       'Pred1' = predict(back_1, newdata = test_u_subset,
                                         type = 'response'),
                       'Pred2' = predict(glm_2, newdata = test_u_subset,
                                         type = 'response'),
                       'Pred3' = predict(back_2, newdata = test_u_subset,
                                         type = 'response'))

# ROC curves
plotROC(test_pred$LATracts10, test_pred$Pred1)
# 0.9029
plotROC(test_pred$LATracts10, test_pred$Pred2)
# 0.8853
plotROC(test_pred$LATracts10, test_pred$Pred3)
# 0.8829


###############################################################################
#                                                                             #
#                                 Score Models                                #
#                                                                             #
###############################################################################

# Creating Bins again
combined3 = combined2 %>%
  mutate(EP_UNEMP_BIN = cut(EP_UNEMP,
                            breaks = c(-Inf, 15, Inf))) %>%
  mutate(EP_PCI_BIN = cut(EP_PCI,
                          breaks = c(-Inf, 20000, 30000, 75000, Inf))) %>%
  mutate(EP_AGE65_BIN = cut(EP_AGE65,
                            breaks = c(-Inf, 25, Inf))) %>%
  mutate(EP_SNGPNT_BIN = cut(EP_SNGPNT,
                             breaks = c(-Inf, 5, 15, Inf))) %>%
  mutate(EP_MINRTY_BIN = cut(EP_MINRTY,
                             breaks = c(-Inf, 20, 50, 70, Inf))) %>%
  mutate(EP_LIMENG_BIN = cut(EP_LIMENG,
                             breaks = c(-Inf, 5, 10, 25, 42, Inf))) %>%
  mutate(EP_MOBILE_BIN = cut(EP_MOBILE,
                             breaks = c(-Inf, 10, 25, 57, Inf))) %>%
  mutate(EP_GROUPQ_BIN = cut(EP_GROUPQ,
                             breaks = c(-Inf, 20, 70, Inf)))

# Creating dataframe of KY tract predictions
ky_predictions = data.frame(combined3,
                            'prediction' = predict(back_2, newdata = combined3,
                                                   type = 'response'))

# Subsetting to certain variables
ky_predictions = ky_predictions %>%
  filter(ST_ABBR == 'KY') %>%
  select(FID, ST, STATE, ST_ABBR, STCNTY, COUNTY, FIPS,
         EP_UNEMP, EP_UNEMP_BIN, EP_PCI, EP_PCI_BIN, EP_AGE65, EP_AGE65_BIN, EP_AGE17,
         EP_SNGPNT, EP_SNGPNT_BIN, EP_MINRTY, EP_MINRTY_BIN, EP_LIMENG, EP_LIMENG_BIN,
         EP_MUNIT, EP_MOBILE, EP_MOBILE_BIN, EP_CROWD, EP_GROUPQ, EP_GROUPQ_BIN,
         LATracts_half, LATracts1, LATracts10, LATracts20,
         prediction)


