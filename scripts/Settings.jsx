import * as React from 'react';
import "../static/settingstyle.css";


export function Settings(props) {
    return (
        <div className="settings-window">
            <div className="settings-content">
                <span className="display-count">Chat length:  </span>
                <input className="display-input"
                    type="text"
                    value={ props.displayCount }
                    onChange={ props.handleChange }
                />
            </div>
        </div>
    );
}