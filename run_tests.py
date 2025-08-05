import sys
import pytest


def run_tests():
    """
    Runs the pytest test suite, generates a JUnitXML test report,
    and creates a code coverage report.

    This script acts as a standardized entry point for running tests,
    ensuring that the same arguments are used every time. This is
    particularly useful for CI/CD pipelines.
    """
    print("Starting test run with coverage analysis...")

    # Define the arguments to pass to pytest.
    # '--junitxml=report.xml': creates a report of test results.
    # '--cov=main': specifies that we want to measure code coverage for the 'main.py' file.
    #               You could also use '--cov=.' to measure coverage for the whole directory.
    # '--cov-report=xml': generates the coverage report in Cobertura XML format (coverage.xml).
    # 'test_main.py': specifies the test file to run.
    args = ["--junitxml=report.xml", "--cov=main", "--cov-report=xml", "test_main.py"]

    # Execute pytest with the specified arguments.
    # pytest.main() returns an exit code.
    exit_code = pytest.main(args)

    print(f"Test run finished with exit code: {exit_code}")

    # Exit the script with the same exit code as the pytest run.
    # This ensures that if tests fail, the script will also report a failure status.
    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()
