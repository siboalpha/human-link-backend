# Test Guide

## General Guidelines
- Use Django's default testing module (`django.test`) for all test cases.
- Utilize Factory Boy or similar libraries to create reusable and consistent testing instances.
- Create a `BaseTestCase` class to centralize common setup logic and utilities for all tests.
- Follow the principle of one test class per method. Each test class should:
  - Test all expected success scenarios.
  - Test all expected failure scenarios.

## Example Structure

```python
class AuthService:
    def loginWithPassword(self):
        pass

    def loginWithGoogle(self):
        pass

# Corresponding test classes:

class TestLoginWithPassword(BaseTestCase):
    def test_login_success(self):
        """Test successful login with valid credentials."""
        pass

    def test_login_invalid_credentials(self):
        """Test login failure with invalid credentials."""
        pass

    def test_login_user_not_found(self):
        """Test login failure when user does not exist."""
        pass

class TestLoginWithGoogle(BaseTestCase):
    def test_login_success(self):
        """Test successful login with a valid Google token."""
        pass

    def test_login_invalid_token(self):
        """Test login failure with an invalid Google token."""
        pass

    def test_login_user_not_found(self):
        """Test login failure when user does not exist."""
        pass
```

## Best Practices
1. **Descriptive Test Names**: Use the `test_<scenario>` naming convention.
2. **Mock External Dependencies**: Use `unittest.mock` or `pytest-mock` to simulate external services.
3. **Comprehensive Coverage**: Validate both positive and negative test cases.
4. **Readability**: Maintain a high level of readability and organization in test files.
5. **Repeatability**: Ensure tests are deterministic and do not rely on external state.

## Running Tests

To run the tests, follow these steps:

1. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Run Specific Tests**:
   ```bash
   python manage.py test [class or method path]
   ```
   Replace `[class or method path]` with the specific test class or method you want to run.

3. **Run App Tests**:
   ```bash
   python manage.py test [app name]
   ```
   Replace `[app name]` with the name of the app whose tests you want to execute.
