from setuptools import setup

setup(
    name='pinecone-cli',
    description='pinecone-cli is a command-line client for interacting with the pinecone vector embedding database.',
    version='0.1.1',
    url='https://github.com/tullytim/pinecone-cli',
    author='Tim Tully',
    author_email='tim@menlovc.com',
    license='MIT',
    keywords='pinecone vector vectors embeddings database transformers models',
    python_requires='>=3',
    py_modules=['pinecli'],
    install_requires=[
        'Click', 'pandas', 'numpy', 'openai', 'pinecone-client', 'matplotlib', \
            'scikit-learn', 'beautifulsoup4', 'nltk', 'sklearn', 'rich'
    ],
    entry_points={
        'console_scripts': [
            'pinecli = pinecli:cli',
        ],
    },
)
