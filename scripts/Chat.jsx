import * as React from 'react';
import { Input } from './Input';
import { Message } from './Message';
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
        <div class="chat-window">
            <div class="chat-box">
                {chat.map((message, index) => (
                    <Message key={ index } message={ message } />))}
            </div>
            <div class="input-box">
                <Input />
            </div>
        </div>
    );
}
