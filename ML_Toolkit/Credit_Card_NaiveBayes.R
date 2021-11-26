# Needed Libraries for Analysis 
library(tidyverse)
library(caret)
library(e1071)
library(ggplot2)
library(klaR)
library(h2o)
library(DescTools)
library(ROCR)
library(InformationValue)

#Loading Dataset
df = read.csv("BankChurners.csv")

#Removing Not Needed Variables
df <- df[ -c(22,23) ]

#Changing Response Variable to 0,1
df = df %>% 
  mutate(Attrition_Flag = ifelse(as.character(Attrition_Flag) == "Existing Customer", 0, 1))

#Factorizing Categorical Variables
df$Attrition_Flag <- as.factor(df$Attrition_Flag)
df$Gender <- as.factor(df$Gender)
df$Education_Level <- as.factor(df$Education_Level)
df$Marital_Status <- as.factor(df$Marital_Status)
df$Income_Category <- as.factor(df$Income_Category)
df$Card_Category <- as.factor(df$Card_Category)


#Setting Seed
set.seed(12345)

#Splitting Training/Testing Data
training <- df %>% sample_frac(0.7)
testing <- anti_join(df, training, by = 'CLIENTNUM')

training <- training[ -c(1) ]
testing <- testing[ -c(1) ]


training %>%
  filter(Attrition_Flag == 1) %>%
  select_if(is.numeric) %>%
  cor() %>%
  corrplot::corrplot()


#Naive Bayes model
set.seed(12345)
nb.cc <- naiveBayes(Attrition_Flag ~ ., data = training, laplace = 0, usekernel = TRUE)

q <- predict(nb.cc, testing, type = 'class')


#Confusion Matrix
table(q, testing$Attrition_Flag)

#ROC Curve
predictions = predict(nb.cc, testing, type = "class")
testing$predictions = as.numeric(predictions) - 1
testing$Attrition_Flag = as.numeric(testing$Attrition_Flag) - 1

plotROC(testing$Attrition_Flag, testing$predictions)

