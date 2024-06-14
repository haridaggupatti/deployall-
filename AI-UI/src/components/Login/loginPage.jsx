import { useState } from "react"
import "./login.css"
import {  useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons';

export default function LoginPage() {
    const [cred, setCred] = useState({ email: "", password: "" })
    const navigate = useNavigate()
    const [showPassword, setShowPassword] = useState(false)
    const [error, setError] = useState(null);

    const handleonchange = (event) => {
        setCred({ ...cred, [event.target.name]: event.target.value })
    }

    const handlePassword = () => {
        setShowPassword(!showPassword)
    }
    const handleLogin = async (event) => {
        event.preventDefault()
        setError(null); // Reset error before new login attempt
        try {
            const response = await fetch("http://127.0.0.1:8000/api/users/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email: cred.email, password: cred.password })
            })
            const resp = await response.json()
            if (response.status === 200) {
                localStorage.setItem('access_token', resp.access_token)
                navigate("/")
            } else {
                throw new Error(resp.message || "Failed to login");
            }
        } catch (error) {
            setError(error.message);
        }
    }

    return (
        <div className="login-box">
            <div className="left-container">
                <form onSubmit={handleLogin}>
                    <h2 id="login-cotation">Login in to Crack Your Interview</h2>
                    <p>Choose a job you love, and you will never have to work a day in your life.</p>
                    <div className="form-box">
                        <label htmlFor="email">Email Id</label>
                        <input type="text" onChange={handleonchange} name="email" value={cred.email} placeholder="Email" />
                        <label htmlFor="">Password</label>
                        <input type={showPassword ? "text" : "password"} id="" onChange={handleonchange} name="password" value={cred.password} placeholder="Password" />
                        <FontAwesomeIcon
                            id="toggle-Password"
                            icon={showPassword ? faEye : faEyeSlash}
                            onClick={handlePassword}
                            style={{ cursor: 'pointer', marginLeft: '5px' }}
                        />
                        {/* <Link id="forgot-anch" to="/email-otp">Forgot Password?</Link>
                        <Link id="create-account" to="/register">Don't have an account?<span id="resend-span" >Create an account</span> </Link> */}
                        <button id="login-button">Login</button>
                    </div>
                    {error && <p className="error">{error}</p>} {/* Display error message if error exists */}
                </form>

            </div>
            <div className="right-container"></div>
        </div>
    )
}