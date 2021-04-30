import os
from pathlib import Path


class Utils:
    def run_code_file(self, file_path, creator_dir):
        # Input file name of the contest which is needed to calculate result for attendee
        # Currently, it is forced to have name: input.txt
        input_file_path = Path(creator_dir).joinpath('input.txt')
        # Output file name of the contest which is needed sample result to compare with result from attendee
        # Currently, it is forced to have name: output.txt
        result_file_path = Path(creator_dir).joinpath('result.txt')

        output_file = file_path.parent.joinpath('output.txt')
        result_file = file_path.parent.joinpath('result.txt')
        validate_code_file = Path(creator_dir).joinpath('checkoutput.py')
        os.system('python ' + str(validate_code_file) +
                  ' \'' + str(file_path) + '\'' +
                  ' \'' + str(input_file_path) + '\'' +
                  ' \'' + str(result_file_path) + '\'' +
                  ' \'' + str(output_file) + '\'' +
                  ' > ' + str(result_file))

        result = open(result_file)
        return result.read()

    def check_right_extension(self, file, extensions):
        return file.is_file() and file.name.split('.')[1] in extensions


utils = Utils()
