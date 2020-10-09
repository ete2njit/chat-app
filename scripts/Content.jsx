    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';
import { Chat }   from './Chat';

export function Content() {
    const [chatlog, setChatlog] = React.useState([]);
    
    function getNewAddresses() {
        React.useEffect(() => {
            Socket.on('addresses received', (data) => {
                console.log("Received addresses from server: " + data['allAddresses']);
                setChatlog(data['allAddresses']);
            })
        });
    }
    
    getNewAddresses();

    return (
        <div>
            <Chat chatlog={ chatlog }/>
            <Button />
        </div>
    );
}
 