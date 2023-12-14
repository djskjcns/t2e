import subprocess
from main import read_file, process_text, clean_lines

def test_main(input_file, output_file):
    lines = read_file(input_file)
    lines = clean_lines(lines)
    text = process_text(lines)
    with open(output_file, 'w') as f:
        f.write(text)

if __name__ == '__main__':
    test_input = 'tests/test_input.txt'
    test_output = 'tests/test_output.txt'
    test_main(test_input, test_output)
