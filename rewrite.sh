#!/bin/bash
git filter-branch -f --env-filter '
export GIT_COMMITTER_NAME="Anannya-Vyas"
export GIT_COMMITTER_EMAIL="beyondanannyavyas@gmail.com"
export GIT_AUTHOR_NAME="Anannya-Vyas"
export GIT_AUTHOR_EMAIL="beyondanannyavyas@gmail.com"
' --tag-name-filter cat -- --branches --tags
