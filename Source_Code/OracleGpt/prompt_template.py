
def create_deepui_prompt(role, rules, actions, semantic_descriptions):
    prompt = f"""Role: {role}

Rules: {rules}

Operating Actions on the App: {actions}

Annotated Screenshots:
{semantic_descriptions}

Please identify any logical or UI bugs in the above scenario. If no issues are detected, respond with "No error"."""
    return prompt
