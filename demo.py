#!/usr/bin/env python3
"""
Demo script for the Finite Automaton implementation.

This script provides an interactive demonstration of the finite automaton
that recognizes strings of the form (a + a(b + aa)*b)* a(b + aa)* a.
"""

from finite_automaton import FiniteAutomaton


def interactive_demo():
    """Run an interactive demo of the finite automaton."""
    print("🤖 Finite Automaton Demo")
    print("=" * 50)
    print("Language: (a + a(b + aa)*b)* a(b + aa)* a")
    print("Alphabet: {a, b}")
    print("Type 'help' for commands, 'quit' to exit\n")
    
    fa = FiniteAutomaton()
    
    while True:
        try:
            user_input = input("Enter string to test (or command): ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            elif user_input.lower() == 'help':
                print_help()
                continue
                
            elif user_input.lower() == 'table':
                print(fa.get_transition_table())
                continue
                
            elif user_input.lower() == 'examples':
                show_examples(fa)
                continue
                
            elif user_input.lower() == 'pattern':
                explain_pattern()
                continue
                
            # Test the string
            accepted, trace = fa.process_string(user_input)
            
            print(f"\n📝 Testing: '{user_input}'")
            print(f"🎯 Result: {'✅ ACCEPTED' if accepted else '❌ REJECTED'}")
            
            if len(user_input) <= 10:  # Show trace for short strings
                print("\n📊 Computation Trace:")
                for step, (remaining, consumed, states) in enumerate(trace):
                    if isinstance(states, str):  # Error message
                        print(f"   Step {step}: {states}")
                    else:
                        states_str = '{' + ', '.join(sorted(states)) + '}' if states else '∅'
                        print(f"   Step {step}: '{consumed}' | '{remaining}' | {states_str}")
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def print_help():
    """Print help information."""
    print("\n📚 Available Commands:")
    print("  help     - Show this help message")
    print("  table    - Show transition table")
    print("  examples - Show example strings")
    print("  pattern  - Explain the language pattern")
    print("  quit     - Exit the demo")
    print("\n💡 Or enter any string to test it!")
    print()


def show_examples(fa):
    """Show example strings and their results."""
    print("\n🔍 Example Strings:")
    print("-" * 30)
    
    examples = [
        ("aa", "Simple: a + a"),
        ("aba", "With b: a + b + a"), 
        ("aaaa", "Multiple a's: a + aa + a"),
        ("aaba", "Mixed: a + a + b + a"),
        ("abaa", "Ending aa: a + b + aa"),
        ("aabaa", "Complex: a + a + b + aa"),
        ("", "Empty string"),
        ("a", "Single a"),
        ("ab", "Ending with b"),
        ("ba", "Starting with b"),
    ]
    
    for string, description in examples:
        result = fa.is_accepted(string)
        status = "✅" if result else "❌"
        print(f"  {status} '{string:8}' - {description}")
    
    print()


def explain_pattern():
    """Explain the language pattern."""
    print("\n🎯 Language Pattern: (a + a(b + aa)*b)* a(b + aa)* a")
    print("-" * 55)
    print("Breaking it down:")
    print("  📦 (a + a(b + aa)*b)*  - Zero or more occurrences of:")
    print("     • Just 'a', OR")
    print("     • 'a' + zero or more (b or aa) + 'b'")
    print("  📦 a(b + aa)*          - 'a' + zero or more (b or aa)")
    print("  📦 a                   - Final 'a'")
    print()
    print("🔑 Key insight: Must end with 'a' to reach accepting state q2")
    print()


def batch_test():
    """Run a batch test with predefined strings."""
    print("🧪 Batch Test Mode")
    print("=" * 30)
    
    fa = FiniteAutomaton()
    
    test_strings = [
        # Valid strings
        "aa", "aba", "aaaa", "aaba", "abaa", "aabaa", "abaaba",
        "aababa", "aabaabaa", "abaaabaa",
        
        # Invalid strings  
        "", "a", "b", "ab", "ba", "aab", "baa", "aabab", "babaa"
    ]
    
    print(f"Testing {len(test_strings)} strings...\n")
    
    valid_count = 0
    invalid_count = 0
    
    for string in test_strings:
        result = fa.is_accepted(string)
        status = "✅ VALID" if result else "❌ INVALID"
        print(f"{status:12} | '{string:12}'")
        
        if result:
            valid_count += 1
        else:
            invalid_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Valid strings: {valid_count}")
    print(f"   Invalid strings: {invalid_count}")
    print(f"   Total tested: {len(test_strings)}")


def main():
    """Main function to run the demo."""
    print("Select mode:")
    print("1. Interactive demo")
    print("2. Batch test")
    
    try:
        choice = input("Enter choice (1-2): ").strip()
        
        if choice == "1":
            interactive_demo()
        elif choice == "2":
            batch_test()
        else:
            print("Invalid choice. Running interactive demo...")
            interactive_demo()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()