import * as React from 'react';

import { Socket } from './Socket';
import { GoogleButton } from "./GoogleButton"
import "../static/loginstyle.css";

export function Login(props) {
    return (
        <div className="login">
            <h1>Welcome to the Dagobah System.</h1>
            <h3>To train with Master Yoda, sign in using only your mind (or maybe google)</h3>
            <GoogleButton  />
        </div>
    );
}