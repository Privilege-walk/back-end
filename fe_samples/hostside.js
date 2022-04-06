// The response you get by calling the full event QA APIs
var event_obj = {
        "id": 6,
        "name": "Harleys in Hawaii",
        "status": "created",
        "questions": [
            {
                "id": 4,
                "description": "Have you ever been to a beach?",
                "choices": [
                    {
                        "id": 10,
                        "description": "Yes",
                        "value": 1
                    },
                    {
                        "id": 11,
                        "description": "No",
                        "value": -1
                    }
                ]
            },
            {
                "id": 5,
                "description": "Do you know how to ride a motorbike?",
                "choices": [
                    {
                        "id": 12,
                        "description": "Yes",
                        "value": 1
                    },
                    {
                        "id": 13,
                        "description": "No",
                        "value": -1
                    }
                ]
            },
            {
                "id": 6,
                "description": "Do you listen to Katy Perry's songs?",
                "choices": [
                    {
                        "id": 14,
                        "description": "Yes",
                        "value": 1
                    },
                    {
                        "id": 15,
                        "description": "No",
                        "value": -1
                    }
                ]
            }
        ]
    };
var questions = event_obj["questions"];

// Websocket Connections
var walkSocket = new WebSocket("ws://localhost:8000/ws/walk/qa_control/" + event_obj["id"] + "/");
walkSocket.onopen = function (event) {
    console.log("Connected to websocket");
}


// Question control
var question_display = document.getElementById("question_title");
var current_question_number = -1;
function nextQuestion() {
    current_question_number++;
    if(current_question_number >= questions.length)
    {
        question_display.innerHTML = "Go home now, bye!";
    }
    else
    {
        question_display.innerHTML = questions[current_question_number]["description"];
    }
}