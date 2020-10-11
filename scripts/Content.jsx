  
import * as React from 'react';

import { Socket }       from './Socket';
import { Chat }         from './Chat';
import { Login }        from './Login';
import { Information }  from './Information';
import { Settings }     from './Settings';
import "../static/contentstyle.css";


export function Content() {
    // display count of 0 means show the whole chatlog
    const [displayCount, setDisplayCount] = React.useState(5);     
    const [chatlog, setChatlog] = React.useState([]);
    const [username, setUsername] = React.useState("")
    
    function getAllMessages() {
        React.useEffect(() => {
            Socket.on('message received', (data) => {
                console.log("Received messages from server: " + data['allMessages']);
                setChatlog(data['allMessages']);
            })
        });
    }
    
    function handleChange(event) {
        setDisplayCount(event.target.value);
    }
    
    getAllMessages();


    if(username == "")
    {
        return (
            <div>
                <Login setName={ setUsername } />
            </div>
        )
    }

            
    return (
        <div>
            <Information username={ username } />
            <Chat class="chat-window" chatlog={ chatlog } displayCount={ displayCount }/>
            <Settings displayCount={ displayCount } handleChange={ handleChange } />
        </div>
    
    );
}
 