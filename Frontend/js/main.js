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

function loadCamera1Video() {
    // Get the iframe element by its ID
    var iframe = document.getElementById("frame");

    // Set the source URL of the iframe to the server endpoint that provides the video
    // Replace 'server_video_endpoint' with the actual URL of your video endpoint
    iframe.src = 'http://192.168.18.132:8080/get_latest_processed_frame';
}


// Function to update the video and count
// function updateVideoAndCount() {
//     // Make an AJAX request to get the latest frame and count from the server
//     fetch('http://192.168.18.132:8080/get_latest_processed_frame')
//         .then(response => response.json())
//         .then(data => {
//             // Update the iframe source with the received frame
//             const iframe = document.getElementById('frame');
//             iframe.src = `data:image/jpeg;base64, ${data.frame}`;

//             // Update the count on the web page
//             const countSpan = document.getElementById('countValue');
//             countSpan.textContent = data.count;
            
//             // Call the function again after a delay (e.g., 1000ms for 1 second)
//             setTimeout(updateVideoAndCount, 1000);
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });
// }



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
    const camera1button = document.getElementById("Cam1")

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
            updateVideoAndCount();
            console.log("update");
        });
    }

    if (camera1button) {
        camera1button.addEventListener("click", function (e) {
            e.preventDefault();
            console.log("Clicked on camera1Button");
            scrollToSection("Camera1");
            loadCamera1Video();    
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


