<script lang="ts">
  import AuthManager from "./lib/authentication/AuthenticationComponent.svelte";
  import SubscriptionManager from "./lib/food-alerts/SubscriptionManager.svelte";
  import { checkGlobalCurrentUser, globalCurrentUser } from "./store";
</script>

<main class="d-flex flex-row">
  <div class="flex-1" />
  <div class="flex-3">
    <h2>Canteenfood Tracker Lüneburg</h2>
    <AuthManager />
    {#if $globalCurrentUser}
      <SubscriptionManager />
    {/if}
  </div>
  <div class="flex-1" />
</main>

<style>
  .flex-1 {
    flex: 1;
  }
  .flex-3 {
    flex: 3;
  }
</style>
