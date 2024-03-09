def stv_round(profile, candidates, eliminated = []):
    
    tally = [0] * len(candidates)
    for index in eliminated:
        tally[index] = None

    for pref in profile:
        n = 0
        
        searching = True
        while searching:

            # if the preference is a tie 
            if isinstance(pref[n], list):
                m = 0

                # for each tied preference, check if the candidate has been eliminated otherwise tally the votes
                for _ in pref[n]:

                    if pref[n][m] - 1 not in eliminated:
                        candidate = pref[n][m] - 1
                        tally[candidate] += 1

                    # if the candidate has been eliminated, move to the next tied preference
                    m += 1
                    if m >= len(pref[n]):
                        searching = False

            # if the candidate has not been eliminated, tally the votes
            elif pref[n] - 1 not in eliminated:
                candidate = pref[n] - 1
                tally[candidate] += 1
                searching = False

            # when no candidate is found, move to the next preference
            n += 1
            if n >= len(pref):
                searching = False

    lowest_votes = min(value for value in tally if value is not None)
    loser = [i for i, value in enumerate(tally) if value == lowest_votes]

    highest_votes = max(value for value in tally if value is not None)
    winner = [i for i, value in enumerate(tally) if value == highest_votes]

    return tally, winner, loser


def manipulate(index, preference, target, candidates, profile, first, eliminated=None):
    """
    index = the index of the voter in the profile
    preference = the preference of the voter
    target = the candidate that the manipulator wants to win
    candidates = the set of candidates
    profile = profile
    first = the candidate most highly ranked by the manipulator amongst preferences
    eliminated = the candidates that have been eliminated
    """
    
    if eliminated is None:
        eliminated = []

    profile_copy = profile.copy()

    if len(eliminated) + 1 >= len(candidates):
        x_tally, x_winner, x_loser = stv_round(profile_copy, candidates)
        return (target == x_winner)
    
    if first == [0]:
        x_tally, x_winner, x_loser = stv_round(profile_copy, candidates)
        preference = x_loser + [x for x in preference if x not in x_loser]
        profile_copy[index] = preference
        y_tally, y_winner, y_loser = stv_round(profile_copy, candidates)

        x_eliminated = eliminated.copy()
        y_eliminated = eliminated.copy()
        eliminated.extend(x_loser)
        eliminated.extend(y_loser)

        if x_loser == y_loser:
            return (target != x_loser) and manipulate(index, preference, target, candidates, profile_copy, [0], x_eliminated)
        else:
            return ((target != x_loser) and manipulate(index, preference, target, candidates, profile_copy, [0], x_eliminated)) or ((target != y_loser) and manipulate(index, preference, target, candidates, profile_copy, y_loser[0], y_eliminated))

    else:
        tally, winner, loser = stv_round(profile_copy, candidates)
        eliminated.extend(loser)
        
        if target == loser:
            return False
        elif loser == first:
            print("here")
            return manipulate(index, preference, target, candidates, profile_copy, [0], eliminated)
        else:
            return manipulate(index, preference, target, candidates, profile_copy, first, eliminated)