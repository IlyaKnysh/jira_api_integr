1. Create .env file and place following variables:


    URL=https://jira.{your jira address}

    AUTH={your jira token}

    PACKAGE_NAME={target package name, E.G. smoke}

    LABELS_LIST={target labels, divided by ',', E.G. apiAutomated, SmokeAPI_UDS}

2. Install dependencies


    $ pip install -r requirements.txt
3. Place json files from allure report to some folder and set it's path as a parameter
4. Run main.py