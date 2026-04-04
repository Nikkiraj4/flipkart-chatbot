import pandas as pd

#  sample Flipkart-style data
data = {
    "product_id": [101, 102, 103, 104, 105, 106],
    "product_name": [
        "Apple iPhone 15 (Blue, 128 GB)",
        "SAMSUNG Galaxy S24 Ultra (Titanium Gray)",
        "Apple MacBook AIR M2 (Space Grey, 8GB RAM)",
        "HP Victus Gaming Laptop (Ryzen 5, RTX 3050)",
        "Sony WH-1000XM5 Wireless Headphones",
        "boAt Rockerz 450 Bluetooth Headset"
    ],
    "category": ["Mobile", "Mobile", "Laptop", "Laptop", "Headphones", "Headphones"],
    "price": [65999, 129999, 84900, 58990, 29990, 1499],
    "description": [
        "Advanced camera system, A16 Bionic chip, and long battery life.",
        "AI-powered features, S-Pen included, and 200MP camera.",
        "Supercharged by M2, silent fanless design, and liquid retina display.",
        "Powerful gaming performance with high refresh rate screen.",
        "Industry leading noise cancelling with dual processor V1.",
        "Budget friendly comfortable headphones with 15 hours playback."
    ]
}

# Convert to a DataFrame
df = pd.DataFrame(data)

# Save it as a CSV file
df.to_csv("flipkart_products.csv", index=False)

print("✅ SUCCESS: 'flipkart_products.csv' has been created in your folder!")