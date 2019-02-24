from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='fairsearchcore',
    version='1.0.4',
    description='A Python library with the core algorithms used to do fair search. ',
    long_description=long_description,
    license='Apache 2.0',
    packages=['fairsearchcore'],
    author='Ivan Kitanovski',
    author_email='ivan.kitanovski@gmail.com',
    url='https://github.com/fair-search/fairsearchcore-python',
    keywords=['search','fairness', 'fa*ir', 'ranking', 'reranking'],
    python_requires=">=3.0",
    install_requires=[
        'pandas>=0.23',
        'scipy>=1.1.0',
    ],
    tests_require=[
        'pytest>=2.8.0'
    ],
    setup_requires=['pytest-runner'],
    test_suite="tests",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy'
      ]
)
