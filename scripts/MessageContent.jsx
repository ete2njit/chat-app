import * as React from 'react';
import "../static/messagecontentstyle.css";

export function MessageContent(props) {
    
    if (props.type === "link") {
        return (
                <a href={ props.content }>{ props.content }</a>
            );
    }
    
    if (props.type === "image") {
        return (
                <img src={ props.content } />
            );
    }
    
    return ( 
        <span>{ props.content }</span>
    );
}