 # Create Skill Examples
 
 ## Example: Commit Message Helper
 ```
 ---
 name: commit-message-helper
 description: Generate conventional commit messages. Use when the user asks for commit help.
 ---
 
 # Commit Message Helper
 
 ## When to Use
 - User asks for a git commit message
 - User requests “conventional commit”
 
 ## Instructions
 - Read `git diff` and `git status`
 - Summarize the change type
 - Produce a conventional commit message
 ```
 
 ## Example: API Review Checklist
 ```
 ---
 name: api-review-checklist
 description: Review API changes for correctness and compatibility. Use when reviewing API diffs.
 ---
 
 # API Review Checklist
 
 ## Instructions
 - Validate request/response schema
 - Check error handling and status codes
 - Confirm versioning behavior
 ```
