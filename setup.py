# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:00:17 2020

@author: HuangAlan
"""
import setuptools

# %%
setuptools.setup(
    name = 'self_module',
    version = '0.1.0',
    keywords = 'self_module for generate .whl',
    description = 'used to test the .whl file',
    author = 'Alan Huang',
    author_email ='alanhuang@hipposcreen-nc.com',
    
    url = 'https://github.com/tr1ggerone/python_gen_wheel',
    packages=setuptools.find_packages(),
    install_requires=['cmake==3.18.2.post1',
                      'numpy==1.21.5',
                      'scipy==1.7.3',
                      'matplotlib==3.5.1',
                      'scikit-learn==1.0.2',
                      'pandas==1.3.5',
                      'pillow==9.2.0'],
    license='MIT',
    include_package_data=True,
)
