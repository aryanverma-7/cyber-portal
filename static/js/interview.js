let recognition;

let currentQuestion = "";

let totalQuestions = 5;

let currentQuestionNo = 0;

let totalScore = 0;

function speakText(text){

    let speech =
        new SpeechSynthesisUtterance(
            text
        );

    speech.rate = 1;

    speech.pitch = 1;

    speech.lang = "en-US";

    speechSynthesis.speak(
        speech
    );
}

function startVoiceRecognition(){

    if(
        !(
            'webkitSpeechRecognition'
            in window
        )
    ){
        alert(
            "Speech Recognition Not Supported"
        );
        return;
    }

    recognition =
        new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    recognition.onresult =
    function(event){

        let transcript =
        event.results[0][0].transcript;

        document.getElementById(
            "answer"
        ).value =
        transcript;

    };
}

async function startInterview(){

    currentQuestionNo = 0;

    totalScore = 0;

    await getQuestion();
}

async function getQuestion(){

    let role =
    document.getElementById(
        "role"
    ).value;

    let response =
    await fetch(
        "/interview/question",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                role:role
            })
        }
    );

    let data =
    await response.json();

    currentQuestion =
    data.question;

    document.getElementById(
        "question"
    ).innerHTML =
    currentQuestion;

    speakText(
        currentQuestion
    );

}

async function submitAnswer(){

    let role =
    document.getElementById(
        "role"
    ).value;

    let answer =
    document.getElementById(
        "answer"
    ).value;

    document.getElementById(
        "result"
    ).innerHTML =
    `
    <div class="alert alert-info">
    Evaluating...
    </div>
    `;

    let response =
    await fetch(
        "/interview/evaluate",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                role:role,
                question:currentQuestion,
                answer:answer
            })
        }
    );

    let data =
    await response.json();

    currentQuestionNo++;

    let progress =
    (
        currentQuestionNo /
        totalQuestions
    ) * 100;

    document.getElementById(
        "progressBar"
    ).style.width =
    progress + "%";

    document.getElementById(
        "progressBar"
    ).innerHTML =
    Math.round(progress) + "%";

    document.getElementById(
        "result"
    ).innerHTML =
    `
    <div class="card p-3">

    <h4>
    AI Evaluation
    </h4>

    <pre style="white-space:pre-wrap">
${data.result}
    </pre>

    </div>
    `;

    document.getElementById(
        "answer"
    ).value = "";

    if(
        currentQuestionNo <
        totalQuestions
    ){

        setTimeout(
            getQuestion,
            2000
        );

    }
    else{

        document.getElementById(
            "question"
        ).innerHTML =
        "Interview Completed";

        speakText(
            "Interview Completed"
        );
    }
}

async function generateResumeQuestion(){

    let resumeText =
    prompt(
        "Paste Resume Text"
    );

    let response =
    await fetch(
        "/interview/resume-question",
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                resume_text:resumeText
            })
        }
    );

    let data =
    await response.json();

    currentQuestion =
    data.question;

    document.getElementById(
        "question"
    ).innerHTML =
    currentQuestion;

    speakText(
        currentQuestion
    );
}

async function getFinalScore(
    currentQuestion,
    answer
){

    const response =
    await fetch(
        "/interview/final-score",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                question:question,
                answer:answer
            })
        }
    );

    const data =
    await response.json();

    document.getElementById(
        "scoreCard"
    ).innerHTML =
    `
    <pre>
${data.result}
    </pre>
    `;
}