<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Instant Visual Analyzer</title>
    <!-- 1. Tailwind CSS for styling -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- 2. TensorFlow.js Core library -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@latest/dist/tf.min.js"></script>
    <!-- 3. MobileNet model for image classification -->
    <script src="https://cdn.jsdelivr.net/npm/@tensorflow-models/mobilenet@latest/dist/mobilenet.min.js"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');
    </style>
</head>
<body class="bg-gray-900 text-white flex items-center justify-center min-h-screen">

    <div class="bg-gray-800 p-8 rounded-2xl shadow-2xl w-full max-w-lg text-center">
        <h1 class="text-3xl font-bold mb-2 text-cyan-400">The Instant Visual Analyzer</h1>
        <p class="text-gray-400 mb-6">Drag & Drop an image below to see the magic of AI</p>

        <!-- Drop Zone -->
        <div id="drop-zone" class="border-4 border-dashed border-gray-600 rounded-2xl p-10 cursor-pointer transition-all duration-300 hover:border-cyan-400 hover:bg-gray-700">
            <p id="drop-zone-text" class="text-gray-500">Drop an image here</p>
            <img id="preview-image" class="hidden max-h-64 mx-auto rounded-lg mt-4" />
        </div>

        <!-- Loading Spinner -->
        <div id="loader" class="hidden my-6">
            <svg class="animate-spin h-8 w-8 text-cyan-400 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="mt-2 text-gray-400">Analyzing...</p>
        </div>

        <!-- Results Area -->
        <div id="results" class="hidden mt-6 text-left">
            <h2 class="text-2xl font-semibold mb-4 text-cyan-400">AI Predictions:</h2>
            <div id="predictions" class="space-y-2"></div>
        </div>
    </div>

    <script>
        const dropZone = document.getElementById('drop-zone');
        const dropZoneText = document.getElementById('drop-zone-text');
        const previewImage = document.getElementById('preview-image');
        const loader = document.getElementById('loader');
        const resultsDiv = document.getElementById('results');
        const predictionsDiv = document.getElementById('predictions');

        let model;

        // Prevent default drag behaviors
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Highlight drop zone when item is dragged over it
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.add('border-cyan-400', 'bg-gray-700'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => dropZone.classList.remove('border-cyan-400', 'bg-gray-700'), false);
        });

        // Handle dropped files
        dropZone.addEventListener('drop', handleDrop, false);

        async function handleDrop(e) {
            let dt = e.dataTransfer;
            let file = dt.files[0];
            
            if (file && file.type.startsWith('image/')) {
                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    previewImage.classList.remove('hidden');
                }
                reader.readAsDataURL(file);

                dropZoneText.classList.add('hidden');
                resultsDiv.classList.add('hidden');
                loader.classList.remove('hidden');
                
                // Analyze the image
                await analyzeImage(previewImage);
            }
        }
        
        async function analyzeImage(imageElement) {
            if (!model) {
                // Load the model on first use
                model = await mobilenet.load();
            }
            
            const predictions = await model.classify(imageElement);
            
            loader.classList.add('hidden');
            displayPredictions(predictions);
        }

        function displayPredictions(predictions) {
            predictionsDiv.innerHTML = ''; // Clear previous results
            if (predictions && predictions.length > 0) {
                predictions.forEach(prediction => {
                    const probability = (prediction.probability * 100).toFixed(2);
                    
                    const p = document.createElement('div');
                    p.className = 'bg-gray-700 p-3 rounded-lg flex items-center justify-between';
                    
                    const name = document.createElement('span');
                    name.className = 'text-gray-200 text-lg';
                    name.innerText = prediction.className.split(',')[0]; // Show only the first name
                    
                    const prob = document.createElement('span');
                    prob.className = 'text-cyan-400 font-semibold';
                    prob.innerText = `${probability}%`;

                    p.appendChild(name);
                    p.appendChild(prob);
                    predictionsDiv.appendChild(p);
                });
                resultsDiv.classList.remove('hidden');
            } else {
                predictionsDiv.innerHTML = '<p class="text-red-400">Could not identify the object.</p>';
            }
        }

    </script>
</body>
</html>
