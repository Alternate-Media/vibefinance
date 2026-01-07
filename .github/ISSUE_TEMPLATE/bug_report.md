name: Bug Report
description: Create a report to help us improve
labels: ["bug"]
body:
  - type: markdown
    attributes:
      value: |
        Please provide a clear and concise description of the bug.
  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How did you encounter the bug?
      placeholder: |
        1. Go to '...'
        2. Click on '....'
        3. Scroll down to '....'
        4. See error
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What did you expect to happen?
    validations:
      required: true
  - type: textarea
    id: actual
    attributes:
      label: Actual Behavior
      description: What actually happened?
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs/Screenshots
      description: Please paste any relevant logs (sanitized) or upload screenshots.
  - type: textarea
    id: environment
    attributes:
      label: Environment
      description: OS, Browser, Python version, etc.
