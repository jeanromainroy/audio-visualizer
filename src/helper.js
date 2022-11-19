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


export function getUrlParams(url){
    
    // init array
    const params = {}
    
    // split at params
    let url_split = url.split('?')

    // if no params
    if (url_split.length !== 2) {
        return params
    }
    
    // grab the right end
    url_split = url_split[1]
    
    // split all
    url_split = url_split.split('&')
    
    // go through
    url_split.forEach(param => {
        // check if contains '='
        if (!param.includes('=')) {
            return params;
        }
        
        const vals = param.split('=')
        if (vals.length !== 2) {
            return params;
        }
        
        params[vals[0]] = vals[1]
    })
    
    return params 
}
