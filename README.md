# Options_Sentiment
Read the sentiment regarding an equity through its OTM option's volumes and open interests


# Methodology
Uses yfinance to pull option chains. 
Calculates the call-to-put ratio for each option expiration date. 
Uses these ratios to calculate linear sentiment (linSentiment()) or exponential sentiment (expSentiment())
  
Linear Sentiment:  
Each ratio is weighted equally, regardless of how far in the future they are.  
  
Exponential Sentiment:  
Each ratio is weighted exponentially, the further the expiration date, the heavier the weighting. 
  
