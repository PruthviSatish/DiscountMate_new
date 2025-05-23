# -*- coding: utf-8 -*-
"""Aldi Analysis 1 .ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z1m6M3-GV4GV_mNnNG0QnzKGKDkOaIaS
"""

from google.colab import files
import re
import pandas as pd

uploaded = files.upload()
# Replace 'filename.txt' with the actual name of your file
xodo_result = list(uploaded.keys())[0]  # Automatically takes the uploaded filename
with open(xodo_result, 'r') as file:
    content = file.readlines()
    print(content)

# Initialize lists to store extracted data
item = []
quantity = []
price = []

# Adjusted regex pattern to match item, quantity, and price
pattern = r"([A-Za-z\s']+)\s(\d{1,4}[a-zA-Z]+)?\s?\$(\d{1,2}\.\d{1,2})"

# Process each line in the content
for line in content:
    match = re.search(pattern, line.strip())
    if match:
        item.append(match.group(1).strip())  # Item name
        quantity.append(match.group(2).strip() if match.group(2) else None)
        price.append((match.group(3)))

# Create a DataFrame to display as columns
df = pd.DataFrame({
    'item': item,
    'quantity': quantity,
    'price': price
})

# Display the DataFrame
df

# Remove leading single letters in the 'item' column
df['item'] = df['item'].apply(lambda x: re.sub(r'^[A-Za-z]\s', '', x) if isinstance(x, str) else x)

# Remove rows where 'item' is a single word
df = df[~df['item'].str.match(r'^\w+$', na=False)]

# Reset the index for a clean DataFrame
df = df.reset_index(drop=True)

# Display the cleaned DataFrame
print(df)

# Define categories and keywords
categories = {
    'Fruit & Veg': [
        'Bananas', 'Apples', 'Oranges', 'Grapes', 'Carrots', 'Potatoes', 'Sweet Potatoes',
        'Tomatoes', 'Cucumber', 'Broccoli', 'Cauliflower', 'Spinach', 'Lettuce', 'Peppers',
        'Zucchini', 'Mushrooms', 'Onions', 'Garlic', 'Strawberries', 'Blueberries', 'Avocado'
    ],
    'Bakery': [
        'Bread', 'Wholemeal Bread', 'Croissant', 'Cake', 'Chocolate Cake', 'Muffin', 'Bagel',
        'Donut', 'Baguette', 'Roll', 'Flatbread', 'Pita', 'Brioche', 'Shortbread',
        'Sourdough', 'Focaccia', 'Ciabatta', 'Pastry'
    ],
    'Poultry, Meat & Seafood': [
        'Chicken', 'Chicken Breast', 'Chicken Thigh', 'Beef', 'Steak', 'Pork', 'Lamb',
        'Turkey', 'Bacon', 'Ham', 'Sausage', 'Salami', 'Duck', 'Fish', 'Salmon', 'Tuna',
        'Shrimp', 'Prawns', 'Crab', 'Lobster', 'Cod', 'Haddock', 'Mussels'
    ],
    'Deli & Chilled Meals': [
        'Ham', 'Salami', 'Prosciutto', 'Pasta Salad', 'Quiche', 'Soup', 'Coleslaw',
        'Sandwich', 'Wrap', 'Sausage Roll', 'Ready Meals', 'Lasagna', 'Curry', 'Pizza',
        'Deli Chicken', 'Meat Platter', 'Cheese Platter'
    ],
    'Dairy, Eggs & Fridge': [
        'Milk', 'Almond Milk', 'Oat Milk', 'Soy Milk', 'Cheese', 'Cheddar Cheese', 'Mozzarella',
        'Butter', 'Eggs', 'Free-Range Eggs', 'Greek Yogurt', 'Yogurt', 'Cream', 'Whipping Cream',
        'Sour Cream', 'Cream Cheese', 'Custard'
    ],
    'Lunch Box': [
        'Juice Box', 'Snack Bar', 'Muesli Bar', 'Granola Bar', 'Crackers', 'Rice Crackers',
        'Fruit Cup', 'Cheese Stick', 'String Cheese', 'Sandwich', 'Mini Sandwich', 'Wrap',
        'Chips', 'Popcorn', 'Dried Fruit', 'Nuts'
    ],
    'Pantry': [
        'Rice', 'Brown Rice', 'Basmati Rice', 'Pasta', 'Spaghetti', 'Macaroni', 'Flour',
        'Sugar', 'Brown Sugar', 'Canned Food', 'Canned Tomatoes', 'Canned Beans',
        'Spices', 'Salt', 'Pepper', 'Paprika', 'Curry Powder', 'Oil', 'Olive Oil', 'Vegetable Oil',
        'Vinegar', 'Honey', 'Peanut Butter', 'Jam', 'Cereal', 'Oats', 'Granola'
    ],
    'International Foods': [
        'Soy Sauce', 'Curry Paste', 'Tortilla', 'Noodles', 'Rice Noodles', 'Soba Noodles',
        'Sushi', 'Wasabi', 'Miso', 'Tikka Masala', 'Hoisin Sauce', 'Teriyaki Sauce',
        'Pita Bread', 'Falafel', 'Hummus', 'Pad Thai', 'Kimchi', 'Gyoza', 'Spring Roll'
    ],
    'Snacks & Confectionery': [
        'Chips', 'Potato Chips', 'Chocolate', 'Dark Chocolate', 'Milk Chocolate', 'Candy',
        'Biscuits', 'Cookies', 'Lollies', 'Marshmallows', 'Popcorn', 'Nuts', 'Trail Mix',
        'Pretzels', 'Chewing Gum', 'Mints'
    ],
    'Freezer': [
        'Frozen Pizza', 'Frozen Vegetables', 'Frozen Chips', 'Frozen Fish', 'Frozen Peas',
        'Frozen Corn', 'Ice Cream', 'Sorbet', 'Frozen Yogurt', 'Frozen Chicken',
        'Frozen Sausages', 'Frozen Meatballs', 'Frozen Prawns', 'Frozen Spring Rolls',
        'Frozen Dumplings', 'Frozen Fruit', 'Frozen Berries'
    ]
}


# Function to classify items
def classify_item(item, category_dict):
    for category, keywords in category_dict.items():
        if any(keyword.lower() in item.lower() for keyword in keywords):
            return category
    return 'Miscellaneous'  # Default for unmatched items

# Apply the classification function
df['category'] = df['item'].apply(lambda x: classify_item(x, categories))

# Display the categorized DataFrame
print(df)

df.to_csv('output.csv', index=False)