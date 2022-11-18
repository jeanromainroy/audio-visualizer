'use strict';


// helper function to load json
export async function load_json(url) {

    // params
    const opts = {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    }

    // send request
    const response = await fetch(url, opts);

    // data
    const data = await response.json();

    // return
    return data;
}
