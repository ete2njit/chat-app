import * as React from 'react';
import { Input } from './Input';
import { Message } from './Message';
import { Socket }  from './Socket';
import "../static/informationstyle.css";


export function Information(props) {
    const [users, setUsers] = React.useState([]);
    
     function getUsers() {
        React.useEffect(() => {
            Socket.on('all users', (data) => {
                console.log("Received messages from server: " + data['allUsers']);
                setUsers(data['allUsers']);
            })
        });
    }
    
    getUsers();
    
    return (
        <div className="information-window">
            <div className="information-content">
                <span>Logged in as { props.username }</span>
                <div className="users-box">
                    {users.map((user, index) => (
                    <div>
                        <span>{ user }</span><br></br>
                    </div>))}
                </div>
            </div>
        </div>
    )
}