"""These are the invoke tasks used to test and lint the project"""
from invoke import task
from sys import platform

on_windows = (platform == "win32")
@task
def lint(c):
    print("Pylint Error lint")
    c.run("pylint analytics/*.py --errors-only")
    print("Bandit Security lint")
    c.run("bandit -r . --exclude ./.venv")
