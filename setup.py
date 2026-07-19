from setuptools import setup, find_packages

setup(
    name="3defect",
    version="0.2.0",
    description="A 3D modeling system with optional Blender integration for creating vehicles and mechanical systems",
    author="3defect Team",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
        'scipy>=1.10.0',
        'mathutils>=3.3.0',
    ],
    extras_require={
        'blender': ['bpy>=3.6.0'],  # Optional Blender integration
        'dev': ['pytest>=7.0.0', 'pytest-cov>=4.0.0'],  # Development dependencies
    },
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
