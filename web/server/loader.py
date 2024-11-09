import os
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename

def allowed_file(filename):
    """ Функция проверки расширения файла """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if 'file' not in request.files:
        # После перенаправления на страницу загрузки
        # покажем сообщение пользователю 
        flash('Не могу прочитать файл')
        return redirect(request.url)
    file = request.files['file']
    # Если файл не выбран, то браузер может
    # отправить пустой файл без имени.
    if file.filename == '':
        flash('Нет выбранного файла')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # безопасно извлекаем оригинальное имя файла
        filename = secure_filename(file.filename)
        # сохраняем файл
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # если все прошло успешно, то перенаправляем  
        # на функцию-представление `download_file` 
        # для скачивания файла
        return redirect(url_for('download_file', name=filename))
    return 'file error'