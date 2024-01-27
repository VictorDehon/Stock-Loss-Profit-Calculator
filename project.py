#The code will extract financial data
#User will then put in how much stock they bought and when
#Code will return how much money they made if sold now
#Stock price on day bought will always be the High

import yfinance as yf
import datetime as datetime
import warnings
import emoji

def main():
    Number_Of_Stocks_Bought = int(input("How Many Stocks Did You Buy? "))
    TotalMoney = 0

    for _ in range(Number_Of_Stocks_Bought):
        Stock_ID = input("What Stock Did You Buy (ShortCode)? ")
        Todays_Price, Day_Bought, Stock = Input(Stock_ID)
        
        # Prices function will return 0 if there's no financial data
        Price_On_Day_Bought = Prices(Stock_ID, Day_Bought)

        if Price_On_Day_Bought is not None:
            ProfitOrLoss = MoneyMade(Todays_Price, Price_On_Day_Bought, Stock)
            TotalMoney += ProfitOrLoss
        else:
            print(f"Skipping {Stock_ID} due to missing financial data.")

    print("Your Total Money Made is: $", round(TotalMoney))
    
    

def Input(Stock_ID):
    Day_Bought = input("When Did You Buy The Stock (Date in the form dd-mm-yy)? ")
    Stock = yf.Ticker(Stock_ID)
    Todays_Price = (Stock.info['currentPrice'])

    return Todays_Price, Day_Bought, Stock

def Prices(Stock_ID, Day_Bought):
    Start_Date = datetime.datetime.strptime(Day_Bought, "%d-%m-%y")
    End_Time = Start_Date + datetime.timedelta(days=1)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = yf.download(Stock_ID, start=Start_Date, end=End_Time, interval="1d", progress=False)

        if df.empty:
            raise ValueError("No price data found for the specified date range.")

        Price_On_Day_Bought = df.iloc[0, 1]  # High price On that Day
    except ValueError or IndexError:
        print ("There seems to be a problem accessing financial data for this day, apologies.")
        Price_On_Day_Bought=None

    return Price_On_Day_Bought

def MoneyMade(Todays_Price, Price_On_Day_Bought, Stock): #Amount of money made
    Price_Difference = Todays_Price - Price_On_Day_Bought
    
    Quantity_Stocks = float(input("How many shares did you buy? "))
    ProfitOrLoss = Price_Difference * Quantity_Stocks
    
    if ProfitOrLoss > 0:
        print("You Have Made: $",round(ProfitOrLoss),"On", (Stock.info["shortName"]), emoji.emojize(":beaming_face_with_smiling_eyes:"))
    if ProfitOrLoss == 0:
        print ("You have broke even!")
    if ProfitOrLoss < 0:
        print ("You have lost: $",round(abs(ProfitOrLoss)),"On", (Stock.info["shortName"]), emoji.emojize(":grimacing_face:"))
    return ProfitOrLoss


if __name__ == "__main__":
    main()
