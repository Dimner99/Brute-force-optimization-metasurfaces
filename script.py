#%%
import re
import os
import json
#%%

def convert_mathematica_to_python(file_path, json_key=None, additional_replacements=None, output_file_path=None):
    # Default replacements
    default_replacements = {
        r'Cos': 'cos',
        r'Sin': 'sin',
        r'Tan': 'tan',  
        r'E\^': 'exp',
        r'Log': 'log',
        r'Sqrt': 'sqrt',
        r'Abs': 'abs',
        r'I': '1j',
        r'π': 'np.pi',
        r'Exp': 'exp'
        # Add more functions as needed
    }

    # Merge default with additional replacements
    if additional_replacements:
        replacements = {**default_replacements, **additional_replacements}
    else:
        replacements = default_replacements

    # Determine file type and read formula
    if file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if json_key in data:
                mathematica_formula = data[json_key]
            else:
                raise KeyError(f"Key '{json_key}' not found in JSON file.")
    else:
        with open(file_path, 'r') as file:
            mathematica_formula = file.read()

    # Perform replacements using regular expressions
    for pattern, replacement in replacements.items():
        mathematica_formula = re.sub(pattern, replacement, mathematica_formula)

    # Replace square brackets with parentheses
    mathematica_formula = mathematica_formula.replace('[', '(').replace(']', ')')

    # Replace '^' with '**' for power
    mathematica_formula = mathematica_formula.replace('^', '**')

    # Store the result in the output file if provided
    if output_file_path:
        if os.path.exists(output_file_path):
            with open(output_file_path, 'r') as file:
                output_data = json.load(file)
        else:
            output_data = {}

        output_data[json_key] = mathematica_formula

        with open(output_file_path, 'w') as file:
            json.dump(output_data, file, indent=4)

    return mathematica_formula

# Example usage:
additional_replacements = {
    r'θ': 'theta',
    r'φ': 'phi',
    r'ω': 'om',
    r'ε': 'e',
    r'μ': 'mu',
    r'HankelH2': 'h2v',
    r'HankelH1': 'h1v',
    r'BesselJ': 'jv',
    r'BesselY': 'yv',
    r'σ': 'sigma',
    r'η0': 'eta0',
    r'Sec': 'sec',
    r'Cot': 'cot' # type dict [pattern, replacement]
}
#%%
filepath="/home/dim_ner/Desktop/ΔΙΠΛΩΜΑΤΙΚΗ/results_analytical/results_general_real_xy.json"
keys_of_json=["Rx","Ry","Tx","Ty"]
output_file_path="//home/dim_ner/Desktop/ΔΙΠΛΩΜΑΤΙΚΗ/results_analytical/results_general_real_xy_CONVERTED.json"
for key in keys_of_json:
    convert_mathematica_to_python(filepath,key,additional_replacements,output_file_path)  
# %%
