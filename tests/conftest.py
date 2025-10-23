import pytest
import shutil
import os

@pytest.fixture
def isolated_test_env(tmpdir):
    """
    Creates an isolated test environment with temporary input/output folders
    for a single test run. This is a pytest fixture.
    """
    input_dir = tmpdir.mkdir("input")
    output_dir = tmpdir.mkdir("output")
    
    # Copy our test CSV file into the temporary environment
    source_csv = os.path.abspath('tests/data/test_channels.csv')
    shutil.copy(source_csv, input_dir)
    
    # Yield the paths to the test function
    yield str(input_dir), str(output_dir)
    
    # Teardown (cleanup) happens automatically after the test finishes