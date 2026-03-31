print("🔥 START")

import pandas as pd

print("📂 Step 1: Loading META file...")

df_meta = pd.read_excel(
    r"C:\Users\user\recommender_project\backend\clean_meta_with_item.xlsx"
)

print("✅ META loaded")
print("Meta rows:", len(df_meta))


print("📂 Step 2: Loading REVIEWS file...")

df_reviews = pd.read_csv(
    r"C:\Users\user\recommender_project\backend\reviews_products_merged.csv"
)

print("✅ REVIEWS loaded")
print("Reviews rows:", len(df_reviews))


print("📊 Step 3: Columns check")
print("META columns:", df_meta.columns.tolist())
print("REVIEWS columns:", df_reviews.columns.tolist())


print("🔗 Step 4: Merging...")

# clean column names (IMPORTANT)
df_meta.columns = df_meta.columns.str.strip()
df_reviews.columns = df_reviews.columns.str.strip()

df = pd.merge(df_meta, df_reviews, on="parent_asin", how="left")

df.to_csv(
    r"C:\Users\user\recommender_project\backend\merged_data.csv",
    index=False
)

print("💾 Merged data saved")

print("✅ Merge done")
print("Merged rows:", len(df))


print("🧪 Sample row:")
print(df.head(1))

print("🎉 SCRIPT FINISHED")