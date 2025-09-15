"""
Finite Automaton Implementation

This module implements a finite automaton that recognizes strings of the form:
(a + a(b + aa)*b)* a(b + aa)* a

The automaton has 3 states:
- q0: Initial state
- q1: Intermediate state  
- q2: Final/accepting state (marked with double circle)

Transition function:
1. δ(q0, a) = {q0, q1}  # From q0 with 'a' can go to q0 or q1
2. δ(q1, b) = {q1, q0}  # From q1 with 'b' can go to q1 or q0
3. δ(q1, a) = {q1, q2}  # From q1 with 'a' can go to q1 or q2
4. δ(q2, a) = {q1}      # From q2 with 'a' goes to q1

The pattern (a + a(b + aa)*b)* a(b + aa)* a means:
- (a + a(b + aa)*b)*: Zero or more occurrences of either 'a' or 'a' followed by 
  zero or more (b or aa), then 'b'
- a(b + aa)*: 'a' followed by zero or more (b or aa)
- a: Final 'a'
"""

class FiniteAutomaton:
    """
    A finite automaton that recognizes the language (a + a(b + aa)*b)* a(b + aa)* a
    """
    
    def __init__(self):
        """Initialize the finite automaton with states and transitions."""
        # States
        self.states = {'q0', 'q1', 'q2'}
        self.initial_state = 'q0'
        self.final_states = {'q2'}
        self.alphabet = {'a', 'b'}
        
        # Transition function as a dictionary
        # Key: (current_state, input_symbol), Value: set of next states
        self.transitions = {
            ('q0', 'a'): {'q0', 'q1'},  # Non-deterministic: can go to q0 or q1
            ('q1', 'b'): {'q1', 'q0'},  # Non-deterministic: can go to q1 or q0  
            ('q1', 'a'): {'q1', 'q2'},  # Non-deterministic: can go to q1 or q2
            ('q2', 'a'): {'q1'},        # Deterministic: only goes to q1
        }
        
    def epsilon_closure(self, states):
        """
        Compute epsilon closure (not needed for this automaton as it has no epsilon transitions)
        """
        return states
        
    def delta(self, current_states, symbol):
        """
        Transition function for a set of states and an input symbol.
        
        Args:
            current_states (set): Current set of states
            symbol (str): Input symbol
            
        Returns:
            set: Set of next states reachable from current states with the symbol
        """
        next_states = set()
        for state in current_states:
            if (state, symbol) in self.transitions:
                next_states.update(self.transitions[(state, symbol)])
        return next_states
    
    def process_string(self, input_string):
        """
        Process an input string through the automaton.
        
        Args:
            input_string (str): The input string to process
            
        Returns:
            tuple: (bool, list) - (is_accepted, computation_trace)
        """
        # Start with initial state
        current_states = {self.initial_state}
        computation_trace = [(input_string, '', current_states.copy())]
        
        # Process each character
        for i, symbol in enumerate(input_string):
            if symbol not in self.alphabet:
                return False, computation_trace + [f"Invalid symbol '{symbol}' at position {i}"]
                
            next_states = self.delta(current_states, symbol)
            current_states = next_states
            
            consumed = input_string[:i+1]
            remaining = input_string[i+1:]
            computation_trace.append((remaining, consumed, current_states.copy()))
            
            # If no valid transitions, reject
            if not current_states:
                return False, computation_trace
        
        # Check if any final state is reached
        is_accepted = bool(current_states.intersection(self.final_states))
        return is_accepted, computation_trace
    
    def is_accepted(self, input_string):
        """
        Check if a string is accepted by the automaton.
        
        Args:
            input_string (str): The input string to check
            
        Returns:
            bool: True if the string is accepted, False otherwise
        """
        accepted, _ = self.process_string(input_string)
        return accepted
    
    def get_transition_table(self):
        """
        Get a formatted transition table for display.
        
        Returns:
            str: Formatted transition table
        """
        table = "Transition Table:\n"
        table += "State\t| a\t\t| b\n"
        table += "------|-----------|----------\n"
        
        for state in sorted(self.states):
            row = f"{state}\t|"
            
            # Transitions for 'a'
            if (state, 'a') in self.transitions:
                next_states = self.transitions[(state, 'a')]
                row += f" {{{', '.join(sorted(next_states))}}}\t|"
            else:
                row += " ∅\t\t|"
                
            # Transitions for 'b'
            if (state, 'b') in self.transitions:
                next_states = self.transitions[(state, 'b')]
                row += f" {{{', '.join(sorted(next_states))}}}"
            else:
                row += " ∅"
                
            table += row + "\n"
            
        return table
    
    def validate_language_pattern(self, test_strings):
        """
        Validate that the automaton recognizes strings matching the pattern
        (a + a(b + aa)*b)* a(b + aa)* a
        
        Args:
            test_strings (list): List of tuples (string, expected_result, description)
            
        Returns:
            tuple: (all_passed, results) where results is a list of test outcomes
        """
        results = []
        all_passed = True
        
        for test_string, expected, description in test_strings:
            actual = self.is_accepted(test_string)
            passed = actual == expected
            all_passed = all_passed and passed
            
            result = {
                'string': test_string,
                'expected': expected,
                'actual': actual,
                'passed': passed,
                'description': description
            }
            results.append(result)
            
        return all_passed, results


