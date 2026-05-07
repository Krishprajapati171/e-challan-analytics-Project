

# =========================================================
# 📊 E-CHALLAN DATA ANALYSIS PROJECT (PANDAS)
# =========================================================

# =========================================================
# 1. IMPORTING LIBRARIES
# =========================================================
import pandas as pd
import matplotlib.pyplot as pt
import seaborn as sns
from flask import Flask,render_template
import os

app=Flask(__name__)
# =========================================================
# 2. DATA LOADING & BASIC INSPECTION
# =========================================================

df=pd.read_csv('echallan_daily_data.csv')
print(df.head(5))
print('----------------------------------------------------')
print(df.columns)
print('----------------------------------------------------')
print(df.index)
print('----------------------------------------------------')
print(df.size)
print('----------------------------------------------------')
print(df.info())
print('----------------------------------------------------')
print(df.describe())
print('----------------------------------------------------')


# =========================================================
# 3. DATA CLEANING & PREPARATION
# =========================================================
df['date']=pd.to_datetime(df['date'])
df.set_index('date',inplace=True)
print(df.index.dtype)

print('----------------------------------------------------')
print(df.index)
print('----------------------------------------------------')
df=df.rename(columns={
    'totalChallan':'Total_Challan',
    'disposedChallan':'Disposed_Challan',
    'pendingChallan':'Pending_Challan',
    'pendingAmount':'Pending_Amount',
    'disposedAmount':'Disposed_Amount',
    'totalAmount':'Total_Amount',
    'pendingCourt':'Pending_Court',
    'disposedCourt':'Disposed_Court',
    'total_Court':'Total_Court'
})
print(df)
print('----------------------------------------------------')
print(df.columns)
print('----------------------------------------------------')

# =========================================================
# 4. BASIC FEATURE CHECK
# =========================================================

print(df['Total_Challan'])
print('----------------------------------------------------')

# =========================================================
# 5. TIME SERIES ANALYSIS - TOTAL CHALLAN
# =========================================================

monthly=df['Total_Challan'].resample('ME').sum()
print(monthly)
print('----------------------------------------------------')
monthy_highest_Challan_value=monthly.max()
monthy_highest_Challan_idmax=monthly.idxmax()
print(monthy_highest_Challan_idmax,monthy_highest_Challan_value)
print('----------------------------------------------------')
start=monthly.iloc[0]
end=monthly.iloc[-1]
print(start)
print(end)
if(end>start):
    print('Trend is increasing....')
else:
    print('Trend is decresing....')
print('----------------------------------------------------')
yearly=df['Total_Challan'].resample('YE').sum()
print(yearly)
print('----------------------------------------------------')
print(yearly.idxmax(),yearly.max())
print('----------------------------------------------------')
start_1=yearly.iloc[0]
end_1=yearly.iloc[-1]
print(start_1)
print(end_1)
if(end_1>start_1):
    print('Trend is increasing....')
else:
    print('Trend is decresing....')
print('----------------------------------------------------')
rolling=df['Total_Challan'].rolling(7).mean()
rolled=rolling.dropna()
print('----------------------------------------------------')
start_2=rolled.iloc[0]
end_2=rolled.iloc[-1]
if(end_2>start_2):
    print('It is increasing')
else:
    print('It is decresing')
print('----------------------------------------------------')
month_pattern=df.groupby(df.index.month_name())['Total_Challan'].sum()
print(month_pattern)


# =========================================================
# 6. SEASONALITY ANALYSIS (MONTH-WISE PATTERN)
# =========================================================

print('----------------------------------------------------')
month_pattern=month_pattern.reindex(['January','February','March','April','May','June','July','August','September','October','November','December'])
print(month_pattern)
print('----------------------------------------------------')
month_highest=month_pattern.idxmax(),month_pattern.max()
print(month_highest)
print('----------------------------------------------------')
month_low=month_pattern.idxmin(),month_pattern.min()
print(month_low)
print('----------------------------------------------------')
top_5_month=month_pattern.sort_values(ascending=False).head(5)
print(top_5_month)

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

