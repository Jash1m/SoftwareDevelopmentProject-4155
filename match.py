from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas.schemas import db, Response, Student

# Database configuration
dbUser = "..."  # Update with your database user
dbPass = "..."  # Update with your database password
dbName = "..."  # Update with your database name
dbHost = "127.0.0.1"
dbPort = 3306

# Create a SQLAlchemy engine
engine = create_engine(f'mysql://{dbUser}:{dbPass}@{dbHost}:{dbPort}/{dbName}')
Session = sessionmaker(bind=engine)
session = Session()

def calculate_likeness(response1, response2):
    """Calculate the likeness value between two responses based on matching answers."""
    score = 0
    # Compare responses for all questions
    for question_num in range(1, 12):  # Assuming 11 questions
        answer1 = getattr(response1, f'q{question_num}')
        answer2 = getattr(response2, f'q{question_num}')
        if answer1 == answer2:
            score += 1  # Increment score for each matching answer
            print(f"Match found for Response ID {response1.id} and {response2.id} on question {question_num}: {answer1}")
    return score

def find_best_matches():
    """Find and print the best matches for each response."""
    all_responses = session.query(Response).all()
    print(f"Total responses fetched: {len(all_responses)}")  # Debug print for the number of responses
    matches = {}

    for response in all_responses:
        likeness_scores = []
        for other_response in all_responses:
            if response.id != other_response.id:  # Avoid comparing the same response
                likeness = calculate_likeness(response, other_response)
                likeness_scores.append((other_response.id, likeness))
                print(f"Calculated likeness between Response ID {response.id} and {other_response.id}: {likeness}")

        # Sort the matches by likeness score in descending order
        likeness_scores.sort(key=lambda x: x[1], reverse=True)

        # Store the best matches (for example, top 3)
        matches[response.id] = likeness_scores[:3]  # Keep top 3 matches

    # Print the matches
    for response_id, match_list in matches.items():
        print(f"Response ID {response_id} matches:")
        if not match_list:
            print("    No matches found.")
        for match_id, score in match_list:
            print(f"    - Response ID {match_id} with likeness score {score}")
        print()  # New line for better readability

if __name__ == "__main__":
    find_best_matches()
