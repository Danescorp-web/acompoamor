from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave-secreta-supersegura'

UPLOAD_FOLDER = 'static/uploads'
PDF_FOLDER = 'static/pdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PDF_FOLDER'] = PDF_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

especialista_info = {
    'direccion': 'Calle Ejemplo 123',
    'celular': '+593 999 999 999',
    'correo': 'ejemplo@correo.com',
    'img_especialista': 'uploads/foto-especialista.jpg',
    'logo': 'uploads/dd2e513b-474b-4e96-ad12-dc14c64317eb.png',
    'formulario': 'pdf/formulario.pdf',
    'imagenes_servicios': []
}

ADMIN_PASSWORD = "acompoamor2025"

@app.route('/')
def index():
    return render_template('index.html', info=especialista_info)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global especialista_info
    if request.method == 'POST':
        clave = request.form.get('clave')
        if clave != ADMIN_PASSWORD:
            flash("Clave incorrecta. Acceso denegado.")
            return redirect(url_for('index'))

        if 'img_especialista' in request.files:
            file = request.files['img_especialista']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                especialista_info['img_especialista'] = f'uploads/{filename}'

        if 'img_logo' in request.files:
            file = request.files['img_logo']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                especialista_info['logo'] = f'uploads/{filename}'

        if 'formulario_pdf' in request.files:
            file = request.files['formulario_pdf']
            if file.filename:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['PDF_FOLDER'], filename)
                file.save(file_path)
                especialista_info['formulario'] = f'pdf/{filename}'

        especialista_info['direccion'] = request.form.get('direccion', especialista_info['direccion'])
        especialista_info['celular'] = request.form.get('celular', especialista_info['celular'])
        especialista_info['correo'] = request.form.get('correo', especialista_info['correo'])

        if 'servicios_imgs' in request.files:
            files = request.files.getlist('servicios_imgs')
            for file in files:
                if file.filename:
                    filename = secure_filename(file.filename)
                    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(path)
                    if f'uploads/{filename}' not in especialista_info['imagenes_servicios']:
                        especialista_info['imagenes_servicios'].append(f'uploads/{filename}')

        return redirect(url_for('admin'))

    return render_template('admin.html', info=especialista_info)

@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
