import * as React from 'react';
import { MessageContent } from "./MessageContent";
import "../static/messagestyle.css";


export function Message(props) {
    let messageType = "other";
    
    if (props.message[1] === props.username)
    {
        messageType = "own";
    }
    
    if (props.message[1].endsWith("bot"))
    {
        messageType = "bot";
    }
    
    return (
        <div className={messageType}>
            <div className="message">
                <div className="author">
                    <span> <img className="profilepicture" src={ props.message[3] } />{ props.message[1] }:</span>
                </div>
                <div className="content">
                    <MessageContent content={ props.message[0] } type={ props.message[4] } />
                </div>
            </div>
        </div>
    );
}
