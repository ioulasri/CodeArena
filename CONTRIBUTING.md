# Contributing to CodeArena

## Branch Strategy

We follow a Git Flow branching model:

### Branches

- **main** - Production-ready code. Protected branch.
- **staging** - Pre-production testing environment
- **develop** - Main development branch. All features merge here first.
- **feature/** - Feature branches (e.g., `feature/user-auth`)
- **bugfix/** - Bug fix branches (e.g., `bugfix/login-error`)
- **hotfix/** - Urgent production fixes (e.g., `hotfix/security-patch`)

## Workflow

### Starting New Work

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit regularly:
   ```bash
   git add .
   git commit -m "feat: add user authentication"
   ```

3. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Create a Pull Request to `develop`

### Commit Messages

Follow conventional commits:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add user registration endpoint
fix: resolve login validation error
docs: update API documentation
```

### Pull Request Process

1. Ensure your code passes all tests
2. Update documentation if needed
3. Request review from team members
4. Address review comments
5. Squash commits if requested
6. Merge after approval

### Release Process

1. Merge `develop` into `staging` for testing
2. After QA approval, merge `staging` into `main`
3. Tag the release: `git tag -a v1.0.0 -m "Release 1.0.0"`
4. Push tags: `git push origin --tags`

## Code Review Guidelines

- Keep PRs focused and reasonably sized
- Write clear descriptions
- Add screenshots for UI changes
- Ensure tests pass
- Follow project coding standards

## Questions?

Open an issue or contact the maintainers.
