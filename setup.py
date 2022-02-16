from setuptools import setup, find_packages
import versioneer
setup(
    name='ghrs',
    description='GHRS Report Generation Package',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    url='http://gitlabsdm.saipemnet.saipem.intranet/dst/packages/ghrs',
    author='Data and Smart Technologies',
    author_email='xbot@saipem.com',
    keywords=['pip','ghrs'],
    test_suite="tests",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    )