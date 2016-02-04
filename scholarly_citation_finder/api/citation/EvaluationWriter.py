import os.path

class EvaluationWriter:
    
    def __init__(self, path):
        self.path = path
        self.num_total_inspected_publications = 0
        self.output = None
        
    def open(self, name):
        filename = os.path.join(self.path, '{}.csv'.format(name))
        self.output = open(filename, 'w+')
        self.write_values(0, 0)
        return filename
        
    def close(self):
        self.output.close()
        
    def write_line(self, string):
        self.output.write(string + '\n')
        
    def write_header(self, string):
        self.write_line('# ' + string)
    
    def write_values(self, num_inspected_publications, num_total_citations):
        self.num_total_inspected_publications += num_inspected_publications
        self.write_line('{}, {}'.format(self.num_total_inspected_publications, num_total_citations))
