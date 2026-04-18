echo "Running Selenium Tests"
pytest pythonSel/test_e2eTestFramework.py

echo "Generating Mail HTML"
python3 pythonSel/generate_mail.py

echo "Test execution + Mail HTML generation completed"