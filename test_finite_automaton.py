"""
Test suite for the Finite Automaton implementation.

This module contains comprehensive tests to validate that the finite automaton
correctly recognizes strings of the form (a + a(b + aa)*b)* a(b + aa)* a.
"""

import unittest
import sys
import os

# Add the current directory to the path to import our module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from finite_automaton import FiniteAutomaton


class TestFiniteAutomaton(unittest.TestCase):
    """Test cases for the FiniteAutomaton class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.fa = FiniteAutomaton()
    
    def test_initialization(self):
        """Test that the automaton is properly initialized."""
        self.assertEqual(self.fa.initial_state, 'q0')
        self.assertEqual(self.fa.final_states, {'q2'})
        self.assertEqual(self.fa.states, {'q0', 'q1', 'q2'})
        self.assertEqual(self.fa.alphabet, {'a', 'b'})
    
    def test_transition_function(self):
        """Test the transition function with various inputs."""
        # Test transitions from q0
        self.assertEqual(self.fa.delta({'q0'}, 'a'), {'q0', 'q1'})
        self.assertEqual(self.fa.delta({'q0'}, 'b'), set())
        
        # Test transitions from q1  
        self.assertEqual(self.fa.delta({'q1'}, 'a'), {'q1', 'q2'})
        self.assertEqual(self.fa.delta({'q1'}, 'b'), {'q0', 'q1'})
        
        # Test transitions from q2
        self.assertEqual(self.fa.delta({'q2'}, 'a'), {'q1'})
        self.assertEqual(self.fa.delta({'q2'}, 'b'), set())
    
    def test_simple_valid_strings(self):
        """Test simple valid strings."""
        valid_strings = ["aa", "aba", "aaaa", "aaba", "abaa"]
        for string in valid_strings:
            with self.subTest(string=string):
                self.assertTrue(self.fa.is_accepted(string), 
                              f"String '{string}' should be accepted")
    
    def test_simple_invalid_strings(self):
        """Test simple invalid strings."""
        invalid_strings = ["", "a", "b", "ab", "ba", "aab", "baa"]
        for string in invalid_strings:
            with self.subTest(string=string):
                self.assertFalse(self.fa.is_accepted(string), 
                               f"String '{string}' should be rejected")
    
    def test_complex_valid_strings(self):
        """Test more complex valid strings that match the pattern."""
        complex_valid = [
            "aabaa",      # a + a + b + aa
            "abaaba",     # (a + a(b)b) + a + b + a  
            "aababa",     # a + a + b + a + b + a
            "aabaabaa",   # a + a + b + a + a + b + aa
            "abaaabaa",   # a + b + aa + a + b + aa
            "aabaabaabaa", # Complex pattern with multiple segments
        ]
        
        for string in complex_valid:
            with self.subTest(string=string):
                self.assertTrue(self.fa.is_accepted(string), 
                              f"Complex string '{string}' should be accepted")
    
    def test_complex_invalid_strings(self):
        """Test complex strings that should be rejected."""
        complex_invalid = [
            "aabab",      # Ends with 'b'
            "babaa",      # Starts with 'b' 
            "aabaab",     # Ends with 'b'
            "baabaa",     # Starts with 'b'
            "abab",       # Ends with 'b'
        ]
        
        for string in complex_invalid:
            with self.subTest(string=string):
                self.assertFalse(self.fa.is_accepted(string), 
                               f"Complex string '{string}' should be rejected")
    
    def test_invalid_symbols(self):
        """Test strings with invalid symbols."""
        invalid_symbol_strings = [
            "c", "aac", "aca", "abc", "xyz", "a1a", "a+a"
        ]
        
        for string in invalid_symbol_strings:
            with self.subTest(string=string):
                self.assertFalse(self.fa.is_accepted(string), 
                               f"String with invalid symbols '{string}' should be rejected")
    
    def test_computation_trace(self):
        """Test that computation traces are generated correctly."""
        accepted, trace = self.fa.process_string("aa")
        
        self.assertTrue(accepted)
        self.assertIsInstance(trace, list)
        self.assertTrue(len(trace) > 0)
        
        # Check initial state
        self.assertIn('q0', trace[0][2])
        
        # Check final state contains q2 (accepting state)
        final_states = trace[-1][2]
        self.assertIn('q2', final_states)
    
    def test_empty_string_handling(self):
        """Test empty string is properly rejected."""
        accepted, trace = self.fa.process_string("")
        self.assertFalse(accepted)
        self.assertEqual(len(trace), 1)  # Only initial state
    
    def test_pattern_validation_method(self):
        """Test the pattern validation method."""
        test_cases = [
            ("aa", True, "Test case"),
            ("ab", False, "Test case"),
        ]
        
        all_passed, results = self.fa.validate_language_pattern(test_cases)
        self.assertTrue(all_passed)
        self.assertEqual(len(results), 2)
        
        for result in results:
            self.assertIn('string', result)
            self.assertIn('expected', result)
            self.assertIn('actual', result)
            self.assertIn('passed', result)
            self.assertIn('description', result)
    
    def test_boundary_cases(self):
        """Test boundary cases and edge conditions."""
        # Shortest valid strings
        self.assertTrue(self.fa.is_accepted("aa"))
        
        # Strings that barely miss acceptance
        self.assertFalse(self.fa.is_accepted("a"))
        self.assertFalse(self.fa.is_accepted("ab"))
        
        # Longer valid patterns
        long_valid = "a" + "a" * 10 + "b" + "aa" * 5 + "a"
        # This represents a + a^10 + b + (aa)^5 + a, which should be valid
        self.assertTrue(self.fa.is_accepted(long_valid))
    
    def test_transition_table_generation(self):
        """Test that transition table is generated correctly."""
        table = self.fa.get_transition_table()
        
        self.assertIsInstance(table, str)
        self.assertIn("q0", table)
        self.assertIn("q1", table)
        self.assertIn("q2", table)
        self.assertIn("Transition Table", table)


class TestPatternMatching(unittest.TestCase):
    """Test cases specifically for pattern matching validation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fa = FiniteAutomaton()
    
    def test_pattern_component_a(self):
        """Test the 'a' component of the pattern."""
        # Single 'a' should not be accepted as it doesn't reach final state
        self.assertFalse(self.fa.is_accepted("a"))
    
    def test_pattern_component_aa(self):
        """Test the 'aa' component."""
        # Should be accepted: a(empty)a
        self.assertTrue(self.fa.is_accepted("aa"))
    
    def test_pattern_component_aba(self):
        """Test the 'a + b + a' component."""
        # Should be accepted: a + b + a
        self.assertTrue(self.fa.is_accepted("aba"))
    
    def test_pattern_zero_or_more_prefix(self):
        """Test the (a + a(b + aa)*b)* prefix."""
        # Empty prefix + aa should work
        self.assertTrue(self.fa.is_accepted("aa"))
        
        # One iteration of prefix + aa
        self.assertTrue(self.fa.is_accepted("aaa"))  # a + aa
        self.assertTrue(self.fa.is_accepted("aabaa")) # a + a + b + aa
    
    def test_pattern_middle_section(self):
        """Test the a(b + aa)* middle section."""
        # Just 'a' followed by 'a' (so 'aa' total)
        self.assertTrue(self.fa.is_accepted("aa"))
        
        # 'a' followed by 'b' then 'a' (so 'aba' total)  
        self.assertTrue(self.fa.is_accepted("aba"))
        
        # 'a' followed by 'aa' then 'a' (so 'aaaa' total)
        self.assertTrue(self.fa.is_accepted("aaaa"))


def run_comprehensive_tests():
    """Run all tests and display results."""
    print("Running Comprehensive Test Suite")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFiniteAutomaton))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternMatching))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")  
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall Result: {'SUCCESS' if success else 'FAILURE'}")
    
    return success


if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)