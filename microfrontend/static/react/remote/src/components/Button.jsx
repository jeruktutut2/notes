import React from 'react';

export default function Button() {
    const log = async () => {
        console.log("log from remote button")
    }
    return <>
        <div>
            <button className="bg-blue-500 text-white px-4 py-2 rounded" onClick={log}>Button React</button>
        </div>
    </>
}