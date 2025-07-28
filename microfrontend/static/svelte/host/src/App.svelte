<script>
  // import svelteLogo from './assets/svelte.svg'
  // import viteLogo from '/vite.svg'
  // import Counter from './lib/Counter.svelte'
    import { onMount } from 'svelte';
    import Loading from './lib/Loading.svelte'
    import ErrorFallback from './lib/ErrorFallback.svelte'
    // let Button
    // let Text
    // import('remote/Button').then((module) => {
    //     Button = module.default;
    // });
    // import('remote/Text').then((module) => {
    //     Text = module.default;
    // });
    // let Button = Loading;
    // let Text = Loading;
    // let errorMessage = "";
    let Button

    // function loadRemoteEntry(url) {
    //     return new Promise((resolve, reject) => {
    //         const script = document.createElement('script');
    //         script.src = url;
    //         script.type = 'text/javascript';
    //         script.async = true;
    //         script.onload = () => resolve();
    //         script.onerror = () => reject(new Error(`Failed to load remote entry ${url}`));
    //         document.head.appendChild(script);
    //     });
    // }

    onMount(async () => {
        // try {
            // console.log("remote entry belum masuk")
            // await loadRemoteEntry('http://localhost:3001/assets/remoteEntry.js');
            // console.log("remote entry masuk")
            const buttonRemote = await import('remote/Button');
            Button = buttonRemote.default;
            // const textRemote = await import('remote/Text');
            // Text = textRemote.default;
        // } catch (err) {
        //     console.error('Error loading remote', err);
        //     errorMessage = `Error: ${err.message || 'Failed to load component.'}`;
        //     Button = ErrorFallback;
        //     Text = ErrorFallback;
        // }
  });
</script>

<main>
  <!-- <div>
    <a href="https://vite.dev" target="_blank" rel="noreferrer">
      <img src={viteLogo} class="logo" alt="Vite Logo" />
    </a>
    <a href="https://svelte.dev" target="_blank" rel="noreferrer">
      <img src={svelteLogo} class="logo svelte" alt="Svelte Logo" />
    </a>
  </div> -->
  <!-- <h1>Vite + Svelte</h1> -->

  <!-- <div class="card">
    <Counter />
  </div> -->

  <!-- <p>
    Check out <a href="https://github.com/sveltejs/kit#readme" target="_blank" rel="noreferrer">SvelteKit</a>, the official Svelte app framework powered by Vite!
  </p> -->

  <!-- <p class="read-the-docs">
    Click on the Vite and Svelte logos to learn more
  </p> -->
    <!-- <Button /> -->
    <span>This is a svelte host</span>
    <!-- <Button {errorMessage} /> -->
    <!-- <Text {errorMessage} /> -->
    {#if Button}
        <svelte:component this={Button} name="Button Host App" />
    {:else}
        <p>Loading Button remote component...</p>
    {/if}

    <!-- {#if Text}
        <svelte:component this={Text} name="Text Host App" />
    {:else}
        <p>Loading Text remote component...</p>
    {/if} -->
</main>

<style>
  /* .logo {
    height: 6em;
    padding: 1.5em;
    will-change: filter;
    transition: filter 300ms;
  } */
  /* .logo:hover {
    filter: drop-shadow(0 0 2em #646cffaa);
  } */
  /* .logo.svelte:hover {
    filter: drop-shadow(0 0 2em #ff3e00aa);
  } */
  /* .read-the-docs {
    color: #888;
  } */
</style>
