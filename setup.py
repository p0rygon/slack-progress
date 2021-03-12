from setuptools import setup, find_packages

setup(
    name='slack-progress',
    version='0.6',
    packages=find_packages(),
    description='A realtime progress bar for Slack',
    author='Bradley Cicenas',
    author_email='bradley@vektor.nyc',
    url='https://github.com/bcicen/slack-progress',
    install_requires=['slack_sdk'],
    license='http://opensource.org/licenses/MIT',
    classifiers=(
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ),
    keywords='slack chatops devops'
)
