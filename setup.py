from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = "-e ."

def get_requirements(file_path:str) -> List[str] :
    req = []
    with open(file_path) as file:
        req = file.readlines()
        req = [r.replace("\n","") for r in req]
        if HYPHEN_E_DOT in req:
            req.remove(HYPHEN_E_DOT)
    return req

setup(
    name='mlproject',
    version='0.0.1',
    author='Nirad',
    author_email='yeola.nirad@gmail.com',
    packages=find_packages(),
    requires= get_requirements("requirements.txt")
    )