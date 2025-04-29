import pandas as pd

# Load the dataset
df = pd.read_csv("listings.csv")

# Define the cleaning function
def clean_listings_data(df):
    cleaned_df = df.copy()
    
    # Drop completely empty column
    if 'neighbourhood_group' in cleaned_df.columns:
        cleaned_df = cleaned_df.drop(columns=['neighbourhood_group'])
    
    # Remove rows with missing 'price'
    cleaned_df = cleaned_df[~cleaned_df['price'].isna()]
    
    # Fill missing reviews_per_month with 0
    cleaned_df['reviews_per_month'] = cleaned_df['reviews_per_month'].fillna(0)
    
    # Convert 'last_review' to datetime
    cleaned_df['last_review'] = pd.to_datetime(cleaned_df['last_review'], errors='coerce')
    
    # Fill missing host_name with "Unknown"
    cleaned_df['host_name'] = cleaned_df['host_name'].fillna("Unknown")
    
    return cleaned_df

# Apply the cleaning function
df_cleaned = clean_listings_data(df)

# Save cleaned data to CSV
df_cleaned.to_csv("cleaned_listings.csv", index=False)

# Check the cleaned dataset info
print(df_cleaned.info())
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_eda(df):
    # Convert date column
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')

    print("----- BASIC INFO -----")
    print(df.info())
    print("\n----- MISSING VALUES -----")
    print(df.isnull().sum())
    print("\n----- SUMMARY STATISTICS -----")
    print(df.describe(include='all'))

    print("\n----- VALUE COUNTS (Room Type) -----")
    print(df['room_type'].value_counts())

    print("\n----- VALUE COUNTS (Neighbourhood - Top 10) -----")
    print(df['neighbourhood'].value_counts().head(10))
run_eda(df_cleaned)


# Ensure 'last_review' is datetime
df_cleaned['last_review'] = pd.to_datetime(df_cleaned['last_review'], errors='coerce')

# 1. Boxplot - Price by Room Type
def boxplot_room_price(df):
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x='room_type', y='price')
    plt.title("Boxplot: Price by Room Type")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def lineplot_total_reviews_by_month(df):
    # Ensure last_review is datetime
    df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')

    # Create 'review_month' column
    df['review_month'] = df['last_review'].dt.to_period('M')

    # Group by month and sum reviews
    monthly_reviews = df.groupby('review_month')['number_of_reviews'].sum().reset_index()

    # Convert Period to string for plotting
    monthly_reviews['review_month'] = monthly_reviews['review_month'].astype(str)

    # Plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly_reviews, x='review_month', y='number_of_reviews')
    plt.title("Total Reviews per Month")
    plt.xlabel("Month")
    plt.ylabel("Total Reviews")

    # Reduce x-axis labels: show every 3rd month
    xticks = monthly_reviews['review_month'][::3]
    plt.xticks(ticks=range(0, len(monthly_reviews), 3), labels=xticks, rotation=45)

    plt.tight_layout()
    plt.show()



# 3. Scatterplot - Price vs Reviews
def scatterplot_price_reviews(df):
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x='number_of_reviews', y='price', hue='room_type')
    plt.title("Scatterplot: Price vs Number of Reviews")
    plt.tight_layout()
    plt.show()

# 4. Histogram - Availability Distribution
def histogram_availability(df):
    plt.figure(figsize=(8, 5))
    sns.histplot(df['availability_365'], bins=30, kde=False)
    plt.title("Histogram: Availability Distribution")
    plt.xlabel("Availability (days/year)")
    plt.tight_layout()
    plt.show()

# 5. Barplot - Avg Price by Neighbourhood (Top 10)
def barplot_avg_price_by_neighbourhood(df):
    top_neigh = df['neighbourhood'].value_counts().head(10).index
    avg_price = df[df['neighbourhood'].isin(top_neigh)].groupby('neighbourhood')['price'].mean().sort_values()

    plt.figure(figsize=(10, 5))
    sns.barplot(x=avg_price.values, y=avg_price.index)
    plt.title("Barplot: Average Price by Top 10 Neighbourhoods")
    plt.xlabel("Average Price")
    plt.tight_layout()
    plt.show()

# 6. Pieplot - Room Type Distribution
def pieplot_room_type(df):
    room_counts = df['room_type'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(room_counts, labels=room_counts.index, autopct='%1.1f%%', startangle=140)
    plt.title("Pieplot: Room Type Distribution")
    plt.tight_layout()
    plt.show()

# 7. Heatmap - Correlation Matrix
def heatmap_correlations(df):
    corr = df[['price', 'number_of_reviews', 'reviews_per_month', 'availability_365']].corr()
    plt.figure(figsize=(6, 5))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Heatmap: Feature Correlations")
    plt.tight_layout()
    plt.show()

# Run all visualizations
run_eda(df_cleaned)
boxplot_room_price(df_cleaned)
lineplot_total_reviews_by_month(df_cleaned)
scatterplot_price_reviews(df_cleaned)
histogram_availability(df_cleaned)
barplot_avg_price_by_neighbourhood(df_cleaned)
pieplot_room_type(df_cleaned)
heatmap_correlations(df_cleaned)

