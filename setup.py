from setuptools import setup, find_packages


if __name__ == "__main__":
    setup(
        name='LimeSoup',
        version="0.3.1",
        python_requires='>=3.4',
        author="Ceder Group",
        license="MIT License",
        packages=find_packages(),
        zip_safe=False,
        install_requires=[
            'beautifulsoup4>=4.6.1',
            # lxml 4.4.0 changed default namespace to '', which causes
            # unexpected behaviors. For compatibility reasons, keep using
            # old versions for now.
            'lxml>=4.2.6,<=4.3.5',
        ]
    )