# =========================================================
# 7. PENDING vs DISPOSED ANALYSIS
# =========================================================

Pending_Challan_monthly=df['Pending_Challan'].resample('ME').sum()
print(Pending_Challan_monthly)
print('----------------------------------------------------')
Disposed_Challan_monthly=df['Disposed_Challan'].resample('ME').sum()
print(Disposed_Challan_monthly)
print('----------------------------------------------------')
comparison=pd.DataFrame({
    'Pending':Pending_Challan_monthly,
    'Disposed':Disposed_Challan_monthly
})
print(comparison)

if(comparison['Pending'].mean()>comparison['Disposed'].mean()):
    print('Backlog is increasing..')
else:
    print('System is working Fine..')
print('----------------------------------------------------')
start_3=Pending_Challan_monthly.iloc[0]
end_3=Pending_Challan_monthly.iloc[-1]

if(end_3>start_3):
    print('Pending is increasing...')
else:
    print('Pending is decresing....')
print('----------------------------------------------------')
start_4=Disposed_Challan_monthly.iloc[0]
end_4=Disposed_Challan_monthly.iloc[-1]

if(end_4>start_4):
    print('Disposed is increasing....')
else:
    print('Disposed is decresing...')
print('----------------------------------------------------')
comparison['Gap']=comparison['Pending']-comparison['Disposed']
print(comparison)
print('----------------------------------------------------')
start_5=comparison['Gap'].iloc[0]
end_5=comparison['Gap'].iloc[-1]
if(end_5 > start_5):
    print('Gap is increasing and Backlog growing....')
else:
    print('Gap is decresing and system is working fine...')

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')



# =========================================================
# 8. REVENUE ANALYSIS
# =========================================================


revenue_monthly=df['Total_Amount'].resample('ME').sum()
print(revenue_monthly)
print('----------------------------------------------------')
print(revenue_monthly.idxmax(),revenue_monthly.max())
print('----------------------------------------------------')
start_6=revenue_monthly.iloc[0]
end_6=revenue_monthly.iloc[-1]

if(end_6>start_6):
    print('Revenue is incresing....')
else:
    print('Revenue is decresing...')
print('----------------------------------------------------')

monthly_Challan=df['Total_Challan'].resample('ME').sum()
revenue_monthly=df['Total_Amount'].resample('ME').sum()

compare_ev=pd.DataFrame({
    'Challan':monthly_Challan,
    'Revenue':revenue_monthly
})

print(compare_ev)
print('----------------------------------------------------')


# =========================================================
# 9. EFFICIENCY ANALYSIS
# =========================================================

df['Efficiency']=df['Disposed_Challan']/df['Total_Challan']
print(df['Efficiency'])
print('----------------------------------------------------')
monthly_Efficiency=df['Efficiency'].resample('ME').mean()
print(monthly_Efficiency)
print('----------------------------------------------------')

start_7=monthly_Efficiency.iloc[0]
end_7=monthly_Efficiency.iloc[-1]

if(end_7>start_7):
    print('Efficiency improving ')
else:
    print('Efficiency declining')

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')


# =========================================================
# 10. COURT CASE ANALYSIS
# =========================================================

Pending_Court_monthly=df['Pending_Court'].resample('ME').sum()
print(Pending_Court_monthly)
print('----------------------------------------------------')
Disposed_Court_monthly=df['Disposed_Court'].resample('ME').sum()
print(Disposed_Court_monthly)
print('----------------------------------------------------')

court_compare=pd.DataFrame({
    'Pending_Court':Pending_Court_monthly,
    'Disposed_Court':Disposed_Court_monthly
})
print(court_compare)
print('----------------------------------------------------')

start_8=Pending_Court_monthly.iloc[0]
end_8=Pending_Court_monthly.iloc[-1]

if(end_8>start_8):
    print('Pending Court Cases are increases')
else:
    print('Pending Court Cases are descresing')
print('----------------------------------------------------')

