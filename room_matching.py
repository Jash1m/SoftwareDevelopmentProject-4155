import itertools

def calculate_group_compatibility(group, best_matches):
    """
    Calculate the average likeness score for a group based on the likeness scores between students.
    """
    total_compatibility = 0
    num_pairs = 0
    
    # Iterate over all pairs in the group to calculate the compatibility
    for i in range(len(group)):
        for j in range(i + 1, len(group)):
            student1 = group[i]
            student2 = group[j]
            
            # Check if there's a match (non-zero likeness score)
            if student1 in best_matches and best_matches[student1][0] == student2:
                total_compatibility += best_matches[student1][1]
                num_pairs += 1
            elif student2 in best_matches and best_matches[student2][0] == student1:
                total_compatibility += best_matches[student2][1]
                num_pairs += 1
    
    # If there are no pairs, return 0 as the average compatibility score
    if num_pairs == 0:
        return 0
    return total_compatibility / num_pairs


def assign_rooms(best_matches, total_students):
    """
    Assign students to rooms based on their best match, and calculate the average compatibility
    score for each room. Aim to split students into 2, 3, and 4-person rooms while maximizing compatibility.
    """
    students = list(best_matches.keys())
    
    # Calculate number of rooms for each type based on an even 1/3 split
    num_rooms_of_4 = total_students // 3 // 4
    num_rooms_of_3 = total_students // 3 // 3
    num_rooms_of_2 = total_students // 3 // 2
    
    total_assigned_students = num_rooms_of_4 * 4 + num_rooms_of_3 * 3 + num_rooms_of_2 * 2
    remaining_students = total_students - total_assigned_students

    if remaining_students > 0:
        num_rooms_of_3 += remaining_students // 3
        num_rooms_of_2 += (remaining_students % 3) // 2

    print(f"Total Students: {total_students}")
    print(f"Rooms of 4: {num_rooms_of_4}")
    print(f"Rooms of 3: {num_rooms_of_3}")
    print(f"Rooms of 2: {num_rooms_of_2}")
    
    students_per_room = [4] * num_rooms_of_4 + [3] * num_rooms_of_3 + [2] * num_rooms_of_2
    
    print("Room Assignments:")
    
    # Start by randomly assigning students, and then optimize the room composition
    assigned_rooms = []
    remaining_students_set = set(students)
    
    for room_size in students_per_room:
        best_room = None
        best_room_compatibility = -1  # We want to maximize this
        
        # Try all combinations of students to form a room of the current size
        for group in itertools.combinations(remaining_students_set, room_size):
            group_compatibility = calculate_group_compatibility(group, best_matches)
            
            if group_compatibility > best_room_compatibility:
                best_room_compatibility = group_compatibility
                best_room = group
        
        # Assign the best room and remove those students from the remaining pool
        assigned_rooms.append(list(best_room))
        remaining_students_set -= set(best_room)
        
        # Output the average compatibility for this room
        print(f"Room {len(assigned_rooms)}: {best_room}")
        print(f"Average Compatibility: {best_room_compatibility:.2f}")
    
    # If there are any remaining students, place them in their own room
    if remaining_students_set:
        remaining_room = list(remaining_students_set)
        assigned_rooms.append(remaining_room)
        remaining_room_compatibility = calculate_group_compatibility(remaining_room, best_matches)
        
        print(f"Room {len(assigned_rooms)} (Remaining): {remaining_room}")
        print(f"Average Compatibility: {remaining_room_compatibility:.2f}")
    
    print("All students have been assigned to rooms.")
