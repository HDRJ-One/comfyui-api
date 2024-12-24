// Function to fetch all generated images
function fetchAllGeneratedImages() {
    fetch('/get_images')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const imageTableBody = document.getElementById('imageTableBody');
            imageTableBody.innerHTML = ''; // Clear existing images

            // Populate the table with images
            data.images.forEach(image => {
                const row = `<tr>
                    <td>${image.name}</td>
                    <td><img src="output/${image.name}" class="img-thumbnail" width="512" height="512" alt="${image.name}"></td>
                </tr>`;
                imageTableBody.innerHTML += row;
            });

            // Update the last generated image
            if (data.images.length > 0) {
                const lastImage = data.images[data.images.length - 1]; // Assuming the last image is the newest
                document.getElementById('lastGeneratedImage').src = `output/${lastImage.name}`;
            } else {
                // Handle case where no images are available
                const lastImage = document.getElementById('lastGeneratedImage');
                lastImage.src = ''; // Clear the image
                lastImage.alt = 'No images available';
            }
        })
        .catch(error => {
            console.error('Error fetching generated images:', error);
        });
}

// Call the function to fetch all generated images on page load
window.onload = function() {
    fetchAllGeneratedImages(); // Fetch all images on load

    // Poll for new images every 5 seconds
    setInterval(fetchAllGeneratedImages, 5000);
};

// Generate a new image
fetch('/generate_image', {
    method: 'POST'
})
.then(response => response.json())
.then(data => {
    if (data.image) {
        document.getElementById('lastGeneratedImage').src = 'data:image/png;base64,' + data.image;
    }
    // Call to refresh the images after generation
    fetchAllGeneratedImages();
});

// Generate a new image
fetch('/generate_image', {
    method: 'POST'
})
.then(response => response.json())
.then(data => {
    if (data.image) {
        document.getElementById('lastGeneratedImage').src = 'data:image/png;base64,' + data.image;
    }
    // Call to refresh the images after generation
    fetchAllGeneratedImages();
});

// Generate a new image
fetch('/generate_image', {
    method: 'POST'
})
.then(response => response.json())
.then(data => {
    if (data.image) {
        document.getElementById('lastGeneratedImage').src = 'data:image/png;base64,' + data.image;
    }
    // Call to refresh the images after generation
    fetchAllGeneratedImages();
});
