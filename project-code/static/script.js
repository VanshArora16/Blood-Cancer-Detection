document.getElementById('uploadButton').addEventListener('click', function() {
    var fileInput = document.getElementById('imageUpload');
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('image', file);

    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        var resultDiv = document.getElementById('result');
        var uploadedImage = document.getElementById('uploadedImage');
        var analysisText = document.getElementById('analysisText');
        var removeButton = document.getElementById('removeButton');

        resultDiv.style.display = 'block';
        uploadedImage.src = URL.createObjectURL(file);
        analysisText.textContent = 'Prediction: ' + data.prediction;
        removeButton.style.display = 'block';
        
        // Add event listener to remove the image
        removeButton.addEventListener('click', function() {
            resultDiv.style.display = 'none';
            uploadedImage.src = '';
            analysisText.textContent = '';
            removeButton.style.display = 'none';
            fileInput.value = ''; // Reset the file input
        });
        image.src = uploadedImage.src;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
