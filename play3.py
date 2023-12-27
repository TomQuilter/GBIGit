import itertools
import math
#import tensorflow as tf

prob = math.exp(math.log(0.01/0.8) / 300)

def add_commas_to_first_element_of_tuple(input_tuple):
    """
    Function to add commas between the characters of the first element of a tuple.

    :param input_tuple: Tuple with the first element as a string and any other element.
    :return: New tuple with commas added to the first element.
    """
    if not input_tuple or not isinstance(input_tuple[0], str):
        return input_tuple

    # Add commas between characters of the first element
    modified_first_element = ','.join(input_tuple[0])

    # Create a new tuple with the modified first element and the rest of the original tuple elements
    return (modified_first_element,) + input_tuple[1:]



# Example usage with different tuples
example_tuples = [
    ('4567', 'other elements', 42),
    ('hello', [1, 2, 3], {'key': 'value'}),
    ('abcd',)
]

modified_tuples = [add_commas_to_first_element_of_tuple(tup) for tup in example_tuples]

for original, modified in zip(example_tuples, modified_tuples):
    print(f"Original: {original}, Modified: {modified}")


# Example usage
coords = [(0, 2), (1, 2), (1, 3)]
closest_coordinate = closest_to_origin(coords)
print("Closest coordinate to (0, 0):", closest_coordinate)



print("prob = " , prob)

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

