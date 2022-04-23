<!--
    if we want 100% ptyhon is this cheating
    if it is, then we can change this to '.txt'.
    i dont think github counts '.txt'
-->

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
                        let fileInput = document.querySelector('input');
                        fileInput.files = ev.dataTransfer.files;
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
        <h3>Malware Detection with Machine Learning<h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            Is the program goodware or malware:
            <select id="class_true" name="class_true">
                <option value="unknown">Unknown</option>
                <option value="goodware">Goodware</option>
                <option value="malware">Malware</option>
            </select><br/>
            Select program to upload:
            <input type="file" name="file">
            <div id="drop_zone" name="file-drop" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);">
                <p>Drag one or more files to this Drop Zone ...</p>
            </div>
            <input type="submit" value="Predict">
        </form>
        Or submit a URL:
        <form action="/classify-url" method="get">
            <input type="url" name="url">
            <input type="submit" value="Fetch and analyze image">
        </form>
    </body>
    <footer>
        <p>Created by: <a href="http://www.github.com/bbdcmf" target="_blank">Ryan Frederick</a> & <a href="http://www.github.com/JoeyShapiro" target="_blank">Joseph Shaprio</a></p>
        <p>With the advising of Ricardo Calix Ph.D.</p>
    </footer>
</html>