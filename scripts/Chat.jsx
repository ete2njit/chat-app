import * as React from 'react';
import { Input } from './Input';
import { Message } from './Message';
import { Socket } from './Socket';
import "../static/chatstyle.css";


export function Chat(props) {
    const [chatlog, setChatlog] = React.useState([]);
    let chat = [];
    
    function getAllMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received messages from server " + data['allMessages']);
                setChatlog(data['allMessages'])
            })
        });
    }
    

    if(props.displayCount == 0)
        chat = chatlog;
    else
        for(let i = 0; i < chatlog.length && (props.displayCount == 0 || i < props.displayCount); i++)
        {
            chat[props.displayCount-i] = chatlog[chatlog.length-1-i];
            
        }
        
    getAllMessages();
    
    return (
        <div className="chat-window">
            <div className="chat-box">
                {chat.map((message, index) => (
                    <Message className="message" key={ index } message={ message } username={ props.username } />))}
            </div>
            <div className="input-box">
                <Input />
            </div>
        </div>
    );
}
