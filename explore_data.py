import pandas as pd
df = pd.read_csv("typhoon_data_csv.csv")
print(df.head())

# remove other years
df = df[(df['year'] >= 2020) & (df['year'] <= 2024)]
print(df['year'].unique())

# check region names
df['region'].unique()
print(df['region'].unique())

# check province names
df['province'].unique()
print(df['province'].unique())

# find provinces with multiple regions
province_region_check = df.groupby('province')['region'].nunique()
problem_provinces = province_region_check[province_region_check > 1]

#show mismatched rows
mismatches = df[df['province'].isin(problem_provinces.index)] \
    .sort_values(['province', 'year'])

pd.set_option('display.max_rows', None)
print(mismatches)

# export first cleaned dataset
df.to_csv("cleaned_step1.csv", index=False)

# cleaning (Maguindanao del Norte and Maguindanao del Sur combined into Maguindanao)
df['province'] = df['province'].replace({
    "Maguindanao del Norte": "Maguindanao",
    "Maguindanao del Sur": "Maguindanao"
})
print(df['province'].unique())

# export second cleaned dataset
df.to_csv("cleaned_step2.csv", index=False)

# assign the most common region for each province
df['region'] = df.groupby('province')['region'].transform(lambda x: x.mode()[0])

# check (problem_provinces should now be empty)
province_region_check = df.groupby('province')['region'].nunique()
problem_provinces = province_region_check[province_region_check > 1]
print(problem_provinces)

# export third cleaned dataset
df.to_csv("cleaned_step3.csv", index=False)