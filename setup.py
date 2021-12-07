from setuptools import setup


def __parse_requirements(path: str):
    with open(path, "r", encoding="utf-8") as rqrmts:
        return [
            line
            for line in rqrmts.readlines()
            if not line.strip().startswith("#") and len(line.strip()) > 0
        ]


setup(
    install_requires=__parse_requirements("requirements.txt"),
    extras_require={"dev": __parse_requirements("dev-requirement.txt")},
)
