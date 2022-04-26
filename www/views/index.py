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
    
	<script type="text/javascript" src="https://code.jquery.com/jquery-1.9.0.js"></script>
    <script src="https://code.jquery.com/ui/1.13.1/jquery-ui.js"></script>
	<script>
		$(function() {
			$("#tabs").tabs({
			});
		});
	</script>
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
        
        function change_url_class() {
            document.getElementById("url_class_true").value = document.getElementById("class_true").value;
                    }
        
    </script>
    <style>
    	.ui-helper-hidden {
			display: none;
		}
		.ui-helper-hidden-accessible {
			border: 0;
			clip: rect(0 0 0 0);
			height: 1px;
			margin: -1px;
			overflow: hidden;
			padding: 0;
			position: absolute;
			width: 1px;
		}
		.ui-helper-reset {
			margin: 0;
			padding: 0;
			border: 0;
			outline: 0;
			line-height: 1.3;
			text-decoration: none;
			font-size: 100%;
			list-style: none;
		}
		.ui-helper-clearfix:before,
		.ui-helper-clearfix:after {
			content: "";
			display: table;
			border-collapse: collapse;
		}
		.ui-helper-clearfix:after {
			clear: both;
		}
		.ui-helper-zfix {
			width:100%;
			height: 100%;
			top: 0;
			left: 0;
			position: absolute;
			opacity: 0;
			filter:Alpha(Opacity=0); /* support: IE8 */
		}
		.ui-front {
			z-index: 100;
		}
		
		/* Interaction Cues
		----------------------------------*/
		.ui-state-disabled {
			cursor: default !important;
			pointer-events: none;
		}

		/* Icons
		----------------------------------*/
		.ui-icon {
			display: inline-block;
			vertical-align: middle;
			margin-top: -.25em;
			position: relative;
			text-indent: -99999px;
			overflow: hidden;
			background-repeat: no-repeat;
		}
		.ui-widget-icon-block {
			left: 50%;
			margin-left: -8px;
			display: block;
		}
		.ui-tabs {
			position: relative;/* position: relative prevents IE scroll bug (element with position: relative inside container with overflow: auto appear as "fixed") */
			padding: .2em;
		}
		.ui-tabs .ui-tabs-nav {
			margin: 0;
			padding: .2em .2em 0;
		}
		.ui-tabs .ui-tabs-nav li {
			list-style: none;
			float: left;
			position: relative;
			top: 0;
			margin: 1px .2em 0 0;
			border-bottom-width: 0;
			padding: 0;
			white-space: nowrap;
		}
		.ui-tabs .ui-tabs-nav .ui-tabs-anchor {
			float: left;
			padding: .5em 1em;
			text-decoration: none;
		}
		.ui-tabs .ui-tabs-nav li.ui-tabs-active {
			margin-bottom: -1px;
			padding-bottom: 1px;
		}
		.ui-tabs .ui-tabs-nav li.ui-tabs-active .ui-tabs-anchor,
		.ui-tabs .ui-tabs-nav li.ui-state-disabled .ui-tabs-anchor,
		.ui-tabs .ui-tabs-nav li.ui-tabs-loading .ui-tabs-anchor {
			cursor: text;
		}
		.ui-tabs .ui-tabs-panel {
			display: block;
			border-width: 0;
			padding: 1em 1.4em;
			background: none;
		}
		
		/* Component containers
		----------------------------------*/
		.ui-widget {
			font-family: Arial,Helvetica,sans-serif;
			font-size: 1em;
		}
		.ui-widget .ui-widget {
			font-size: 1em;
		}

		.ui-widget.ui-widget-content {
			border: 1px solid #c5c5c5;
		}
		.ui-widget-content {
			border: 1px solid #dddddd;
			background: #ffffff;
			color: #333333;
		}
		.ui-widget-content a {
			color: #333333;
		}
		.ui-widget-header {
			border: 1px solid #dddddd;
			background: #e9e9e9;
			color: #333333;
			font-weight: bold;
		}

		/* Interaction states
		----------------------------------*/
		.ui-state-default,
		/* We use html here because we need a greater specificity to make sure disabled
		works properly when clicked or hovered */
		html .ui-button.ui-state-disabled:hover,
		html .ui-button.ui-state-disabled:active {
			border: 1px solid #c5c5c5;
			background: #f6f6f6;
			font-weight: normal;
			color: #454545;
		}

		.ui-state-hover a,
		.ui-state-hover a:hover,
		.ui-state-hover a:link,
		.ui-state-hover a:visited,
		.ui-state-focus a,
		.ui-state-focus a:hover,
		.ui-state-focus a:link,
		.ui-state-focus a:visited,
		a.ui-button:hover,
		a.ui-button:focus {
			color: #2b2b2b;
			text-decoration: none;
		}
		.ui-state-active,
		.ui-widget-content .ui-state-active,
		.ui-widget-header .ui-state-active,
		a.ui-button:active,
		.ui-button:active,
		.ui-button.ui-state-active:hover {
			border: 1px solid #003eff;
			background: #007fff;
			font-weight: normal;
			color: #ffffff;
		}
		.ui-state-active a,
		.ui-state-active a:link,
		.ui-state-active a:visited {
			color: #ffffff;
			text-decoration: none;
		}
		
		body {
			overflow: hidden;
		}
		
		table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        
        th, td {
            padding: 10px;
        }
		
        #drop_zone {
            border: 5px solid red;
            width:  200px;
            height: 100px;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-left: auto;
            margin-right: auto;
        }

        .content {
            margin: 2em;
            margin: 0 auto;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
        }
        
    </style>
    <header style="text-align: center;">
        <h1>Malware Detection with Machine Learning!!!!1</h1>
    </header>
    <body>
            <div class="content" style="text-align: center;">
                <form action="/upload" method="post" enctype="multipart/form-data">
                    Is the program goodware or malware:
                    <select id="class_true" name="class_true" onchange="change_url_class()">
                        <option value="unknown">Unknown</option>
                        <option value="goodware">Goodware</option>
                        <option value="malware">Malware</option>
                    </select><br/>
                    <div id="tabs">
                    	<ul>
                    		<li><a href="#tabs-1">File</a></li>
                    		<li><a href="#tabs-2">URL</a></li>
                		</ul>
                		<div id="tabs-1">
                    		Select a program to upload:
                    		<input type="file" name="file"><br><br>
                    		<div id="drop_zone" name="file-drop" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);">
                      	 		<p>Or drag it here</p>
                    		</div><br/>
                    		<input type="submit" value="Predict" style="padding: 5px;">
                		</div>
                	</form><br><br>
                		<div id="tabs-2">
                			Submit a URL:<br><br>
                			<form action="/classify-url" method="get">
                    			<input type="url" name="url">
                    			<input type="submit" value="Fetch and analyze image">
                    			<input type="hidden" value="unknown" id="url_class_true" name="url_class_true">
                			</form>
                		</div>
                    
                    </div>
            </div>
    </body>
    <footer style="position: absolute; bottom: 0; width: 100%; height: 2.5rem;">
        <p>Created by: <a href="http://www.github.com/bbdcmf" target="_blank">Ryan Frederick</a> & <a href="http://www.github.com/JoeyShapiro" target="_blank">Joseph Shaprio</a> and with the advising of Ricardo Calix Ph.D.</p>
    </footer>
</html>
