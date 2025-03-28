from setuptools import setup, find_packages

setup(
    name="github_ai_analyzer",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "streamlit==1.24.0",
        "python-dotenv==1.0.0",
        "openai==1.0.0",
        "PyGithub==2.1.1",
        "redis==4.5.0",
        "selenium==4.11.2",
        "webdriver-manager==4.0.0",
        "requests==2.31.0",
        "python-dateutil==2.8.2",
    ],
) 