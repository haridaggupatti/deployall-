import './App.css';
import InterView from './components/InterviewPage';
import ResumeUpload from './components/Resume_Upload';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ResumeInput from './components/resumeInput';
import ResumeContext from './context/resumeContext';
import { useState } from 'react';
import LoginPage from './components/Login/loginPage';

function App() {
  const [resume, setResume] = useState("");

  return (
    <div className="App">
      <ResumeContext.Provider value={{ resume, setResume }}>
        <Router>
          <Routes>
            <Route path="/" element={<InterView />} />
            <Route exact path='/login' element={<LoginPage />}></Route>
            <Route path="/resume" element={<ResumeUpload />} />
            <Route path='/update-resume' element={<ResumeInput />} />
          </Routes>
        </Router>
      </ResumeContext.Provider>
    </div>
  );
}

export default App;
