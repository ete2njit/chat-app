import * as React from 'react';
import { Socket }  from './Socket';
import "../static/informationstyle.css";


    //https://www.robinwieruch.de/react-remove-item-from-list
    function removeUser(id) {
        
      }
      
      
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
    
    function userConnected() {
        React.useEffect(() => {
            Socket.on('user connected', (data) => {
                console.log("Received message of user connected: " + data['name'])
                const newList = users.concat(data['name'])
                setUsers(newList);
            })
        })
    }
    

    
    function userDisconnected() {
        React.useEffect(() => {
            Socket.on('user disconnected', (data) => {
                console.log("Received message of user disconnect: " + data['name'])
                const newList = users.filter((item) => item !== data['name']);
                setUsers(newList);
            })
        })
    }
    
    getUsers();
    userConnected();
    userDisconnected();
    
    return (
        <div className="information-window">
            <div className="information-content">
                <span>Logged in as { props.username }</span>
                <div className="users-box">
                    {users.map((user, index) => (
                        <li>{ user }</li>))}
                </div>
            </div>
        </div>
    )
}