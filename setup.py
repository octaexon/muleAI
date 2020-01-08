from setuptools import setup, Extension, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


joystick_module = Extension("mule.calibrate.ext._jsio", ["mule/calibrate/ext/jsiomodule.c"])

setup(
    name='mule_ai',
    version='0.1a1',
    description='muleAI: a lightweight python library for autonomous driving',
    long_description=readme(),
    keywords='autonomous driving rc car',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    url='http://github.com/bmj-autonomous/muleAI',
    author='Marcus Jones, James Ryan',
    author_email='jones.bm@gmail.com, octaexon@gmail.com',
    license='MIT',
    packages=['mule'],
    ext_modules=[joystick_module],
    install_requires=[
        'Click',
        'numpy',
        # 'opencv-contrib-python-headless',
        # 'tensorflow',
        'pyyaml',
        'adafruit-blinka',
        'adafruit-circuitpython-pca9685',
    ],
    # extras_require={
    #     'pi': [
    #         'opencv-python-contrib-headless=4.0.23',
    #         'picamera==',
    #         'tensorflow=2.0.0',
    #         ]
    #     },
    include_package_data=True,
    # packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mule=mule.mule:cli',
        ],
    },
    zip_safe=False)
