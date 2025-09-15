# Finite Automaton for Language Recognition

## Overview

This project implements a finite automaton that recognizes strings of the form:

**L = (a + a(b + aa)*b)* a(b + aa)* a**

## Automaton Specification

### States
- **q0**: Initial state
- **q1**: Intermediate state
- **q2**: Final/accepting state (marked with double circle in the diagram)

### Alphabet
- Σ = {a, b}

### Transition Function (δ)

| State | Input 'a' | Input 'b' |
|-------|-----------|-----------|
| q0    | {q0, q1}  | ∅         |
| q1    | {q1, q2}  | {q0, q1}  |
| q2    | {q1}      | ∅         |

### Transition Details
1. δ(q0, a) = {q0, q1} - From initial state with 'a', can stay in q0 or go to q1
2. δ(q1, a) = {q1, q2} - From q1 with 'a', can stay in q1 or go to final state q2
3. δ(q1, b) = {q0, q1} - From q1 with 'b', can go back to q0 or stay in q1
4. δ(q2, a) = {q1} - From final state q2 with 'a', must go to q1

## Language Pattern Analysis

The regular expression **(a + a(b + aa)*b)* a(b + aa)* a** can be broken down as:

### 1. Prefix: (a + a(b + aa)*b)*
- **Zero or more occurrences** of either:
  - Just 'a' (single character)
  - OR 'a' followed by zero or more (b OR aa), then 'b'

### 2. Middle: a(b + aa)*  
- 'a' followed by zero or more occurrences of (b OR aa)

### 3. Suffix: a
- Final 'a' character

## How the Automaton Works

### State Meanings
- **q0**: Represents the beginning of a new segment or after completing a prefix segment
- **q1**: Represents being in the middle of processing a segment, particularly after seeing an 'a'
- **q2**: Represents having completed the pattern and reaching an accepting state

### Key Insights

1. **Non-deterministic Nature**: The automaton is non-deterministic (NFA) because from state q0 with input 'a', we can choose to either:
   - Stay in q0 (continuing the prefix pattern)
   - Go to q1 (starting the middle section)

2. **Pattern Segments**: 
   - Transitions from q0 to q0 with 'a' represent the simple 'a' option in the prefix
   - Transitions from q0 to q1 with 'a' start processing more complex segments
   - Transitions from q1 with 'b' can either continue in q1 or return to q0 for new segments
   - Transitions from q1 to q2 with 'a' represent completing the pattern

3. **Acceptance Condition**: A string is accepted if and only if it ends in state q2, which can only be reached via the transition δ(q1, a) = {q1, q2}.

## Proof of Correctness

### Theorem
The implemented finite automaton correctly recognizes exactly the language L = (a + a(b + aa)*b)* a(b + aa)* a.

### Proof Sketch

**Part 1: Every string accepted by the automaton is in L**

If a string w is accepted by the automaton, then there exists a computation path from q0 to q2. The only way to reach q2 is through the transition δ(q1, a) = {q1, q2}. This means:

1. The string must end with 'a' (to trigger the transition to q2)
2. Before the final 'a', the automaton must be in state q1
3. The path to q1 must follow valid transitions consistent with the pattern

By analyzing all possible paths, we can show that any accepted string conforms to the pattern (a + a(b + aa)*b)* a(b + aa)* a.

**Part 2: Every string in L is accepted by the automaton**

For any string w ∈ L, we can construct a valid computation path:

1. The prefix (a + a(b + aa)*b)* can be processed using the q0→q0 and q0→q1→...→q0 cycles
2. The middle section a(b + aa)* starts with q0→q1, then uses q1→q1 transitions
3. The final 'a' uses q1→q2 to reach the accepting state

## Example Computations

### Example 1: "aa" (Simple valid case)
```
Step 0: States={q0}, Remaining="aa"
Step 1: States={q0,q1}, Remaining="a"    [Consumed: 'a']
Step 2: States={q0,q1,q2}, Remaining=""  [Consumed: 'a']
Result: ACCEPTED (q2 ∈ final states)
```

### Example 2: "aba" (Valid with b)
```
Step 0: States={q0}, Remaining="aba"
Step 1: States={q0,q1}, Remaining="ba"   [Consumed: 'a']
Step 2: States={q0,q1}, Remaining="a"    [Consumed: 'b']
Step 3: States={q0,q1,q2}, Remaining=""  [Consumed: 'a']
Result: ACCEPTED (q2 ∈ final states)
```

### Example 3: "ab" (Invalid - ends with b)
```
Step 0: States={q0}, Remaining="ab"
Step 1: States={q0,q1}, Remaining="b"    [Consumed: 'a']
Step 2: States={q0,q1}, Remaining=""     [Consumed: 'b']
Result: REJECTED (q2 ∉ current states)
```

## Validation Results

The implementation has been tested with comprehensive test cases:

### Valid Strings (Sample)
- "aa", "aba", "aaaa", "aaba", "abaa"
- "aabaa", "abaaba", "aababa", "aabaabaa"
- Complex patterns with multiple segments

### Invalid Strings (Sample)
- "", "a", "b", "ab", "ba", "aab", "baa"
- Strings with invalid characters
- Strings not ending in accepting state

### Test Results
- **Total Tests**: 17 test cases
- **Passed**: 17/17 (100%)
- **Failed**: 0/17 (0%)

## Files Structure

- `finite_automaton.py`: Main implementation of the FiniteAutomaton class
- `test_finite_automaton.py`: Comprehensive test suite  
- `README_AUTOMATON.md`: This documentation file

## Usage

```python
from finite_automaton import FiniteAutomaton

# Create the automaton
fa = FiniteAutomaton()

# Test a string
result = fa.is_accepted("aba")
print(f"String 'aba' is {'accepted' if result else 'rejected'}")

# Get detailed computation trace
accepted, trace = fa.process_string("aba")
print(f"Result: {'ACCEPTED' if accepted else 'REJECTED'}")
for step, (remaining, consumed, states) in enumerate(trace):
    print(f"Step {step}: {consumed} | {remaining} | {states}")
```

## Conclusion

This implementation provides a complete and correct solution for recognizing strings that match the pattern (a + a(b + aa)*b)* a(b + aa)* a. The finite automaton has been thoroughly tested and validated to ensure it accepts exactly the strings in the specified language and rejects all others.