# File: switch_env.sh
#!/bin/bash

# Get current branch name
branch=$(git rev-parse --abbrev-ref HEAD)

# Check if it's the develop branch and switch environments accordingly
if [ "$branch" = "develop" ]; then
  cp frontend/.env.development frontend/.env
  cp backend/.env.development backend/.env
else
  cp frontend/.env.production frontend/.env
  cp backend/.env.production backend/.env
fi