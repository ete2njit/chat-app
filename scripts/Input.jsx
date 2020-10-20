import * as React from 'react';
import { Socket } from './Socket';
import "../static/inputstyle.css";

function handleSubmit(event) {
    let newMessage = document.getElementById("message");
    Socket.emit('new message input', {
        'message': newMessage.value,
    });
    
    console.log('Sent the message ' + newMessage.value + ' to server!');
    newMessage.value = '';
    
    event.preventDefault();
}

export function Input() {
    return (
        <form onSubmit={handleSubmit}>
            <input id="message" placeholder="..."></input>
            <button>Send</button>
        </form>
    );
}