<script>
  import AuthManager from "./lib/AuthManager.svelte";
  import SubscriptionManager from "./lib/SubscriptionManager.svelte";
</script>

<main class="d-flex">
  <div class="w-50">
    <AuthManager></AuthManager>
  </div>
  <div class="w-50">
    <SubscriptionManager />
  </div>
</main>

<style>
</style>
