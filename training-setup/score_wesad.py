import csv

# Function to adjust scores based on specified indices for adding or subtracting
def adjust_scores(scores, add_indices, subtract_indices):
    total_score = 0
    for i, score in enumerate(scores):
        if i in add_indices:
            total_score += 2 * score  # Double the score at these indices before adding
        elif i in subtract_indices:
            total_score -= score  # Subtract the score at these indices
    return total_score

# Function to calculate stress scores from a specified CSV file
def calculate_stress_scores(input_file):
    with open(input_file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')  # Read the file with semicolon as delimiter
        
        # Define indices for adjusting scores for different questions on each questionnaire  
        add_panas_indices = [1, 4, 6, 7, 8, 11, 13, 15, 18, 19, 20, 21, 23, 24, 25]  
        subtract_panas_indices = [0, 2, 3, 5, 9, 10, 12, 14, 16, 17, 22]  

        add_stai_indices = [1, 2, 4]
        subtract_stai_indices = [0, 3, 5]

        add_dim_indices = [1]
        subtract_dim_indices = [0]

        # Lists to hold scores for each section
        panas_scores = []
        stai_scores = []
        dim_scores = []

        # Read and parse the CSV rows
        for row in reader:
            if row[0].startswith('# PANAS'):
                scores = [int(score) if score else 0 for score in row[1:27]]  # Convert to integers, handle empty as zero
                panas_scores.append(scores)
            elif row[0].startswith('# STAI'):
                scores = [int(score) if score else 0 for score in row[1:7]]
                stai_scores.append(scores)
            elif row[0].startswith('# DIM'):
                scores = [int(score) if score else 0 for score in row[1:3]]
                dim_scores.append(scores)
        
        # Adjust scores for each test
        final_panas = [adjust_scores(scores, add_panas_indices, subtract_panas_indices) for scores in panas_scores]
        final_stai = [adjust_scores(scores, add_stai_indices, subtract_stai_indices) for scores in stai_scores]
        final_dim = [adjust_scores(scores, add_dim_indices, subtract_dim_indices) for scores in dim_scores]

        # Calculate raw and normalized scores
        raw_scores = []
        normalized_scores = []
        for i in range(0,5):
            raw_score = int(final_panas[i]) + int(final_stai[i]) + int(final_dim[i])
            raw_scores.append(raw_score)

            shifted_score = raw_score + 24  # Shift the range to be non-negative
            normalized_score = (shifted_score / 143) * 100  # Normalize to 0-100 scale
            normalized_scores.append(normalized_score)

        print("raw:", raw_scores)
        print("normalized:", normalized_scores)

# Main function to process files sequentially except for specified cases
def main():
    for i in range(1, 18):
        if i == 1 or i == 12:  # Skip files for subject 1 and 12 (they don't exist)
            continue
        file_name = f'http-and-webhook-server/ml-algorithm/training-setup/quest/S{i}_quest.csv'  # Generate file name
        print(f'Processing {file_name}...')
        calculate_stress_scores(file_name)
        print('')  # Print a newline for better readability between files

# To run main
if __name__ == "__main__":
    main()