start_9=Disposed_Court_monthly.iloc[0]
end_9=Disposed_Court_monthly.iloc[-1]

if(end_9 > start_9):
    print("Disposed Court Cases are increases")
else:
    print('Disposed Court are decreases')
print('----------------------------------------------------')
Gap_Court=court_compare['Pending_Court']-court_compare['Disposed_Court']
print(Gap_Court)

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

# =========================================================
# 11. VISUALIZATION SECTION
# =========================================================

monthly.plot()
pt.title('Monthly Traffic Challan Trend')
pt.xlabel('Years')
pt.ylabel('Number of Challans')
pt.grid()
pt.savefig('static/charts/monthly_trend.png')
pt.close()
print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

compare_ev.plot()
pt.title('Revenue Vs Challan Trend')
pt.xlabel('Years')
pt.ylabel('Values')
pt.grid()
pt.savefig('static/charts/revenue_vs_challan.png')
pt.close()
print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

monthly_Efficiency.plot()
pt.title('Efficiency Over Time')
pt.xlabel('Years')
pt.ylabel('Efficiency (0 to 1)')
pt.grid()
pt.savefig('static/charts/efficiency.png')
pt.close()

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

comparison[['Pending','Disposed']].plot()
pt.title('Pending Vs Disposed Challan')
pt.xlabel('Year')
pt.ylabel('Numbers of Challan')
pt.grid()
pt.savefig('static/charts/pending_vs_disposed.png')
pt.close()

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

comparison['Gap'].plot()
pt.title('Gap between Pending Vs Disposed')
pt.xlabel('Years')
pt.ylabel('Values')
pt.grid()
pt.savefig('static/charts/gap_analysis.png')
pt.close()

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')

month_pattern.plot(kind='bar')
pt.title('Monthly Season of Challan')
pt.xlabel('Month')
pt.ylabel('Total Challan')
pt.grid()
pt.savefig('static/charts/seasonality.png')
pt.close()

print('----------------------------------------------------')
print('----------------------------------------------------')
print('----------------------------------------------------')


# =========================================================
# 12. GROWTH ANALYSIS
# =========================================================
monthly_growth_pct_Challan=((monthly.iloc[-1]-monthly.iloc[0])/monthly.iloc[0])*100
print("Monthly Growth Rate:", monthly_growth_pct_Challan, "%")

print('----------------------------------------------------')

yearly_growth_pct_Challan=((yearly.iloc[-1]-yearly.iloc[0])/yearly.iloc[0])*100
print("Yearly Growth Rate:", yearly_growth_pct_Challan, "%")

print('----------------------------------------------------')

revenue_growth_pct_Challan=((revenue_monthly.iloc[-1]-revenue_monthly.iloc[0])/revenue_monthly.iloc[0])*100
print("Revenue Growth Rate:", revenue_growth_pct_Challan, "%")

print('----------------------------------------------------')



# =========================================================
# 13. CORRELATION ANALYSIS
# =========================================================

correlation_betweeen_Challan_and_Amount=df['Total_Challan'].corr(df['Total_Amount'])
print('correlation_betweeen_Challan_and_Amount::',correlation_betweeen_Challan_and_Amount)
print('----------------------------------------------------')
correlation_betweeen_Pending_Challan_and_Disposed_Challan=df['Pending_Challan'].corr(df['Disposed_Challan'])
print('correlation_betweeen_Pending_Challan_and_Disposed_Challan::',correlation_betweeen_Pending_Challan_and_Disposed_Challan)
print('----------------------------------------------------')
correlation_betweeen_Pending_Court_and_Disposed_Court=df['Pending_Court'].corr(df['Disposed_Court'])
print('correlation_betweeen_Pending_Court_and_Disposed_Court::',correlation_betweeen_Pending_Court_and_Disposed_Court)
print('----------------------------------------------------')


corr = df[['Total_Challan',
           'Total_Amount',
           'Pending_Challan',
           'Disposed_Challan',
           'Pending_Court',
           'Disposed_Court']].corr()



