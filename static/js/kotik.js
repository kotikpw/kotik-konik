// Put event listeners into place
window.addEventListener("DOMContentLoaded", function() {
	// Grab elements, create settings, etc.
	var canvas = document.getElementById("canvas"),
	context = canvas.getContext("2d"),
	video = document.getElementById("video"),
	videoObj = { "video": true },
	errBack = function(error) { console.log("Video capture error: ", error.code); video.className = 'hidden';};
        nonDefaultImage = false;
	unknownImage = new Image;
	unknownImage.onload = function() {
		context.drawImage(unknownImage, 0, 0, 265, 200);
	};
	unknownImage.src = "avatar/";
	// Put video listeners into place
	if(navigator.getUserMedia) { // Standard
		navigator.getUserMedia(videoObj, function(stream) {
			video.src = stream;
			video.play();
		}, errBack);
	} else if(navigator.webkitGetUserMedia) { // WebKit-prefixed
		navigator.webkitGetUserMedia(videoObj, function(stream){
			video.src = window.webkitURL.createObjectURL(stream);
			video.play();
		}, errBack);
        }

	document.getElementById("video").addEventListener("click", function() {
		nonDefaultImage = true;
		context.drawImage(video, 0, 0, 265, 200);
        });
	document.getElementById("canvas").addEventListener("click", function() {
		nonDefaultImage = false;
		context.drawImage(unknownImage, 0, 0, 265, 200);
        });
	document.getElementById("registration").addEventListener("submit", function() {
		if (nonDefaultImage)
			document.getElementById("avatar").value = canvas.toDataURL();
	});
}, false);
