<script>
    
    // libs
    import { onMount } from 'svelte';

    // UI properties
    let concept_tree = {};
    let concept_keys = null;
    let dataframe = null;
    let prompt_displayed = '';
    let url_gif = null;
    let selector = {};
    let ready = false;


    // helper function to load prompts
    async function load_dataframe() {

        // params
        const url = '/prompts.json';
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


    // helper function to get prompts from a selection
    function get_prompts_by_selection(selection) {
        return dataframe.filter(datum => {
            for (const concept_key of concept_keys){
                if (datum[concept_key] != selection[concept_key]) return false;
            }
            return true;
        });
    }


    function update(concept_key, subconcept_key){

        // map to button id
        const button_id = `${concept_key}-${subconcept_key}`;

        // change appeareace of button
        document.querySelectorAll(`button[id^="${concept_key}-"]`).forEach(el => el.style.backgroundColor = 'lightgray');
        document.getElementById(button_id).style.backgroundColor = 'gray';

        // update selector
        selector[concept_key] = subconcept_key;
        
        // if selector is not fully set, stop here
        if (Object.values(selector).filter(val => val === undefined || val === null).length > 0) return;

        // get prompts matching selector
        const prompts = get_prompts_by_selection(selector);

        // select at random
        const prompt_selected = prompts[Math.floor(Math.random() * prompts.length)];

        // destructure
        const { uid, prompt } = prompt_selected;

        // update ui
        url_gif = `gifs/${uid}.gif`;
        prompt_displayed = prompt
    }


    onMount(async () => {

        // load prompts
        dataframe = await load_dataframe();

        // extract concepts, subconcepts and prompts from dataframe
        concept_keys = Object.keys(dataframe[0]).filter(d => !['uid', 'prompt'].includes(d));
        concept_keys.forEach(concept_key => concept_tree[concept_key] = new Set());
        dataframe.forEach(datum => {
            concept_keys.forEach(concept_key => {
                concept_tree[concept_key].add(datum[concept_key]);
            })
        });
        concept_keys.forEach(concept_key => concept_tree[concept_key] = [...concept_tree[concept_key]])


        // scaffold selector
        concept_keys.forEach(concept_key => selector[concept_key] = null);


        // set ready flag
        ready = true;
    })

</script>

<main>
    
    <div style="z-index: 1; position: absolute; width: 100%; height: 100%;">

        {#if url_gif !== null}
            <img alt="visualizer" src={url_gif}/>
        {/if}

        <div style="position: absolute; bottom: 0px; left: 0px; right: 0px; text-align: center; z-index: 2; padding: 8px">
            <p style="font-size: 22px; font-family: monospace; color: white">{prompt_displayed}</p>
        </div>

    </div> 


    <div id="config-panel">

        <!-- For each concept -->
        {#if ready === true}
        {#each Object.keys(concept_tree) as concept_key}

            <!-- Title -->
            <h2>{concept_key}</h2>
        
            <!-- Subconcepts -->
            <div class="container-buttons">
                {#each concept_tree[concept_key] as subconcept_key}
                    <button id={`${concept_key}-${subconcept_key}`} on:click={() => update(concept_key, subconcept_key)}><p>{subconcept_key}</p></button>
                {/each}
            </div>

        {/each}
        {/if}

    </div>

</main>

<style>

    @font-face {
        font-family: 'Noto Sans';
        font-style: normal;
        font-weight: 100;
        font-display: swap;
        src: url(/fonts/noto-sans-100-normal.woff2) format('woff2');
        unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }

    :root { 
        --font-family: 'Noto Sans';
    }

    :global(body) {
        margin: 0px;
        padding: 0px;
        font-family: var(--font-family);
    }

    main {
        display: flex;
        margin: 0px;
        width: 100vw;
        height: 100vh;
        padding: 0px;
    }

    h2 {
        margin: 0px;
        padding: 0px;
        font-size: 16px;
        font-family: var(--font-family);
    }

    p {
        margin: 0px;
        padding: 0px;
        font-size: 12px;
        font-family: var(--font-family);
    }

    #config-panel {
        z-index: 2; 
        position: absolute; 
        width: 100%; 
        height: 100%; 
        opacity: 0.4;
        padding: 8px;
    }

    .container-buttons {
        margin: 0px;
        padding: 0px;
        margin-bottom: 16px; 
    }

    button {
        margin: 8px;
        padding: 8px;
        background-color: lightgray;
        border: none;
    }

    img { 
        position: absolute;
        top: 0px;
        left: 0px;
        right: 0px;
        bottom: 0px;
        object-fit: cover;
        width: 100%;
        height: 100%;
    }

</style>