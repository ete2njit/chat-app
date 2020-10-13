  
import * as React from 'react';

import { Socket }       from './Socket';
import { Chat }         from './Chat';
import { Login }        from './Login';
import { Information }  from './Information';
import { Settings }     from './Settings';
import "../static/contentstyle.css";


export function Content() {
    // display count of 0 means show the whole chatlog
    const [displayCount, setDisplayCount] = React.useState(15);     
    const [username, setUsername] = React.useState("")
    

    
    function handleChange(event) {
        setDisplayCount(event.target.value);
    }
    
    

    if(username == "")
    {
        return (
            <div className="login-page">
                <Login setName={ setUsername } />
            </div>
        )
    }

            
    return (
        <div className="main-page">
            <Information    class="information-window"  username={ username } />
            <Chat           class="chat-window"         username={ username }           displayCount={ displayCount }/>
            <Settings       class="settings-window"     displayCount={ displayCount }   handleChange={ handleChange } />
        </div>
    
    );
}
 