<script lang="ts">
  import { Auth } from "aws-amplify";

  let meals = [];

  getMeals();

  async function getMeals() {
    let user: any;
    let email = "";
    let authToken = "";
    try {
      user = await Auth.currentAuthenticatedUser();
      authToken = (await Auth.currentSession()).getAccessToken().getJwtToken();
    } catch (err) {
      console.error("User not authenticated. Please login.");
      return;
    }
    email = user.attributes.email;
    fetch(`https://t2yvxytyne.execute-api.eu-central-1.amazonaws.com/recipients/${email}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    })
      .then((res) => res.json())
      .then((mealsData) => {
        meals = mealsData;
      })
      .catch(() => {
        meals = [];
      });
  }
</script>

<h3>Food Alerts</h3>
<div class="card">
  <ul class="list-group list-group-flush">
    {#each meals as meal}
      <li class="list-group-item">{meal}</li>
    {/each}
    {#if meals.length === 0}
      <li class="list-group-item">No alerts</li>
    {/if}
  </ul>
</div>
