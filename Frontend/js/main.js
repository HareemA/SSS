// Function to scroll to a section smoothly
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        window.scrollTo({
            top: section.offsetTop,
            behavior: 'smooth'
        });
    }
}

function getvideo() {
    const iframe = document.getElementById("frame");
    const countSpan = document.getElementById('countValue');
            
    async function fetchAndUpdate() {
        try {
            
            const response = await fetch('http://192.168.100.10:8080/get_latest_processed_frame'); // Update the URL if needed
    
            if (response.status === 200) {
                const data = await response.json();
                
                // Decode and set the frame source
                const imageData = data.frame; // Assuming data.frame contains the Latin1 encoded image data
    
                // Create an ArrayBuffer from the Latin1 encoded string
                const buffer = new ArrayBuffer(imageData.length);
                const view = new Uint8Array(buffer);
                for (let i = 0; i < imageData.length; i++) {
                    view[i] = imageData.charCodeAt(i) & 0xff;
                }
                
    
                // Create a Blob from the ArrayBuffer and set it as the source of the image
                const blob = new Blob([buffer], { type: 'image/jpeg' }); // Adjust the type as needed
                const imageUrl = URL.createObjectURL(blob);
                
                // Create an <img> element
                const img = new Image();
    
                // Set dimensions for the image (adjust these values as needed)
                img.width = 560; // Set the desired width
                img.height = 315; // Set the desired height
    
                // Set the image source to the Object URL
                img.src = imageUrl;
    
                // Replace the iframe's content with the image
                iframe.contentDocument.body.innerHTML = ''; // Clear previous content
                iframe.contentDocument.body.appendChild(img);
    
                // Update the count on the web page
                countSpan.textContent = data.count;
                console.log(data.count);
            } else {
                console.error('Error fetching data. Status:', response.status);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
            // Handle errors if necessary
            return;
        }
        
        // Call the function again after a delay to continuously send requests
        setTimeout(fetchAndUpdate, 0); // Adjust the delay as needed (e.g., 1000 ms = 1 second)
    }
    fetchAndUpdate()
}


// Initialize the Typed.js instance
var typed = new Typed(".text", {
    strings: ["Person Count", "Gender Determination", "Group Differentiation", "Time Tracking"],
    typeSpeed: 100,
    backSpeed: 100,
    backDelay: 1000,
    loop: true
});

document.addEventListener("DOMContentLoaded", function () {
    const homeLink = document.getElementById("homeLink");
    const camera1Link = document.getElementById("camera1Link");
    const camera2Link = document.getElementById("camera2Link");
    const camera3Link = document.getElementById("camera3Link");
    const camera1button = document.getElementById("Cam1");

    if (homeLink) {
        homeLink.addEventListener("click", function (e) {
            e.preventDefault();
            scrollToSection("home");
        });
    }

    if (camera1Link) {
        camera1Link.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Clicked on camera1Link");
            scrollToSection("Camera1");
            getvideo(); // Start fetching and updating
            console.log("update");
        });
    }

    if (camera1button) {
        camera1button.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Clicked on camera1Button");
            scrollToSection("Camera1");
            getvideo(); // Start fetching and updating
        });
    }

    // if (camera2Link) {
    //     camera2Link.addEventListener("click", function (e) {
    //         e.preventDefault();
    //         scrollToSection("camera2");
    //     });
    // }

    // if (camera3Link) {
    //     camera3Link.addEventListener("click", function (e) {
    //         e.preventDefault();
    //         scrollToSection("camera3");
    //     });
    // }
});


