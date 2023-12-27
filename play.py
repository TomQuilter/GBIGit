import itertools

# Initialize an empty set to store the unique coordinate combinations
unique_coordinate_combinations = set()

# Create a list of all possible single coordinates in a 5x5 grid, excluding (0, 0)
single_coordinates = [(i, j) for i in range(4) for j in range(3) if (i, j) != (0, 0)]
print("single_coordinates",single_coordinates)
print("Length",len(single_coordinates))
# Generate combinations of increasing length
for r in range(1, 11):  # This will generate combinations of lengths 1 to 5
    # itertools.combinations will create all **unique** combinations of the coordinates with length r
    for combination in itertools.combinations(single_coordinates, r):
        # Flatten the combination and add to the set
        flattened_combination = tuple(coord for pair in combination for coord in pair)
        unique_coordinate_combinations.add(flattened_combination)

# Convert the set to a list and sort it for display purposes
sorted_combinations = sorted(unique_coordinate_combinations, key=lambda x: (len(x), x))

# Now, sorted_combinations contains all unique combinations of coordinates without repeats and excluding (0, 0)
# Display some of the combinations
for combination in sorted_combinations:  # Print all combinations
    print(combination)

number_of_combinations = len(sorted_combinations)

# Display the count
print(f"The number of unique coordinate combinations excluding (0, 0) is: {number_of_combinations}")

