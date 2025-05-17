document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM Loaded");

    const usernameInput = document.getElementById('username');
    if (usernameInput) {
        const username = usernameInput.value.trim();
        if (username) {
            localStorage.setItem('studentName', username);
            window.studentName = username;
            console.log(`✅ Username set to: ${username}`);
        } else {
            console.warn("⚠️ Username is empty!");
        }
    } else {
        console.log("🟡 Skipping username input setup (Not on login page)");
    }
});



console.log("Script loaded successfully!");


// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}

// KTU CSE 2019 Scheme Subjects for each semester
const ktuSubjects = {
    1: ["Linear Algebra and Calculus", "Engineering Chemistry", "Engineering Graphics", "Basics of Civil and Mechanical Engineering", "Life Skills"],
    2: ["Engineering Physics", "Basics of Electrical and Electronics Engineering", "Vector Calculus Differential Equations and Transforms", "Engineering Mechanics", "Programming in C", "Professional Communication"],
    3: ["Design and Engineering", "Sustainable Engineering", "Discrete Mathematical Structures", "Data Structures", "Logic System Design", "Object-Oriented Programming using Java"],
    4: ["Professional Ethics", "Constitution of India", "Graph Theory", "Computer Organisation and Architecture", "Database Management Systems", "Operating Systems"]
    
};

// Function to generate semester cards with subjects
function generateSemesters() {
    const container = document.getElementById('semesters-container');
    if (!container) return;

    container.innerHTML = "";

    for (let semester = 1; semester <= 4; semester++) {
        const semesterDiv = document.createElement('div');
        semesterDiv.className = 'semester';
        semesterDiv.innerHTML = `
            <h3>Semester ${semester}</h3>
            <div class="semester-subjects">
                ${ktuSubjects[semester].map((subject, index) => `
                    <div class="subject-row">
                        <label for="grade${semester}_${index + 1}">${subject}:</label>
                        <input type="text" id="grade${semester}_${index + 1}" name="grade${semester}_${index + 1}" required>
                    </div>
                `).join('')}
            </div>
            <div class="backlog-section">
                <label for="backlogs${semester}">Backlogs:</label>
                <textarea id="backlogs${semester}" name="backlogs${semester}"></textarea>
            </div>
        `;
        container.appendChild(semesterDiv);
    }
}
// Ensure semester details are generated on load
document.addEventListener("DOMContentLoaded", function() {
    console.log("✅ DOM Loaded - Generating Semesters");
    generateSemesters();
});


// Function to save student data and send it to the backend
function saveStudentData() {
    const formData = new FormData();

    // Collect data from the first page
    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    formData.append('username', username);
    formData.append('email', email);

    // Collect data from the semester form
    for (let i = 1; i <= 4; i++) {
        for (let j = 1; j <= 4; j++) {
            const grade = document.getElementById(`grade${i}_${j}`).value.trim();
            formData.append(`grade${i}_${j}`, grade);
        }
        const backlogs = document.getElementById(`backlogs${i}`).value.trim();
        formData.append(`backlogs${i}`, backlogs);
    }

    // Collect data from the preferences form
    const preferencesForm = document.getElementById('preferences-form');
    new FormData(preferencesForm).forEach((value, key) => {
        formData.append(key, value);
    });

    fetch("http://127.0.0.1:8000/api/save-student/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        console.log("✅ Data saved:", data);
        alert("Student data saved successfully!");
        // Store the current student ID for matching
        localStorage.setItem("current_student_id", data.student_id);
    })
    .catch(error => console.error("❌ Error:", error));
}

