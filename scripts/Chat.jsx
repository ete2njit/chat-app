import * as React from 'react';
import { Socket } from './Socket';


export function Chat(props) {
    // display count of 0 means show the whole chatlog
    const [displayCount, setDisplayCount] = React.useState(5);      
    let chat = [];
    let chatLength = props.chatlog.length;
    
    
    if(displayCount == 0)
        chat = props.chatlog;
    else
        for(let i = 0; i < chatLength && (displayCount == 0 || i < displayCount); i++)
        {
            chat[displayCount-i] = props.chatlog[chatLength-1-i];
        }
        
    
    function handleChange(event) {
        setDisplayCount(event.target.value);
    }
    
    return (
        <ol>
            {chat.map((address, index) =>
                <li key={index}>{address}</li>)}
                
            <input
                type="text"
                value={displayCount}
                onChange={handleChange}
            />
        
        </ol>
    );
}
