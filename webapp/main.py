from flask import Flask, render_template, redirect, url_for, make_response
from dataset_reader import GFF3DatasetReader
from dataset import *

filepath='webapp/Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

global global_active_op, current_dataset_name
global_active_op = human_genome.get_active_operations()
current_dataset_name = 'human_genome'

#the filter operations are handled differently, we want to make the user able to perform operations
#on a filtered dataset
datasets = {'human_genome': human_genome}
datasets.update(human_genome.get_subdatasets())

# Setting up the application
app = Flask(__name__, static_folder='static')

# making route
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/active_operations/<dataset_name>')
def active_operations(dataset_name):
    global global_active_op, current_dataset_name

    if current_dataset_name != dataset_name:
        global_active_op = datasets[dataset_name].get_active_operations()
        current_dataset_name = dataset_name

    return render_template('active_operations.html', active_op = global_active_op, dataset = datasets[dataset_name], dataset_name = dataset_name)

@app.route('/operation/<dataset_name>/<operation_name>')
def operation(dataset_name,operation_name):
    global global_active_op
    
    if operation_name != 'show_gff3':   #an operation on the dataset has been selected
        output = global_active_op[operation_name]()

        if type(output) == Dataset: #a normal operation has been selected
            df = output.get_df()
            return render_template('operation.html', operation_name = operation_name, df = df, dataset_name = dataset_name)
        
        else:   #a filter operation has been selected, the dataset is not shown completely
            return redirect(url_for('active_operations', dataset_name = operation_name))
    
    else:   #the user wants to see a gff3 dataset
        df = datasets[dataset_name].get_df().reset_index(drop = True)
        return render_template('operation.html', operation_name = operation_name, df = df, dataset_name = dataset_name)
    
@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/download/<dataset_name>/<operation_name>')
def download(dataset_name,operation_name):
    #c'è da controllare un minimo la documentazione e capire la funzione make response
    global global_active_op

    if operation_name == 'dataset':
        df = datasets[dataset_name].get_df()
    else:
        df = global_active_op[operation_name]().get_df()

    response = make_response(df.to_csv())
    response.headers["Content-Disposition"] = f"attachment; filename = {dataset_name} - {operation_name}.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# running application
if __name__ == '__main__':
    # reading the human genome
    app.run(debug=True)