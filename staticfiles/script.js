

function getUserName() {
    return localStorage.getItem('studentName') || 'Unknown';
}

const username = document.getElementById('username').value.trim();
if (username) {
    localStorage.setItem('studentName', username);
    window.studentName = localStorage.getItem('studentName') || 'Anonymous'; // ✅ Store globally
}


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
    1: ["Linear Algebra and Calculus", "Engineering Chemistry", "Engineering Graphics", "Basics of Civil and Mechanical Engineering", "Life Skills", "Backlogs"],
    2: ["Engineering Physics", "Basics of Electrical and Electronics Engineering", "Vector Calculus Differential Equations and Transforms", "Engineering Mechanics", "Programming in C", "Professional Communication", "Backlogs"],
    3: ["Design and Engineering", "Sustainable Engineering", "Discrete Mathematical Structures", "Data Structures", "Logic System Design", "Object-Oriented Programming using Java", "Backlogs"],
    4: ["Professional Ethics", "Constitution of India", "Graph Theory", "Computer Organisation and Architecture", "Database Management Systems", "Operating Systems", "Backlogs"]
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
        for (let j = 1; j <= 6; j++) {
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
    
        if (!data.matches || Object.keys(data.matches).length === 0) {
            alert("No matches found. Try again later.");
            return;
        }
    
        console.log("📌 API Response Keys:", Object.keys(data.matches));

        const currentStudentId = localStorage.getItem("current_student_id");
        console.log("📌 Stored Student ID:", currentStudentId);

        if (!data.matches.hasOwnProperty(currentStudentId)) {
            console.warn(`⚠ No match data found for student ID ${currentStudentId}`);
            alert("No suitable matches found.");
            return;
        }

        let studentMatches = data.matches[currentStudentId];

        console.log("📌 Raw studentMatches:", studentMatches);
        console.log("📌 Type of studentMatches:", typeof studentMatches);

        // 🛠 Ensure studentMatches is always an array
        studentMatches = Array.isArray(studentMatches) ? studentMatches : [studentMatches];

        console.log("📌 Final Matches Array:", studentMatches);

        // ✅ Ensure at least 5 matches are displayed
        const topMatches = studentMatches.slice(0, 5);

        const matchedResultsDiv = document.getElementById('matchedResults');
        matchedResultsDiv.innerHTML = `<h3>Your Best Study Partners</h3>`;

        topMatches.forEach(match => {
            let matchElement = document.createElement("div");
            matchElement.classList.add("match");
            matchElement.innerHTML = `
                <p>${match.student_name_2} (Match Probability: ${match.match_probability.toFixed(2)}%)</p>
                <button onclick="openChat('${match.student_id_2}', '${match.student_name_2}')">Chat</button>
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

let currentChatSocket = null;
let currentRoomName = null;

// Function to open chat for a specific partner
function openChat(studentId, studentName) {
    console.log(`💬 Opening chat with: ${studentName} (ID: ${studentId})`);

    // Redirect to chat.html inside the 'frontend' folder
    window.location.href = 'http://127.0.0.1:8000/chat/?studentId=' + studentId + '&studentName=' + encodeURIComponent(studentName);
    const roomName = `chat_${localStorage.getItem("current_student_id")}_${studentId}`;
    const socket = new WebSocket(`ws://127.0.0.1:8000/ws/chat/${roomName}/`);

    window.currentChatSocket = socket;

    socket.onopen = function(event) {
        console.log("✅ WebSocket Connection Opened!");
    };

    socket.onmessage = function(event) {
        let data = JSON.parse(event.data);
        console.log("📩 Message from server:", data);

        let messageElement = document.createElement("div");
        messageElement.classList.add("message");
        messageElement.innerHTML = `<strong>${data.sender}:</strong> ${data.message}`;
        document.getElementById("chatMessages").appendChild(messageElement);
    };

    socket.onerror = function(event) {
        console.error("❌ WebSocket Error:", event);
    };

    socket.onclose = function(event) {
        console.log("🔴 WebSocket Connection Closed!", event);
    };
}


function sendMessage() {
    let messageInput = document.getElementById("chatInput");
    let message = messageInput.value.trim();

    if (message && window.currentChatSocket) {
        window.currentChatSocket.send(JSON.stringify({
            "sender": "You",  // Replace with actual user ID
            "message": message
        }));

        // Append sent message to chat
        let messageElement = document.createElement("div");
        messageElement.classList.add("message", "sent");
        messageElement.innerHTML = `<strong>You:</strong> ${message}`;
        document.getElementById("chatMessages").appendChild(messageElement);

        messageInput.value = "";  // Clear input
    }
}

function closeChat() {
    document.getElementById("chatContainer").style.display = "none";
    if (window.currentChatSocket) {
        window.currentChatSocket.close();
    }
}

function goToRecommendations() {
    console.log("Button clicked!");
    window.location.href = "/api/recommendations/?weak_subjects=Math&weak_subjects=Algorithms";
  }
  
  
