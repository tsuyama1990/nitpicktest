git rm -r src tests
mkdir -p src/domain_models src/todo tests/e2e tests/unit
touch src/domain_models/.keep src/todo/.keep tests/e2e/.keep tests/unit/.keep
git add .
git commit -m "chore: replace dirs with empty dirs"
