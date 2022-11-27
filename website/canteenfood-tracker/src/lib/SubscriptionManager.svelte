<script lang="ts">
  let email = "";
  let meals = [];
  function getMeals() {
    fetch(`http://localhost:3000/meals/${email}`)
      .then((res) => res.json())
      .then((m) => (meals = m))
      .catch((e) => (meals = []));
  }
</script>

<h1>Subscription Manager</h1>
<input
  bind:value={email}
  type="email" />
<button on:click={getMeals}> Get Meals </button>
<ul id="list">
  {#each meals as meal}
    <li>{meal}</li>
  {/each}
</ul>

<style>
  input[type="email"] {
    width: 250px;
  }

  button {
    background-color: #007bff;
    padding: 10px;
    border: none;
    border-radius: 10px;
  }
</style>