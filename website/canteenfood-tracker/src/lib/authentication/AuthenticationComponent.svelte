<script lang="ts">
  import { Auth } from "aws-amplify";
  import { globalCurrentUser } from "../../store";
  import LoginComponent from "./LoginComponent.svelte";
  import RegistrationComponent from "./RegistrationComponent.svelte";

  let authStep: 'login' | 'registration' = 'login';

  async function logout() {
    try {
      await Auth.signOut();
      globalCurrentUser.set(undefined);
      authStep = "login";
    } catch (error) {
      console.error("error logging out", error);
    }
  }
</script>

<nav class="navbar navbar-dark bg-primary">
  {#if !$globalCurrentUser}
    <div class="m-1 d-flex flex-row gap-1">
      <button
        on:click={() => (authStep = "registration")}
        class:active={authStep === "registration"}
        class="btn text-light bg-primary">Register</button>
      <button
        on:click={() => (authStep = "login")}
        class:active={authStep === "login"}
        class="btn text-light bg-primary">Login</button>
    </div>
  {:else}
    <div class="w-100 m-1 d-flex flex-row justify-content-between">
      <!-- Because bootstrap button has padding: 0.375rem -->
      <!-- | -->
      <!-- V -->
      <p
        style="padding: 0.375rem"
        class="mt-0 mb-0 text-light">
        Logged in as <span class="badge bg-secondary">{$globalCurrentUser.attributes.email}</span>
      </p>
      <button
        on:click={logout}
        class="btn btn-primary">Logout</button>
    </div>
  {/if}
</nav>

{#if !$globalCurrentUser}
  {#if authStep === "registration"}
    <RegistrationComponent />
  {/if}
  {#if authStep === "login"}
    <LoginComponent />
  {/if}
{/if}
