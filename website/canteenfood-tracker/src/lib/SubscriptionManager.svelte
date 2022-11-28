<script lang="ts">
  let email = "";
  let emailUnknown = false;
  let meals = [];
  function getMeals() {
    fetch(`http://localhost:3000/meals/${email}`)
      .then((res) => res.json())
      .then((mealsData) => {
        emailUnknown = false;
        meals = mealsData;
      })
      .catch((e) => {
        emailUnknown = true;
        meals = [];
      });
  }
</script>

<div class="flex-column m-2">
  <h3>Subscription Manager</h3>
  <div class="form-group d-flex flex-wrap">
    <input
      bind:value={email}
      class="form-control" />
    <button
      on:click={getMeals}
      class="btn btn-primary ms-1">
      Get Meals
    </button>
  </div>
  {#if meals.length > 0 || emailUnknown == true}
    <div class="card mt-1">
      <ul class="list-group list-group-flush">
        {#each meals as meal}
          <li class="list-group-item">{meal}</li>
        {/each}
        {#if emailUnknown}
          <li class="list-group-item">No subscriptions found for given email</li>
        {/if}
      </ul>
    </div>
  {/if}
</div>

<style>
  .form-control {
    width: auto;
  }
</style>
