from flask import Flask, render_template
from dataset_reader import GFF3DatasetReader
from dataset import *

# Setting up the application
app = Flask(__name__, static_folder='static')

# making route
@app.route('/')
def home():
    return render_template('homepage.html')

@app.route('/active_operations')
def active_operations():
    return render_template('active_operations.html', active_op = active_op)

@app.route('/operation/<operation_name>')
def operation(operation_name):
    output = active_op[operation_name]()
    df = output.get_df()
    if type(output) == Dataset:
        return render_template('operation.html', operation_name = operation_name, df = df)
    else:
        return render_template('filter.html', operation_name = operation_name,)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')
  
# running application
if __name__ == '__main__':
    # reading the human genome
    filepath='Homo_sapiens.GRCh38.85.gff3.gz'
    reader = GFF3DatasetReader()
    human_genome = reader.read(filepath)

    active_op = human_genome.get_active_operations()
    app.run(debug=True)