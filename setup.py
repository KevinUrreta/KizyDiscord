from setuptools import setup, find_packages # type: ignore

setup(
    name='mi-bot-discord',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'discord.py==2.3.2',
        'ffmpeg==1.4',
        'googletrans==4.0.0rc1',
        'PyNaCl==1.5.0',
        'yt-dlp==2024.4.9'
    ],
    entry_points={
        'console_scripts': [
            'mi-bot-discord=mi_bot_discord.bot:main'
        ]
    },
    author='Tu Nombre',
    description='Un bot de Discord genial creado con discord.py',
    license='MIT',
    keywords='discord bot',
    url='https://github.com/tu-usuario/mi-bot-discord',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
