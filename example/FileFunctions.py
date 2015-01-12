#Read in a file and return a two-dimensional list representation
def file_to_matrix(filename):
        result_str = ''
        f = open(filename)
        result_str = f.read()
        f.close()
        result_matrix = []
        for row in result_str.split('\n'):
                if (row != ''):
                        new_row = []
                        for entry in row.split('\t'):
                                new_row.append(entry)
                                result_matrix.append(new_row)
        return result_matrix