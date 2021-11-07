library(tseries)
library(forecast)
library(haven)
library(fma)
library(expsmooth)
library(lmtest)
library(zoo)
library(seasonal)
library(ggplot2)
library(seasonalview)
library(aTSA)
library(imputeTS)
library(prophet)

energy = read.csv("hydro.csv")
ex_data = read.csv("additional_data.csv")


###############################################################################
#                                                                             #
#                             DATA POSTURING                                  #
#                                                                             #
###############################################################################

# Subsetting datasets down
energy <- energy[c(18:42),c(1,2)]
ex_data <- ex_data[c(18:42),c(1,2,3)]

# Only taking the sunhours varible from the exogenous variables dataset
sunhours <- ex_data[c(-3)]

# Creating time series object for splits
hydro = ts(energy$Hydro, start=c(2017, 10), frequency = 6)
hydro_train = subset(hydro, end = length(hydro)-6)
hydro_val = subset(hydro, start = length(hydro)-5, end=length(hydro))


# Creating time series object for splits
sunhours_ts = ts(sunhours$Sun, start=c(2017, 10), frequency = 6)
sunhours_train = subset(sunhours_ts, end = length(sunhours_ts)-6)
sunhours_val = subset(sunhours_ts, start = length(sunhours_ts)-5, end=length(sunhours_ts))

# Plotting Hydroelectricity Data
plot(hydro)

# Checking for Seasonal Differences
hydro %>% nsdiffs()

# Difference, ACF, and PACF plots
hydro %>% diff(lag = 12) %>% ggtsdisplay()

# Creating Model with sunhours as exogenous variable
SARIMAX <- Arima(hydro_train, order=c(2,0,2), seasonal=c(1,1,1), xreg=cbind(sunhours_train),
                  method="ML")

# Checking Summary
summary(SARIMAX)

# Checking Residuals and Performing Ljung-Box test for White Noise
checkresiduals(SARIMAX)

# Calculate prediction errors from forecast
SARIMAX.error <- hydro_val - forecast::forecast(SARIMAX, h = 6, xreg= cbind(sunhours_train))$mean

# Calculate prediction error statistics (MAE and MAPE)
SARIMAX.MAE <- mean(abs(SARIMAX.error))
SARIMAX.MAPE <- mean(abs(SARIMAX.error)/abs(hydro_val))*100

#MAE - 64.87673
SARIMAX.MAE

#MAPE - 13.01763%
SARIMAX.MAPE

# Printing out actual forecasted values for sanity check
forecast::forecast(SARIMAX, h = 6, xreg= cbind(sunhours_train))$mean

# Plotting actual data, fitted model, and forecast
autoplot(forecast::forecast(SARIMAX, h = 12, xreg=cbind(sunhours_train)), PI=FALSE) + autolayer(fitted(SARIMAX), color = '#D21404', series="Fitted") + 
  ylab("Hydro-Electricity") + 
  autolayer(hydro, series = "Actuals", color = 'black') +
  geom_vline(xintercept = 2020.65,color="orange",linetype="dashed") +
  xlim(2017.7, 2024.66) + 
  theme_minimal() +
  ggtitle('Seasonal Additive ARIMA Model')

