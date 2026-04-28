import os

def format_minified_css(minified_css):
    formatted = []
    indent_level = 0
    in_string = False
    string_char = ''

    # Clean up any existing odd spacing
    minified_css = minified_css.replace('\n', '').replace('\r', '').replace('\t', '')

    i = 0
    while i < len(minified_css):
        char = minified_css[i]

        # Handle strings to avoid formatting inside content: "" or urls
        if in_string:
            formatted.append(char)
            if char == string_char and minified_css[i-1] != '\\':
                in_string = False
        elif char in ('"', "'"):
            in_string = True
            string_char = char
            formatted.append(char)
            
        elif char == '{':
            indent_level += 1
            formatted.append(' {\n' + ('    ' * indent_level))
            
        elif char == '}':
            indent_level = max(0, indent_level - 1)
            # Clean up trailing indents from empty blocks
            if formatted[-1].endswith('    '):
                formatted[-1] = formatted[-1][:-4]
            if not formatted[-1].endswith('\n'):
                formatted.append('\n')
            formatted.append(('    ' * indent_level) + '}\n\n')
            
        elif char == ';':
            formatted.append(';\n' + ('    ' * indent_level))
            
        elif char == ',':
            if indent_level == 0:
                # Break long comma-separated selectors onto new lines
                formatted.append(',\n')
            else:
                formatted.append(', ')
                
        else:
            # Skip extra spaces at the start of a newly indented line
            if char == ' ' and (not formatted or formatted[-1].endswith('    ') or formatted[-1].endswith('\n')):
                pass
            else:
                formatted.append(char)

        i += 1

    return "".join(formatted)

if __name__ == "__main__":
    input_file = "./css/darkmodecss.js"
    output_file = "./css/darkmodecss_formatted.js"

    print(f"Reading from {input_file}...")
    
    if not os.path.exists(input_file):
        print(f"Error: Create an '{input_file}' file in this directory and paste your minified CSS inside it.")
        exit(1)

    with open(input_file, "r", encoding="utf-8") as f:
        minified = f.read()

    formatted = format_minified_css(minified)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(formatted)

    print(f"Done! Formatted CSS saved to {output_file}")