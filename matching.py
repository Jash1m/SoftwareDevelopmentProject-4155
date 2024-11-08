def calculate_likeness_score(response1, response2):
    """
    Calculate the likeness score between two responses.
    The more answers match, the higher the score.
    """
    score = 0
    questions = [
        "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11"
    ]
    
    for question in questions:
        if getattr(response1, question) == getattr(response2, question):
            score += 1  # Increase score for each matching response
            
    return score

def find_best_match_for_each(responses):
    """
    For each response, find the best match with the highest likeness score.
    Returns a dictionary where the key is the response ID and the value is the best match.
    """
    best_matches = {}

    # Compare each response with every other response
    for i, response1 in enumerate(responses):
        best_match = None
        highest_score = -1  # Initialize with a low score

        for response2 in responses:
            if response1.id != response2.id:  # Don't compare the response with itself
                score = calculate_likeness_score(response1, response2)
                
                # Update the best match if the score is higher
                if score > highest_score:
                    highest_score = score
                    best_match = (response2.id, score)
        
        best_matches[response1.id] = best_match
    
    return best_matches
