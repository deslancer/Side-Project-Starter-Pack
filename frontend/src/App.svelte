<script lang="ts">
  let count = 0;

  function increment() {
    count += 1;
  }
</script>

<main>
  <div class="container">
    <h1>Vite + Svelte + TypeScript</h1>
    <div class="card">
      <button on:click={increment}>
        count is {count}
      </button>
      <p>
        Edit <code>src/App.svelte</code> to get started
      </p>
    </div>
  </div>
</main>

<style>
  main {
    width: 100%;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .container {
    text-align: center;
  }

  h1 {
    font-size: 3.2em;
    line-height: 1.1;
    margin-bottom: 2rem;
  }

  .card {
    padding: 2em;
  }

  button {
    border-radius: 8px;
    border: 1px solid transparent;
    padding: 0.6em 1.2em;
    font-size: 1em;
    font-weight: 500;
    font-family: inherit;
    background-color: #1a1a1a;
    color: white;
    cursor: pointer;
    transition: border-color 0.25s;
    margin-bottom: 1rem;
  }

  button:hover {
    border-color: #646cff;
  }

  button:focus,
  button:focus-visible {
    outline: 4px auto -webkit-focus-ring-color;
  }

  code {
    background-color: rgba(255, 255, 255, 0.1);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-family: monospace;
  }
</style>

