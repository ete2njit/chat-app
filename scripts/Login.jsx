import * as React from 'react';



export function Login(props) {
    
    function handleSubmit(event) {
        let name = document.getElementById("usernameInput");
        
        props.setName(name.value);
        
        console.log("set name to " + name.value);
        
        event.preventDefault();
    }


    return (
        <form onSubmit={handleSubmit}>
            <input id="usernameInput" placeholder=""></input>
            <button>Choose username</button>
        </form>
    );
}