---
name: "source-command-code-review"
description: "Review changes and new-code for architectural consistency and risks."
---

# source-command-code-review

Use this skill when the user asks to run the migrated source command `code-review`.

## Command Template

# Code Review Command

Perform a quick code review of the current git diff to catch common issues before submitting a PR.

## Steps to Follow

1. **Get the changes**
   - Run `git diff` for unstaged changes
   - Run `git diff --staged` for staged changes
   - If both are empty, inform the user there are no changes to review

2. **Review for common issues**

   **Functionality:**
   - Are there obvious logic errors or bugs?
   - Are edge cases handled appropriately?
   - Is error handling present where needed?

   **Code Quality:**
   - Are variable and function names clear and descriptive?
   - Is the code easy to understand?
   - Are there overly complex sections that could be simplified?
   - Are there code duplications that should be refactored?

   **Security & Best Practices:**
   - Are there any hardcoded credentials, API keys, or secrets?
   - Are user inputs validated?
   - Are there any console.log or debug statements left in?
   - Are there commented-out code blocks that should be removed?

   **Documentation:**
   - Do complex functions have comments explaining their purpose?
   - Are any TODOs or FIXMEs left without context?

3. **Provide feedback**
   - List issues found with file name and approximate line number
   - Keep feedback constructive and specific
   - Separate critical issues from suggestions
   - If no issues found, give a brief positive summary

4. **Summarize**
   - Give an overall assessment (ready to merge / needs fixes / minor improvements suggested)
   - Highlight any blocking issues that must be addressed

## Notes

- Focus on substantive issues, not minor style preferences
- Be concise - this is a quick review, not an exhaustive audit
- Assume the developer knows their codebase
