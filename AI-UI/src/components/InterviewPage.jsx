import "./InterviewPage.css";
import { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from "react-router-dom";

export default function InterviewPage() {
    const [responseData, setResponseData] = useState('');
    const [start, setStart] = useState("");
    const [speech, setSpeech] = useState("");
    const [text, setText] = useState(false);
    const [textareaeditor, setTextareaeditor] = useState("text area editor")
    const speechRef = useRef(speech);
    const navigate = useNavigate()

    useEffect(()=>{
        if (localStorage.getItem("access_token")){
            navigate("/")
        }
        else{
            navigate("/login")
        }
    })

    const handleInputChange = (event) => {
        setSpeech(event.target.value);
        speechRef.current = event.target.value;
    };

    const handleFetchData = async (event) => {
        event.preventDefault();
        setStart("Fetching Answer");
        const resume = localStorage.getItem("resume"); 
        const prompt = localStorage.getItem("prompt"); 
        console.log(prompt) 
        try {
            const response = await fetch("http://127.0.0.1:8000/api/get_answer", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "prompt_text": speechRef.current,
                    "resume_context": resume || "" ,
                    "resume_prompt" : prompt
                })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const resp = await response.json();
            setResponseData(resp);
            console.log(resp);
        } catch (error) {
            console.error('Failed to fetch data:', error);
        }
    };

    const handleStart = async (event) => {
        event.preventDefault();
        setText(true)
        setTimeout(() => {
            setStart("Start Speaking");
        }, 1200);
        try {
            const response = await fetch("http://127.0.0.1:8000/api/start-recognition", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const resp = await response.json();
            setSpeech(resp);
            speechRef.current = resp; // Update the ref when speech is set
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    };


    const handleInputChangearea = event =>{
        setTextareaeditor(event.target.value)
    }


    const handleStop = async (event) => {
        event.preventDefault();
        setText(false)
        try {
            const response = await fetch("http://127.0.0.1:8000/api/stop-recognition", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            await response.json();
            setStart("Listening Stopped");
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
    };

    return (
        <>
            <Link id="upload_resume" to="/update-resume">Upload Resume</Link>
            <button id="started">{start}</button>
            <div className="interview-box">
            {text && (
                <div className="paragra1">
                 <textarea style={{ whiteSpace: "pre-wrap", textAlign: "left", resize: "vertical" }} id="input3" className="input_box_textarea" onChange={handleInputChangearea} value={textareaeditor} />
            </div>
            ) }
            <br/>
                <div className="paragra">
                    <pre id="input1" style={{ whiteSpace: "pre-wrap" }}>{responseData}</pre>
                </div>
                <div className="inp-box">
                    <textarea style={{ whiteSpace: "pre-wrap", textAlign: "left", resize: "vertical" }} id="input2" className="input_box" onChange={handleInputChange} value={speech} />
                    <button onClick={handleStart}>Open</button>
                    <button onClick={handleStop}>Close</button>
                    <button onClick={handleFetchData}>Get Answer</button>
                </div>
            </div>
        </>
    );
}