// Function to find matches for the current student
function findMatches() {
    console.log("findMatches function called!");
     // Get the spinner element and show it
     const spinner = document.getElementById("loading-spinner");
     if (spinner) {
         spinner.style.display = "block";
     }
   

    const current_student_id = localStorage.getItem("current_student_id");
    if (!current_student_id) {
        alert("Please save your data first before finding matches.");
        return;
    }

    fetch("http://127.0.0.1:8000/api/train/", {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
        body: JSON.stringify({ current_student_id: current_student_id })
    })
    .then(res => res.json())
    .then(data => {
        console.log("✅ Matches from API:", data);
        // Hide spinner after receiving the response
        if (spinner) {
            spinner.style.display = "none";
        }

        if (!data.matches || data.matches.length === 0) {
            alert("No matches found. Try again later.");
            return;
        }

        // ✅ Directly take the top 5 matches from the array
        let topMatches = data.matches.slice(0, 5);

        const matchedResultsDiv = document.getElementById('matchedResults');
        matchedResultsDiv.innerHTML = `<h3>Your Best Study Partners</h3>`;

        topMatches.forEach(match => {
            console.log("📌 Match Object:", match);

            // ✅ Use correct keys from API response
            let studentId = match.student_id_2;  
            let studentName = match.student_name_2;  

            if (!studentId || !studentName) {
                console.error("❌ Error: studentId or studentName is missing!", match);
                return;
            }

            let matchElement = document.createElement("div");
            matchElement.classList.add("match");
            matchElement.innerHTML = `
                <p class="match-name">${studentName}</p>
                <button onclick="openChat('${studentId}', '${studentName}')">Chat</button>
            `;
            matchedResultsDiv.appendChild(matchElement);
        });
    })
    .catch(error => {
        console.error("❌ Fetch Error:", error);
        alert(`Error finding matches: ${error.message}`);
    });
}


// Navigation Functions
window.nextPage = function(pageNumber) {
    window.showPage(pageNumber);
    console.log(typeof nextPage); // Should log 'function'
};

window.showPage = function(pageNumber) {
    const pages = document.querySelectorAll('.form-container > div');
    pages.forEach(page => page.style.display = 'none');

    const targetPage = document.getElementById(`page${pageNumber}`);
    if (targetPage) targetPage.style.display = 'block';
    console.log(`✅ Showing Page ${pageNumber}`);
};

// Add previousPage function
window.previousPage = function(pageNumber) {
    window.showPage(pageNumber);
};

// Fixing Submit Button Click Issue
document.addEventListener("DOMContentLoaded", function () {
    const submitBtn = document.getElementById("submit-btn");

    if (!submitBtn) {
        console.error("❌ Button with ID 'submit-btn' not found!");
        return;
    }

    submitBtn.addEventListener("click", function (event) {
        event.preventDefault(); // Prevent form from refreshing

        console.log("✅ Submit Button Clicked!");

        // Ensure required fields are filled
        const username = document.getElementById("username").value.trim();
        const email = document.getElementById("email").value.trim();

        if (!username || !email) {
            alert("Please fill in all required fields before submitting.");
            return;
        }

        // Call function to save student data to backend
        saveStudentData();
    });
});
// ✅ Global Variables
var socket = null;
var currentRoomName = null;
var client = null;

