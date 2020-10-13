import * as React from 'react';
import "../static/messagestyle.css";


export function Message(props) {
    let messageType = "other"
    
    if (props.message[1] === props.username)
    {
        messageType = "own"
    }
    
    if (props.message[1].slice(props.message[1].length - 3) === "bot")
    {
        messageType = "bot"
    }
    
    
    return (
        <div className={messageType}>
            <div className="message">
                <div className="author">
                    <span>{ props.message[1] }:</span>
                </div>
                <div className="content">
                    <span>{ props.message[0] }</span>
                </div>
            </div>
        </div>
    );
}
