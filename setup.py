from distutils.core import setup

version = '0.1'

setup(
    name='python-oas-dependency-injector',
    version=version,
    package_dir={'oas_dependency_injection': 'oas_di'},
    packages=['oas_dependency_injection'],
    url='https://github.com/omerbn/python-oas-dependency-injector',
    license='GNU GPL 3.0',
    author='Omer Ben-Nahum',
    author_email='bn.omer@gmail.com',
    description='',
    entry_points={
        "console_scripts": [
            "oas_dependency_injection= oas_di:__main__",
        ]
    },
    install_requires=['PyYAML',
                      "Jinja2",
                      "jsonschema"]
)
