# DSA

## Finite Automaton Implementation

This repository contains a complete implementation of a finite automaton that recognizes strings of the form:

**L = (a + a(b + aa)*b)* a(b + aa)* a**

### 🚀 Quick Start

```bash
# Run the main demonstration
python finite_automaton.py

# Run comprehensive tests
python test_finite_automaton.py  

# Interactive demo
python demo.py
```

### 📁 Files

- **`finite_automaton.py`** - Main implementation of the FiniteAutomaton class
- **`test_finite_automaton.py`** - Comprehensive test suite with 17 test cases
- **`demo.py`** - Interactive demonstration script
- **`README_AUTOMATON.md`** - Detailed documentation and proof of correctness

### 🎯 Features

- ✅ Complete finite automaton implementation (NFA)
- ✅ String acceptance testing
- ✅ Detailed computation traces
- ✅ Comprehensive test coverage (17/17 tests passing)
- ✅ Interactive demonstration modes
- ✅ Mathematical proof of correctness
- ✅ Clear documentation and examples

### 🔍 Example Usage

```python
from finite_automaton import FiniteAutomaton

fa = FiniteAutomaton()

# Test strings
print(fa.is_accepted("aa"))      # True
print(fa.is_accepted("aba"))     # True  
print(fa.is_accepted("ab"))      # False

# Get computation trace
accepted, trace = fa.process_string("aba")
print(f"Result: {'ACCEPTED' if accepted else 'REJECTED'}")
```

### 📊 Language Pattern

The automaton recognizes strings matching: **(a + a(b + aa)*b)* a(b + aa)* a**

- **Prefix**: `(a + a(b + aa)*b)*` - Zero or more pattern segments
- **Middle**: `a(b + aa)*` - Required 'a' followed by optional b's or aa's  
- **Suffix**: `a` - Final required 'a'

### ✅ Validation

All test cases pass with 100% success rate:
- ✅ Simple valid strings: "aa", "aba", "aaaa"
- ✅ Complex valid strings: "aabaa", "abaaba", "aabaabaa" 
- ✅ Invalid strings properly rejected: "", "a", "ab", "ba"
- ✅ Error handling for invalid symbols
- ✅ Edge cases and boundary conditions

See `README_AUTOMATON.md` for detailed technical documentation.
