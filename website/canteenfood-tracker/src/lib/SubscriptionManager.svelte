<script lang="ts">
  import { Auth } from "aws-amplify";
  let emailUnknown = false;
  let meals = [];

  async function getMeals() {
    const user = await Auth.currentAuthenticatedUser();
    const email = user.attributes.email;
    const authToken = (await Auth.currentSession()).getAccessToken().getJwtToken();
    fetch(`https://t2yvxytyne.execute-api.eu-central-1.amazonaws.com/recipients/${email}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    })
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
  <div class="form-group d-flex">
    <button
      on:click={getMeals}
      class="btn btn-primary">
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
</style>
