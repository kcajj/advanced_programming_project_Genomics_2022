from flask import Flask, render_template, redirect, url_for, make_response
import io
from dataset_reader import GFF3DatasetReader
from dataset import *

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

global global_active_op, current_dataset_name
global_active_op = human_genome.get_active_operations()
current_dataset_name = 'human_genome'

#the filter operations are handled differently, we want to make the user able to perform operations
#on a filtered dataset
datasets = {'human_genome': human_genome,
            'get_chromosomes': human_genome.get_chromosomes(),
            'ensembl_havana': human_genome.ensembl_havana()}

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

    output = global_active_op[operation_name]()

    if type(output) == Dataset:
        df = output.get_df()
        return render_template('operation.html', operation_name = operation_name, df = df, dataset_name = dataset_name)
    
    else:
        return redirect(url_for('active_operations', dataset_name = operation_name))

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/GFF3view/<dataset_name>')
def GFF3view(dataset_name):
    df = datasets[dataset_name].get_df()
    return render_template('GFF3view.html', dataset_name = dataset_name, dataset = df)

@app.route('/download/<dataset_name>/<operation_name>')
def download(dataset_name,operation_name): #fatto con chatgpt, c'è da controllare un minimo la documentazione e capire
                            #la funzione make response e io.StringIO
                            #se è roba troppo complicata concelliamo tutto
    global global_active_op

    if operation_name == '':
        df = datasets[dataset_name].get_df()
    else:
        df = global_active_op[operation_name]().get_df()
    # Create a buffer
    buffer = io.StringIO()
    
    # Write the DataFrame to the buffer
    df.to_csv(buffer, index=False)
    
    # Get the value of the buffer
    buffer.seek(0)
    csv_data = buffer.getvalue()
    
    # Create a response object with the content-type and content-disposition headers
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = f"attachment; filename = {dataset_name} - {operation_name}.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

# running application
if __name__ == '__main__':
    # reading the human genome
    app.run(debug=True)