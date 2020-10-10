  
import * as React from 'react';

import { Socket } from './Socket';
import { Chat }   from './Chat';

export function Content() {
    // display count of 0 means show the whole chatlog
    const [displayCount, setDisplayCount] = React.useState(5);     
    const [chatlog, setChatlog] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('addresses received', (data) => {
                console.log("Received addresses from server: " + data['allAddresses']);
                setChatlog(data['allAddresses']);
            })
        });
    }
    
    function handleChange(event) {
        setDisplayCount(event.target.value);
    }
    
    getNewAddresses();

    return (
        <div>
            <div class="displayCount">
                <input
                    type="text"
                    value={displayCount}
                    onChange={handleChange}
                />
            </div>
            <div>
                <Chat chatlog={ chatlog } displayCount={ displayCount }/>
            </div>
        </div>
    
    );
}
 