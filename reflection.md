1. Which issues were the easiest to fix, and which were the hardest? Why?
   
Easiest: The easiest fixes were the single-line, mechanical changes. Things like removing the eval() line, fixing the KeyError bug in getQty() with .get(), and renaming functions to snake_case were simple because
they didn't require changing the program's logic.
Hardest: The hardest fix by far was removing the global variable. This was an architectural change, not just a bug fix. It required us to re-think the flow of data, update the function signatures for almost every
function, and then change how main() was structured to pass the stock_data dictionary around as an argument.

2. Did the static analysis tools report any false positives? If so, describe one example.
   
No, in this lab, the tools were extremely accurate. There were no clear false positives. Every major issue reported were the eval() use, the bare-except:, the mutable default argument (logs=[]), and the use of global
which was a legitimate and significant problem that needed to be fixed.

3. How would you integrate static analysis tools into your actual software development workflow?

I would  use an IDE (like VS Code) with plugins that run tools like Pylint and Flake8 in real-time. This gives instant feedback, showing errors as I type. I would also set up a Git pre-commit hook that runs all the 
tools (Pylint, Bandit, Flake8) before a commit is even allowed. This prevents bad code from ever entering the repository.
I would configure a CI pipeline (like GitHub Actions) to run the static analysis tools as a required step. If the code score is too low or any new high-severity security issues are found, the build would fail, 
and the pull request would be blocked from merging. This acts as a final safety net for the whole team.

4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Robustness: The code's robustness was significantly improved. It no longer crashes from KeyError exceptions, thanks to the use of .get(), or from invalid data types, due to the implementation of input validation. 
Security was enhanced by removing the eval() call, and bug-hiding was eliminated by replacing the bare-except block. Furthermore, file handling operations are now safer through the consistent use of with open(...).

Readability: Code readability was enhanced. The enforcement of standard snake_case naming conventions makes the code more familiar and compliant with PEP 8. The addition of docstrings clearly defines the purpose,
arguments, and return values for each function. Finally, the integration of the logging module provides a clear execution trace, detailing operations and errors.

Maintainability: The removal of the global variable yielded the most significant improvement in maintainability. The code no longer relies on a mutable shared state, which was a source of potential side effects.
Functions now have explicit dependencies passed as arguments, making them easier to test in isolation and safer to modify.
