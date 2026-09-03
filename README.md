# Engineering Dashboard Apps

This project contains two separate Streamlit engineering apps built for the assignment requirement:

1. Heat Transfer Analyser
2. Thermodynamics Calculator

## App 1: Heat Transfer Analyser
- File: `heat_transfer_analyser.py`
- Purpose: analyse conduction, convection, and radiation heat transfer
- Run with:
  `py -3.13 -m streamlit run heat_transfer_analyser.py`

## App 2: Thermodynamics Calculator
- File: `thermodynamics_calculator.py`
- Purpose: calculate ideal gas properties, first law analysis, and thermodynamic cycle efficiency
- Run with:
  `py -3.13 -m streamlit run thermodynamics_calculator.py`

The thermodynamics app uses Streamlit 1.45.1, which avoids browser compatibility issues with newer Streamlit releases.

## Install dependencies
`py -3.13 -m pip install -r heat_transfer_requirements.txt`
`py -3.13 -m pip install -r thermodynamics_requirements.txt`

## Deployment note
These apps are designed to run locally in a Streamlit environment and can be deployed to a public URL on Streamlit Community Cloud.

## AI documentation
This project includes an AI documentation comment block at the top of each app file listing the AI tools used, key prompts, and manual verification steps.
