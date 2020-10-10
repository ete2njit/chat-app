import * as React from 'react';
import { Socket } from './Socket';
import { Input } from './Input';
import "../static/chatstyle.css";


export function Chat(props) {
    let chat = [];
    let chatLength = props.chatlog.length;

    if(props.displayCount == 0)
        chat = props.chatlog;
    else
        for(let i = 0; i < chatLength && (props.displayCount == 0 || i < props.displayCount); i++)
        {
            chat[props.displayCount-i] = props.chatlog[chatLength-1-i];
        }
    
    return (
        <div class="chat-box">
            <ol>
                {chat.map((address, index) =>
                    <li key={index}>{address}</li>)}
            </ol>
            <Input />
        </div>
    );
}
