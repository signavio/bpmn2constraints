import setuptools

setuptools.setup(name='bpmnsignal',
                 version='0.0.2',
                 description='Compiles BPMN models to SIGNAL queries and LTL constraints',
                 long_description=open('README.md').read().strip(),
                 author='Arvid Bergman, Timotheus Kampik, Adrian Rebmann',
                 author_email='timotheus.kampik@sap.com',
                 url='https://github.com/signavio/bpmn-to-signal',
                 py_modules=['bpmnsignal'],
                 entry_points = {
                    'console_scripts': ['bpmnsignal=bpmnsignal.script:run']
                 },
                 install_requires=[],
                 keywords='BPMN Conformance',
                 classifiers=['BPMN', 'Conformance Checking'])