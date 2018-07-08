import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='gym_gopherfx',
      version='0.1.1',
      install_requires=['gym'],author="Sergiu Ionescu",
      author_email="sergiu.ionescu@gmail.com",
      description="A gym environment for reinforcement training on forex historical data.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/sergiuionescu/gym-gopherfx",
      packages=setuptools.find_packages(),
      classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
),
)