import sys
import multiprocessing
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.schemas import Response

# Function to calculate the likeness score between two responses
def calculate_likeness_score(response1, response2):
    score = 0
    questions = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11"]
    
    for question in questions:
        if getattr(response1, question) == getattr(response2, question):
            score += 1  # Increase score for each matching response
            
    return score

# Function to process and match a chunk of responses
def match_chunk(start_index, end_index, responses, return_dict, engine_url, process_id):
    # Print debug information to stderr
    print(f"Process {process_id} started. Processing responses from index {start_index} to {end_index}", file=sys.stderr)
    
    # Create a session using the engine URL passed from Flask
    engine = create_engine(engine_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    best_matches = {}
    for i in range(start_index, end_index):
        response1 = responses[i]
        best_match = None
        highest_score = -1

        for response2 in responses:
            if response1.id != response2.id:  # Skip self-comparison
                score = calculate_likeness_score(response1, response2)
                if score > highest_score:
                    highest_score = score
                    best_match = (response2.id, score)

        best_matches[response1.id] = best_match
    
    session.close()  # Close session once done
    return_dict.update(best_matches)  # Update the dictionary with the results

    # Print chunk processing results to stderr
    print(f"Process {process_id} completed. Best matches for chunk {start_index} to {end_index} added to return_dict.", file=sys.stderr)

# Function to find the best matches for all responses
def find_best_match_for_each(responses, engine_url):
    # Calculate the number of responses
    num_responses = len(responses)

    # Automatically scale the number of processes based on the number of responses
    if num_responses < 100:  # If there are fewer than 100 responses, use 1 process
        num_processes = 1
    elif num_responses < 500:  # If there are fewer than 500 responses, use 2 processes
        num_processes = 2
    elif num_responses < 1000:  # If there are fewer than 1000 responses, use 4 processes
        num_processes = 4
    else:  # If there are more than 1000 responses, use 8 processes (you can adjust this cap)
        num_processes = 8

    # Print scaling information to stderr
    print(f"Scaling to {num_processes} processes based on {num_responses} responses.", file=sys.stderr)
    
    # Define chunk size based on the number of processes
    chunk_size = num_responses // num_processes
    processes = []
    manager = multiprocessing.Manager()
    return_dict = manager.dict()

    # Divide the work into chunks for multiprocessing
    for i in range(num_processes):
        start_index = i * chunk_size
        end_index = (i + 1) * chunk_size if i != num_processes - 1 else num_responses
        process_id = i + 1  # Just a unique ID for each process in the print statements
        process = multiprocessing.Process(target=match_chunk, args=(start_index, end_index, responses, return_dict, engine_url, process_id))
        processes.append(process)
        process.start()

        # Print process start info to stderr
        print(f"Process {process_id} started for range {start_index} to {end_index}", file=sys.stderr)

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Print completion info to stderr
    print(f"All {num_processes} processes completed. Returning results.", file=sys.stderr)

    return dict(return_dict)  # Convert the manager dictionary to a regular dictionary

# Main script execution. This is needed since multiprocessing will not make the extra processes without it. It's also why we are running this as a subprocess, instead of in the main flask process. I wish it was easier.
if __name__ == '__main__':
    # Get the database URL passed from Flask
    engine_url = sys.argv[1]  # First argument is the DB URL

    # Create engine and session for fetching responses
    engine = create_engine(engine_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Fetch all responses from the database
    responses = session.query(Response).all()
    print(f"Fetched {len(responses)} responses from the database.", file=sys.stderr)

    # Find the best matches
    best_matches = find_best_match_for_each(responses, engine_url)

    # Save or return the matches (you can update the database, write to a file, etc.)
    if best_matches:
        for response_id, match in best_matches.items():
            print(f"Response {response_id} best match: {match}")  # Output to stdout
    else:
        print("No matches found", file=sys.stderr)  # If no matches are found, output to stderr

    session.close()  # Close session once done
    print("Script execution completed.", file=sys.stderr)
