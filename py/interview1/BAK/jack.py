#!/usr/bin/env python

def helper(current_step, jump, action_number, n, k):
    '''
    return the step we get to by taking the action
    return None if we can't move
    '''

#    print "%scurrent_step=%s,jump=%s,action=%s,n=%s,k=%s" % (
#        '    ' * action_number, current_step, jump, action_number, n, k)

    if action_number > n:
        return None
    next_step = current_step
    if jump:
        next_step += action_number
        if next_step == k:
            return None

    jump_case = helper(next_step, True, action_number + 1, n, k)
    stay_case = helper(next_step, False, action_number + 1, n, k)
    
    if not jump_case and not stay_case:
        return next_step

    if not jump_case:
        next_step = stay_case
    elif not stay_case:
        next_step = jump_case
    else:
        next_step = max(stay_case, jump_case)

    return next_step


def maxStep(n, k):
    '''
    n - number of actions
    k - step NOT to land on

    returns highest step reachable
    '''

    # actions numbered from 1..n
    jump_case = helper(0, True, 1, n, k)
    stay_case = helper(0, False, 1, n, k)

    if not jump_case and not stay_case:
        return None

    if not jump_case:
        return stay_case

    if not stay_case:
        return jump_case

    return max(stay_case, jump_case)
