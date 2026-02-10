---
trigger: always_on
description: Ensures prompts include a workflow; analyzes intent and maps to available workflows when missing.
---

All prompts should contain a workflow. If not, you should analyze the prompt for its objectives and determine which available workflows are needed to process those objectives. You can rewrite the prompt, placing the workflows intertwined with the text between brackets `[/workflow]` to clarify intent; then, and only then, you should execute the prompt. 