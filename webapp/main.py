from flask import Flask, render_template, make_response
import io
from dataset_reader import GFF3DatasetReader
from dataset import *

filepath='Homo_sapiens.GRCh38.85.gff3.gz'
reader = GFF3DatasetReader()
human_genome = reader.read(filepath)

global global_active_op, fixed_active_op
global_active_op = human_genome.get_active_operations()
fixed_active_op = global_active_op

# Setting up the application
app = Flask(__name__, static_folder='static')

# making route
@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/active_operations/human_genome')
def active_operations():
    global global_active_op, fixed_active_op
    global_active_op = fixed_active_op
    return render_template('active_operations.html', active_op = global_active_op, dataset = human_genome, dataset_name = 'human_genome')

@app.route('/operation/<operation_name>')
def operation(operation_name):
    global global_active_op

    output = global_active_op[operation_name]()

    if type(output) == Dataset:
        df = output.get_df()
        return render_template('operation.html', operation_name = operation_name, df = df)
    
    else:
        global_active_op = output.get_active_operations()
        return render_template('active_operations.html', active_op = global_active_op, dataset = output, dataset_name = operation_name)

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/GFF3view/<dataset_name>')
def GFF3view(dataset_name):
    if dataset_name == 'human_genome':
        df = human_genome.get_df()
    if dataset_name == 'get_chromosomes':
        df = human_genome.get_chromosomes().get_df()
    return render_template('GFF3view.html', dataset_name = dataset_name, dataset=df)

@app.route('/download/<dataset_name>')
def download(dataset_name): #fatto con chatgpt, c'è da controllare un minimo la documentazione e capire
                            #la funzione make response e io.StringIO
                            #se è roba troppo complicata concelliamo tutto
    if dataset_name == "human_genome":
        df = human_genome.get_df()
    # Create a buffer
    buffer = io.StringIO()
    
    # Write the DataFrame to the buffer
    df.to_csv(buffer, index=False)
    
    # Get the value of the buffer
    buffer.seek(0)
    csv_data = buffer.getvalue()
    
    # Create a response object with the content-type and content-disposition headers
    response = make_response(csv_data)
    response.headers["Content-Disposition"] = f"attachment; filename = {dataset_name}.csv"
    response.headers["Content-type"] = "text/csv"
    
    return response

# running application
if __name__ == '__main__':
    # reading the human genome
    app.run(debug=True)