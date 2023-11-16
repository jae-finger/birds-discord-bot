def is_member_greeted(member_id):
    """
    Function to check if a member's ID is in the file
    """
    with open('data/greeted_members.txt', 'r') as file:
        greeted_members = file.read().splitlines()
    return str(member_id) in greeted_members

# Function to add a member's ID to the file
def add_greeted_member(member_id):
    """
    Function to add a member's ID to the file
    """
    with open('data/greeted_members.txt', 'a') as file:
        file.write(f'{member_id}\n')