// ✅ Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ DOM Loaded");

    setTimeout(() => {
        const messageInput = document.getElementById('chatInput');
        if (messageInput) {
            messageInput.addEventListener('keypress', (event) => {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            });
        } else {
            console.warn("⚠️ chatInput element not found!");
        }

        const chatTitleElement = document.getElementById("chatTitle");
        if (chatTitleElement) {
            chatTitleElement.innerText = `Chat with ${window.studentName || 'Anonymous'}`;
        } else {
            console.warn("⚠️ chatTitle element not found!");
        }
    }, 500);

    // ✅ WebSocket Initialization
    const urlParams = new URLSearchParams(window.location.search);
    const studentId = urlParams.get('studentId') || localStorage.getItem("chatStudentId");
    window.studentName = urlParams.get('studentName') || localStorage.getItem("chatStudentName") || 'Anonymous';

    if (!studentId) {
        console.error("❌ Error: studentId is missing!");
        alert("Error: studentId is missing!");
        return;
    }

    currentRoomName = `chat_${localStorage.getItem("current_student_id")}_${studentId}`;
    console.log("🌐 Room Name:", currentRoomName);

    if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.log("⚠️ Initializing new WebSocket connection...");
        socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${currentRoomName}/`);

        socket.onopen = () => console.log(`✅ Connected to room: ${currentRoomName}`);
        socket.onerror = (error) => console.error("❌ WebSocket Error:", error);
        socket.onclose = (event) => console.log(`🔴 WebSocket closed: ${event.reason || 'Connection closed'}`);

        socket.onmessage = (event) => {
            let data = JSON.parse(event.data);
            console.log("📩 Message from server:", data);

            let chatBox = document.getElementById("chatMessages");
            if (!chatBox) {
                console.error("❌ Chat container not found!");
                return;
            }

            let messageElement = document.createElement("div");
            messageElement.classList.add("message", data.sender === window.studentName ? "sent" : "received");
            messageElement.innerHTML = `
                ${data.message}
                <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            `;
            chatBox.appendChild(messageElement);
            chatBox.scrollTop = chatBox.scrollHeight;
        };
    }
});

// ✅ Open Chat
window.openChat = function(studentId, studentName) {
    console.log("🔄 openChat() function triggered!");

    if (!studentId) {
        console.error("❌ Error: studentId is missing!");
        alert("Error: studentId is missing!");
        return;
    }

    const currentStudentId = localStorage.getItem("current_student_id");
    if (!currentStudentId) {
        console.error("❌ Error: current_student_id is not set in localStorage!");
        return;
    }

    localStorage.setItem("chatStudentId", studentId);
    localStorage.setItem("chatStudentName", studentName);

    window.location.href = `/chat/?studentId=${studentId}&studentName=${encodeURIComponent(studentName)}`;
};
function sendMessage() {
    const messageInput = document.getElementById('chatInput');
    if (!messageInput) {
        console.error("❌ Error: chatInput element not found!");
        alert("Error: chat input field not found!");
        return;
    }

    const message = messageInput.value.trim();
    if (!message) {
        console.error("❌ Error: Empty message cannot be sent!");
        alert("Cannot send an empty message!");
        return;
    }

    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            sender: window.studentName || 'TestUser',
            message: message
        }));

        console.log('🔜 Message sent:', message);

        const messageElement = document.createElement('div');
        messageElement.classList.add('message', 'sent');
        messageElement.innerHTML = `
            ${message}
            <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
        `;
        document.getElementById('chatMessages').appendChild(messageElement);

        messageInput.value = "";
        document.getElementById('chatMessages').scrollTop = document.getElementById('chatMessages').scrollHeight;
    } else {
        console.error('❌ Error: Socket not initialized or message is empty');
        alert('Socket is not connected yet!');
    }
}




// ✅ Upload File
function uploadFile(event) {
    const file = event.target.files[0];
    if (!file) {
        console.error("❌ No file selected");
        return;
    }

    console.log("📎 File selected:", file.name);

    const formData = new FormData();
    formData.append('file', file);

    fetch('/api/chat/upload/', { // ✅ Make sure this URL matches your Django endpoint!
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCSRFToken() // ✅ Include CSRF token if needed
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log("✅ File uploaded:", data);

        if (data.file_url && data.file_type) {
            // ✅ Build different HTML based on file_type
            let messageHTML;
            if (data.file_type.includes("image")) {
                // Show an inline image preview
                messageHTML = `<img src="${data.file_url}" alt="Uploaded image" style="max-width: 200px; border-radius: 8px;" />`;
            } else if (data.file_type.includes("pdf")) {
                // Provide a direct PDF link
                messageHTML = `<a href="${data.file_url}" target="_blank" download>📎 View PDF</a>`;
            } else {
                // Generic file link for docx, txt, etc.
                messageHTML = `<a href="${data.file_url}" target="_blank" download>📎 Download ${file.name}</a>`;
            }

            // ✅ Send the HTML snippet over WebSocket
            if (socket && socket.readyState === WebSocket.OPEN) {
                const fileMessage = {
                    sender: window.studentName || "TestUser",
                    type: "file",
                    message: messageHTML
                };
                socket.send(JSON.stringify(fileMessage));
                console.log("📎 File URL sent:", data.file_url);
            } else {
                console.error("❌ Error: WebSocket not connected");
            }
        } else {
            console.error("❌ No file_url or file_type returned from server");
        }
    })
    .catch(error => {
        console.error("❌ Upload failed:", error);
        alert("Failed to upload file!");
    });
}

// ✅ Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken'))
        ?.split('=')[1];
}


// ✅ Close Chat
function closeChat() {
    if (socket) {
        socket.close();
        socket = null;
        console.log('🔴 Chat Closed');
    }
    window.location.href = "/";
}

// ✅ Record Voice (Placeholder)
function recordVoice() {
    alert("🎙️ Voice recording feature coming soon!");
}

// Global variables for voice recording
let voiceRecorder;
let voiceChunks = [];

// Function to start voice recording
function startVoiceRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            voiceRecorder = new MediaRecorder(stream);
            voiceRecorder.start();
            voiceChunks = [];
            console.log("🎙️ Recording started...");

            voiceRecorder.ondataavailable = event => {
                voiceChunks.push(event.data);
            };

            voiceRecorder.onstop = () => {
                const audioBlob = new Blob(voiceChunks, { type: 'audio/webm' });
                const audioUrl = URL.createObjectURL(audioBlob);
                // Preview the recorded audio (optional)
                displayVoiceMessage(audioUrl);

                // Prepare form data to send the audio to backend
                const formData = new FormData();
                formData.append('audio_file', audioBlob, 'voice_message.webm');
                formData.append('sender_id', localStorage.getItem("current_student_id")); // Assumes current student ID is stored

                fetch('/api/upload_voice_message/', { // Adjust URL if needed
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: formData
                })
                .then(res => res.json())
                .then(data => {
                    console.log("✅ Voice message upload response:", data);
                })
                .catch(error => console.error("❌ Voice message upload error:", error));
            };
        })
        .catch(error => {
            console.error("❌ Error accessing microphone:", error);
            alert("Error accessing your microphone.");
        });
}

// Function to stop voice recording
function stopVoiceRecording() {
    if (voiceRecorder && voiceRecorder.state !== "inactive") {
        voiceRecorder.stop();
        console.log("🎙️ Recording stopped.");
    }
}

// Function to display the recorded voice message in the chat UI
function displayVoiceMessage(audioUrl) {
    const chatBox = document.getElementById("chatMessages");
    if (!chatBox) {
        console.error("❌ Chat container not found!");
        return;
    }
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", "sent"); // mark as sent
    messageElement.innerHTML = `
        <audio controls>
            <source src="${audioUrl}" type="audio/webm">
            Your browser does not support the audio element.
        </audio>
        <span class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
    `;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Modified recordVoice function toggles recording on and off
function recordVoice() {
    const recordBtn = document.getElementById("recordVoiceBtn");
    if (!voiceRecorder || voiceRecorder.state === "inactive") {
        // Start recording
        startVoiceRecording();
        recordBtn.innerText = "Stop Recording";
    } else {
        // Stop recording
        stopVoiceRecording();
        recordBtn.innerText = "Record Voice";
    }
}
function goToRecommendations() {
    const studentId = localStorage.getItem("current_student_id");

    if (!studentId || studentId === "undefined") {
        alert("Student ID not found in localStorage! 🫠");
        console.error("🚨 studentId is missing or undefined:", studentId);
        return;
    }

    fetch(`/api/get_student_data?studentId=${studentId}`)
        .then(res => res.json())
        .then(data => {
            const weakSubjects = data.weak_subjects || [];
            const backlogs = data.backlogs || [];

            const queryParams = new URLSearchParams();
            queryParams.append("studentId", studentId); // this was missing before!

            weakSubjects.forEach(subject => queryParams.append("weak_subjects", subject));
            backlogs.forEach(subject => queryParams.append("backlogs", subject));

            const redirectURL = `/recommendations/?${queryParams.toString()}`;
            console.log("🔗 Redirecting to:", redirectURL);
            window.location.href = redirectURL;
        })
        .catch(err => {
            console.error("❌ Error fetching student data:", err);
            alert("Couldn't fetch recommendation data 😞");
        });
}


