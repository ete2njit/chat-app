import * as React from 'react';
import { Socket } from './Socket';


export function Chat(props) {
    const [displayCount, setDisplayCount] = React.useState(2);      // display count of 0 means show the whole chatlog
    let chat = [];
    let chatLength = props.chatlog.length;
    
    
    if(displayCount == 0)
        chat = props.chatlog;
    else
        for(let i = 0; i < chatLength && (displayCount == 0 || i < displayCount); i++)
        {
            chat[displayCount-i] = props.chatlog[chatLength-1-i];
        }
    
    
    
    return (
        <ol>
            {chat.map((address, index) =>
                <li key={index}>{address}</li>)}
        </ol>
    );
}
