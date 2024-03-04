from collections import Counter, defaultdict

# Redefine the parsing function with additional checks for empty strings
def parse_input(file_path):
    votes = []
    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('#') and line.strip():
                # Check if line contains a colon before attempting to unpack
                if ':' in line:
                    count, vote_str = line.strip().split(':')
                    vote = []
                    for part in vote_str.split('{'):
                        part = part.replace('}', '')
                        if part:
                            # Handle ties or individual votes, checking for empty strings
                            vote_part = tuple(filter(None, map(lambda x: x.strip(), part.split(','))))
                            if len(vote_part) > 1:
                                vote.append(tuple(map(int, vote_part)))
                            elif vote_part:
                                vote.append(int(vote_part[0]))
                    votes.extend([vote] * int(count))
                else:
                    # Handle lines that do not contain a colon
                    print(f"Warning: Line skipped due to unexpected format: {line.strip()}")
    return votes

# Define the STV function for a single winner
def stv_single_winner(votes, candidate_names):
    quota = 1 + len(votes) // 2
    round_number = 0
    eliminated_candidates = set()

    while True:
        round_number += 1
        print(f"\nRound {round_number}:")
        vote_counts = defaultdict(int)

        for vote in votes:
            for pref in vote:
                if isinstance(pref, tuple):
                    # Check if any of the tied preferences are not eliminated
                    found = False
                    for p in pref:
                        if p not in eliminated_candidates:
                            vote_counts[p] += 1
                            found = True
                            break
                    if found:
                        break
                else:
                    if pref not in eliminated_candidates:
                        vote_counts[pref] += 1
                        break

        for candidate, count in vote_counts.items():
            print(f"  Candidate {candidate_names[candidate]} has {count} votes.")

        # Identify candidates meeting or exceeding the quota
        elected_candidates = [candidate for candidate, count in vote_counts.items() if count >= quota]

        if elected_candidates:
            # Assuming a single winner scenario, but could be adjusted for multiple winners
            winner = max(vote_counts, key=vote_counts.get)
            if vote_counts[winner] >= quota or len(eliminated_candidates) + 1 == len(candidate_names):
                print(f"  Candidate {candidate_names[winner]} is the winner.")
                return candidate_names[winner]

        # Eliminate the candidate with the least votes if no one has won yet
        if not elected_candidates:
            min_votes = min(vote_counts.values())
            for candidate, count in list(vote_counts.items()):
                if count == min_votes:
                    print(f"  Candidate {candidate_names[candidate]} is eliminated.")
                    eliminated_candidates.add(candidate)
                    del vote_counts[candidate]

        if len(vote_counts) == 1:
            # If only one candidate remains, they are the winner
            winner = next(iter(vote_counts))
            print(f"  Candidate {candidate_names[winner]} is the winner.")
            return candidate_names[winner]

        if not vote_counts:
            print("  No more votes left to distribute, and no winner could be determined.")
            break

# Define candidate names
# TO-DO: I'm a bit confused about 10 & 11 with write in 1/2. Do we just count the votes for those then?
candidate_names = {
    1: "Jackie Kasabach",
    2: "Jack Johnson",
    3: "Adam Frisch",
    4: "Torre",
    5: "Michael Behrendt",
    6: "Jason Lasser",
    7: "Michael Wampler",
    8: "Derek Johnson",
    9: "Brian D. Speck",
    10: "Write In 1",
    11: "Write In 2"
}

file_path = 'data-csc.txt'
votes = parse_input(file_path)

print(votes)

winner_or_tie = stv_single_winner(votes, candidate_names)

print(f"Winner or Tie: {winner_or_tie}")



