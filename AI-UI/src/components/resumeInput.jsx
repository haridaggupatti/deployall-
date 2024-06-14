import { useNavigate } from "react-router-dom";
import "./resumeInput.css";
import { useState, useEffect } from 'react';

export default function ResumeInput() {
    const [localResume, setLocalResume] = useState("");
    const [localPrompt,setLocalPrompt] = useState("")
    const navigate = useNavigate()
    useEffect(()=>{
        if (localStorage.getItem("access_token")){
            navigate("/update-resume")
        }
        else{
            navigate("/login")
        }
    })
    const handleInputChange = (event) => {
        const newResumeValue = event.target.value;
        setLocalResume(newResumeValue);
        localStorage.setItem("resume", newResumeValue);  // Save to localStorage
    };
    const handlePromptChange = (event) =>{
        const newPromptValue = event.target.value;
        setLocalPrompt(newPromptValue);
        localStorage.setItem("prompt", newPromptValue);
    }
    const handleSave = ()=>{
        console.log("Save function triggred")
        navigate("/")
    }

    useEffect(() => {
        const savedResume = localStorage.getItem("resume");
        const savedPrompt = localStorage.getItem("prompt")
        if (savedResume) {
            setLocalResume(savedResume);
        }
        if(savedPrompt){
            setLocalPrompt(savedPrompt);
        }
    }, []);

    return (
        <div className="resumeInput">
            <h2>Enter Your Resume Details</h2>
            <textarea className="input_box1" onChange={handleInputChange} value={localResume}></textarea>
            <h2>Prompt</h2>
            <textarea className="input_box2" onChange={handlePromptChange} value={localPrompt}></textarea>
            <button className="inp-box" onClick={handleSave}>Save</button>
        </div>
    );
}
