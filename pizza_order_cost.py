# Get user input
pizza_size = input("Enter pizza size (small or large): ").lower()
toppings = int(input("Enter number of toppings: "))
distance = int(input("Enter delivery distance in miles: "))

# Determine base pizza cost
if pizza_size == "small":
    base_cost = 8
elif pizza_size == "large":
    base_cost = 12
else:
    print("Invalid pizza size!")
    exit()

# Calculate toppings cost
toppings_cost = toppings * 1

# Calculate delivery fee
if distance == 0:
    delivery_fee = 0
elif distance <= 5:
    delivery_fee = 2
else:
    delivery_fee = 2 + (distance - 5) * 1

# Calculate total cost
total_cost = base_cost + toppings_cost + delivery_fee

# Display result
print(f"Total cost of your pizza order is: ${total_cost}")