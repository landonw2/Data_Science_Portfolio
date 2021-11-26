library(tidyverse)
library(caret)
library(nnet)
library(NeuralNetTools)
library(ggplot2)
library(reshape2)
library(mgcv)
library(DescTools)
library(ROCR)
library(InformationValue)
library(e1071)

#Loading in Dataset
df = read.csv("BankChurners.csv")

#Removing Not Needed Variables
df <- df[ -c(22,23) ]

#Changing Response Variable to 0,1
df = df %>% 
  mutate(Attrition_Flag = ifelse(as.character(Attrition_Flag) == "Existing Customer", 0, 1))

#Setting Seed
set.seed(4321)

#Splitting Training/Testing Data
training <- df %>% sample_frac(0.7)
testing <- anti_join(df, training, by = 'CLIENTNUM')

training <- training[ -c(1) ]
testing <- testing[ -c(1) ]

# Standardizing Continuous Variables
training <- training %>%
  mutate(s_Customer_Age = scale(Customer_Age),
         s_Dependent_count = scale(Dependent_count),
         s_Months_on_book = scale(Months_on_book),
         s_Total_Relationship_Count = scale(Total_Relationship_Count),
         s_Months_Inactive_12_mon = scale(Months_Inactive_12_mon),
         s_Contacts_Count_12_mon = scale(Contacts_Count_12_mon),
         s_Credit_Limit = scale(Credit_Limit),
         s_Total_Revolving_Bal = scale(Total_Revolving_Bal),
         s_Avg_Open_To_Buy = scale(Avg_Open_To_Buy),
         s_Total_Amt_Chng_Q4_Q1 = scale(Total_Amt_Chng_Q4_Q1),
         s_Total_Trans_Amt = scale(Total_Trans_Amt),
         s_Total_Trans_Ct = scale(Total_Trans_Ct),
         s_Total_Ct_Chng_Q4_Q1 = scale(Total_Ct_Chng_Q4_Q1),
         s_Avg_Utilization_Ratio = scale(Avg_Utilization_Ratio))

training$Attrition_Flag <- as.factor(training$Attrition_Flag)
training$Gender <- as.factor(training$Gender)
training$Education_Level <- as.factor(training$Education_Level)
training$Marital_Status <- as.factor(training$Marital_Status)
training$Income_Category <- as.factor(training$Income_Category)
training$Card_Category <- as.factor(training$Card_Category)

# Standardizing Continuous Variables
testing <- testing %>%
  mutate(s_Customer_Age = scale(Customer_Age),
         s_Dependent_count = scale(Dependent_count),
         s_Months_on_book = scale(Months_on_book),
         s_Total_Relationship_Count = scale(Total_Relationship_Count),
         s_Months_Inactive_12_mon = scale(Months_Inactive_12_mon),
         s_Contacts_Count_12_mon = scale(Contacts_Count_12_mon),
         s_Credit_Limit = scale(Credit_Limit),
         s_Total_Revolving_Bal = scale(Total_Revolving_Bal),
         s_Avg_Open_To_Buy = scale(Avg_Open_To_Buy),
         s_Total_Amt_Chng_Q4_Q1 = scale(Total_Amt_Chng_Q4_Q1),
         s_Total_Trans_Amt = scale(Total_Trans_Amt),
         s_Total_Trans_Ct = scale(Total_Trans_Ct),
         s_Total_Ct_Chng_Q4_Q1 = scale(Total_Ct_Chng_Q4_Q1),
         s_Avg_Utilization_Ratio = scale(Avg_Utilization_Ratio))

testing$Attrition_Flag <- as.factor(testing$Attrition_Flag)
testing$Gender <- as.factor(testing$Gender)
testing$Education_Level <- as.factor(testing$Education_Level)
testing$Marital_Status <- as.factor(testing$Marital_Status)
testing$Income_Category <- as.factor(testing$Income_Category)
testing$Card_Category <- as.factor(testing$Card_Category)


# Neural Network model
set.seed(12345)
nn.df <- nnet(Attrition_Flag ~ s_Customer_Age + s_Dependent_count + s_Months_on_book + 
                s_Total_Relationship_Count + s_Months_Inactive_12_mon + s_Contacts_Count_12_mon +
                s_Credit_Limit + s_Total_Revolving_Bal + s_Avg_Open_To_Buy + s_Total_Amt_Chng_Q4_Q1 +
                s_Total_Trans_Amt + s_Total_Trans_Ct + s_Total_Ct_Chng_Q4_Q1 + s_Avg_Utilization_Ratio +
                Gender + Education_Level + Marital_Status + Income_Category + Card_Category, data = training, size = 8)


