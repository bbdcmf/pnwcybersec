from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == 'GET':
        return HttpResponse('''
    <!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Malware Detection with Machine Learning</title>
    </head>
    <script>
        function dropHandler(ev) {
        console.log('File(s) dropped');
            // Prevent default behavior (Prevent file from being opened)
            ev.preventDefault();

            if (ev.dataTransfer.items) {
                // Use DataTransferItemList interface to access the file(s)
                for (var i = 0; i < ev.dataTransfer.items.length; i++) {
                // If dropped items aren't files, reject them
                if (ev.dataTransfer.items[i].kind === 'file') {
                    var file = ev.dataTransfer.items[i].getAsFile();
                    console.log('... file[' + i + '].name = ' + file.name);
                    let formData = new FormData();
                    formData.append("file", file);
                    fetch('', {method: "POST", body: formData});
                }
                }
            } else {
                // Use DataTransfer interface to access the file(s)
                for (var i = 0; i < ev.dataTransfer.files.length; i++) {
                console.log('... file[' + i + '].name = ' + ev.dataTransfer.files[i].name);
                }
            }
        }

        function dragOverHandler(ev) {
            console.log('File(s) in drop zone');

            // Prevent default behavior (Prevent file from being opened)
            ev.preventDefault();
        }
    </script>
    <style>
        #drop_zone {
            border: 5px solid red;
            width:  200px;
            height: 100px;
        }
    </style>
    <body>
        <h1>Malware Detection & Analysis with Machine Learning</h1>
        <h2>Created by: <a href="http://www.github.com/bbdcmf" target="_blank">Ryan Frederick</a> & <a href="http://www.github.com/JoeyShapiro" target="_blank">Joseph Shaprio</a></h2>
        <h2>With the advising of Ricardo Calix Ph.D.</h2>

        <div id="drop_zone" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);">
            <p>Drag one or more files to this Drop Zone ...</p>
        </div>
    </body>
</html>
    ''')

    elif request.method == 'POST':
        upload_file(request)

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('questionable.exe', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)