import * as React from 'react';

import { Socket } from './Socket';
import "../static/loginstyle.css";

export function Login(props) {
    
    function handleSubmit(event) {
        let name = document.getElementById("usernameInput");
        
        props.setName(name.value);
        
        console.log("set name to " + name.value);
        
        Socket.emit('new user', {
            'name': name.value,
        });
    
        event.preventDefault();
    }


    return (
        <div className="login">
            <h1>Welcome to &lt;TBA&gt;</h1>
            <h2>the greatest chatroom ever made!</h2>
            <h3>Type in your username below and hit enter to get started!</h3>
            <form onSubmit={handleSubmit}>
                <input id="usernameInput" placeholder=""></input>
            </form>
        </div>
    );
}