# Plot the network
NeuralNetTools::plotnet(nn.df)

# Optimize Number of Hidden Nodes and Regularization (decay option)
tune_grid <- expand.grid(
  .size = c(4, 5, 6, 7, 8, 9, 10),
  .decay = c(0, 0.5, 1)
)

# Training New Neural Network with Parameter Tuning
nn.df.caret <- train(Attrition_Flag ~ s_Customer_Age + s_Dependent_count + s_Months_on_book + 
                         s_Total_Relationship_Count + s_Months_Inactive_12_mon + s_Contacts_Count_12_mon +
                         s_Credit_Limit + s_Total_Revolving_Bal + s_Avg_Open_To_Buy + s_Total_Amt_Chng_Q4_Q1 +
                         s_Total_Trans_Amt + s_Total_Trans_Ct + s_Total_Ct_Chng_Q4_Q1 + s_Avg_Utilization_Ratio +
                         Gender + Education_Level + Marital_Status + Income_Category + Card_Category
                       , data = training,
                       method = "nnet", 
                       tuneGrid = tune_grid,
                       trControl = trainControl(method = 'cv',
                                                number = 10),
                       trace = FALSE)

nn.df.caret$bestTune



#Creating final neural network with size = 8 and decay = 0.5
set.seed(12345)
nn.df <- nnet(Attrition_Flag ~ s_Customer_Age + s_Dependent_count + s_Months_on_book + 
                s_Total_Relationship_Count + s_Months_Inactive_12_mon + s_Contacts_Count_12_mon +
                s_Credit_Limit + s_Total_Revolving_Bal + s_Avg_Open_To_Buy + s_Total_Amt_Chng_Q4_Q1 +
                s_Total_Trans_Amt + s_Total_Trans_Ct + s_Total_Ct_Chng_Q4_Q1 + s_Avg_Utilization_Ratio +
                Gender + Education_Level + Marital_Status + Income_Category + Card_Category, data = training, size = 8, decay = 0.5)



#Plotting
plotnet(nn.df)

# Hinton Diagram
nn_weights <- matrix(data = nn.df$wts[1:264], ncol = 8, nrow = 33)
rownames(nn_weights) <- c("bias", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10", "v11", "v12", "v13", "v14", "v15", "v16", "v17", "v18", "v19", "v20", "v21", "v22", "v23", "v24", "v25", "v26", "v27", "v28", "v29", "v30", "v31", "v32")
colnames(nn_weights) <- c("n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8")

ggplot(melt(nn_weights), aes(x=Var1, y=Var2, size=abs(value), color=as.factor(sign(value)))) +
  geom_point(shape = 15) +
  scale_size_area(max_size = 15) +
  labs(x = "", y = "", title = "Hinton Diagram of NN Weights") +
  theme_bw()


# Accuracy of 95.7%
table(testing$Attrition_Flag, predict(nn.df, testing, type = "class"))

# Accuracy of 96.1%
table(training$Attrition_Flag, predict(nn.df, training, type = "class"))

predictions = predict(nn.df, testing, type = "class")

testing$predictions = as.numeric(predictions)



#Coefficient of Discrimmination - 0.7989307
p1 <- testing$predictions[testing$Attrition_Flag == 1]
p0 <- testing$predictions[testing$Attrition_Flag == 0]
coef_discrim <- mean(p1) - mean(p0)
coef_discrim

#Plotting Coefficient of Discrimmination
ggplot(testing, aes(predictions, fill = factor(Attrition_Flag))) +
  geom_density(alpha = 0.55) +
  scale_fill_manual(labels = c("Did not churn", "Did churn"), values = c('#0072B2', '#808080')) +
  labs(x = "Predicted Probability",
       fill = "Outcome",
       title = paste("Coefficient of Discrimination = ",
                     round(coef_discrim, 3), sep = "")) +
  theme_minimal()

#ROC Curve - 0.8942
plotROC(testing$Attrition_Flag, testing$predictions)








