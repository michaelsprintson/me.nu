function show_cam() {
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 100
    });
    Webcam.attach('#my_camera');
}

window.onload = show_cam;

function take_snapshot() {
    Webcam.snap( function(data_uri) {
        document.getElementById('my_result').innerHTML = '<img src="'+data_uri+'"/>';

        Webcam.upload( data_uri, '/saveImage', function(code, text) {
            console.log(code);
			// 'code' will be the HTTP response code from the server, e.g. 200
			// 'text' will be the raw response content
		} );
        window.location.href = '/';
    } );
}