def main():
    """
    Main function to demonstrate the finite automaton functionality.
    """
    print("Finite Automaton for Language: (a + a(b + aa)*b)* a(b + aa)* a")
    print("=" * 60)
    
    # Create the automaton
    fa = FiniteAutomaton()
    
    # Display transition table
    print(fa.get_transition_table())
    print()
    
    # Test cases based on the pattern (a + a(b + aa)*b)* a(b + aa)* a
    test_cases = [
        # Valid strings
        ("aa", True, "Simple valid string: a(empty)a"),
        ("aba", True, "Valid: a + b + a"),
        ("aaaa", True, "Valid: a + aa + a"), 
        ("aaba", True, "Valid: a + a + b + a"),
        ("abaa", True, "Valid: a + b + aa"),
        ("aabaa", True, "Valid: a + a + b + aa"),
        ("abaaba", True, "Valid: (a + a(b)b) + a + b + a"),
        ("aababa", True, "Valid: a + a + b + a + b + a"),
        ("aabaabaa", True, "Valid: a + a + b + a + a + b + aa"),
        
        # Invalid strings  
        ("", False, "Empty string - invalid"),
        ("a", False, "Single 'a' - doesn't end in accepting state"),
        ("b", False, "Starts with 'b' - no transition from q0"),
        ("ab", False, "Ends with 'b' - not in accepting state"),
        ("ba", False, "Starts with 'b' - invalid"),
        ("aab", False, "Ends with 'b' - not in accepting state"),
        ("baa", False, "Starts with 'b' - invalid"),
        ("aabab", False, "Ends with 'b' - not in accepting state"),
        ("c", False, "Invalid symbol 'c'"),
        ("aaca", False, "Invalid symbol 'c'"),
    ]
    
    # Run validation
    all_passed, results = fa.validate_language_pattern(test_cases)
    
    print("Test Results:")
    print("-" * 80)
    for result in results:
        status = "✓ PASS" if result['passed'] else "✗ FAIL"
        print(f"{status} | '{result['string']:<12}' | Expected: {str(result['expected']):<5} | "
              f"Actual: {str(result['actual']):<5} | {result['description']}")
    
    print("-" * 80)
    print(f"Overall Result: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
    print(f"Passed: {sum(1 for r in results if r['passed'])}/{len(results)} tests")
    
    # Demonstrate computation trace for a few examples
    print("\nDetailed Computation Traces:")
    print("-" * 50)
    
    examples = ["aa", "aba", "ab", "aabaa"]
    for example in examples:
        print(f"\nProcessing '{example}':")
        accepted, trace = fa.process_string(example)
        print(f"Result: {'ACCEPTED' if accepted else 'REJECTED'}")
        
        for step, (remaining, consumed, states) in enumerate(trace):
            if isinstance(states, str):  # Error message
                print(f"  Step {step}: {states}")
            else:
                states_str = '{' + ', '.join(sorted(states)) + '}' if states else '∅'
                print(f"  Step {step}: Consumed='{consumed}', Remaining='{remaining}', States={states_str}")


if __name__ == "__main__":
    main()