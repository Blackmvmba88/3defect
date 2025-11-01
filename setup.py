from setuptools import setup, find_packages

setup(
    name="3defect",
    version="0.1.0",
    description="A 3D modeling system with Blender integration for creating vehicles and mechanical systems",
    author="3defect Team",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics :: 3D Modeling',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
