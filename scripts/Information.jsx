import * as React from 'react';
import { Input } from './Input';
import { Message } from './Message';
import "../static/informationstyle.css";


export function Information(props) {
    return (
        <div className="information-window">
            <div className="information-content">
                <span>Logged in as { props.username }</span>
            </div>
        </div>
    )
}