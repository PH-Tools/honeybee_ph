---
name: "source-command-cleanup"
description: "Review the current git-diff code and branch and cleanup before merging."
---

# source-command-cleanup

Use this skill when the user asks to run the migrated source command `cleanup`.

## Command Template

# Cleanup Command

Review the current git diff/feature-branch and check for common issues before committing.

- Run `git diff` to see all unstaged changes
- If empty, run `git diff --staged` to check staged changes

# Refactor the NEW code to address any of the follwing issues:

1. **Function/Component Size**
   - Check the NEW code for large functions or components, and where practical break them down into smaller functions and smaller components.
   - Focus on READABILITY and CLARITY in the code
   - Where possible, implement clean-code and SOLID pracrices (Single-responsibility, Open-closed, etc.)

2. **FIX for Consistency**
   - Check the NEW code for consistency with EXISTING code patterns, naming and other existing conventions.
   - Ensure any NEW files of folders match the EXISTING code style and structure.

3. **FIX formatting issues**
   - Trailing whitespace
   - Inconsistent indentation (tabs vs spaces)
   - Missing newlines at end of files
   - Multiple consecutive blank lines
   - Lines exceeding 100 characters

4. **FIX for spelling errors**
   - Scan comments and documentation for common typos
   - Check variable/function names for misspellings
   - Ignore code-specific terms, technical jargon, and camelCase/snake_case identifiers
   - Focus on user-facing strings and documentation

5. **FIX code style issues**
   - Inconsistent naming conventions
   - Console.log or debug statements left in code
   - Commented-out code blocks
   - TODO/FIXME comments without context
   - Missing or inconsistent error handling

## Notes:

- Be practical - don't flag every minor style preference
- Focus on issues that could cause bugs or reduce code quality
- Respect existing code style in the repository
