from setuptools import setup

setup(name='AcmeWine',
      version='0.1',
      description='Check a wine order for completeness',
      url='https://github.com/ninehundred1/AcmeWine',
      author='Stephan Meyer',
      author_email='meyernsen@gmail.com',
      license='MIT',
      packages=['verify_orders', 'validate_CSV'],
      zip_safe=False)