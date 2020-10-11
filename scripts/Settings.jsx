import * as React from 'react';
//import "../static/settingstyle.css";


export function Settings(props) {
    return (
        <div>
            <div class="displayCount">
                <input
                    type="text"
                    value={ props.displayCount }
                    onChange={ props.handleChange }
                />
            </div>
            
            
        </div>
    )
}