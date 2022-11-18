<script>
    
    // libs
    import { onMount } from 'svelte';
    import { load_json } from './helper.js';

    // config
    const NBR_IMAGES_PER_UID = 60;
    const NBR_IMAGES_SAMPLED_PER_UID = 8; // must be smaller than NBR_IMAGES_PER_UID

    // properties - data
    let concept_tree = {};
    let concept_keys = null;
    let prompts_df = null;
    let images_df = null;

    // properties - displayed
    let uid_displayed = null;
    let prompt_displayed = '';
    let image_url = null;

    // properties - controls
    let selector = {};
    let ready = false;
    let speed_val = 50;
    let preloaded_counter = 0;
    

    // helper function to get prompts from a selection
    function get_prompts_by_selection(selection) {
        return prompts_df.filter(datum => {
            for (const concept_key of concept_keys){
                if (datum[concept_key] != selection[concept_key]) return false;
            }
            return true;
        });
    }


    async function preload_artworks(){

        // init
        images_df = {};
        
        // load images
        for (const prompt_datum of prompts_df){

            // destructure
            const { uid } = prompt_datum;

            // init
            images_df[uid] = [];

            // push a random sample of the images
            while ( images_df[uid].length < NBR_IMAGES_SAMPLED_PER_UID ) {

                // generate a random index
                const random_index = Math.round(Math.random() * NBR_IMAGES_PER_UID);

                // build url
                const image_url = `assets/${uid}/${random_index}.jpg`;

                // instantiate
                const img = new Image();
                img.src = image_url;

                // wait until it's done loading 
                await new Promise(resolve => {
                    img.onload = () => {
                        images_df[uid].push(img);
                        preloaded_counter += 1;
                        resolve();
                    }
                    img.onerror = () => {
                        resolve();
                    }
                });
            }
        }
    }


    async function animate(){

        // grab DOM container
        const container = document.getElementById('image-container');

        // variables
        let i = 0;

        while(true){

            // sleep
            await new Promise(resolve => {
                setTimeout(() => {
                    resolve()
                }, speed_val * 10);
            });

            // check
            if (uid_displayed === undefined || uid_displayed === null) continue;

            // increment
            i = ( i + 1 ) % images_df[uid_displayed].length

            // select
            const img = images_df[uid_displayed][i];

            // append
            container.childNodes.forEach(el => el.remove());
            container.appendChild(img);
        }
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
        uid_displayed = uid;
        prompt_displayed = prompt
    }


    onMount(async () => {

        // load prompts
        prompts_df = await load_json('/prompts.json');

        // extract concepts, subconcepts and prompts from prompts_df
        concept_keys = Object.keys(prompts_df[0]).filter(d => !['uid', 'prompt'].includes(d));
        concept_keys.forEach(concept_key => concept_tree[concept_key] = new Set());
        prompts_df.forEach(datum => {
            concept_keys.forEach(concept_key => {
                concept_tree[concept_key].add(datum[concept_key]);
            })
        });
        concept_keys.forEach(concept_key => concept_tree[concept_key] = [...concept_tree[concept_key]])


        // scaffold selector
        concept_keys.forEach(concept_key => selector[concept_key] = null);

        // preload assets
        await preload_artworks();

        // start animation
        animate();

        // set ready flag
        ready = true;
    })

</script>

<main>
    
    <div style="z-index: 1; position: absolute; width: 100%; height: 100%;">

        <div id="image-container">
            {#if image_url !== null}
                <img alt="visualizer" src={image_url}/>
            {/if}
        </div>

        <div style="position: absolute; bottom: 0px; left: 0px; right: 0px; text-align: center; z-index: 2; padding: 8px">
            <p style="font-size: 22px; font-family: monospace; color: white">{prompt_displayed}</p>
        </div>

    </div> 


    <div id="config-panel">
        <div style="padding: 8px;">

        {#if ready === true}

            <!-- For each concept -->
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

            <!-- Speed Slider -->
            <h2>Speed</h2>

            <div class="slider-container">
                <input style="width: 15vw;" type="range" bind:value={speed_val}>
                <p style="margin-left: 16px;">{speed_val}</p>
            </div>

        {:else}
            <p style="text-align: center; margin-top: 40vh; font-size: 24px">{preloaded_counter} artworks loaded</p>
        {/if}
        </div>
    </div>


    <div id="preloaded-assets" style="display: none;"></div>

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

    :global(img) { 
        object-fit: cover;
        width: 100%;
        height: 100%;
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
        padding: 0px;
    }

    .container-buttons {
        margin: 0px;
        padding: 0px;
        margin-bottom: 16px; 
    }

    .slider-container {
        display: flex;
        flex-direction: row;
    }

    button {
        margin: 8px;
        padding: 8px;
        background-color: lightgray;
        border: none;
    }

    #image-container {
        position: absolute;
        top: 0px;
        left: 0px;
        right: 0px;
        bottom: 0px;
    }

</style>