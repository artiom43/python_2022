from setuptools import setup

setup()
=IF(AND($H4>=2; $L4>=70); 5; IF(AND($H4>=1; $L4>=60); 4; IF($L4>=50; 3; "None")))