pt.figure(figsize=(10,6))
sns.heatmap(corr, annot=True, cmap='coolwarm', linewidths=0.5)
pt.title("Correlation Heatmap - E-Challan System Analysis")
pt.savefig('static/charts/heatmap.png')
pt.close()

print('----------------------------------------------------')

pt.figure(figsize=(6,4))
sns.scatterplot(x=df['Total_Challan'],y=df['Total_Amount'])
pt.grid()
pt.title('Total Challan Vs Total Revenue')
pt.savefig('static/charts/challan_vs_revenue.png')
pt.close()

print('----------------------------------------------------')

pt.figure(figsize=(6,4))
sns.scatterplot(x=df['Pending_Challan'],y=df['Disposed_Challan'])
pt.grid()
pt.title('Pending Challan Vs Total Amount')
pt.savefig('static/charts/pending_vs_disposed_scatter.png')
pt.close()

print('----------------------------------------------------')

pt.figure(figsize=(6,4))
sns.scatterplot(x=df['Efficiency'],y=df['Pending_Challan'])
pt.grid()
pt.title('Efficiency Vs Pending_Challan')
pt.savefig('static/charts/efficiency_vs_pending.png')
pt.close()

print('----------------------------------------------------')



# -----------------------------
# ROUTE
# -----------------------------
@app.route("/")
def dashboard():

    # ---------------- KPIs ----------------
    total_challan = df['Total_Challan'].sum()
    total_revenue = df['Total_Amount'].sum()
    pending = df['Pending_Court'].sum()
    disposed = df['Disposed_Court'].sum()

    # ---------------- Time Series ----------------
    monthly = df['Total_Challan'].resample('ME').sum()
    revenue = df['Total_Amount'].resample('ME').sum()

    # ---------------- Insights ----------------
    highest_month = monthly.idxmax().strftime("%Y-%m")
    lowest_month = monthly.idxmin().strftime("%Y-%m")

    growth = round(((monthly.iloc[-1] - monthly.iloc[0]) / monthly.iloc[0]) * 100, 2)

    efficiency = round((disposed / total_challan) * 100, 2)

    # ---------------- FORMAT NUMBERS (IMPORTANT) ----------------
    def fmt(x):
        return f"{int(x):,}"   # adds comma formatting

    # ---------------- TABLE ----------------
    summary = pd.DataFrame({
        "Month": monthly.index.strftime("%Y-%m"),
        "Challan": monthly.values,
        "Revenue": revenue.values
    })

    # format table values too
    summary["Challan"] = summary["Challan"].apply(lambda x: f"{int(x):,}")
    summary["Revenue"] = summary["Revenue"].apply(lambda x: f"{int(x):,}")

    total_challan = int(total_challan)
    total_revenue = int(total_revenue)
    pending = int(pending)
    disposed = int(disposed)

    # ---------------- RENDER ----------------
    return render_template(
        "index.html",

        # KPIs (formatted)
        total_challan=fmt(total_challan),
        total_revenue=fmt(total_revenue),
        pending=fmt(pending),
        disposed=fmt(disposed),

        # Insights
        highest_month=highest_month,
        lowest_month=lowest_month,
        growth=growth,
        efficiency=efficiency,

        # Table
        summary_table=summary.to_dict(orient="records"),

        #graphs
        challan_vs_revenue_chart="charts/challan_vs_revenue.png",
        efficiency_chart="charts/efficiency.png",
        efficiency_vs_pending="charts/efficiency_vs_pending.png",
        gap_analysis_chart="charts/gap_analysis.png",
        heatmap_chart="charts/heatmap.png",
        monthly_chart="charts/monthly_trend.png",
        pending_vs_disposed_challan_chart="charts/pending_vs_disposed.png",
        pending_vs_disposed_scatter_chart="charts/pending_vs_disposed_scatter.png",
        revenue_vs_challan_chart="charts/revenue_vs_challan.png",
        seasonality_chart="charts/seasonality.png"
    )
if __name__ == "__main__":
    app.run(debug=True)